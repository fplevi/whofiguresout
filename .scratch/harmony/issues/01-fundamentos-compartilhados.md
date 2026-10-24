# 01: Apresentar os fundamentos compartilhados

**What to build:** Permitir que a pessoa compreenda a base compartilhada do Harmony por três evidências próprias: escalas primitivas, papéis semânticos e variáveis responsivas. Substituir o par de organização antes/depois por esse início demonstrável da progressão aprovada, integrando biblioteca compartilhada e governança à explicação visual.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] A leitura apresenta, nesta ordem, exemplos de escalas primitivas, papéis semânticos por uso e variáveis Desktop/Tablet/Mobile, usando respectivamente as fontes aprovadas `color=primitives.png`, `semantic-tokerns.png` e `variables.png` ou derivados fiéis dessas fontes.
- [x] Cada evidência tem uma linha própria, título e explicação factual em inglês. A explicação antecede a imagem no DOM e no mobile; a sequência explica relações entre camadas, sem afirmar cronologia histórica.
- [x] Biblioteca compartilhada, governança e exceções definidas aparecem junto dos fundamentos, preservando o sentido da referência comum para decisões. Não se afirma que todos os recursos passaram a um único arquivo físico.
- [x] O par antigo deixa a apresentação sem excluir seus originais. Não reaparece a afirmação de que Harmony não existia na imagem anterior. Argumentos de manutenção e acessibilidade/conteúdo ainda não integrados pelas próximas fatias permanecem disponíveis sem perda de sentido.
- [x] Escalas não são apresentadas como paleta completa ou contagem independente de tokens; papéis semânticos não comprovam resolução de aliases nem conformidade AA; variáveis são descritas como responsividade, sem alegação de temas claro/escuro.
- [x] A composição própria de Harmony usa blocos largos quando a densidade exigir. Alternância lateral só é aplicada onde a evidência continuar legível; nenhuma linha contém duas imagens, link de imagem crua ou controle para esconder explicações.
- [x] Derivados necessários têm nomes descritivos e mantêm contexto suficiente para escalas, papéis e modos responsivos. Os originais permanecem inalterados e o manifesto registra origem, recorte, dimensões, formato/qualidade, motivo e contexto preservado de cada derivado.
- [x] No navegador em 320, 375, 768 e 1440 px, as três imagens carregam e conservam proporção; explicações, detalhes relevantes e títulos são legíveis, sem overflow, sobreposição ou corte de texto significativo. Fontes não são reduzidas para resolver quebras; textos orientativos usam o tratamento secundário mais forte e contraste legível.
- [x] Nas quatro larguras, movimento normal e reduzido mantêm o conteúdo alcançável. A verificação normal parte do topo, usa rolagem real com viewport de 700 px de altura e observa cada seção ao chegar nela; nenhuma seção alta fica oculta pelo mecanismo de entrada. Sem JavaScript, a narrativa estática continua disponível.
- [x] Hierarquia de títulos, alternativas de imagem, associação explicação/evidência, navegação relevante por teclado e foco visível são conferidos. Hero, navegação, próximo projeto, contato, adoção gradual e iniciativas em desenvolvimento são preservados; formulário não é enviado.
- [x] Estilos novos ficam restritos a Harmony. Qualquer alteração compartilhada exige necessidade demonstrada e validação das páginas afetadas. Analytics e percurso no portfólio respeitam o ADR de continuidade; alterações locais anteriores e conteúdo fora do escopo são preservados.
- [x] A abordagem de QA de navegador existente é reaproveitada, adaptando expectativas ao comportamento externo. Um novo registro de validação da narrativa reúne capturas por viewport/elemento após carregamento das imagens, ambiente, combinações verificadas, resultados e limites reais; o registro editorial anterior permanece intacto. Critérios planejados não são apresentados como testes já realizados.

## Answer

Concluído em 2026-10-24, limitado ao ticket 01. Recuperado o checkpoint 268faa6 a partir do baseline de integração confirmado; preservados derivados, manifesto e evidências red/green existentes. A apresentação tem três linhas próprias com explicação antes da imagem e governança junto dos fundamentos; o par antigo saiu do render sem exclusão de originais. Argumentos de manutenção e acessibilidade/conteúdo foram preservados para os próximos tickets.

[Registro de validação e limites](../visual-narrative-validation.md): execução completa nesta worktree com 216 verificações de navegador aprovadas (320/375/768/1440, normal/reduzido, wheel real desde o topo em 700 px de altura, no-JS e teclado), inspeção visual dos recortes e 33 verificações de integridade aprovadas. Sem envio de formulário, PR ou publicação. O registro distingue as evidências herdadas, a antiga matriz interrompida e a execução completa atual. Os critérios acima foram marcados com base nesses resultados; não representam auditoria do sistema Harmony nem conclusão das sete evidências dos tickets seguintes.
