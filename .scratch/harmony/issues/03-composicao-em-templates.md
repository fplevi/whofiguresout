# 03: Explicar a composição em templates

**What to build:** Permitir que a pessoa compreenda templates do Harmony como composições configuráveis dos padrões, por uma evidência legível acompanhada de explicação própria. Essa entrega pode avançar independentemente da aplicação nos componentes, usando a estrutura estabelecida nos fundamentos e mantendo a posição de leitura prevista para a composição.

**Blocked by:** 01 — Apresentar os fundamentos compartilhados.

**Status:** resolved

- [x] Uma evidência baseada em `templates.png` ou derivado fiel demonstra composições configuráveis em design, com título e explicação próprios em inglês.
- [x] A explicação relaciona templates aos padrões compartilhados. O recorte preserva exemplos de composição e contexto de configuração suficiente para sustentar o argumento, sem depender da leitura de todo o texto minúsculo do canvas.
- [x] A posição editorial é posterior à aplicação nos componentes e anterior à documentação/implementação quando essas fatias estiverem presentes. Não há dependência artificial do ticket 02 para começar ou verificar esta entrega, nem se criam placeholders públicos para conteúdo ainda não integrado.
- [x] A copy não alega geração automática de telas, paridade entre design e código, velocidade medida ou entrega da conversão de protótipos para React. A sequência continua sendo progressão de leitura, sem cronologia histórica inventada.
- [x] A explicação vem antes da imagem no DOM/mobile. A evidência recebe bloco largo ou largura comprovadamente suficiente para sua densidade, com uma imagem na linha, texto orientativo de contraste legível e sem reduzir fontes para resolver quebras.
- [x] O conteúdo fica visível sem disclosure, galeria ou link para imagem crua. O exemplo permanece evidência estática de configuração no design, sem simulação de ferramenta ou funcionalidade de produção.
- [x] Todo derivado necessário tem nome descritivo e registro no manifesto com origem, recorte, dimensões, formato/qualidade, motivo e contexto retido. Originais são preservados, sem recuperar artificialmente conteúdo que não está na captura.
- [x] No navegador em 320, 375, 768 e 1440 px, a imagem carrega, mantém proporção e oferece detalhe útil ao argumento. Não há overflow, sobreposição ou corte de texto significativo; título, explicação e legenda são legíveis.
- [x] Nas quatro larguras, a página é percorrida desde o topo com rolagem real, movimento normal e viewport de 700 px de altura, observando a visibilidade de cada seção quando alcançada. Movimento reduzido e JavaScript desabilitado mantêm a narrativa disponível; a nova seção não esconde as evidências anteriores.
- [x] Hierarquia de títulos, texto alternativo, ordem de leitura, teclado e foco relevante são conferidos. Hero, navegação, próximo projeto, contato, adoção gradual, autoria e iniciativas em desenvolvimento são preservados; formulário não é enviado.
- [x] Estilos novos são próprios de Harmony. Alteração compartilhada só ocorre com necessidade demonstrada e validação de todas as páginas afetadas, preservando analytics conforme o ADR de continuidade, demais alterações locais e conteúdo fora do escopo.
- [x] A fatia reaproveita a abordagem de QA existente no navegador e registra resultados externos, capturas por viewport/elemento após carregamento, ambiente e limites reais no registro de validação da narrativa. Registros editoriais anteriores são preservados e verificação planejada não é declarada executada.


## Answer

Implemented template composition as one static, named evidence with factual English copy before the image. It follows the existing foundations/application slot and precedes the retained maintenance decision section. No component or Storybook placeholder was introduced. The wide source crop retains composition/configuration in the original relationship; narrow screens receive explicitly identified card/success/configuration excerpts. Originals are untouched and styles remain local to `.harmony-case`.

Browser TDD: missing evidence red **0/1**, evidence green **3/0**; a visually detected 320 px heading-word break produced red **3/1**, then green **4/0** after wording changed without reducing typography. Completed browser matrix: **291 passed, 0 failed**, including four widths ? two motion modes, real wheel traversal from the top at 700 px height, no-JS, loaded-image captures, heading/read order, navigation/focus and contact without submission. Artifact integrity: **37 passed, 0 failed**. `git diff --check` passed.

Evidence and honest environment/limits: [appended validation](../visual-narrative-validation.md#ticket-03--template-composition-2026-10-24), [browser results](../qa/template-verified/results.json), [artifact results](../qa/template-artifact-integrity.json), and [slice manifest with exact hashes/rectangles](../template-image-manifest.json). [Image manifest narrative](../image-manifest.md#ticket-03--template-composition-2026-10-24) preserves and extends the prior record. Separate helper `template-narrative-qa.py` avoids sibling changes to the shared QA script. Final seven-image integration remains ticket 04; this result does not claim its completion or a live system accessibility/analytics audit.
