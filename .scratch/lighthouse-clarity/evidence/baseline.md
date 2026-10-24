# Baseline Lighthouse — 2026-10-24

Ticket: [01](../issues/01-baseline.md). Resumos completos (com auditorias reprovadas): [produção](baseline/production-summary.md) · [local de partida](baseline/local-start-summary.md). JSON por célula em `baseline/<ambiente>/<pagina>/<perfil>/run-N.json` (identificadores de cookies em URLs redigidos com `tools/redact.mjs`).

## Condições

| Item | Valor |
| --- | --- |
| Lighthouse | 13.5.0 (mesma versão do anexo), fixada em `tools/package.json` |
| Chrome | 156.0.8078.47 estável, Windows 11, `--headless=new`, perfil temporário novo por execução (chrome-launcher), sem extensões |
| Desktop | `--preset=desktop`: 1350×940, DPR 1, throttling simulado RTT 40 ms / 10 Mbps / CPU 1× |
| Mobile | padrão do Lighthouse 13: Moto G Power 412×823, DPR 1,75, RTT 150 ms / 1,6 Mbps / CPU 4× (simulado) |
| Política de cookies | padrão do Chrome 156 (cookies de terceiros permitidos, com aviso `WarnThirdPartyPhaseout`) |
| Consentimento | nenhum CMP/API; Clarity reporta `ad_Storage`/`analytics_Storage` = `granted`, `source: 0` (acesso a partir do Brasil). Ver [analytics](analytics.md) |
| Máquina | benchmarkIndex ≈ 3265 |
| Comando | `cd tools && npm ci && node run-matrix.mjs <ambiente> <baseUrl> <saida> 3` |

## Revisões

- **Produção** `https://www.felipelevi.site` = `origin/master` `d2d74df` (build do GitHub Pages de 2026-05-08, confirmado pela API de Pages). `case-studies/convenios.html` **não existe em produção** (HTTP 404), por isso a matriz de produção tem 4 páginas × 2 perfis × 3 = **24** coletas, não 30.
- **Local de partida** = HEAD `7c87df3` (6 commits à frente de produção) + alterações não commitadas do usuário (diff SHA-1 `877376b8…`), copiado para `D:/Projetos/_lh-snapshots/start` e servido por `python -m http.server` (HTTP/1.0, sem compressão, sem cache). 5 × 2 × 3 = 30 coletas.
- Durante a execução o checkout continuou recebendo edições do usuário (ex.: tag "Product Leadership" no card de Convênios). Elas foram preservadas e não fazem parte do snapshot de partida.

## Medianas (variação = máx − mín entre 3 execuções)

### Produção (`d2d74df`)

| Página | Perfil | Perf | A11y | BP | SEO | FCP ms | LCP ms | TBT ms | CLS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| home | desktop | 99 (±16) | 96 | 73 | 100 | 550 | 896 | 0 | 0,004 (±0,226) |
| home | mobile | 73 (±26) | 96 | 73 | 100 | 3012 | 5932 | 91 | 0,000 |
| billing | desktop | 65 (±10) | 96 | 73 | 100 | 553 | **30 025** | 0 | 0,001 |
| billing | mobile | 67 (±6) | 96 | 73 | 100 | 3029 | **183 424** | 101 | 0,000 |
| enrollment | desktop | 65 (±11) | 96 | 73 | 100 | 562 | **22 396** | 0 | 0,001 |
| enrollment | mobile | 69 (±4) | 96 | 73 | 100 | 3038 | **136 585** | 88 | 0,000 |
| harmony | desktop | 65 (±10) | 96 | 73 | 100 | 548 | **19 168** | 0 | 0,001 |
| harmony | mobile | 58 (±4) | 96 | 73 | 100 | 3176 | **118 100** | 109 | 0,000 (±0,044) |

### Local de partida

| Página | Perfil | Perf | A11y | BP | SEO | FCP ms | LCP ms | TBT ms | CLS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| home | desktop | 99 (±1) | 96 | 73 | 100 | 576 | 805 | 0 | 0,003 |
| home | mobile | 96 (±23) | 96 | 73 | 100 | 1781 | 2538 | 64 | 0,007 |
| billing | desktop | 74 | 97 | 73 | 100 | 953 | **29 851** | 0 | 0,001 |
| billing | mobile | 67 (±1) | 97 | 73 | 100 | 3322 | **186 046** | 66 | 0,012 |
| convenios | desktop | 99 | 100 | 73 | 100 | 570 | 898 | 0 | 0,015 |
| convenios | mobile | 70 (±23) | 100 | 73 | 100 | 3153 | 6816 | 43 | 0,039 |
| enrollment | desktop | 74 (±1) | 97 | 73 | 100 | 912 | **21 481** | 0 | 0,001 |
| enrollment | mobile | 68 (±4) | 97 | 73 | 100 | 3298 | **138 451** | 84 | 0,000 |
| harmony | desktop | 74 (±1) | 97 | 73 | 100 | 920 | **18 627** | 0 | 0,000 |
| harmony | mobile | 68 (±1) | 97 | 73 | 100 | 3153 | **119 169** | 73 | 0,014 |

## Auditorias com peso reprovadas e atribuição

| Auditoria | Onde | Atribuição | Evidência |
| --- | --- | --- | --- |
| `color-contrast` | home e 3 cases (não Convênios) | **Própria** — tokens `--text-secondary`/`--text-muted` (α 0,45 → 4,12–4,16:1) e `--text-ghost` (α 0,20 → 1,74:1) | nós listados no JSON; auditoria de estado final em [contrast.md](contrast.md) mostra que o Lighthouse só vê a parte visível no carregamento |
| `errors-in-console` | todas as páginas, ambos ambientes | **Própria** — `GET /favicon.ico` 404 (nenhuma página declara ícone) | `details.items[].sourceLocation.url` |
| `largest-contentful-paint`, `speed-index`, `first-contentful-paint` (cases) | billing, enrollment, harmony | **Própria** — GIFs de topo de 36,1 / 26,5 / 22,8 MB (1440×900, 25 fps) | `total-byte-weight` e LCP 19–30 s desktop, 118–186 s mobile |
| `first-contentful-paint` (mobile) | todas | Própria + ambiente — cadeia `@import` de Google Fonts em `global.css` atrasa o CSS crítico; variação alta entre execuções | `network-dependency-tree-insight` |
| `cumulative-layout-shift` | home desktop produção (1/3: 0,226 em `<main>`) | Própria, só na revisão publicada; não reproduzido no local de partida (0,003) | `layout-shifts` |
| `third-party-cookies`, `inspector-issues` | todas | **Fornecedor (Clarity)** — CLID, MUID, MR, SM, ANONCHK, SRM_B | [analytics.md](analytics.md) |

GA4 aparece apenas em diagnósticos sem peso (`unused-javascript`, ~71 KiB de `gtag.js`); não é causa de pontos perdidos.

## Analytics observados (produção, navegador limpo)

Um carregamento por documento de `googletagmanager.com/gtag/js?id=G-C0GC2E2VMN` e de `www.clarity.ms/tag/wo2llblzgf` → `scripts.clarity.ms/0.8.72/clarity.js`. Cookies por nome/domínio e motivo dos avisos em [analytics.md](analytics.md). Confirmação nos painéis não é possível pelo agente — pendente no ticket 05.

## Capturas de referência

[`screenshots/before/`](screenshots/before/) — 5 páginas × desktop/mobile/320 px, topo e página inteira, com `prefers-reduced-motion` para revelar as seções de forma estável (snapshot local de partida; produção não tem Convênios).
