# Billing — validação da narrativa visual

Data: 2026-10-24. Ticket: [04](issues/04-validation.md). Spec: [spec.md](spec.md).

## Como foi verificado

- Servidor local já ativo em `http://localhost:8000` (confirmado com HTTP 200 antes do uso).
- Rotina nova com Playwright Python (Chromium headless): [visual-narrative-qa.py](visual-narrative-qa.py). Resultado bruto: [visual-narrative-qa.json](visual-narrative-qa.json). O `verify.py` anterior não foi usado, conforme o ticket.
- Resultado final: **71 verificações, 71 aprovadas** (após a revisão de 2026-10-24, ver abaixo), sem erros/avisos de console e sem requisições com falha ou status ≥ 400.
- Inspeção visual das capturas de evidência listadas abaixo, além de capturas de trabalho durante a implementação.

## Larguras e layout (320, 375, 768, 1440 px)

Em todas as larguras: sem overflow horizontal (`scrollWidth` = largura) e nenhum elemento de `main` fora do viewport. As 8 screenshots carregam (`naturalWidth > 0`), mantêm a proporção intrínseca (atributos `width`/`height`) e usam `loading="lazy"`. Cada `.billing-row` contém exatamente uma imagem. Texto e imagem não se sobrepõem. Texto e legenda vêm antes da imagem no DOM.

- 320/375/768: explicação acima da imagem na tela (coluna única).
- 1440: alternância conforme o spec: decisão 02 imagem à esquerda, decisão 03 à direita, reativação à esquerda, à vista à direita, parcelado à esquerda, revisão em bloco largo, boletos à esquerda, dashboard em bloco largo.
- Fluxo: 4 colunas em 1440, 2 em 768, 1 em 320/375, sempre na ordem 01→08 (leitura por linha). Conectores decorativos só apontam para a etapa seguinte na mesma linha. Não há conector no fim de linha nem após a etapa 08; no mobile, as setas são verticais.

Ajuste feito durante a validação visual: em 1440, telas laterais em 5/12 da linha deixavam pagamento e parcelamento com texto de interface muito pequeno. A coluna de imagem passou para 8/12. No mobile, os recortes largos ficam com ~325 px; os links “View full-size screen” foram removidos na revisão do usuário (abriam a imagem crua no navegador).

## Fluxo da jornada

Revisão do usuário (2026-10-24): o fluxo deixou de ser interativo. Agora são cards estáticos com todo o conteúdo visível, sem `details`/`summary`, sem instrução de seleção e sem elementos focáveis.

- Oito etapas na ordem documentada, numeradas 01–08, todas com explicação visível. Lista `<ol role="list">` com `aria-label` “Shared negotiation journey”; cada etapa tem um `h4` com número e título.
- Etapas 01 (início) e 08 (fim) mantêm o visual do antigo card expandido: borda pêssego, fundo levemente tingido e filete superior. As demais usam o card neutro.
- Setas: SVG fornecido pelo usuário, aplicado via `mask` com `background-color: var(--accent-primary)`, 20 px. No mobile, a seta é girada 90° e aponta para baixo.
- Sem JavaScript: as 8 etapas e explicações aparecem e as seções ficam visíveis.

## Movimento

- Movimento reduzido: seções visíveis imediatamente (todas as capturas de layout foram feitas assim).
- Movimento normal (375 e 1440, viewport de 700 px): as 5 `.cs-section` começam ocultas pelo `IntersectionObserver`. Com rolagem por roda a partir do topo, todas terminam com opacidade 1. Em 375, a seção mais alta (Decisions) mede ~3800 px; 8% dela (~300 px) fica abaixo do viewport, então o limiar de 0,08 é alcançável.

## Copy e precisão

- Ausentes da página: “in real time”, “participant-facing”, `tela.png`, a imagem do fluxograma e `.cs-image-grid`.
- Cinco minutos permanece como meta de design, junto da menção histórica ao Clarity.
- Pagamento único é rotulado “Example with reactivation” e parcelamento, “Example without reactivation”. Uma frase introdutória em What Shipped informa que as telas vêm de negociações diferentes.
- Revisão é descrita como conferência antes da validação por código, não como sucesso ou pagamento. Boletos são descritos como parcelas pendentes e geração de documentos.
- Textos orientativos (legendas, corpo das linhas e explicações do fluxo) usam `--text-secondary-strong` (0,65), sem a opacidade baixa de `.cs-image-caption`.

## Preservação

- Telas sem links: nenhum `<a>` dentro das linhas de screenshot.
- Navegação (`../`, `../#work`, `../#contact`, `../#about`), próximo projeto (`enrollment.html`), hook do hero, os quatro números e rótulos de resultado, botão de copiar e-mail e formulário (Formspree, 3 campos) estão preservados. O formulário não foi enviado.
- `git diff --check` sem ocorrências em `case-studies/billing.html` e `assets/css/billing.css`.
- Originais em `assets/images/billing/` estão intactos: datas de modificação inalteradas e nenhum arquivo sobrescrito. O fluxograma JPG/PNG continua lá.

## Arquivos alterados nesta entrega

- `case-studies/billing.html`: fluxo interativo na decisão 01, telas nas decisões 02/03 e linhas de What Shipped. As alterações anteriores no arquivo (meta, hook, Problem, link do `billing.css`) foram mantidas.
- `assets/css/billing.css`: estilos do fluxo (cards estáticos e setas) e das linhas, acrescentados às máscaras existentes.
- `assets/images/billing/editorial/*.jpg`: 7 derivados (ver [image-manifest.md](image-manifest.md)).
- `.scratch/billing/`: manifesto, este relatório, rotina e JSON de QA, capturas `narrative-*.png` e comentários dos tickets.

Nenhum estilo ou script compartilhado foi alterado. Durante a sessão surgiram mudanças externas no checkout (`assets/css/footer.css`, remoção de `assets/images/Photo — Full width.jpg`, novos `felipe-levi.avif/.webp`). Não foram tocadas.

## Evidências

`narrative-{flow,access,payments,installments,review,documents,dashboard}-{1440,375}.png` e `narrative-flow-{320,768}.png`, recapturadas após a revisão.

## Limites

- Só Chromium headless; Firefox, Safari e dispositivos reais não foram testados. A semântica da `<ol role="list">` não foi conferida com leitor de tela real; a verificação usou nomes e estados expostos no DOM.
- Contraste não foi medido com ferramenta; foi verificado o token aplicado.
- A primeira tentativa de capturas de página inteira mostrou áreas vazias em imagens lazy. Capturas por elemento confirmaram que elas renderizam; a falha era do modo de página inteira. As evidências finais usam capturas de viewport.
- Sem commit, deploy ou PR.
