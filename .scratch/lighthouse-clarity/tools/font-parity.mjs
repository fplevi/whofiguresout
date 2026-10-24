// Mesmo HTML, fontes do Google vs auto-hospedadas: diferença de pixels na página inteira.
import { chromium } from 'playwright-core';
const GF = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;0,9..144,900;1,9..144,700&family=Inter:wght@400;500&display=swap" />';
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
for (const path of ['/', '/case-studies/convenios.html', '/case-studies/harmony.html']) {
  for (const mode of ['google', 'self']) {
    const ctx = await b.newContext({ viewport: { width: 1350, height: 940 }, reducedMotion: 'reduce' });
    await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
    if (mode === 'google') await ctx.route(/\.html$|\/$/, async (r) => {
      const resp = await r.fetch(); let h = await resp.text();
      h = h.replace(/<link rel="preload"[^>]*woff2[^>]*>\s*/g, '').replace(/<link rel="stylesheet" href="(\.\.\/)?assets\/css\/fonts\.css" \/>/, GF);
      r.fulfill({ response: resp, body: h });
    });
    const p = await ctx.newPage();
    await p.goto(process.argv[2] + path, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate(() => { document.querySelectorAll('video').forEach((v) => { v.pause(); v.currentTime = 0; }); document.querySelectorAll('.hero__char').forEach((c) => c.textContent = 'X'); });
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `D:/Projetos/_lh-snapshots/parity-${path.replace(/\W/g, '_')}-${mode}.png`, fullPage: true });
    await ctx.close();
  }
}
await b.close();
