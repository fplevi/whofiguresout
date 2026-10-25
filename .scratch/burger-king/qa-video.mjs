import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
for (const reducedMotion of ['no-preference', 'reduce']) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion });
  await page.goto('http://localhost:8766/case-studies/burger-king.html'); await page.waitForTimeout(800);
  const v = page.locator('video.bk-video');
  const before = await v.evaluate(v => ({ paused: v.paused, t: v.currentTime }));
  await v.scrollIntoViewIfNeeded(); await page.waitForTimeout(3000);
  const during = await v.evaluate(v => ({ paused: v.paused, t: +v.currentTime.toFixed(2), controls: v.controls }));
  if (reducedMotion === 'no-preference') { await v.evaluate(v => { v.currentTime = v.duration - 0.6; }); await page.waitForTimeout(1500); }
  const after = await v.evaluate(v => ({ paused: v.paused, t: +v.currentTime.toFixed(2) }));
  console.log(reducedMotion, { before, during, after });
  await page.locator('.bk-row--media-left').first().screenshot({ path: `.scratch/burger-king/qa/video-${reducedMotion}.png` });
  await page.close();
}
await browser.close();
