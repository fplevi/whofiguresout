# 02: Demonstrar a aplicação nos componentes

**What to build:** Permitir que a pessoa veja como os fundamentos do Harmony se aplicam a variantes e estados de botões e à navegação adaptada entre contextos. Integrar acessibilidade e conteúdo como requisitos contínuos de design dos componentes, com uma explicação própria para cada evidência e sem promessas de conformidade auditada.

**Blocked by:** 01 — Apresentar os fundamentos compartilhados.

**Status:** resolved

- [x] Depois dos fundamentos, a leitura apresenta duas evidências próprias, nesta ordem: variantes/estados de botões a partir de `buttons.png` e navegação por contexto a partir de `components.png`, usando originais ou derivados fiéis.
- [x] A explicação de botões identifica uma seleção legível de variantes, tamanhos e estados. A explicação de navegação distingue Portal/Intranet e contextos de perfil, sem transformar a imagem em catálogo completo de componentes.
- [x] Cada imagem tem título e texto orientativo factual em inglês antes dela no DOM/mobile. Os recortes mostram o detalhe necessário ao argumento, preservando identificação e contexto; miniaturas panorâmicas ilegíveis não substituem essa demonstração.
- [x] O argumento existente de acessibilidade e conteúdo fica integrado a essa aplicação: contraste, semântica e mensagens de erro são considerações contínuas de design/desenvolvimento. Não se inventa uma regra documentada específica, auditoria aprovada ou comportamento implementado com base apenas nos pixels.
- [x] A antiga apresentação separada de acessibilidade/conteúdo deixa de repetir o argumento integrado. O sentido da nota de requisitos contínuos permanece, e os argumentos de manutenção reservados ao fechamento continuam preservados.
- [x] A apresentação combina alternância lateral onde os recortes permitem leitura e blocos largos quando necessário. Há uma imagem por linha, sem galeria, links crus ou interação criada apenas para esconder conteúdo; as fontes não são reduzidas para corrigir quebras.
- [x] Derivados têm nomes descritivos, originais inalterados e manifesto atualizado com origem, limites do recorte, dimensões, formato/qualidade e justificativa. Não se fabricam controles ou detalhes ausentes das fontes.
- [x] No navegador em 320, 375, 768 e 1440 px, as novas imagens carregam com proporção correta; explicações, legendas e detalhes relevantes ficam legíveis, sem overflow, sobreposição ou corte significativo. Texto orientativo mantém tratamento secundário forte e contraste legível.
- [x] Nas quatro larguras, rolagem real desde o topo com movimento normal e viewport de 700 px de altura revela as seções ao longo da leitura. Movimento reduzido e ausência de JavaScript mantêm a mesma narrativa estática disponível; os fundamentos continuam alcançáveis após a ampliação da página.
- [x] Títulos, alternativas de imagem, ordem de leitura, navegação por teclado e foco visível são conferidos. Hero, navegação, próximo projeto, contato, adoção gradual, autoria e trabalho em desenvolvimento permanecem preservados, sem envio do formulário.
- [x] A fatia usa estilos específicos de Harmony e preserva alterações locais anteriores. Qualquer mudança compartilhada exige necessidade demonstrada e validação de todas as páginas afetadas; analytics e percurso no portfólio mantêm a continuidade definida no ADR.
- [x] QA existente é adaptado à evidência e ao comportamento externo desta fatia. O registro de validação da narrativa recebe capturas por viewport/elemento após carregamento, resultados, ambiente e limites efetivamente observados, preservando os documentos anteriores e distinguindo testes executados de pendentes.

## Comments

2026-10-24: Claimed in isolated worktree `C:/Users/fplev/.t3/worktrees/Portfolio/t3-585c7417`, branch `t3/585c7417`. Clean HEAD and integration tip both confirmed as `2a58eb63b2ca1d5cad14ee3047370be4e826f436` before edits. Ticket 01 is resolved. Using the approved rendered-browser seam and existing Playwright workflow; scope limited to ticket 02.

## Answer

Concluído em 2026-10-24, limitado ao ticket 02. Duas evidências próprias seguem os fundamentos: Standard solid/outline em NormalSize/SmallSize e navegação de perfil Portal/Intranet. Recortes fiéis preservam rótulos e contexto, uma imagem por evidência, prosa em inglês antes da imagem no DOM/mobile e alternância lateral em 1440. Acessibilidade/conteúdo entram como requisitos contínuos junto da aplicação; o bloco separado foi removido. React/Next, manutenção e contratação ficam preservados para 04. Nenhuma implementação dos tickets irmãos, mudança compartilhada, PR ou publicação.

[Validação desta fatia](../visual-narrative-validation.md#ticket-02--component-application): ciclos red/green por comportamento; matriz final com **308 verificações aprovadas**, capturas de leitura com **20 aprovadas**, integridade com **46 aprovadas**, todas sem falhas. Inclui 320/375/768/1440 × 700, movimento normal/reduzido, wheel real desde o topo, no-JS e teclado/foco, sem envio de formulário. Originais e fundamentos preservados, manifesto acrescentado com limites, dimensões e hashes exatos. Inspeção visual das imagens carregadas reconhece o texto pequeno suavizado e nomes sobrepostos da fonte; não representa teste funcional ou auditoria do Harmony. Os critérios marcados são sustentados pelo registro, que explicita limites e mantém o histórico anterior.
