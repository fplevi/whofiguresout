// Inventário das imagens efetivamente usadas: formato, bytes, resolução intrínseca vs exibida (×DPR).
// Rola a página inteira para disparar lazy-load. Uso: node image-inventory.mjs <baseUrl> [saida.json]
import { chromium } from 'playwright-core';
import { statSync, writeFileSync } from 'node:fs';
const [base, out] = process.argv.slice(2);
const ROOT = 'D:/Projetos/Portfolio';
const PAGES = ['/', '/case-studies/billing.html', '/case-studies/convenios.html', '/case-studies/burger-king.html', '/case-studies/enrollment.html', '/case-studies/harmony.html'];
const VPS = { desktop: { viewport: { width: 1350, height: 940 }, deviceScaleFactor: 1 }, mobile: { viewport: { width: 412, height: 823 }, deviceScaleFactor: 1.75, isMobile: true } };
const b = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const rows = {};
for (const [vpName, opts] of Object.entries(VPS)) {
  for (const path of PAGES) {
    const ctx = await b.newContext({ ...opts, reducedMotion: 'reduce' });
    await ctx.route(/clarity|googletagmanager|google-analytics/, (r) => r.abort());
    const p = await ctx.newPage();
    await p.goto(base + path, { waitUntil: 'networkidle' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } });
    await p.waitForTimeout(800);
    const imgs = await p.evaluate(() => [...document.images].filter((i) => i.currentSrc && !i.currentSrc.startsWith('data:')).map((i) => ({
      src: decodeURIComponent(new URL(i.currentSrc).pathname), nw: i.naturalWidth, nh: i.naturalHeight,
      dw: Math.round(i.getBoundingClientRect().width), picture: i.parentElement.tagName === 'PICTURE', srcset: !!i.srcset,
      lazy: i.loading, fit: getComputedStyle(i).objectFit })));
    const posters = await p.evaluate(() => [...document.querySelectorAll('video[poster]')].map((v) => ({ src: decodeURIComponent(new URL(v.poster).pathname), poster: true, dw: Math.round(v.getBoundingClientRect().width) })));
    for (const i of [...imgs, ...posters]) {
      const key = i.src;
      const r = rows[key] ??= { src: key, bytes: statSync(ROOT + key).size, ext: key.split('.').pop().toLowerCase(), pages: new Set(), nw: i.nw, nh: i.nh, picture: i.picture, srcset: i.srcset, lazy: i.lazy, need: {} };
      r.pages.add(path.split('/').pop() || 'home');
      r.need[vpName] = Math.max(r.need[vpName] ?? 0, Math.round(i.dw * opts.deviceScaleFactor));
    }
    await ctx.close();
  }
}
await b.close();
const list = Object.values(rows).map((r) => ({ ...r, pages: [...r.pages].join(',') })).sort((a, b) => b.bytes - a.bytes);
for (const r of list) console.log(`${(r.bytes / 1024).toFixed(0).padStart(5)}K ${r.ext.padEnd(4)} ${String(r.nw + 'x' + r.nh).padEnd(10)} need d:${r.need.desktop ?? '-'} m:${r.need.mobile ?? '-'} ${r.picture ? 'picture' : ''}${r.srcset ? ' srcset' : ''} ${r.lazy} ${r.src} [${r.pages}]`);
if (out) writeFileSync(out, JSON.stringify(list, null, 2));
