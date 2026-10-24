# Contraste — antes/depois

Ticket: [02](../issues/02-contraste.md). Ferramenta: `tools/contrast-audit.mjs` (axe-core 4.14.0, o motor do Lighthouse 13.5.0, regra `color-contrast`), em Chrome 156, nas 5 páginas × desktop 1350×940 / mobile 412×823 / estreito 320×640. A página é rolada até o fim e espera 5 s (transições de revelação + revelação automática do hero) antes de medir; depois mede hover de link da nav no topo e a nav no estado `scrolled`. JSON: [antes](contrast-before.json) · [depois](contrast-after.json).

## Por que o Lighthouse via só 5 nós

`scroll-animations.js` inicia `.contact`, `.about`, `.footer`, `.cs-section` e os cards com `opacity: 0` até entrarem na viewport, e o axe ignora texto invisível. O Lighthouse só auditava nav e subtítulo do hero (home) e nav, hook, labels de meta e "next" (cases). No estado final, **todos** os consumidores dos tokens reprovavam:

| Token | Antes | Cor composta | Fundo | Razão | Consumidores reprovados (estado final) |
| --- | --- | --- | --- | ---: | --- |
| `--text-secondary` / `--text-muted` | α 0,45 | `#74757d` | `#0d0f1a` | 4,16 | nav (Contact, About), subtítulo do hero, `.contact__sub`, `.about__bio`, `.footer__tagline`, `.cs-header__hook`, `.cs-section__body`, `.cs-decision__body` |
| idem | α 0,45 | `#777884` | `#121528` | 4,12 | `.case-card__hook`, `.case-card__stat-label`, `.cs-stat__label` |
| `--text-ghost` | α 0,20 | `#3b3c46` | `#0d0f1a` | 1,74 | `.cs-meta__label`, `.cs-decision__number`, `.cs-next__label`, `figcaption` (harmony); também placeholders do formulário e `.hero__scroll-hint` (não medidos pelo axe) |

Convênios já passava: `.cs-app` sobrescreve os três tokens com `--text-secondary-strong` (0,65) e `--text-muted-strong` (0,60).

Totais antes (estado final + hover + nav rolada): home 39–41, billing 62, enrollment 59, harmony 65, convênios 0 violações por largura.

## Alteração

Somente `assets/css/tokens.css`, porque a reprovação atinge todos os consumidores em todas as páginas afetadas (não um caso local):

| Token | Antes | Depois | `#0d0f1a` | `#121528` | card hover (`+3 %` branco) | tinta billing (6 % accent) | `--accent-subtle` sobre primário |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `--text-secondary`, `--text-muted` | 0,45 | **0,58** | 6,20 | 6,06 | 5,87 | 5,79 | 5,64 |
| `--text-ghost` | 0,20 | **0,52** | 5,19 | 5,11 | 4,98 | 4,93 | 4,82 |

Critério: menor α com ≥ 4,5:1 em todas as superfícies, hovers e tintas em uso, com folga para arredondamento do navegador, mantendo a hierarquia primário (1,0) > secundário (0,58) > ghost (0,52) — a mesma relação já usada em Convênios (0,65 > 0,60), porém mais próxima do visual original. Nenhum texto foi tratado como "grande" para usar 3:1. `--text-index` (0,025, numeração decorativa gigante) não foi alterado. Convênios continua com suas sobrescritas.

## Depois

0 violações em todas as 45 combinações (5 páginas × 3 larguras × 3 estados). Ver também `color-contrast` nos relatórios do [candidato](candidate/local/).

## Revisão visual

Capturas em [`screenshots/before/`](screenshots/before/) e [`screenshots/after/`](screenshots/after/) (`<pagina>-<desktop|mobile|narrow>-<top|full>.png`). Composição, tipografia, espaçamentos e quebras de linha idênticos; apenas o texto secundário/labels ficam mais claros. A cor de destaque, hover e item ativo da nav (accent `#F4A87C`) não mudaram. Diferenças no topo dos cases vêm do quadro da animação (o GIF é capturado em momento arbitrário; o vídeo, no 1º quadro) e no hero da home vêm dos caracteres aleatórios.
