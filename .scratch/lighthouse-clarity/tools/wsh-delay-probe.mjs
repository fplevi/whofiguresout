// CLS quando o JS do caça-palavras chega 1 s depois do 1º paint (condição de rede lenta / Lighthouse).
// Modo "head": serve o CSS do commit HEAD; modo "work": CSS do checkout. Também confere a visão sem JS.
import { chromium } from 'playwright-core';
import { readFileSync } from 'node:fs';
const base = process.argv[2];
const headCss = readFileSync('D:/Projetos/_lh-snapshots/wsh-head.css', 'utf8');
const PAGES = ['/case-studies/billing.html', '/case-studies/convenios.html', '/case-studies/burger-king.html', '/case-studies/enrollment.html', '/case-studies/harmony.html'];
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
for (const mode of ['head', 'work']) for (const vp of [{ width: 1350, height: 940 }, { width: 412, height: 823 }]) {
  const res = [];
  for (const path of PAGES) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
    await ctx.route(/case-hero-wordsearch\.js/, async (r) => { await new Promise((s) => setTimeout(s, 1000)); r.continue(); });
    if (mode === 'head') await ctx.route(/case-hero-wordsearch\.css/, (r) => r.fulfill({ contentType: 'text/css', body: headCss }));
    const p = await ctx.newPage();
    await p.addInitScript(() => { window.__c = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__c += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
    await p.goto(base + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
    res.push((path.split('/').pop().replace('.html', '')) + ':' + (await p.evaluate(() => window.__c)).toFixed(3));
    await ctx.close();
  }
  console.log(mode, vp.width, res.join(' '));
}
// Sem JS: legenda legível, grade oculta
const ctx = await b.newContext({ javaScriptEnabled: false });
const p = await ctx.newPage(); await p.goto(base + '/case-studies/billing.html');
console.log('no-JS', JSON.stringify(await p.evaluate(() => ({ grid: getComputedStyle(document.querySelector('.wsh__grid')).display, term: getComputedStyle(document.querySelector('.wsh__term-text')).position, blank: getComputedStyle(document.querySelector('.wsh__term-blank')).display }))));
await b.close();
