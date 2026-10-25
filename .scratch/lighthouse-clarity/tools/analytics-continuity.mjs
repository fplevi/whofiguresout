// Evidência de rede da continuidade dos analytics em produção (uma visita de teste real, sem bloqueio).
// Percurso por cliques: home → case → outro case → home; depois nova visita no mesmo perfil.
// Registra apenas igualdades/contagens — nenhum valor de ID ou cookie é gravado.
// Uso: node analytics-continuity.mjs <baseUrl> [saida.json]
import { chromium } from 'playwright-core';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [base, out] = process.argv.slice(2);
const profile = mkdtempSync(join(tmpdir(), 'lh-continuity-'));
const launch = () => chromium.launchPersistentContext(profile, {
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  viewport: { width: 1350, height: 940 },
});

const meta = (page) => page.evaluate(() => new Promise((res) => {
  const t = setTimeout(() => res(null), 8000);
  window.clarity('metadata', (d) => { clearTimeout(t); res({ user: d.userId, session: d.sessionId, page: d.pageNum }); }, false, true, true);
}));

const steps = [];
const ga = [];
let ctx = await launch();
let page = ctx.pages()[0] ?? await ctx.newPage();
const watchGa = (pg) => pg.on('request', (r) => {
  const u = r.url();
  if (!/google-analytics\.com\/g\/collect|analytics\.google\.com\/g\/collect/.test(u)) return;
  const q = new URL(u).searchParams;
  const body = (r.postData() || '').split(/\r?\n/).filter(Boolean).map((l) => new URLSearchParams(l));
  // Um evento por linha do corpo; sem corpo, o evento está na própria query
  const events = body.length ? body.map((l) => l.get('en')).filter(Boolean) : [q.get('en')].filter(Boolean);
  for (const en of events) ga.push({ tid: q.get('tid'), cid: q.get('cid'), sid: q.get('sid'), dl: new URL(q.get('dl') || base).pathname, en });
});
watchGa(page);
const record = async (label) => {
  await page.waitForLoadState('networkidle'); await page.waitForTimeout(7000); // GA4 envia em lote alguns segundos depois
  steps.push({ label, path: new URL(page.url()).pathname, clarity: await meta(page) });
};

await page.goto(base + '/'); await record('home');
await page.click('a.case-card[href*="billing"]'); await record('case billing');
await page.click('a[href*="enrollment.html"], a[href*="harmony.html"], a[href*="convenios.html"], a[href*="burger-king.html"]'); await record('outro case');
await page.click('a.nav__logo'); await record('home');
await ctx.close();

// Visita recorrente: mesmo perfil, navegador reaberto
ctx = await launch();
page = ctx.pages()[0] ?? await ctx.newPage();
watchGa(page);
await page.goto(base + '/'); await record('nova visita (home)');
const cookies = (await ctx.cookies()).map((c) => c.name);
await ctx.close();

const first = steps[0].clarity, journey = steps.slice(0, 4), revisit = steps[4].clarity;
const gaFirst = ga.filter((g) => g.en === 'page_view');
const report = {
  date: new Date().toISOString(), base,
  path: steps.map((s) => s.path),
  clarity: {
    metadataEmEtapas: steps.filter((s) => s.clarity).length + '/' + steps.length,
    mesmoUsuarioNoPercurso: journey.every((s) => s.clarity && s.clarity.user === first.user),
    mesmaSessaoNoPercurso: journey.every((s) => s.clarity && s.clarity.session === first.session),
    pageNumCrescente: journey.every((s, i) => i === 0 || s.clarity?.page > journey[i - 1].clarity?.page),
    mesmoUsuarioNaNovaVisita: !!revisit && revisit.user === first.user,
  },
  ga4: {
    propriedade: [...new Set(ga.map((g) => g.tid))],
    pageViewsEmOrdem: gaFirst.map((g) => g.dl),
    pageViewsPorCaminho: gaFirst.reduce((m, g) => ((m[g.dl] = (m[g.dl] || 0) + 1), m), {}),
    mesmoClientIdEmTudo: new Set(ga.map((g) => g.cid)).size === 1,
    sessoesDistintas: new Set(ga.map((g) => g.sid)).size,
  },
  cookiesPrimariosPresentes: ['_clck', '_clsk', '_ga'].filter((n) => cookies.includes(n)),
};
console.log(JSON.stringify(report, null, 2));
if (out) writeFileSync(out, JSON.stringify(report, null, 2));
