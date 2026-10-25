// Executa a matriz Lighthouse: páginas × perfis × execuções, cada uma em Chrome novo
// (perfil temporário, sem extensões). Uso:
//   node run-matrix.mjs <ambiente> <baseUrl> <saida> [runs=3] [paginas=home,billing,...]
// Ex.: node run-matrix.mjs production https://www.felipelevi.site ../evidence/baseline/production
import { execFileSync } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';

const [envName, baseUrl, outDir, runsArg = '3', pagesArg] = process.argv.slice(2);
if (!envName || !baseUrl || !outDir) {
  console.error('uso: node run-matrix.mjs <ambiente> <baseUrl> <saida> [runs] [paginas]');
  process.exit(1);
}

const ALL_PAGES = {
  home: '/',
  billing: '/case-studies/billing.html',
  convenios: '/case-studies/convenios.html',
  'burger-king': '/case-studies/burger-king.html',
  enrollment: '/case-studies/enrollment.html',
  harmony: '/case-studies/harmony.html',
};
const pages = pagesArg ? pagesArg.split(',') : Object.keys(ALL_PAGES);
const runs = Number(runsArg);
const profiles = {
  desktop: ['--preset=desktop'],
  mobile: [], // padrão do Lighthouse 13: Moto G Power, 4G lento simulado, CPU 4x
};

const lhBin = resolve('node_modules/lighthouse/cli/index.js');
const chromePath = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';

for (const page of pages) {
  for (const [profile, flags] of Object.entries(profiles)) {
    for (let n = 1; n <= runs; n++) {
      const dir = join(outDir, page, profile);
      mkdirSync(dir, { recursive: true });
      const out = join(dir, `run-${n}.json`);
      if (existsSync(out) && !process.env.FORCE) { console.log('skip', out); continue; }
      const url = baseUrl.replace(/\/$/, '') + ALL_PAGES[page];
      console.log(`[${envName}] ${page} ${profile} run-${n} ${url}`);
      execFileSync(process.execPath, [
        lhBin, url, ...flags,
        '--output=json', `--output-path=${out}`,
        '--chrome-flags=--headless=new --no-first-run --no-default-browser-check',
        '--quiet',
      ], { stdio: 'inherit', env: { ...process.env, CHROME_PATH: chromePath } });
    }
  }
}
