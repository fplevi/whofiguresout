// Caixas (x, y, w, h) de todas as <img> de conteúdo e altura da página, por página/largura.
// Uso: node layout-boxes.mjs <baseUrl> <saida.json>  — compare duas saídas com --diff a.json b.json
import { chromium } from 'playwright-core';
import { readFileSync, writeFileSync } from 'node:fs';
if (process.argv[2] === '--diff') {
  const [a, b] = [3, 4].map((i) => JSON.parse(readFileSync(process.argv[i], 'utf8')));
  let bad = 0;
  for (const k of Object.keys(a)) {
    const x = a[k], y = b[k];
    const same = y && x.page === y.page && x.boxes.length === y.boxes.length && x.boxes.every((bx, i) => ['x', 'y', 'w', 'h'].every((p) => Math.abs(bx[p] - y.boxes[i][p]) <= 1));
    if (!same) bad++;
    console.log(same ? 'IGUAL     ' : 'DIFERENTE ', k, `imgs=${x.boxes.length}/${y?.boxes.length} altura=${x.page}/${y?.page}`);
  }
  process.exit(bad ? 1 : 0);
}
const [base, out] = process.argv.slice(2);
const PAGES = ['/case-studies/billing.html', '/case-studies/convenios.html', '/case-studies/burger-king.html', '/case-studies/enrollment.html', '/case-studies/harmony.html'];
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const res = {};
for (const vp of [{ width: 1440, height: 1000 }, { width: 1024, height: 900 }, { width: 412, height: 823 }, { width: 320, height: 640 }]) for (const path of PAGES) {
  const ctx = await b.newContext({ viewport: vp, reducedMotion: 'reduce' });
  await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
  const p = await ctx.newPage();
  await p.goto(base + path, { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 50)); } scrollTo(0, 0); });
  await p.waitForTimeout(600);
  res[`${vp.width} ${path}`] = await p.evaluate(() => ({ page: document.documentElement.scrollHeight,
    boxes: [...document.querySelectorAll('main img')].map((i) => { const r = i.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) }; }) }));
  await ctx.close();
}
await b.close();
writeFileSync(out, JSON.stringify(res, null, 1));
console.log('ok', Object.keys(res).length);
