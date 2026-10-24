# Recursos próprios — decisões com evidência

Ticket: [04](../issues/04-recursos-proprios.md). Ambiente de comparação: local (`python -m http.server`, Chrome 156, Lighthouse 13.5.0, mesmas condições do [baseline](baseline.md)). Partida = snapshot `D:/Projetos/_lh-snapshots/start`; candidato = checkout de trabalho servido em `127.0.0.1:8004`. Ferramentas em `tools/`. Matrizes intermediárias guardadas em `candidate/local-v1` (contraste + favicon + vídeo + fontes por `<link>`) e `candidate/local-v2` (+ fontes auto-hospedadas); final em `candidate/local`.

## Alterações retidas

### 1. GIFs de topo dos cases → vídeo MP4 com pôster

- **Problema:** `digital-billing-platform.gif` 36,1 MB, `enrollment.gif` 26,5 MB, `harmony-hero.gif` 22,8 MB (1440×900, 25 fps, 6–9 s). LCP de 19–30 s no desktop e 118–186 s no mobile, em produção e local; Performance 58–74.
- **Mudança:** `<img src="….gif">` → `<video src="….mp4" poster="…-poster.webp" width="1440" height="900" autoplay muted loop playsinline>` dentro do mesmo contêiner `role="img"` com `aria-label` (nome acessível inalterado). H.264 `crf 22`, `yuv420p`, `+faststart`, sem áudio; pôster = 1º quadro em WebP q82. Seletor `.cs-hero-image img` passou a incluir `video` (mesmo `object-fit: cover`).
- **Tamanhos:** 3,26 MB / 2,71 MB / 1,95 MB (−91 % a −92 %); pôsteres 46–61 KB. SSIM vídeo×GIF: 0,990 / 0,990 / 0,992.
- **Comportamento:** reprodução automática, muda, em loop, inline no iOS — como o GIF. O GIF já ignorava `prefers-reduced-motion`; o vídeo mantém o mesmo comportamento para não mudar a experiência (pausar com reduced motion fica como sugestão, não aplicada). Os GIFs continuam no repositório, sem referências; o usuário decide se remove.
- **Hospedagem:** GitHub Pages responde `206 Partial Content` com `Accept-Ranges: bytes` (testado num asset grande publicado), necessário para vídeo.
- **Resultado:** LCP desktop dos cases 18,6–29,9 s → ~0,6–0,7 s; Performance desktop 74 → 100.

### 2. Fontes do Google auto-hospedadas, com preload dos 2 arquivos críticos

- **Problema:** `@import` em `global.css` encadeava HTML → CSS → CSS do Google → woff2 (render-blocking estimado em ~870 ms no mobile). Ao mover para `<link>` no head (v1) o problema principal apareceu: em **50–75 % das execuções** nos cases (e ocasionalmente em Convênios/home) o 1º quadro só era apresentado ~1,26 s após a navegação, embora texto e pôster já estivessem pintados em ~260 ms (trace: `PaintTimingVisualizer::LayoutObjectPainted` em 261 ms, nenhum screenshot entre 19 ms e 1262 ms). Reproduz também com Chrome visível. Isolamento (4 execuções cada, mobile): página atual 1266/282/1271/277 ms; sem vídeo 272/254/1220/1250; **sem a folha do Google 116/112/91/103**; auto-hospedada 112/130/119/88; auto-hospedada + preload 91/177/184/87. O Lantern usa esse FCP observado tardio para incluir GA4/Clarity no grafo simulado, e o Performance mobile oscilava entre 71 e 98.
- **Mudança:** mesmos arquivos woff2 servidos pelo Google (Inter v20 e Fraunces v38, subconjuntos `latin` e `latin-ext`, normal e itálico do Fraunces) em `assets/fonts/`, `@font-face` idênticos ao CSS do Google (famílias, pesos 400/500/700/900, `unicode-range`, `font-display: swap`) em `assets/css/fonts.css`; licenças OFL em `assets/fonts/OFL-*.txt`. Preload só de `inter-normal-latin.woff2` e `fraunces-normal-latin.woff2` (usados acima da dobra em todas as páginas). Removidos o `@import` e os `preconnect` para Google Fonts, que deixaram de ser usados.
- **Paridade visual:** mesmo HTML renderizado com o CSS do Google vs auto-hospedado, página inteira desktop: **0 pixels diferentes** na home e em Harmony (`tools/font-parity.mjs`).
- **Resultado:** FCP mobile observado estável em ~90–180 ms; FCP simulado dos cases 3,0 s → 1,36 s; variação entre execuções de ±23 → ±1 ponto.

