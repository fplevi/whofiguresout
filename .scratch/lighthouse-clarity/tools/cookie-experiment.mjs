// Experimento diagnóstico de cookies do Clarity em produção, navegador limpo por cenário.
// Registra SOMENTE nome/domínio/origem dos cookies e o motivo dos avisos (sem valores).
// /collect do Clarity e os hits do GA4 são abortados para não gerar gravações/sessões
// de teste nos painéis reais; o bootstrap (tag), a biblioteca e os pixels c.gif seguem.
// Cenários:
//   default          — como o site está publicado
//   consent-ad-denied — consentv2 {ad_Storage: denied, analytics_Storage: granted} enfileirado
//                       ANTES do bootstrap (escolha explícita do testador, só nesta sessão)
// Uso: node cookie-experiment.mjs <url> [saida.json]
import { chromium } from 'playwright-core';
import { writeFileSync } from 'node:fs';

const [url, outFile] = process.argv.slice(2);
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
});
const scenarios = {
  default: null,
  'consent-ad-denied': `window.clarity = window.clarity || function(){(window.clarity.q = window.clarity.q || []).push(arguments)};
    window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'granted' });`,
};
const strip = (u) => u.split('?')[0];
const out = {};
for (const [name, init] of Object.entries(scenarios)) {
  const ctx = await browser.newContext();
  await ctx.route(/t\.clarity\.ms\/collect|google-analytics\.com\/g\/collect|analytics\.google\.com\/g\/collect/, (r) => r.abort());
  if (init) await ctx.addInitScript(init);
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Audits.enable');
  const issues = [];
  cdp.on('Audits.issueAdded', ({ issue }) => {
    const d = issue.details.cookieIssueDetails;
    issues.push({ code: issue.code, reasons: [...(d?.cookieWarningReasons ?? []), ...(d?.cookieExclusionReasons ?? [])],
      cookie: d?.cookie?.name ?? d?.rawCookieLine?.split('=')[0], domain: d?.cookie?.domain, url: d?.request?.url && strip(d.request.url), op: d?.operation });
  });
  const setCookies = [];
  page.on('response', async (resp) => {
    const h = await resp.headersArray().catch(() => []);
    for (const { name: hn, value } of h) if (hn.toLowerCase() === 'set-cookie')
      for (const line of value.split('\n')) setCookies.push({ url: strip(resp.url()), cookie: line.split('=')[0], attrs: line.split(';').slice(1).map((s) => s.trim().split('=')[0]).join(';') });
  });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);
  const consent = await page.evaluate(() => new Promise((res) => {
    try { window.clarity('metadata', (d, upgrade, consent) => res(consent), false, true, true); setTimeout(() => res('sem resposta'), 3000); }
    catch (e) { res('erro: ' + e.message); }
  }));
  const cookies = (await ctx.cookies()).map((c) => ({ name: c.name, domain: c.domain, sameSite: c.sameSite, secure: c.secure }));
  out[name] = { consent, cookies, setCookies, issues };
  console.log(`\n== ${name}  consent=${JSON.stringify(consent)}`);
  console.log('cookies:', cookies.map((c) => `${c.name}@${c.domain}`).join(', '));
  console.log('set-cookie:', setCookies.map((s) => `${s.cookie}<-${s.url}`).join(', '));
  console.log('issues:', JSON.stringify([...new Map(issues.map((i) => [i.code + i.reasons + i.cookie, i])).values()]));
  await ctx.close();
}
await browser.close();
if (outFile) writeFileSync(outFile, JSON.stringify(out, null, 2));
