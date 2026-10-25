// CLS de carregamento (sem interação) por página/largura, com as fontes de deslocamento.
import { chromium } from 'playwright-core';
const base = process.argv[2];
const PAGES = ['/', '/case-studies/billing.html', '/case-studies/convenios.html', '/case-studies/burger-king.html', '/case-studies/enrollment.html', '/case-studies/harmony.html'];
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
for (const vp of [{ width: 1350, height: 940 }, { width: 412, height: 823 }, { width: 320, height: 640 }]) {
  for (const path of PAGES) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
    const p = await ctx.newPage();
    await p.addInitScript(() => { window.__s = []; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__s.push({ v: e.value, t: Math.round(e.startTime), src: e.sources.map((s) => (s.node?.className || s.node?.nodeName || '?').toString().slice(0, 40)) }); }).observe({ type: 'layout-shift', buffered: true }); });
    await p.goto(base + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
    const s = await p.evaluate(() => window.__s);
    const cls = s.reduce((a, x) => a + x.v, 0);
    console.log(vp.width, path, 'CLS', cls.toFixed(4), s.filter((x) => x.v > 0.001).map((x) => `${x.v.toFixed(3)}@${x.t}ms[${[...new Set(x.src)].join(',')}]`).join(' '));
    await ctx.close();
  }
}
await b.close();
