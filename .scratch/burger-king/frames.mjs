import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto('file:///D:/Projetos/BurguerKingNewSite/output/portfolio-v2/ingredient-control.mp4');
await page.waitForTimeout(1500);
const info = await page.evaluate(() => { const v = document.querySelector('video'); return { d: v.duration, w: v.videoWidth, h: v.videoHeight }; });
console.log(info);
for (const t of [1, 1.5, 2, 2.5, 3, 8, 9, 10, 10.9]) {
  await page.evaluate((t) => new Promise(r => { const v = document.querySelector('video'); v.pause(); v.onseeked = r; v.currentTime = t; }), t);
  await page.screenshot({ path: `captures/vframe-${t.toFixed(1)}.png` });
}
await browser.close();
