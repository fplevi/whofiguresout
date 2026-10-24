import { chromium } from 'playwright-core';
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const variants = {
  asis: (h) => h,
  noVideo: (h) => h.replace(/<video[^>]*><\/video>/, ''),
  noAnalytics: (h) => h.replace(/<script async src="https:\/\/www.googletagmanager[\s\S]*?"wo2llblzgf"\);\s*<\/script>/, ''),
  noFonts: (h) => h.replace(/<link rel="stylesheet" href="https:\/\/fonts.googleapis[^>]*>/, ''),
};
for (const [name, fn] of Object.entries(variants)) {
  const res = [];
  for (let i = 0; i < 3; i++) {
    const ctx = await b.newContext({ viewport: { width: 412, height: 823 }, deviceScaleFactor: 1.75, isMobile: true, hasTouch: true });
    await ctx.route('**/case-studies/billing.html', async (r) => { const resp = await r.fetch(); r.fulfill({ response: resp, body: fn(await resp.text()) }); });
    await ctx.route(/t\.clarity\.ms\/collect|g\/collect/, (r) => r.abort());
    const p = await ctx.newPage();
    await p.goto('http://127.0.0.1:8002/case-studies/billing.html', { waitUntil: 'load' });
    await p.waitForTimeout(2500);
    res.push(Math.round(await p.evaluate(() => performance.getEntriesByName('first-contentful-paint')[0]?.startTime)));
    await ctx.close();
  }
  console.log(name, res.join(' '));
}
await b.close();
