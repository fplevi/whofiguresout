# 02: Demonstrar a aplicação nos componentes

**What to build:** Permitir que a pessoa veja como os fundamentos do Harmony se aplicam a variantes e estados de botões e à navegação adaptada entre contextos. Integrar acessibilidade e conteúdo como requisitos contínuos de design dos componentes, com uma explicação própria para cada evidência e sem promessas de conformidade auditada.

**Blocked by:** 01 — Apresentar os fundamentos compartilhados.

**Status:** ready-for-agent

- [ ] Depois dos fundamentos, a leitura apresenta duas evidências próprias, nesta ordem: variantes/estados de botões a partir de `buttons.png` e navegação por contexto a partir de `components.png`, usando originais ou derivados fiéis.
- [ ] A explicação de botões identifica uma seleção legível de variantes, tamanhos e estados. A explicação de navegação distingue Portal/Intranet e contextos de perfil, sem transformar a imagem em catálogo completo de componentes.
- [ ] Cada imagem tem título e texto orientativo factual em inglês antes dela no DOM/mobile. Os recortes mostram o detalhe necessário ao argumento, preservando identificação e contexto; miniaturas panorâmicas ilegíveis não substituem essa demonstração.
- [ ] O argumento existente de acessibilidade e conteúdo fica integrado a essa aplicação: contraste, semântica e mensagens de erro são considerações contínuas de design/desenvolvimento. Não se inventa uma regra documentada específica, auditoria aprovada ou comportamento implementado com base apenas nos pixels.
- [ ] A antiga apresentação separada de acessibilidade/conteúdo deixa de repetir o argumento integrado. O sentido da nota de requisitos contínuos permanece, e os argumentos de manutenção reservados ao fechamento continuam preservados.
- [ ] A apresentação combina alternância lateral onde os recortes permitem leitura e blocos largos quando necessário. Há uma imagem por linha, sem galeria, links crus ou interação criada apenas para esconder conteúdo; as fontes não são reduzidas para corrigir quebras.
- [ ] Derivados têm nomes descritivos, originais inalterados e manifesto atualizado com origem, limites do recorte, dimensões, formato/qualidade e justificativa. Não se fabricam controles ou detalhes ausentes das fontes.
- [ ] No navegador em 320, 375, 768 e 1440 px, as novas imagens carregam com proporção correta; explicações, legendas e detalhes relevantes ficam legíveis, sem overflow, sobreposição ou corte significativo. Texto orientativo mantém tratamento secundário forte e contraste legível.
- [ ] Nas quatro larguras, rolagem real desde o topo com movimento normal e viewport de 700 px de altura revela as seções ao longo da leitura. Movimento reduzido e ausência de JavaScript mantêm a mesma narrativa estática disponível; os fundamentos continuam alcançáveis após a ampliação da página.
- [ ] Títulos, alternativas de imagem, ordem de leitura, navegação por teclado e foco visível são conferidos. Hero, navegação, próximo projeto, contato, adoção gradual, autoria e trabalho em desenvolvimento permanecem preservados, sem envio do formulário.
- [ ] A fatia usa estilos específicos de Harmony e preserva alterações locais anteriores. Qualquer mudança compartilhada exige necessidade demonstrada e validação de todas as páginas afetadas; analytics e percurso no portfólio mantêm a continuidade definida no ADR.
- [ ] QA existente é adaptado à evidência e ao comportamento externo desta fatia. O registro de validação da narrativa recebe capturas por viewport/elemento após carregamento, resultados, ambiente e limites efetivamente observados, preservando os documentos anteriores e distinguindo testes executados de pendentes.
