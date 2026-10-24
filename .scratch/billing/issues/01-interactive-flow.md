# 01 — Substituir o fluxograma por etapas interativas

Status: resolved
Type: task
Dependências: nenhuma
Spec: [../spec.md](../spec.md)

## Entrega

Implementar o componente definido em “Fluxo interativo” do spec junto da decisão 01 de `case-studies/billing.html`. Usar lista ordenada com oito etapas, elementos nativos `details`/`summary` e estilo específico em `assets/css/billing.css`. Remover a exibição da imagem do fluxograma, preservando seu arquivo como referência.

## Passos

1. Ler o spec e inspecionar a página, estilos e alterações existentes antes de editar.
2. Construir as oito etapas na ordem documentada, com primeira etapa aberta e textos em inglês.
3. Aplicar composição responsiva e estados de interação coerentes com os tokens atuais.
4. Conferir o componente por mouse e teclado e com JavaScript desativado; registrar resultado.

## Aceite

- Todas as oito etapas e suas explicações estão presentes; cada etapa expande/recolhe independentemente.
- Tab alcança todos os controles, Enter/Espaço os operam e o foco é visível.
- Ordem visual, DOM e numeração são coerentes, inclusive nas quebras de linha.
- Funciona sem JavaScript e sem movimento; conectores são decorativos.
- O componente é uma explicação da jornada, sem simular dados ou operações reais de negociação.
- Arquivos do fluxograma permanecem intactos, e a interface deixa de exibir a antiga legenda incorreta.

## Comments

- 2026-10-24: usuário substituiu a proposta de usar a primeira imagem por um fluxo redesenhado como componentes interativos. A mecânica de etapas expansíveis foi definida como opção técnica deste handoff.
- 2026-10-24 (Claude Code): implementado em `case-studies/billing.html` (decisão 01) e `assets/css/billing.css`. `<ol role="list">` com 8 `details`/`summary`, primeira aberta, instrução “Select a step to explore the shared journey.” Layout em 4/2/1 colunas (≥1025/641–1024/≤640 px), com conectores decorativos só entre etapas consecutivas da mesma linha e setas verticais no mobile. Estados: ícone +/−, filete superior no aberto, sublinhado no hover, foco com contorno pêssego de 2 px. Imagem do fluxograma e legenda incorreta removidas da página; arquivos preservados. Verificado por clique, teclado (Tab/Enter/Espaço) e com JS desativado; ver [validação](../visual-narrative-validation.md).
- Concluído em: 2026-10-24
- 2026-10-24 (revisão do usuário): interação de clique removida. O fluxo virou 8 cards estáticos com todo o conteúdo visível. As etapas 01 e 08 mantêm o visual do card expandido para marcar início e fim. As setas foram trocadas pelo SVG fornecido, com preenchimento no accent via `mask`; no mobile, giradas para baixo. Revalidado em 320/375/768/1440, inclusive sem JS; ver [validação](../visual-narrative-validation.md).
