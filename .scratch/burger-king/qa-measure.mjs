import { createRequire } from 'module';
const require = createRequire('D:/Projetos/BurguerKingNewSite/prototype/package.json');
const { chromium } = require('@playwright/test');
const browser = await chromium.launch({ channel: 'chrome' });
for (const w of [1750, 1440, 1280, 1024, 768, 375]) {
  const page = await browser.newPage({ viewport: { width: w, height: 1000 } });
  await page.goto('http://localhost:8766/'); await page.waitForTimeout(800);
  const r = await page.locator('.case-card--burger-king .case-card__stat-number').evaluate(el => {
    const box = el.parentElement.getBoundingClientRect().width;
    const probe = el.cloneNode(); probe.style.cssText = 'position:absolute;white-space:nowrap;visibility:hidden';
    const out = {};
    for (const t of ['Self-initiated', 'Launched', 'Concept', 'Prototype']) { probe.textContent = t; el.parentElement.append(probe); out[t] = Math.round(probe.getBoundingClientRect().width); probe.remove(); }
    return { column: Math.round(box), ...out };
  });
  console.log(w, r);
  await page.close();
}
await browser.close();
