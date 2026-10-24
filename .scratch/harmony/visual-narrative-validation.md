# Harmony — validação da narrativa visual

Data: 2026-10-24. Escopo concluído: [ticket 01, fundamentos compartilhados](issues/01-fundamentos-compartilhados.md). Este registro cobre três evidências; não declara concluídas as sete evidências dos tickets 01–04. [validation.md](validation.md), [visual-narrative-review.md](visual-narrative-review.md), spec e copy draft anteriores permanecem intactos.

## Recuperação e ambiente

- Worktree isolada: `C:/Users/fplev/.t3/worktrees/Portfolio/t3-99f79a41`, branch `t3/harmony-shared-foundations-1`.
- Antes da recuperação, HEAD e `integration/harmony-visual-narrative` eram ambos `f8f9034fb32de4b7839ac0a003db2bb791af883e`, com checkout limpo. O checkpoint `268faa61d17c88049d77fddd0d8446de00830ede` foi recuperado por cherry-pick como `9aaf8b6`. Implementação, derivados e evidências existentes foram reaproveitados.
- Windows, Python 3.14, Playwright Python já instalado, Chromium headless `156.0.8078.4`. Nenhum pacote foi adicionado ao projeto.
- Servidor desta execução: `python -m http.server 8013 --bind 127.0.0.1 --directory C:/Users/fplev/.t3/worktrees/Portfolio/t3-99f79a41`. Porta diferente da execução anterior para garantir o checkout correto.
- Reutilizado o fluxo Playwright existente, autorizado pelo Testing Decisions da spec e pelo pedido de retomada. Seam: comportamento externo do Harmony renderizado. Verificações de integridade são complementares, não uma nova interface de teste do produto.

## Evidência herdada de red/green

Inspecionada antes de completar a execução; não foi recriada nem sobrescrita:

- `qa/red-primitives`, `qa/red-semantics`, `qa/red-responsive`: cada resultado registra a ausência da respectiva região nomeada (0 passou, 1 falhou). Os pares `qa/green-primitives`, `qa/green-semantics`, `qa/green-responsive` registram título/região, imagem carregada com alternativa e explicação anterior à imagem (3 passaram por fatia).
- `qa/red-mobile-width/results.json`: 134 passaram e 18 expectativas de largura falharam nas três evidências em 320/375/768, nos dois modos. A versão final verifica largura útil limitada ao tamanho natural do raster, sem exigir seu alargamento. Derivados focais atendem mobile/tablet; as seleções completas aparecem acima de 1024 px.
- `qa/navigation-focus/results.json`: 40 passaram e quatro verificações de foco falharam. `qa/green-navigation-focus/results.json`: 44 passaram após o outline local dos campos de contato, sem alterar o CSS compartilhado.
- `qa/reading-captures`: 12 verificações passaram, com viewports sobrepostos para percorrer imagens altas após `decode()`.
- `qa/verified-matrix/results.json` não tem resumo final: é uma execução interrompida, não uma matriz aprovada. `qa/green-foundations` contém capturas, mas não um resultado estruturado completo. Ambos permanecem preservados como histórico, sem substituir a nova execução abaixo.

## Execução completa nesta worktree

Comando: `python .scratch/harmony/visual-narrative-qa.py --slice all --label completed-foundations --url http://localhost:8013/case-studies/harmony.html`.

Resultado: **216 verificações passaram, 0 falharam**, processo terminou com exit code 0. [Resultado estruturado](qa/completed-foundations/results.json). Nenhuma exceção de página, requisição falha ou resposta HTTP de erro registrada pelos listeners dos contextos da matriz.

- **320 × 700, 375 × 700, 768 × 700 e 1440 × 700**, cada uma com `no-preference` e `reduce`: oito combinações concluídas. Em todas, três evidências na ordem escalas → papéis → variáveis; uma imagem carregada por linha, proporção preservada, sem overflow horizontal; explicação anterior à imagem no DOM e no render, figura associada à explicação, alternativas presentes, sem links de imagem/disclosures. Prosa manteve pelo menos 16 px.
- A rolagem de cada combinação começou em `scrollY=0`, usou `mouse.wheel(0, 300)` e observou o conteúdo a cada chegada, com 600 ms entre passos. Chegou ao fundo em 34/33/28/26 passos, respectivamente; `scrollY` final 10088/9612/8181/7519 nos dois modos. Nenhum ancestral oculto foi encontrado para o conteúdo observado. Capturas `wheel-<largura>-<movimento>-<id>.png` foram feitas durante a travessia, antes dos saltos para capturas de elementos.
- **Sem JavaScript**, quatro larguras: as três imagens carregaram, a narrativa estática permaneceu visível e não houve overflow horizontal. `no-js-<largura>.png` registra variáveis com explicação e imagem; não é prova isolada do restante da página, conferido também pelo resultado estruturado.
- **Teclado**, quatro larguras: sequência real de Tab por navegação, voltar, próximo projeto, links/controle de contato, campos e envio; outlines computados presentes e elementos dentro da largura da viewport. Capturas de Work, próximo projeto e botão de envio. Enter ativou home/logo, voltar, Work, About, Contact e Billing, com destinos/âncoras corretos. Formulário permaneceu presente e não foi enviado; os campos não foram preenchidos.
- Hierarquia com um h1 e sem salto de nível; títulos, regiões nomeadas, alternativas e associação da figura conferidos no DOM renderizado. Isto não é um teste com leitor de tela.
- Cor computada da prosa orientativa e legendas dos fundamentos: `rgba(242, 242, 245, 0.65)`, tratamento `--text-secondary-strong`. Cálculo de luminância, incluindo composição alpha sobre os fundos computados, resultou em aproximadamente **7,55:1** nas quatro larguras. É cálculo das cores DOM desses textos; não mede contraste dos pixels das fontes nem certifica acessibilidade do sistema Harmony.