### 3. Favicon declarado

- **Problema:** nenhuma página declara ícone; `GET /favicon.ico` 404 gera `errors-in-console` (Boas práticas) em todas as páginas, em produção e local.
- **Mudança:** `<link rel="icon" href="data:," />` (declaração de "sem ícone"; o navegador não pede `/favicon.ico`). Não esconde erro nem afeta analytics. Criar um favicon de verdade é decisão de design, recomendada mas fora do escopo.

### 4. Altura da grade do hero reservada em CSS

- **Problema:** `hero-reveal.js` define `height` da grade depois do 1º paint, empurrando o subtítulo. CLS de carregamento medido: 0,007 (412 px), 0,022 (1350 px), 0,030 (320 px). Com as fontes deixando de atrasar o 1º paint, o deslocamento passou a aparecer no Lighthouse mobile (0,0276 em v2).
- **Mudança:** `.hero__grid { aspect-ratio: 1254 / 690; }`, a mesma fórmula do JS (6 linhas × largura/22 × 115/57). O JS continua definindo a altura inline (mesmo valor).
- **Resultado:** altura reservada = altura final nas três larguras (200,28 / 654,78 / 149,66 px); CLS de carregamento 0 (`tools/cls-probe.mjs`).

### 5. `loading="lazy"` + dimensões nas imagens abaixo da dobra de Enrollment e Harmony

- Quatro imagens (comparação antes/depois) eram as únicas sem `loading="lazy"` nos cases e eram baixadas antes do LCP. Adicionados `loading="lazy" decoding="async"` e `width`/`height` reais (1440×1485, 1216×724) para não haver deslocamento quando carregarem, seguindo o padrão já usado em Billing e Convênios.

## Avaliado sem alteração

- **Parallax (`scroll-animations.js`):** a leitura de geometria acontece uma vez por quadro dentro de `requestAnimationFrame` (uma leitura, depois uma escrita), mais uma chamada síncrona na inicialização. Os 11,6 ms de reflow do anexo vêm dessa inicialização; não há thrashing no scroll. No candidato final, `scroll-animations.js` aparece como long task em 5/30 execuções (só mobile, 59–100 ms simulados com CPU 4×, ou seja ~15–25 ms reais), vinda da inicialização (estilos de revelação + layout), não do parallax por quadro. TBT: 0 no desktop, 51–84 ms no mobile (score ≥ 0,99), dominado por GA4 e Clarity. Ganho possível marginal; não alterado.
- **GA4 (`unused-javascript` ~71 KiB):** diagnóstico sem peso; remover ou adiar o GA4 é proibido pelo spec.
- **Convênios mobile (LCP simulado ~3,4 s):** o LCP é o texto do hook, renderizado em ~90 ms; o valor simulado sobe porque o Chrome busca cedo imagens `lazy` próximas da viewport (`convenios-card.webp`, `convenios-accounts.webp`), já otimizadas pelo autor. Sem mudança.
- **Cache/compressão:** GitHub Pages (GET com `Accept-Encoding: gzip, br`): HTML/CSS/JS com `Content-Encoding: gzip`, imagens sem compressão (correto), `Cache-Control: max-age=600` em tudo, `Vary: Accept-Encoding`, Fastly `X-Cache: HIT`. TTL não configurável no Pages; não foi criado `_headers` (ignorado pelo host). O servidor local (HTTP/1.0, sem compressão, TTL 0) não representa produção.
- **CSP/HSTS/COOP/Trusted Types:** não pontuam neste relatório; não alterados.
