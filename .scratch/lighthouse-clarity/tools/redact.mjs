// Remove dos relatórios identificadores de cookies/sincronização que aparecem em URLs
// de terceiros (MUID, CtsSyncId, MXFR etc.). Os relatórios são de navegadores temporários,
// mas o spec pede não guardar valores de cookies nos artefatos.
// Uso: node redact.mjs <dir>...
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const PARAMS = /([?&](?:MUID|CtsSyncId|MXFR|MUIDB|cid|clid|ANID|_clck|_clsk|_ga|sid)=)[^&"\\\s]+/gi;
let files = 0, hits = 0;
const walk = (d) => {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith('.json')) {
      const s = readFileSync(p, 'utf8');
      const out = s.replace(PARAMS, (_, k) => { hits++; return k + 'REDACTED'; });
      if (out !== s) { writeFileSync(p, out); files++; }
    }
  }
};
for (const d of process.argv.slice(2)) walk(d);
console.log(`redigidos ${hits} valores em ${files} arquivos`);
