// Auditoria de contraste no estado FINAL das animações (o Lighthouse só vê o que está
// visível no carregamento; seções reveladas por scroll começam com opacity 0).
// Rola a página inteira, espera as transições, roda axe-core (o mesmo motor do Lighthouse)
// só com a regra color-contrast, e testa :hover/:focus dos links da nav.
// Analytics são bloqueados AQUI apenas para diagnóstico de contraste (não conta como aceite).
// Uso: node contrast-audit.mjs <baseUrl> [saida.json]
import { chromium } from 'playwright-core';
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const axeSource = readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const [baseUrl, outFile] = process.argv.slice(2);
const PAGES = ['/', '/case-studies/billing.html', '/case-studies/convenios.html',
  '/case-studies/enrollment.html', '/case-studies/harmony.html'];
const VIEWPORTS = { desktop: { width: 1350, height: 940 }, mobile: { width: 412, height: 823 }, narrow: { width: 320, height: 640 } };

const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
});
const results = [];
for (const [vpName, viewport] of Object.entries(VIEWPORTS)) {
  for (const path of PAGES) {
    const ctx = await browser.newContext({ viewport });
    await ctx.route(/clarity\.ms|googletagmanager|google-analytics|bing\.com/, (r) => r.abort());
    const page = await ctx.newPage();
    const resp = await page.goto(baseUrl.replace(/\/$/, '') + path, { waitUntil: 'networkidle' });
    if (!resp || resp.status() >= 400) { results.push({ vp: vpName, path, status: resp?.status() }); await ctx.close(); continue; }
    await page.evaluate(() => document.fonts.ready);
    // Rolar até o fim em passos para disparar os IntersectionObservers
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight / 2) {
        window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120));
      }
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(5000); // transições + revelação automática do hero (4s)
    await page.addScriptTag({ content: axeSource });
    const run = async (label) => {
      const r = await page.evaluate(async () => {
        const res = await window.axe.run(document, { runOnly: ['color-contrast'] });
        const pick = (n) => ({ target: n.target.join(' '), html: n.html.slice(0, 120),
          data: n.any?.[0]?.data && { fg: n.any[0].data.fgColor, bg: n.any[0].data.bgColor,
            ratio: n.any[0].data.contrastRatio, expected: n.any[0].data.expectedContrastRatio,
            fontSize: n.any[0].data.fontSize, fontWeight: n.any[0].data.fontWeight } });
        return { violations: res.violations.flatMap((v) => v.nodes.map(pick)),
          incomplete: res.incomplete.flatMap((v) => v.nodes.map(pick)).length };
      });
      return { label, ...r };
    };
    const states = [await run('final')];
    // Estados da nav: hover e foco do primeiro link não ativo
    const link = page.locator('.nav__link:not(.nav__link--active)').first();
    if (await link.count()) {
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(400);
      await link.hover(); await page.waitForTimeout(300); states.push(await run('nav-hover-top'));
      await page.mouse.move(0, 0);
      await page.evaluate(() => window.scrollTo(0, 2000)); await page.waitForTimeout(400);
      states.push(await run('nav-scrolled'));
    }
    results.push({ vp: vpName, path, status: resp.status(), states });
    const n = states.reduce((s, x) => s + x.violations.length, 0);
    console.log(`${vpName} ${path}: ${n} violações (${states.map((s) => s.label + '=' + s.violations.length).join(', ')})`);
    for (const s of states) for (const v of s.violations)
      console.log(`   [${s.label}] ${v.target} ${v.data?.fg} on ${v.data?.bg} = ${v.data?.ratio} (min ${v.data?.expected})`);
    await ctx.close();
  }
}
await browser.close();
if (outFile) writeFileSync(outFile, JSON.stringify(results, null, 2));
