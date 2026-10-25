import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
const cases = [
  ['range server', 'http://localhost:8766/case-studies/burger-king.html', 'no-preference'],
  ['range server, reduced', 'http://localhost:8766/case-studies/burger-king.html', 'reduce'],
  ['file://', 'file:///D:/Projetos/Portfolio/case-studies/burger-king.html', 'no-preference'],
  ['no-range server', 'http://localhost:8765/case-studies/burger-king.html', 'no-preference'],
];
for (const [name, url, reducedMotion] of cases) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion });
  await page.goto(url); await page.waitForTimeout(800);
  const v = page.locator('video.bk-video');
  await v.scrollIntoViewIfNeeded();
  const t1 = await v.evaluate(v => v.currentTime); await page.waitForTimeout(2500);
  const r = await v.evaluate(v => ({ paused: v.paused, t: +v.currentTime.toFixed(2), controls: v.controls }));
  console.log(name.padEnd(24), { ...r, advanced: r.t > t1 });
  await page.close();
}
await browser.close();
