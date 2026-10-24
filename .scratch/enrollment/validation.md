# Validação de Enrollment Journey

Data: 2026-10-24.

## Resultado

Implementação concluída no checkout principal, limitada a `case-studies/enrollment.html`, `assets/css/enrollment.css`, `assets/icons/tabler/enrollment/` e `.scratch/enrollment/`.

Contexto em três bullets abaixo da introdução. Decisões em uma coluna com três mensagens e ícones abaixo dos parágrafos. Nenhum card lateral de contexto ou pílula de trade-off permanece neste case. Reutilizados os quatro componentes compartilhados indicados no handoff, sem editar o CSS compartilhado.

Os 171% referem-se ao crescimento de propostas, conforme confirmação do usuário. Não equivalem a adesões concluídas nem a uma taxa de conversão. Reduzir dependência do atendimento aparece como objetivo, sem alegação de redução medida. Fonte e definição específica do evento permanecem em `issues/01-metric-definition.md`.

## Verificação de navegador

- Site servido pelo servidor já existente em `http://localhost:8000`; não foi iniciado outro servidor.
- Preview T3 consultado e aba própria aberta: `tab_9_ff47e609-afe1-4b1f-8504-1a7b8917e60f`. A leitura por evaluate confirmou a estrutura; capturas falharam duas vezes com `Preview automation snapshot timed out after 15000ms.`
- Aplicado o fallback documentado: Playwright/Chromium disponível em `%TEMP%/portfolio-convenios-qa`, sem instalar dependências no projeto.
- `python .scratch/enrollment/qa.py` passou em **320, 375, 768 e 1440 px**: largura do documento igual à viewport, zero imagens quebradas, zero erros JavaScript, três bullets, três notas abaixo dos respectivos parágrafos e zero elementos do contexto/pílulas anteriores.
- Os três SVGs receberam HTTP 200 em todas as quatro larguras; máscaras CSS resolvidas, ícones decorativos com `aria-hidden="true"` e mensagens textuais acessíveis.
- Comparador verificado por **Home, End, ArrowRight e ArrowLeft**, com valores e posição de recorte/handle correspondentes. Clique por ponteiro também alterou o valor em todas as larguras.
- `python .scratch/enrollment/final_checks.py` passou: comparador por teclado com movimento reduzido em **375, 1025, 1280 e 1440 px**; números contidos nos cards também nos pontos intermediários de desktop.
- Comparador, navegação principal e navegação de próximo projeto comparados ao HTML em HEAD e idênticos. Destino `convenios.html` preservado. O trabalho anterior de contato presente na árvore suja foi mantido pelo patch.
- `git diff --check -- case-studies/enrollment.html` passou.

## Inspeção visual

Capturas de cabeçalho, contexto, decisões, comparador e resultados em 375 e 1440 px foram inspecionadas. Bullets têm marcadores visíveis; ícones e notas estão alinhados abaixo dos parágrafos; textos e números não ficam cortados; o comparador conserva as duas imagens e os rótulos.

Evidências em `qa/`: `after-header-*.png`, `after-problem-*.png`, `after-decisions-*.png`, `after-shipped-*.png`, `after-outcome-*.png`, `validation.json` e `final-checks.json`. As capturas isoladas de seções ocultam a navegação fixa somente na opção `style` do screenshot para evitar sua repetição na imagem longa; a página e o código de produção não são alterados por isso. As capturas de cabeçalho mostram a navegação normalmente.

Uma primeira execução do QA encontrou um erro de posicionamento no clique automatizado: o ponto usado ficava sob a navegação ou fora da área visível no comparador alto de desktop. O script foi corrigido para clicar dentro da parte visível. A execução final passou sem mudança no comparador do produto.

## Limites e continuidade

- Leitura editorial concluída para todas as strings visíveis; textos novos mantêm inglês e vocabulário de propostas. Identidade, tipografia, imagens, links e contato preservados por instrução explícita, com aplicação pontual da skill `design-taste-frontend`.
- Esta revisão não mede resultados empresariais, não refaz a auditoria geral de desempenho/acessibilidade do portfólio e não altera os comportamentos compartilhados existentes.
- Nenhuma escrita em Billing, Harmony, Convênios, home, plano, CSS/JS compartilhado ou arquivos de contato foi realizada por este trabalho. Alterações desses arquivos já existentes ou feitas pelo outro chat não foram revertidas nem incluídas no escopo.
- Proposta de integração da redação da home/plano está em `copy-decisions.md`; esses arquivos permanecem sem edição neste chat.
- Sem commit, staging ou deploy.
