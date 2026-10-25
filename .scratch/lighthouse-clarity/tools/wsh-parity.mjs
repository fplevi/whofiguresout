// 1) Grade idêntica entre HEAD e checkout (letras, palavras, tamanho) em desktop/mobile.
// 2) Override por case (--wsh-cols etc.): grade construída = espaço reservado antes do JS.
import { chromium } from 'playwright-core';
const [headUrl, workUrl] = process.argv.slice(2);
const CASES = ['billing', 'convenios', 'burger-king', 'enrollment', 'harmony'];
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const grab = async (url, vp, init) => {
  const ctx = await b.newContext({ viewport: vp, reducedMotion: 'reduce' });
  await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
  const p = await ctx.newPage();
  if (init) await p.addInitScript(init);
  await p.goto(url, { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => {
    const g = document.querySelector('.wsh__grid'); const cs = getComputedStyle(g);
    return { cells: g.querySelectorAll('.wsh__cell').length, words: [...g.querySelectorAll('.wsh__cell.is-word')].map((c) => c.textContent).join(''),
      cols: cs.getPropertyValue('--cols').trim(), rows: cs.getPropertyValue('--rows').trim(), h: Math.round(g.getBoundingClientRect().height), count: document.querySelector('.wsh__count').textContent };
  });
  await ctx.close(); return r;
};
let ok = true;
for (const vp of [{ width: 1440, height: 1000 }, { width: 375, height: 900 }]) for (const c of CASES) {
  const a = await grab(`${headUrl}/case-studies/${c}.html`, vp), w = await grab(`${workUrl}/case-studies/${c}.html`, vp);
  const same = a.cells === w.cells && a.words === w.words && a.h === w.h;
  ok &&= same;
  console.log(vp.width, c, same ? 'IGUAL' : 'DIFERENTE', `${w.cols}x${w.rows} cells=${w.cells} h=${w.h}`, same ? '' : JSON.stringify({ a, w }));
}
// Override: 20x6 desktop, 10x14 mobile, aplicado inline como um case faria
const init = () => new MutationObserver((_, o) => { const s = document.querySelector('.wsh'); if (s) { s.style.cssText += '--wsh-cols:20;--wsh-rows:6;--wsh-cols-mobile:10;--wsh-rows-mobile:14'; o.disconnect(); } }).observe(document, { childList: true, subtree: true });
for (const vp of [{ width: 1440, height: 1000 }, { width: 375, height: 900 }]) {
  const ctx = await b.newContext({ viewport: vp });
  await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
  await ctx.route(/case-hero-wordsearch\.js/, async (r) => { await new Promise((s) => setTimeout(s, 1000)); r.continue(); });
  const p = await ctx.newPage(); await p.addInitScript(init);
  await p.addInitScript(() => { window.__c = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__c += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
  await p.goto(`${workUrl}/case-studies/billing.html`, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  const r = await p.evaluate(() => ({ cells: document.querySelectorAll('.wsh__cell').length, cls: window.__c, count: document.querySelector('.wsh__count').textContent }));
  const expect = vp.width > 768 ? 120 : 140;
  ok &&= r.cells === expect && r.cls < 0.001;
  console.log('override', vp.width, `cells=${r.cells} (esperado ${expect}) CLS=${r.cls.toFixed(4)} ${r.count}`);
  await ctx.close();
}
await b.close();
console.log(ok ? 'TUDO OK' : 'FALHOU'); process.exit(ok ? 0 : 1);
