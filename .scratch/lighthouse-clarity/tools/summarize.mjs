// Resume uma árvore <raiz>/<pagina>/<perfil>/run-N.json em Markdown (stdout) e JSON (--json).
// Uso: node summarize.mjs <raiz> [--json]
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const root = process.argv[2];
const asJson = process.argv.includes('--json');
const CATS = ['performance', 'accessibility', 'best-practices', 'seo'];
const METRICS = {
  FCP: 'first-contentful-paint',
  LCP: 'largest-contentful-paint',
  TBT: 'total-blocking-time',
  CLS: 'cumulative-layout-shift',
  SI: 'speed-index',
};
const median = (xs) => { const s = [...xs].sort((a, b) => a - b); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const range = (xs) => Math.max(...xs) - Math.min(...xs);

const rows = [];
for (const page of readdirSync(root).filter((d) => !d.includes('.'))) {
  for (const profile of ['desktop', 'mobile']) {
    const dir = join(root, page, profile);
    if (!existsSync(dir)) continue;
    const runs = readdirSync(dir).filter((f) => /^run-\d+\.json$/.test(f)).sort()
      .map((f) => JSON.parse(readFileSync(join(dir, f), 'utf8')));
    if (!runs.length) continue;
    const row = { page, profile, n: runs.length, url: runs[0].finalDisplayedUrl,
      lighthouse: runs[0].lighthouseVersion, chrome: runs[0].environment?.hostUserAgent?.match(/Chrome\/[\d.]+/)?.[0],
      runtimeErrors: runs.map((r) => r.runtimeError?.code).filter(Boolean), cats: {}, metrics: {}, failed: {} };
    for (const c of CATS) {
      const v = runs.map((r) => Math.round((r.categories[c]?.score ?? NaN) * 100));
      row.cats[c] = { median: median(v), range: range(v), runs: v };
    }
    for (const [k, id] of Object.entries(METRICS)) {
      const v = runs.map((r) => r.audits[id]?.numericValue ?? NaN);
      row.metrics[k] = { median: median(v), range: range(v) };
    }
    // Auditorias com peso > 0 que reprovaram (score < 1) em alguma execução
    for (const r of runs) {
      for (const c of CATS) {
        for (const ref of r.categories[c]?.auditRefs ?? []) {
          const a = r.audits[ref.id];
          if (ref.weight > 0 && a.score !== null && a.score < 1 && a.scoreDisplayMode !== 'notApplicable') {
            const key = `${c}:${ref.id}`;
            row.failed[key] = (row.failed[key] ?? 0) + 1;
          }
        }
      }
    }
    rows.push(row);
  }
}

if (asJson) { console.log(JSON.stringify(rows, null, 2)); process.exit(0); }

const fmtMs = (m) => `${Math.round(m.median)} (±${Math.round(m.range)})`;
console.log('| Página | Perfil | n | Perf | A11y | BP | SEO | FCP ms | LCP ms | TBT ms | CLS | SI ms | Reprovadas com peso (execuções) |');
console.log('| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |');
for (const r of rows) {
  const c = (k) => `${r.cats[k].median}${r.cats[k].range ? ` (±${r.cats[k].range})` : ''}`;
  const failed = Object.entries(r.failed).map(([k, n]) => `${k} (${n}/${r.n})`).join('; ') || '—';
  console.log(`| ${r.page} | ${r.profile} | ${r.n} | ${c('performance')} | ${c('accessibility')} | ${c('best-practices')} | ${c('seo')} | ${fmtMs(r.metrics.FCP)} | ${fmtMs(r.metrics.LCP)} | ${fmtMs(r.metrics.TBT)} | ${r.metrics.CLS.median.toFixed(4)} (±${r.metrics.CLS.range.toFixed(4)}) | ${fmtMs(r.metrics.SI)} | ${failed}${r.runtimeErrors.length ? ' **runtimeError: ' + r.runtimeErrors.join(',') + '**' : ''} |`);
}
