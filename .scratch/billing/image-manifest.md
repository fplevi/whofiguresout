# Billing — manifesto de imagens

Data: 2026-10-24. Ticket: [02](issues/02-image-preparation.md).

Originais em `assets/images/billing/` permanecem intactos. Derivados em `assets/images/billing/editorial/`, gerados com Pillow (`crop`, sem redimensionar), salvos como JPEG progressivo qualidade 86. JPEG foi escolhido após comparar com PNG otimizado do mesmo recorte: 2–4× menor e sem perda visível de legibilidade no texto da interface. Coordenadas no formato `(x0, y0, x1, y1)` sobre o original de 1920 × 1200.

| Original | Uso | Derivado | Recorte | Dimensões | Peso | Motivo | Integração |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `MFA.png` (2.2 MB) | Derivado | `access-verification-channel.jpg` | (1300, 365, 1845, 1055) | 545 × 690 | 47 KB | O cartão de identificação ocupa ~25% da largura; em coluna lateral ficaria ilegível. O recorte mantém título, pergunta, opções e-mail/SMS, botão “Enviar código”, “Não reconheço esses dados” e aviso de privacidade. | Decisão 02, imagem à esquerda. |
| `tela-inicial.png` | Derivado | `negotiation-options.jpg` | (100, 172, 1820, 1150) | 1720 × 978 | 97 KB | Remove cabeçalho/menu do site e o card seguinte cortado no rodapé. Mantém as duas opções com valores e botões e o quadro “Sua pendência”. | Decisão 03, imagem à direita. |
| `oferta-reativação.png` | Derivado | `reactivation-offer.jpg` | (250, 240, 1670, 960) | 1420 × 720 | 92 KB | Remove cabeçalho e rodapé. Mantém plano, benefícios, mensalidade após reativação, valor, explicação e ações “Voltar”, “Negociar sem reativação” e “Continuar”. | What Shipped — reativação, imagem à esquerda. |
| `pagamento-a-vista.png` | Derivado | `single-payment-with-reactivation.jpg` | (90, 55, 1830, 745) | 1740 × 690 | 90 KB | Remove rodapé. Mantém resumo “Sua negociação com reativação”, escolha da forma de pagamento, parcela única, avisos e ações. | Pagamento único, imagem à direita. |
| `pagamento-parcelado.png` | Derivado | `installments-without-reactivation.jpg` | (85, 55, 1835, 835) | 1750 × 780 | 113 KB | Remove rodapé. Mantém resumo “Sua negociação sem reativação”, entrada opcional, quantidade de parcelas, nota sobre entrada e ações. | Parcelamento, imagem à esquerda. |
| `resumo.png` | Derivado | `review-and-validation.jpg` | (85, 225, 1835, 975) | 1750 × 750 | 90 KB | Remove cabeçalho/menu e rodapé. Mantém dívida antes da negociação, negociação, total, vencimentos e o painel de verificação com código e “Validar negociação”. | Revisão e validação, bloco largo. |
| `3-boletos.png` | Derivado | `pending-payment-documents.jpg` | (85, 0, 1835, 630) | 1750 × 630 | 72 KB | Foca o acompanhamento: mensagem para manter a negociação em dia, “3 boletos pendentes”, valores, vencimentos e “Gerar documento”. Exclui o bloco inferior de contribuição trabalhista, fora do argumento. | Acompanhamento, imagem à esquerda. |
| `billing-digital-platform-dashboard.jpg` | Uso integral | — | — | 1920 × 1080 | 64 KB | Escolhido entre JPG (64 KB) e PNG (212 KB) do mesmo conteúdo: legibilidade equivalente, menor peso. O PNG não é exibido. | Operação, bloco largo antes de “The Outcome”. |
| `tela.png` | Fora da seleção | — | — | — | — | Sobrepõe o acompanhamento (decisão aprovada). | — |
| `billing-digital-platform-flow.jpg` / `.png` | Fora da apresentação | — | — | — | — | Substituído pelo fluxo interativo (ticket 01); arquivos preservados como referência. | — |

## Links para versão maior

Removidos na revisão do usuário (2026-10-24): abriam a imagem crua no navegador, sem ganho real nem no celular. As imagens aparecem somente na página.

## Cenários

Os derivados não são recortados para comparação: pagamento único (com reativação) e parcelado (sem reativação) mantêm cada um seu próprio resumo de negociação, com valores distintos visíveis e títulos “com reativação”/“sem reativação” preservados.
