// Mede altura reservada da grade do hero (sem JS) vs altura final (com JS) e CLS de carregamento.
import { chromium } from 'playwright-core';
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
for (const vp of [{ width: 412, height: 823 }, { width: 1350, height: 940 }, { width: 320, height: 640 }]) {
  const noJs = await b.newContext({ viewport: vp, javaScriptEnabled: false });
  const p1 = await noJs.newPage(); await p1.goto(process.argv[2]);
  const reserved = await p1.evaluate(() => document.getElementById('hero-grid').getBoundingClientRect().height);
  const js = await b.newContext({ viewport: vp });
  await js.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
  const p2 = await js.newPage();
  await p2.addInitScript(() => { window.__cls = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
  await p2.goto(process.argv[2], { waitUntil: 'networkidle' }); await p2.waitForTimeout(1500);
  const r = await p2.evaluate(() => ({ h: document.getElementById('hero-grid').getBoundingClientRect().height, inline: document.getElementById('hero-grid').style.height, cls: window.__cls }));
  console.log(vp.width, 'reserved', reserved.toFixed(2), 'final', r.h.toFixed(2), r.inline, 'CLS', r.cls.toFixed(4));
  await noJs.close(); await js.close();
}
await b.close();
