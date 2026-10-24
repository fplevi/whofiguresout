# 03: Tornar legível a biblioteca própria e ajustar o fechamento

**What to build:** quem lê o estudo de caso CASSI Convênios consegue examinar no corpo da página uma evidência legível dos estados e áreas de toque dos botões da biblioteca própria. Essa é a última evidência de funcionalidades e conduz a um fechamento baseado nas entregas sustentadas, com a distinção correta entre Convênios e Harmony.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] A biblioteca permanece como última evidência de funcionalidades. Um recorte legível da documentação de botões mostra estados e áreas de toque com contexto suficiente para entender o exemplo, sem depender de miniatura integral ilegível ou de conteúdo fora das bordas da fonte.
- [ ] A documentação recebe largura adequada no corpo da página. Restrições de apresentação que a comprimem são ajustadas no escopo do case; alternância lateral só é usada onde favorecer leitura, sem transformar o case em uma réplica do Billing e sem reduzir fontes.
- [ ] A explicação inglesa própria antecede a imagem no DOM e no mobile, com contraste legível. A imagem tem alternativa textual específica, proporção e dimensões intrínsecas corretas e carregamento apropriado para o corpo.
- [ ] O link que abre a imagem crua é removido. A leitura completa da evidência e de sua explicação permanece no corpo, sem modal, galeria, acordeão ou interação para esconder conteúdo e sem etiquetas extras.
- [ ] A copy identifica Convênios como produto anterior ao Harmony, com biblioteca e linguagem visual próprias. Não afirma construção sobre Harmony, migração para ele ou reaproveitamento posterior de componentes. Documentar estados e áreas de toque não é apresentado como certificação de acessibilidade.
- [ ] O fechamento se limita ao aplicativo entregue e à biblioteca documentada como base do próprio produto. A alegação de redução de retrabalho é retirada ou qualificada para não representar impacto demonstrado; não há novas métricas, ganhos de eficiência ou ambiguidade de fundação compartilhada com Harmony.
- [ ] Originais são preservados. Derivados mantêm proporção, contexto e transparência quando presente, em formato apropriado, sem impor JPEG. O manifesto registra fonte, limites do recorte, dimensões, formato e motivo editorial, preservando entradas de outros tickets; pares equivalentes não viram evidências adicionais.
- [ ] A página renderizada é verificada em 320, 375, 768 e 1440 px com movimento normal e reduzido, reaproveitando o QA existente. Capturas com imagens efetivamente carregadas são inspecionadas para confirmar leitura dos estados e áreas de toque, ordem, contraste e ausência de sobreposição ou overflow horizontal. Carregar a imagem ou aplicar um token de cor não basta para aprovar a legibilidade.
- [ ] Rolagem real desde o topo nas quatro larguras com movimento normal confirma a aparição de todas as seções, inclusive a mais alta no mobile. Com movimento reduzido, o conteúdo está imediatamente disponível. Saltos para elementos ou cálculos do limiar de animação não substituem essa verificação.
- [ ] São conferidos o percurso pela home até o case, retorno a Work, navegação adjacente, destinos das lojas e teclado/foco nos links relevantes após a remoção do link cru. Hero, home card, cartão, demais linhas no estado encontrado, contato, metadados e analytics permanecem preservados; o formulário não é enviado.
- [ ] Estilos ficam no escopo de Convênios. Uma eventual alteração compartilhada exige necessidade demonstrada e validação de todas as páginas afetadas. Alterações simultâneas e os demais documentos existentes são preservados; este ticket pode ser demonstrado sem aguardar os outros dois.
- [ ] Resultados reais, capturas, ambiente e limitações ficam registrados separadamente dos critérios. Auditorias automáticas e inspeção manual são distinguidas; não se declara validação com leitor de tela, de produção ou desta revisão sem execução correspondente.

