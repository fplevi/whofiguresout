import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
for (const w of [1750, 1440, 1024, 375]) {
  const page = await browser.newPage({ viewport: { width: w, height: 1000 } });
  await page.goto('http://localhost:8766/'); await page.waitForTimeout(800);
  const card = page.locator('.case-card--burger-king');
  await card.scrollIntoViewIfNeeded(); await page.waitForTimeout(1200);
  await card.screenshot({ path: `.scratch/burger-king/qa/card-${w}.png` });
  const lines = await page.locator('.case-card--burger-king .case-card__stat-number').evaluate(el => Math.round(el.getBoundingClientRect().height / parseFloat(getComputedStyle(el).lineHeight)));
  console.log(w, 'stat lines', lines);
  await page.close();
}
await browser.close();
