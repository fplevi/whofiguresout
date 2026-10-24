# 02: Mostrar a síntese de discovery

**What to build:** permitir que o leitor de Enrollment veja como o trabalho de discovery foi organizado antes de conhecer as decisões. Apresentar a prancha fornecida como “Desk Research” em um único bloco largo após “My Role” e antes de “The Decisions”, com explicação própria em inglês que funcione sem decifrar as pequenas anotações da imagem. Seguir o spec de Enrollment e seus limites factuais.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] A prancha aparece uma única vez após o relato existente de “My Role” e antes das decisões. O relato original permanece preservado; a adição tem título, explicação e alternativa de imagem próprios.
- [x] A explicação em inglês identifica a matriz CSD, os brainstorms, a jornada do usuário/cliente e o mapa de empatia como artefatos visíveis de síntese. Não inventa achados, fontes, amostra, participação/autoria de workshops ou relação causal entre notas ilegíveis e decisões.
- [x] O nome “Desk Research” não é tratado como comprovação independente dos métodos e fontes usados. A copy preserva os fatos de discovery já confirmados e distingue esses fatos do que a prancha permite observar.
- [x] A imagem composta permanece um único bloco de evidência, preferencialmente com enquadramento contextual largo, sem nova galeria. As áreas nomeadas continuam reconhecíveis; nenhum material cortado na borda inferior é reconstruído ou apresentado como disponível.
- [x] Em 320, 375, 768 e 1440 px, a explicação é legível e autossuficiente, vem antes da imagem no DOM e no mobile e usa contraste legível. O aceite não depende de ler cada post-it rasterizado. Não se reduzem fontes para resolver quebras.
- [x] A imagem carrega, mantém proporção e possui alternativa específica, dimensões intrínsecas e carregamento apropriado para conteúdo abaixo da dobra. Não há overflow, sobreposição ou corte do texto explicativo.
- [x] O original permanece intacto. Caso seja necessário derivado de apresentação, o manifesto registra origem, enquadramento, dimensões, formato e motivo; se o original for reutilizado, isso também fica registrado. Não se altera a imagem para fabricar texto legível.
- [x] O bloco permanece disponível sem disclosure, carrossel ou link de imagem crua. A navegação por teclado segue uma ordem lógica e a evidência não introduz controles sem finalidade.
- [x] O QA existente é reaproveitado/adaptado para observar a página renderizada. Nas quatro larguras, com movimento normal e reduzido, verifica carregamento, composição e visibilidade; com movimento normal, a rolagem real desde o topo confirma que todas as seções aparecem, sem forçar opacidade ou substituir o percurso por saltos a elementos.
- [x] A entrega verifica também a página já integrada e registra capturas inspecionadas, ambiente, alturas/larguras, preferências de movimento, verificações executadas e limites. Se for a última entrega integrada, registra a matriz completa da prancha, quatro telas e comparador; verificações pendentes não são declaradas aprovadas.
- [x] Hero, contexto, papel original, resultados, navegação, próximo projeto, contato e analytics permanecem preservados em relação ao estado atual anterior à mudança. O formulário não é enviado. Estilos ficam locais; eventual mudança compartilhada exige necessidade demonstrada e validação das páginas afetadas.
- [x] O ticket 01 permanece aberto e inalterado, sem bloquear esta entrega. As alegações de propostas e objetivo não medido de reduzir consultas ao atendimento não são ampliadas.

## Comments

- 2026-10-24: granularidade e ausência de bloqueadores aprovadas pelo usuário com “sim”, na proposta revisada de quatro tickets após a inclusão da prancha. Publicado para implementação futura; nenhum critério foi executado ou validado nesta conversa de especificação.

## Answer

Implemented the single discovery-synthesis block after the preserved My Role account and before The Decisions. Reused the untouched original with factual English orientation, specific alternative text, intrinsic dimensions and lazy/async loading. Local Enrollment styles only.

Red-to-green browser evidence and the post-merge eight-combination matrix passed (320/375/768 at height 700; 1440 at height 900; normal/reduced motion), including real wheel traversal from the top, loaded proportional images, measured 7.55:1 explanatory-text contrast, comparison regression, preserved surfaces against f8f9034 and zero contact submissions. All 16 final captures were visually inspected. Issue 01, original assets and shared CSS/JS remain unchanged.

See [ticket validation](../validation-ticket-02.md), [asset manifest](../presentation-assets-02.json) and [executed evidence](../qa/ticket-02/). This acceptance covers the current ticket-02 page; future ticket 03–05 evidence and final combined validation remain their assigned work. Baseline comparison focus/name limitations are recorded, not claimed fixed here.
