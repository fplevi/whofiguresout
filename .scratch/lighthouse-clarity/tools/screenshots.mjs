// Capturas de referência: topo (viewport) e página inteira com as seções já reveladas.
// Analytics bloqueados aqui só para não gerar sessões de teste; não é medição de aceite.
// Uso: node screenshots.mjs <baseUrl> <saida-dir>
import { chromium } from 'playwright-core';
import { mkdirSync } from 'node:fs';

const [baseUrl, outDir] = process.argv.slice(2);
const PAGES = { home: '/', billing: '/case-studies/billing.html', convenios: '/case-studies/convenios.html', 'burger-king': '/case-studies/burger-king.html',
  enrollment: '/case-studies/enrollment.html', harmony: '/case-studies/harmony.html' };
const VP = { desktop: { width: 1350, height: 940 }, mobile: { width: 412, height: 823 }, narrow: { width: 320, height: 640 } };
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
for (const [vp, viewport] of Object.entries(VP)) {
  for (const [name, path] of Object.entries(PAGES)) {
    const ctx = await browser.newContext({ viewport, reducedMotion: 'reduce' }); // reveal imediato, hero estável
    await ctx.route(/clarity\.ms|googletagmanager|google-analytics|bing\.com/, (r) => r.abort());
    const page = await ctx.newPage();
    const resp = await page.goto(baseUrl.replace(/\/$/, '') + path, { waitUntil: 'networkidle' });
    if (!resp || resp.status() >= 400) { await ctx.close(); continue; }
    await page.evaluate(() => document.fonts.ready);
    // Rolar até o fim para carregar imagens lazy, esperar todas decodificarem, voltar ao topo
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); }
      await Promise.all([...document.images].map((i) => i.decode().catch(() => {})));
      scrollTo(0, 0);
    });
    // Vídeo/GIF: congelar no primeiro quadro para comparação estável
    await page.evaluate(() => document.querySelectorAll('video').forEach((v) => { v.pause(); v.currentTime = 0; }));
    await page.waitForTimeout(1500);
    await page.screenshot({ path: `${outDir}/${name}-${vp}-top.png` });
    await page.screenshot({ path: `${outDir}/${name}-${vp}-full.png`, fullPage: true });
    await ctx.close();
  }
}
await browser.close();
