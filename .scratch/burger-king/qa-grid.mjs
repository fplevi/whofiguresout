import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
for (const [w, h] of [[1440, 1000], [375, 900]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  await page.goto('http://localhost:8766/case-studies/burger-king.html'); await page.waitForTimeout(600);
  await page.locator('.wsh__grid').screenshot({ path: `.scratch/burger-king/qa/grid-seed1341-${w}.png` });
  console.log(w, await page.locator('.wsh__count').textContent());
  await page.close();
}
await browser.close();