## Inspeção visual e recortes

Foram inspecionadas capturas de leitura das três evidências em 320, 375, 768 e 1440, incluindo partes sucessivas das variáveis; fontes em `qa/source-inspection`; capturas atuais de chegada em movimento normal nos quatro tamanhos; explicações atuais em 375; no-JS nas quatro larguras; e foco em navegação, próximo projeto e contato. As 132 capturas da execução completa estão em `qa/completed-foundations`; não se afirma inspeção individual de todos os arquivos.

- Em 320/375, as seleções mantêm Primary/Secondary e valores 50/100; Surface/Border e Default/Soft; e os três cabeçalhos Desktop/Tablet/Mobile com ScreenSize 1440/768/390 e Gap. O terceiro modo é alcançável pela rolagem, sem cortar a imagem por container. O valor 390 pertence à evidência, não à largura do teste.
- Em 768, os recortes ficam centralizados em tamanho natural, com espaço lateral intencional. A imagem alta de variáveis é lida em segmentos; não precisa caber em um viewport. Em 1440, as duas escalas completas selecionadas, as duas linhas semânticas e a tabela original de variáveis usam blocos largos e mantêm contexto.
- Títulos, explicações e legendas se ajustaram à largura sem reduzir a tipografia; nenhum corte significativo ou sobreposição entre blocos da narrativa foi observado. Capturas de detalhes podem começar no meio de uma imagem ou mostrar texto passando sob a navegação fixa durante uma mudança de posição; não são recortes destrutivos do conteúdo. Os alvos de foco inspecionados permanecem visíveis.
- Os rasters originais têm texto suavizado, mais perceptível nos nomes de papéis semânticos. Os nomes relevantes são identificáveis nas seleções; explicação, legenda e alternativa também comunicam o argumento. Não se promete nitidez vetorial, leitura de cada rótulo secundário ou auditoria do sistema capturado. Não houve redesenho de texto, sharpening ou aumento de pixels.
- [Manifesto editorial](image-manifest.md) e [retângulos/valores exatos](image-manifest.json) documentam as cinco imagens derivadas. As montagens mobile repetem fragmentos identificados e usam gutters; as legendas informam que são seleções da fonte, sem fingir que a montagem é o layout original do aplicativo.

## Preservação e limites

`python .scratch/harmony/verify-foundation-artifacts.py`: **33 verificações passaram, 0 falharam**. [Resultado](qa/completed-artifact-integrity.json). Comparação com o baseline confirmou bytes de todos os 15 assets originais Harmony, documentos históricos, HTML da navegação/header/hero, problema/papel, resultado, iniciativas em desenvolvimento, próximo projeto, contato, footer e todos os scripts. Argumentos de React/Next, manutenção, contratação e acessibilidade/conteúdo permanecem literais para integração nos próximos tickets. Manifesto, dimensões, bytes e cada fragmento dos derivados correspondem às fontes.

As três evidências explicam relações entre camadas; não afirmam cronologia, paleta completa, contagem de tokens, resolução de aliases, conformidade AA ou temas claro/escuro. Biblioteca compartilhada, governança e exceções estão junto dos fundamentos, sem alegar um arquivo físico único. O par antes/depois saiu do HTML e seus originais foram preservados. Hero, adoção em novos projetos, migração gradual, atribuição de papéis e iniciativas em desenvolvimento mantêm o texto/configuração anterior.

Estilos novos estão limitados a `.harmony-case` em `assets/css/harmony.css`; nenhum script/CSS compartilhado, analytics, home ou outro case foi alterado. A narrativa alta não entra no mecanismo compartilhado de animação de seções, preservando o conteúdo nos dois modos e sem JS. `git diff --check` passou.

Esta execução usa Chromium desktop com viewport emulado; não cobre Safari/Firefox, aparelhos físicos, leitor de tela, zoom ampliado, execução funcional do design system, Storybook/serviços de produção, entrega de formulário ou medições empresariais. Configuração e bytes do hero e analytics foram preservados; não houve avaliação editorial de reprodução completa do MP4 nem comprovação remota de continuidade GA4/Clarity. Não houve PR ou publicação. Tickets 02–04 e a validação final das sete evidências continuam fora desta entrega.
