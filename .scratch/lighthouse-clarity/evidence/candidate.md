# Candidato local — comparação com a partida

Data: 2026-10-24. Condições idênticas ao [baseline](baseline.md) (Lighthouse 13.5.0, Chrome 156, presets desktop/mobile, 3 execuções, perfil limpo, `python -m http.server`). **Ambiente local**: a comparação vale entre partida local e candidato local; não substitui a validação em produção do ticket 06.

## Revisão

- Checkout de trabalho em `2026-10-24T16:08-03:00`: HEAD `2834e95` (o usuário commitou `edc3d07` e `2834e95` durante a execução, só com as próprias alterações) + alterações não commitadas do usuário + alterações deste trabalho (não commitadas, não publicadas).
- Manifesto SHA-1 de `index.html`, `case-studies/`, `assets/`: [candidate/manifest.sha1](candidate/manifest.sha1) (hash do manifesto `46b472536da0`).
- JSON: `candidate/local/<pagina>/<perfil>/run-N.json`; intermediários em `candidate/local-v1` e `local-v2` (ver [resources.md](resources.md)).

## Alterações deste trabalho

| Arquivo | Mudança | Ticket |
| --- | --- | --- |
| `assets/css/tokens.css` | `--text-secondary`/`--text-muted` 0,45 → 0,58; `--text-ghost` 0,20 → 0,52 | 02 |
| `index.html`, `case-studies/*.html` | `<link rel="icon" href="data:,">`; Google Fonts → `assets/css/fonts.css` + preload de 2 woff2; preconnects do Google removidos | 04 |
| `assets/css/global.css` | removido `@import` do Google Fonts | 04 |
| `assets/css/fonts.css`, `assets/fonts/*` (novos) | 6 woff2 (mesmos arquivos do Google) + licenças OFL | 04 |
| `case-studies/{billing,enrollment,harmony}.html` | GIF de topo → `<video>` MP4 + pôster WebP | 04 |
| `assets/images/{billing,enrollment,harmony}/*.mp4`, `*-poster.webp` (novos) | vídeos e pôsteres | 04 |
| `assets/css/case-study.css` | `.cs-hero-image video` no mesmo seletor de `img` | 04 |
| `assets/css/hero.css` | `aspect-ratio: 1254 / 690` na grade do hero | 04 |
| `case-studies/{enrollment,harmony}.html` | `loading="lazy" decoding="async"` + `width`/`height` em 4 imagens abaixo da dobra | 04 |

Analytics: nenhuma linha dos snippets de GA4/Clarity foi alterada.

## Medianas: partida local → candidato local

| Página | Perfil | Perf | A11y | BP | SEO | FCP ms | LCP ms | TBT ms | CLS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| home | desktop | 99 → **100** | 96 → **100** | 73 → **77** | 100 → **100** | 576 → **290** | 805 → **470** | 0 → **0** | 0,003 → **0,000** |
| home | mobile | 96 → **99** | 96 → **100** | 73 → **77** | 100 → **100** | 1781 → **1212** | 2538 → **1959** | 64 → **62** | 0,007 → **0,000** |
| billing | desktop | 74 → **100** | 97 → **100** | 73 → **77** | 100 → **100** | 953 → **352** | 29 851 → **608** | 0 → **0** | 0,001 → **0,000** |
| billing | mobile | 67 → **97** | 97 → **100** | 73 → **77** | 100 → **100** | 3322 → **1363** | 186 046 → **2484** | 66 → **79** | 0,012 → **0,000** |
| convenios | desktop | 99 → **100** | 100 → **100** | 73 → **77** | 100 → **100** | 570 → **290** | 898 → **770** | 0 → **0** | 0,015 → **0,000** |
| convenios | mobile | 70 → **91** | 100 → **100** | 73 → **77** | 100 → **100** | 3153 → **1210** | 6816 → **3460** | 43 → **51** | 0,039 → **0,000** |
| enrollment | desktop | 74 → **100** | 97 → **100** | 73 → **77** | 100 → **100** | 912 → **349** | 21 481 → **591** | 0 → **0** | 0,001 → **0,000** |
| enrollment | mobile | 68 → **97** (±1) | 97 → **100** | 73 → **77** | 100 → **100** | 3298 → **1363** | 138 451 → **2410** | 84 → **54** | 0,000 → **0,000** |
| harmony | desktop | 74 → **100** | 97 → **100** | 73 → **77** | 100 → **100** | 920 → **328** | 18 627 → **608** | 0 → **0** | 0,000 → **0,000** |
| harmony | mobile | 68 → **97** (±1) | 97 → **100** | 73 → **77** | 100 → **100** (±8) | 3153 → **1422** | 119 169 → **2409** | 73 → **55** | 0,014 → **0,000** |

Variação: categorias com ±0 salvo indicação; antes, Performance mobile variava até ±23. Ver [resumo completo](candidate/local-summary.md).

Observações:

- **SEO harmony mobile (±8):** 1/3 execuções com `robots-txt` "Fetch of robots.txt failed" no servidor local (nas outras, 404 → não aplicável, como em produção). Ambiental, não reproduzido.
- **TBT billing mobile 66 → 79 / Convênios 43 → 51:** dentro da variação do baseline (±45 / ±12), score da auditoria ≥ 0,99; long tasks dominadas por GA4 e Clarity. Não é regressão reproduzível atribuível a código próprio.
- **Boas práticas 77:** somente `third-party-cookies` e `inspector-issues` (Clarity) — limitação residual documentada em [analytics.md](analytics.md). `errors-in-console` (favicon) eliminado.
- **Performance mobile < 100:** LCP/FCP simulados com 4G lento e CPU 4×; o LCP é o texto do hook/subtítulo, renderizado em ~90 ms no trace. Os pontos restantes vêm do custo de rede simulado de CSS + fontes + GA4/Clarity no grafo do Lantern. Convênios (91) é afetado também por imagens `lazy` próximas da viewport, que o Chrome busca cedo. Não há falha própria pendente que justifique outra mudança dentro do escopo.

## Verificações funcionais e visuais

- Contraste no estado final: 0 violações em 5 páginas × 3 larguras × 3 estados ([contrast.md](contrast.md)).
- [functional-candidate.json](functional-candidate.json): 1 `gtag/js?id=G-C0GC2E2VMN` + 1 `clarity.ms/tag/wo2llblzgf` + 1 `clarity.js` por documento; `config` GA4 = `G-C0GC2E2VMN`; nenhuma resposta 4xx/5xx; fontes Inter/Fraunces carregadas; vídeos tocando (`paused: false`, `muted`, `loop`, `readyState 4`); percurso por cliques home → billing → enrollment → home; formulário com Formspree simulado (vazio, e-mail inválido, sucesso, 422, falha de rede) — nenhum envio real; reduced motion deixa todas as seções visíveis. Os 5 erros de console por página nesse teste são as requisições `/collect` que o próprio teste aborta (confirmado: 5 erros = 5 abortos); nas coletas Lighthouse sem bloqueio, `errors-in-console` passa.
- Capturas antes/depois em `screenshots/` (5 páginas × desktop/mobile/320 px).
