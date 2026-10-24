# 04: Evidenciar a organização das etapas

**What to build:** permitir que o leitor compreenda a segunda decisão de Enrollment por três evidências complementares: elegibilidade e sequência, dados pessoais e orientação documental, e portabilidade como situação específica. Integrar as três capturas aprovadas junto da organização das etapas, cada uma com explicação própria, sem transcrever o fluxo completo. Seguir o spec de Enrollment.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] A segunda decisão recebe exatamente três novas linhas de evidência: a captura de parentesco/elegibilidade, a de dados pessoais do proponente e a de explicação/categorias de portabilidade. Cada linha tem uma única imagem, título, explicação em inglês e alternativa específicos.
- [x] A captura de parentesco preserva o contexto de elegibilidade e a sequência lateral de sete etapas. A copy não descreve uma seleção expandida que não aparece na imagem nem apresenta as três telas selecionadas como documentação completa dessas etapas.
- [x] A captura de dados é descrita como dados pessoais do proponente e orientação de documentos, sem deduzir outro titular a partir do nome do arquivo. A explicação respeita o upload parcialmente fora da captura; não promete área completa, envio ou validação bem-sucedida.
- [x] A captura escolhida de portabilidade é a de explicação e categorias. A copy trata essa situação como parte específica da jornada, não como sequência obrigatória entre os três estados disponíveis. Não reproduz requisitos contraditórios de uma tela omitida nem descreve conteúdo dos accordions fechados como visível.
- [x] Não são incluídas telas de início, simulador integral, pagamento, contrato ou os outros dois estados de portabilidade. A entrega mantém a seleção aprovada e os originais de todas as telas, inclusive as omitidas.
- [x] A composição combina alternância lateral onde houver leitura suficiente e blocos largos para imagens densas. A explicação sempre precede a respectiva imagem no DOM e no mobile; não se força alternância à custa da legibilidade ou do contexto.
- [x] Em 320, 375, 768 e 1440 px, textos e evidências relevantes são legíveis, com orientação de contraste adequado, sem redução de fontes, overflow, sobreposição ou distorção. Os três assets carregam e possuem alternativas específicas, dimensões intrínsecas e carregamento apropriado abaixo da dobra.
- [x] Enquadramentos são escolhidos por inspeção renderizada, preservando os elementos que sustentam cada argumento. Qualquer derivado é rastreável no manifesto por origem, limites de recorte, dimensões, formato e motivo; reuso de original também é registrado. Nenhum recorte tenta recuperar conteúdo fora dos limites da captura.
- [x] Toda a explicação fica visível no corpo da página, sem galeria, carrossel, disclosure ou links de imagem crua. As figuras não simulam operações reais de formulário, upload ou portabilidade.
- [x] Reaproveita-se/adapta-se o QA existente para a página renderizada nas quatro larguras, com movimento normal e reduzido. São verificadas ordem, carregamento, composição e a navegação/teclado relevantes; o comparador e as evidências já integradas continuam funcionais.
- [x] A rolagem real desde o topo, com movimento normal em todas as larguras, confirma que todas as seções aparecem, inclusive a decisão agora mais alta. A validação não se limita a movimento reduzido, saltos a elementos ou opacidade forçada; qualquer correção estrutural preserva a leitura e o escopo local.
- [x] A entrega registra revisão editorial, capturas inspecionadas, ambiente, alturas/larguras, movimento, falhas e limitações. Verifica a página já integrada e, se for a última entrega, registra a matriz completa da prancha, quatro telas e comparador, distinguindo testes executados de planejados.
- [x] Hero, contexto, papel, resultados, navegação, próximo projeto, contato e analytics são preservados contra uma referência do checkout anterior à mudança. Não se envia o formulário. Estilos ficam locais; eventual mudança compartilhada exige necessidade demonstrada e validação das páginas afetadas.
- [x] O ticket 01 permanece aberto e inalterado, sem bloquear esta entrega. Não se ampliam alegações de resultado, produção ou causalidade a partir de screenshots com dados de exemplo.

## Comments

- 2026-10-24: granularidade e ausência de bloqueadores aprovadas pelo usuário com “sim”, na proposta revisada de quatro tickets. As três telas formam uma entrega completa do argumento de organização das etapas, incluindo apresentação e QA. Nenhum critério foi executado ou validado nesta conversa de especificação.

## Answer

Implemented the three approved journey evidence blocks with separate English explanations, specific alternatives and responsive full-width presentation of untouched originals. Browser red-to-green tests and the complete current-page matrix pass; preserved surfaces and original integrity were checked against f8f9034. See [ticket 04 validation](../validation-ticket-04.md), [asset manifest](../presentation-assets-04.json), and [executed evidence](../qa/ticket-04/). Baseline comparator focus limitations and final combined-page work owned by other tickets are explicitly recorded. Issue 01 remains unchanged.


## Final integration closure

2026-10-24: resolved after integration of all four slices and final review corrections at 6d3766b. Full matrix: 308/308 checks; all 48 evidence screenshots remained pixel-identical after CSS maintenance. Spec review: zero actionable findings. Standards: three P3 findings corrected. [Final review](../code-review.md). Issue 01 remains unchanged; no contact submission.
