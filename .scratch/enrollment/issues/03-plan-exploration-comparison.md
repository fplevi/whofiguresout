# 03: Integrar o comparador à exploração

**What to build:** permitir que o leitor relacione diretamente a decisão de exploração dos planos à mudança de organização das opções. Integrar o comparador antes/depois existente em um único bloco largo junto da primeira decisão, com orientação factual e operação acessível, eliminando sua apresentação separada em “What Shipped”. Seguir o spec de Enrollment.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] O comparador existente aparece uma única vez junto da primeira decisão sobre exploração antes da criação de conta, com explicação em inglês orientando a leitura dos cartões antigos e da organização comparativa dos benefícios.
- [x] A apresentação anterior em “What Shipped” é removida ao realocar o comparador, sem duplicação nem seção vazia. Não se acrescenta outra captura integral do simulador; o hero e seu poster permanecem preservados.
- [x] A copy distingue a mudança de organização de redução de preço ou catálogo, de comparação entre produtos equivalentes e de prova de ausência de cadastro ou de fornecimento de dados pessoais. Não amplia os fatos já confirmados da primeira decisão.
- [x] O controle nativo e as duas imagens existentes são mantidos. Esse bloco continua sendo a exceção funcional de comparação em duas camadas, sem converter as novas evidências em uma galeria de pares.
- [x] O controle tem nome acessível que explique sua finalidade, foco visível e entrada/saída por Tab. Home, End, ArrowLeft e ArrowRight alteram o valor e a revelação visual de forma correspondente, incluindo os extremos, com movimento normal e reduzido.
- [x] Ponteiro e toque operam o controle de forma correspondente ao antes/depois mostrado. O teste usa uma região realmente visível e não coberta pela navegação fixa.
- [x] Em 320, 375, 768 e 1440 px, o comparador tem composição larga legível, imagens carregadas e proporcionais e rótulos compreensíveis. A explicação precede a evidência no DOM e no mobile; não há overflow, sobreposição ou redução de fontes para ajustar quebras, e o texto orientativo tem contraste legível.
- [x] As imagens originais permanecem intactas, com alternativas específicas, dimensões intrínsecas e carregamento apropriado. O manifesto registra os originais reutilizados ou, se necessário, qualquer derivado com origem, enquadramento, dimensões, formato e motivo.
- [x] Não são acrescentados links de imagem crua, controles de disclosure ou interações destinadas apenas a esconder conteúdo.
- [x] O QA existente é adaptado para a nova posição e o nome acessível do comparador. Verifica comportamento externo, sem exigir correspondência literal com o markup antigo, o seletor de “What Shipped” ou o último commit.
- [x] Nas quatro larguras e com movimento normal/reduzido, verifica-se a página renderizada já integrada. A rolagem real desde o topo com movimento normal confirma que todas as seções aparecem; capturas isoladas, saltos a elementos ou opacidade forçada não substituem esse teste.
- [x] A entrega registra capturas inspecionadas, ambiente, alturas/larguras, movimentos, testes do controle, erros/falhas e limitações. Se for a última entrega integrada, registra a matriz completa da prancha, quatro telas e comparador; não apresenta QA histórico ou pendente como executado nesta revisão.
- [x] Hero, contexto, papel, resultados, navegação, próximo projeto, contato e analytics são preservados contra uma referência do checkout anterior à mudança. Não se envia o formulário. Estilos ficam locais; mudanças compartilhadas só ocorrem com necessidade demonstrada e validação de todas as páginas afetadas.
- [x] O ticket 01 permanece aberto e inalterado, sem bloquear esta entrega. Os 171% continuam sendo crescimento de propostas, sem equivalência a adesões concluídas ou causalidade exclusiva; a redução de consultas ao atendimento continua objetivo não medido.

## Comments

- 2026-10-24: Claimed by implementation sub-agent on `t3/enrollment-plan-comparison`, worktree `t3-7c1e1b19`, server port 8103. Clean HEAD contains integration tip `fa56b5c`; using the approved rendered Enrollment page seam and ticket-specific browser QA.

- 2026-10-24: granularidade e ausência de bloqueadores aprovadas pelo usuário com “sim”, na proposta revisada de quatro tickets. Publicado para implementação futura; nenhum critério foi executado ou validado nesta conversa de especificação.

- 2026-10-24: Recovered commit `66ebc77` into branch `t3/enrollment-visual-narrative`, worktree `t3-6485afe7`, preserving the original branch/worktree and its newer uncommitted QA evidence. Ticket 03 is implemented and the current discovery/journey/comparison page passes 244 browser checks on port 8123. See [validation-ticket-03.md](../validation-ticket-03.md) for fresh evidence, source preservation, editorial review, measured contrast, harness failures and limitations. Ticket 05 and final five-new-image acceptance are not claimed. Integration tip `9b86741` was merged as `61a19d3`; the post-merge complete current-page rerun again passed all eight cases and 244 checks. Final checks and `git diff --check` pass. No contact submission was made; issue 01 remains byte-unchanged.
