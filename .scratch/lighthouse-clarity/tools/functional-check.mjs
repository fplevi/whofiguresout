// Verificação funcional (sem enviar mensagens reais, sem gerar sessões nos painéis):
// - percurso home → case → outro case → home pelos links reais
// - uma inicialização de GA4 e Clarity por documento (requisições do script), IDs
// - erros de console e recursos quebrados (4xx/5xx, falhas de rede próprias)
// - fontes carregadas (document.fonts), vídeo de topo reproduzindo
// - formulário: validação, sucesso e erro com resposta do Formspree SIMULADA
// /collect do Clarity e g/collect do GA4 são abortados (bootstrap e biblioteca seguem).
// Uso: node functional-check.mjs <baseUrl> [saida.json]
import { chromium } from 'playwright-core';
import { writeFileSync } from 'node:fs';

const [baseUrl, outFile] = process.argv.slice(2);
const base = baseUrl.replace(/\/$/, '');
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const report = { baseUrl, pages: [], journey: [], form: {} };

async function newCtx(opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1350, height: 940 }, ...opts });
  await ctx.route(/t\.clarity\.ms\/collect|[a-z]\.clarity\.ms\/collect|google-analytics\.com\/g\/collect|analytics\.google\.com\/g\/collect/, (r) => r.abort());
  return ctx;
}

function instrument(page, bucket) {
  bucket.console = []; bucket.failed = []; bucket.gtag = 0; bucket.clarityTag = 0; bucket.clarityJs = 0;
  page.on('console', (m) => { if (m.type() === 'error') bucket.console.push(m.text().slice(0, 200)); });
  page.on('pageerror', (e) => bucket.console.push('pageerror: ' + e.message.slice(0, 200)));
  page.on('request', (r) => {
    const u = r.url();
    if (u.includes('googletagmanager.com/gtag/js?id=G-C0GC2E2VMN')) bucket.gtag++;
    if (u.includes('www.clarity.ms/tag/wo2llblzgf')) bucket.clarityTag++;
    if (/scripts\.clarity\.ms\/.*clarity\.js/.test(u)) bucket.clarityJs++;
  });
  page.on('requestfailed', (r) => { const u = r.url(); if (!/collect/.test(u)) bucket.failed.push(`${r.failure()?.errorText} ${u.split('?')[0]}`); });
  page.on('response', (r) => { if (r.status() >= 400) bucket.failed.push(`${r.status()} ${r.url().split('?')[0]}`); });
}

// Páginas individuais
const PAGES = ['/', '/case-studies/billing.html', '/case-studies/convenios.html', '/case-studies/burger-king.html', '/case-studies/enrollment.html', '/case-studies/harmony.html'];
for (const path of PAGES) {
  const ctx = await newCtx();
  const page = await ctx.newPage();
  const b = { path };
  instrument(page, b);
  await page.goto(base + path, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  Object.assign(b, await page.evaluate(async () => {
    await document.fonts.ready;
    const fonts = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family.replace(/"/g, '')} ${f.style} ${f.weight}`);
    const v = document.querySelector('.cs-hero-image video');
    const video = v && { paused: v.paused, muted: v.muted, loop: v.loop, readyState: v.readyState, t: +v.currentTime.toFixed(2), w: v.videoWidth, h: v.videoHeight };
    const fam = (sel) => { const e = document.querySelector(sel); return e && getComputedStyle(e).fontFamily; };
    return { title: document.title, fonts: [...new Set(fonts)], video, h1Font: fam('h1'), bodyFont: fam('p'),
      clarityFn: typeof window.clarity, dataLayer: (window.dataLayer || []).filter((x) => x[0] === 'config').map((x) => x[1]) };
  }));
  report.pages.push(b);
  console.log(`${path}: gtag=${b.gtag} clarityTag=${b.clarityTag} clarityJs=${b.clarityJs} config=${b.dataLayer} console=${b.console.length} failed=${b.failed.length} fonts=${b.fonts.length} video=${JSON.stringify(b.video)}`);
  for (const x of [...b.console, ...b.failed]) console.log('   !', x);
  await ctx.close();
}

// Percurso por cliques reais
{
  const ctx = await newCtx();
  const page = await ctx.newPage();
  const b = {}; instrument(page, b);
  const step = async (label) => { await page.waitForLoadState('networkidle'); report.journey.push({ label, url: page.url().replace(base, '') }); };
  await page.goto(base + '/', { waitUntil: 'networkidle' }); await step('home');
  await page.click('a.case-card[href*="billing"]'); await step('click card billing');
  await page.click('.cs-next a, a.cs-next, a[href*="enrollment.html"], a[href*="harmony.html"], a[href*="convenios.html"]'); await step('click next case');
  await page.click('a.nav__logo'); await step('click logo → home');
  report.journey.push({ gtagLoads: b.gtag, clarityTagLoads: b.clarityTag, console: b.console, failed: b.failed });
  console.log('journey:', report.journey.map((j) => j.url || JSON.stringify(j)).join(' → '));
  await ctx.close();
}

// Formulário com respostas simuladas
for (const scenario of ['empty', 'invalid-email', 'success', 'server-error', 'network-error']) {
  const ctx = await newCtx();
  let posted = 0;
  await ctx.route(/formspree\.io/, (r) => {
    posted++;
    if (scenario === 'success') return r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    if (scenario === 'server-error') return r.fulfill({ status: 422, contentType: 'application/json', body: '{"errors":[{"message":"Simulated server error"}]}' });
    return r.abort('failed');
  });
  const page = await ctx.newPage();
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  await page.locator('#contact-form').scrollIntoViewIfNeeded();
  if (scenario !== 'empty') {
    await page.fill('#contact-form [name="name"]', 'Teste');
    await page.fill('#contact-form [name="email"]', scenario === 'invalid-email' ? 'nao-e-email' : 'teste@example.com');
    await page.fill('#contact-form [name="message"]', 'Mensagem de teste simulada');
  }
  await page.click('#contact-form button[type="submit"]');
  await page.waitForTimeout(800);
  const state = await page.evaluate(() => {
    const err = document.querySelector('.contact__error, [id$="contact-error"]');
    const btn = document.querySelector('#contact-form button[type="submit"]');
    return { error: err?.classList.contains('visible') ? err.textContent.trim() : null,
      formVisible: !!document.querySelector('#contact-form') && getComputedStyle(document.querySelector('#contact-form')).display !== 'none',
      success: document.querySelector('.contact__success, [class*="success"]')?.textContent?.trim()?.slice(0, 80) || null,
      button: btn ? { disabled: btn.disabled, text: btn.textContent.trim() } : null };
  });
  report.form[scenario] = { posted, ...state };
  console.log(`form ${scenario}: posted=${posted} ${JSON.stringify(state)}`);
  await ctx.close();
}

// Reduced motion: seções visíveis sem animação
{
  const ctx = await newCtx({ reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(base + '/case-studies/harmony.html', { waitUntil: 'networkidle' });
  report.reducedMotion = await page.evaluate(() => [...document.querySelectorAll('.cs-section, .contact, .footer')].every((e) => getComputedStyle(e).opacity === '1'));
  console.log('reduced motion, all sections visible:', report.reducedMotion);
  await ctx.close();
}

await browser.close();
if (outFile) writeFileSync(outFile, JSON.stringify(report, null, 2));
