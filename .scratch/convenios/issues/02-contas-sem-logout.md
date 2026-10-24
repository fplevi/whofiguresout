# 02: Explicitar a alternância de contas sem logout

**What to build:** quem lê o estudo de caso CASSI Convênios entende que é possível alternar entre contas sem logout. A explicação fica junto do mockup existente e se limita ao comportamento confirmado, sem misturar funções que a imagem de contas não demonstra ou inventar a história da decisão.

**Blocked by:** None (can start immediately).

**Status:** claimed

- [x] A linha existente de contas é preservada e sua copy inglesa explicita a alternância sem logout, sustentada pela confirmação anterior do autor e pelo material Behance registrado. Não é necessário reproduzir essa interação no site.
- [x] Notificações, autorizações e extratos deixam de ser atribuídos à imagem de contas. A revisão não amplia alegações sobre a entrega dessas funções nem acrescenta material de processo para preencher a lacuna.
- [x] O texto não inventa motivação histórica, requisito, alternativa descartada ou contribuição específica de Felipe na decisão. A confirmação da alternância sem logout não é tratada como uma conclusão obtida apenas do mockup.
- [x] O mockup mantém proporção e transparência; continua sendo uma evidência com explicação própria, sem duplicar o PNG/WebP equivalente. Se um derivado for necessário para legibilidade, o original permanece intacto e fonte, recorte, dimensões, formato e motivo são acrescentados ao manifesto do case, preservando as entradas existentes.
- [x] A explicação vem antes da imagem no DOM e no mobile, com contraste legível e alternativa textual específica para o mockup. Não há etiquetas extras, link de imagem crua ou nova interação para esconder conteúdo. Fontes não são reduzidas para resolver quebras.
- [x] A página renderizada é verificada em 320, 375, 768 e 1440 px com movimento normal e reduzido, reaproveitando o QA existente. O texto e a imagem carregada ficam legíveis, proporcionais e sem sobreposição ou overflow horizontal; capturas são inspecionadas visualmente.
- [x] Rolagem real desde o topo nas quatro larguras com movimento normal confirma que as seções, inclusive a de funcionalidades, aparecem durante a leitura. Com movimento reduzido, o conteúdo fica imediatamente disponível. Não se usa apenas salto até a linha ou cálculo do limiar de animação como prova.
- [x] São conferidos o percurso pela home até o case, retorno a Work, navegação adjacente, destinos das lojas e teclado/foco nos links relevantes. Hero, home card, cartão, demais evidências no estado encontrado, contato, metadados e analytics permanecem preservados; o formulário não é enviado.
- [x] Ajustes visuais permanecem próprios do case; mudanças compartilhadas só ocorrem com necessidade demonstrada e validação de todas as páginas afetadas. Alterações simultâneas são preservadas, sem depender da execução dos outros tickets para entregar esta correção narrativa.
- [x] Resultados reais, capturas, ambiente e limitações da validação são registrados, distinguindo a evidência estática, as confirmações do autor e o comportamento do site observado no navegador. Não se afirma ter testado o aplicativo em produção.

## Comments

- 2026-10-24: Implemented in isolated branch `t3/accounts-no-logout`; status remains claimed for integration final review. Accounts-only copy/alt and presentation, unchanged source asset. Browser matrix: 85 passed / 0 failed, including ordinary wheel traversal in normal motion at 320/375/768/1440 and immediate reduced-motion visibility. Actual RED/GREEN, loaded captures and limitations: [02-validation.md](../02-validation.md). Ticket-specific asset record: [02-accounts.json](../assets/02-accounts.json). No shared script changes or production-app validation.

