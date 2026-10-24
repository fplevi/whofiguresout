# 05: Explicar envio para análise e próximos passos

**What to build:** permitir que o leitor compreenda o que a confirmação de envio comunica ao proponente. Integrar a captura aprovada de confirmação junto da terceira decisão, explicando envio para análise, protocolo e próximos passos sem confundir esse momento com aprovação, adesão concluída ou uma consulta real de status. Seguir o spec de Enrollment.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] A confirmação de envio aparece uma única vez junto da terceira decisão, com título, explicação em inglês e alternativa próprios. O argumento é o esclarecimento do momento e dos próximos passos; a tela não é rotulada como aprovação ou adesão concluída.
- [ ] A copy limita a evidência ao envio para análise, protocolo e orientações visíveis. Não apresenta pagamento concluído, consulta real de status, notificação efetivamente entregue ou prazo de atendimento cumprido como fatos demonstrados pela captura.
- [ ] O link de acompanhamento que aparece na imagem é tratado como parte da captura com placeholder. Não é convertido em controle funcional do portfólio nem apresentado como uma tela de status inexistente no material.
- [ ] O relato já confirmado de mensagens e acompanhamento distingue o argumento do projeto do alcance específico desta captura. Reduzir consultas ao atendimento continua sendo objetivo sem medição disponível.
- [ ] A figura tem uma única imagem e explicação própria, com composição lateral ou larga conforme a leitura permitir. A explicação precede a imagem no DOM e no mobile, permanece visível no corpo da página e usa contraste legível, sem galeria, disclosure ou link de imagem crua.
- [ ] Em 320, 375, 768 e 1440 px, protocolo e avisos necessários ao argumento conservam contexto, a orientação textual é legível e não há overflow, sobreposição, distorção ou redução de fontes para resolver quebras.
- [ ] A imagem carrega e possui alternativa específica, dimensões intrínsecas e carregamento apropriado abaixo da dobra. O original permanece intacto; qualquer derivado é registrado no manifesto com origem, limites de recorte, dimensões, formato e motivo. O reuso do original também é registrado.
- [ ] O QA existente é reaproveitado/adaptado para verificar a página renderizada nas quatro larguras, com movimento normal e reduzido, incluindo carregamento, ordem, legibilidade e navegação/teclado relevantes. O comparador e as evidências já integradas permanecem funcionais.
- [ ] A rolagem real desde o topo, com movimento normal em todas as larguras, confirma que todas as seções aparecem. Capturas isoladas, opacidade forçada ou saltos a elementos não substituem a verificação do percurso, inclusive após aumentar a altura das seções.
- [ ] A entrega registra revisão editorial, capturas inspecionadas, ambiente, alturas/larguras, movimento, testes executados, falhas e limites. Verifica a página já integrada e, se for a última entrega, registra a matriz completa da prancha, quatro telas e comparador; não declara como executada uma validação apenas planejada.
- [ ] Hero, contexto, papel, resultados, navegação, próximo projeto, contato e analytics são preservados contra uma referência do checkout anterior à mudança. Não se envia o formulário. Estilos ficam locais; mudanças compartilhadas exigem necessidade demonstrada e validação das páginas afetadas.
- [ ] O ticket 01 permanece aberto e inalterado, sem bloquear esta entrega. Os 171% permanecem crescimento de propostas, sem equivalência com adesões concluídas nem atribuição causal exclusiva ao redesenho. Não se acrescenta comprovação de produção a partir da imagem.

## Comments

- 2026-10-24: granularidade e ausência de bloqueadores aprovadas pelo usuário com “sim”, na proposta revisada de quatro tickets. Publicado para implementação futura; nenhum critério foi executado ou validado nesta conversa de especificação.
