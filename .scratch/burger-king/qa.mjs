import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const out = 'D:/Projetos/Portfolio/.scratch/burger-king/qa/';
const browser = await chromium.launch({ channel: 'chrome' });
for (const [w, h] of [[1440, 1000], [375, 812]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const errors = [];
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('requestfailed', r => errors.push('FAILED ' + r.url()));
  page.on('response', r => r.status() >= 400 && errors.push(r.status() + ' ' + r.url()));
  await page.goto('http://localhost:8766/case-studies/burger-king.html');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}${w}-hero.png` });
  await page.locator('.wsh__reveal').click(); await page.waitForTimeout(1500);
  await page.screenshot({ path: `${out}${w}-revealed.png` });
  // trigger lazy images and scroll animations
  for (let y = 0; y < 20000; y += 600) { await page.evaluate(y => window.scrollTo(0, y), y); await page.waitForTimeout(120); }
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `${out}${w}-full.png`, fullPage: true });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  const words = await page.locator('.wsh__item').count();
  console.log(w, { overflow, words, errors });
  await page.close();
}
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto('http://localhost:8766/'); await page.waitForTimeout(1000);
await page.locator('.case-card--burger-king').scrollIntoViewIfNeeded(); await page.waitForTimeout(1200);
await page.locator('.case-card--burger-king').screenshot({ path: out + 'home-card.png' });
await browser.close();
