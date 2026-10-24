# 03 — Integrar telas e variar a composição da narrativa

Status: resolved
Type: task
Dependências: 01 e 02 concluídos
Spec: [../spec.md](../spec.md)

## Entrega

Integrar as sete capturas e o dashboard na sequência do spec, com textos orientativos em inglês. Alternar imagem/texto nas laterais e usar largura maior nas telas densas. Cada imagem deve ter linha própria.

## Passos

1. Ler a sequência editorial e o manifesto do ticket 02.
2. Associar acesso e tela inicial às decisões 02 e 03, preservando a proximidade das notas com seus parágrafos.
3. Construir os trechos de reativação, pagamento único, parcelamento, revisão/validação e acompanhamento com copy apoiada nos assets.
4. Exibir o dashboard em linha própria antes dos resultados, com explicação de sua função operacional.
5. Ajustar apenas o CSS do Billing quando possível; preservar o sistema visual existente. Desfazer o par atual de `.cs-image-grid` sem alterar o layout dos outros cases.
6. Ajustar alt text, dimensões intrínsecas, carregamento e links para imagens maiores quando necessários à leitura mobile.

## Aceite

- A sequência segue o spec e apresenta as sete novas capturas mais o dashboard, com explicação individual.
- Há blocos laterais nas duas orientações e imagens largas; nenhuma linha contém duas screenshots.
- No mobile, o texto de cada etapa precede sua imagem no DOM e na tela.
- Textos orientativos essenciais têm contraste suficiente e não dependem das legendas apagadas existentes.
- Pagamentos à vista/com reativação e parcelado/sem reativação são identificados como exemplos diferentes.
- Revisão não vira sucesso; boleto pendente não vira pagamento. Métricas e alegações permanecem nos limites do spec.
- Hero, navegação, contato, métricas e próximo projeto permanecem preservados.

## Comments

- 2026-10-24: usuário aprovou alternância com blocos largos e seleção de sete novas telas. O antigo fluxograma foi substituído pelo escopo do ticket 01.
- 2026-10-24 (Claude Code): decisões 02/03 receberam telas laterais com legenda orientativa acima da imagem. What Shipped virou 6 linhas (reativação, à vista, parcelado, revisão, boletos, dashboard), com intro sobre cenários distintos e rótulos “Example with/without reactivation”. `.cs-image-grid` removido só do Billing; nenhum CSS compartilhado foi alterado. Na revisão visual, a coluna de imagem lateral passou de 7/12 para 8/12 por legibilidade. Cada imagem tem dimensões intrínsecas, `loading="lazy"`, alt específico e link “View full-size screen”.
- Concluído em: 2026-10-24
- 2026-10-24 (revisão do usuário): links “View full-size screen” removidos de todas as telas (abriam a imagem crua).
