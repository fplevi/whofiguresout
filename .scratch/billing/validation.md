# Validação do Billing & Debt Recovery

Data: 2026-10-24.

## Implementação

- Contexto lateral substituído por uma lista semântica de três itens abaixo da introdução, usando `cs-problem__points`.
- Decisões na coluna de leitura de até 840 px, com `cs-decisions--stacked`.
- Três mensagens em `cs-decision__note`, imediatamente após seus parágrafos, com ícones decorativos de 24 px. Sem pílulas, fundo ou mensagem isolada à direita.
- Reutilizado `components.svg`. Adicionados os SVGs oficiais `shield-lock.svg` e `clock.svg` em `assets/icons/tabler/billing/`, com origem fixada por commit e registro local. Licença compartilhada preservada.
- CSS complementar `assets/css/billing.css`, importado somente pelo Billing, contém apenas duas máscaras de ícones. Nenhuma dependência de execução adicionada.
- Textos distinguem a meta de cinco minutos do acompanhamento histórico no Clarity, confirmado pelo usuário. Os números existentes foram preservados e contextualizados como retrato histórico. Pendências documentais em `factual-questions.md`.

## Direção visual e preservação

Aplicada a skill `design-taste-frontend` como evolução pontual do portfólio editorial existente. Mantidos paleta escura, destaque pêssego, Fraunces/Inter, imagens reais, espaçamentos, cantos e movimento. Leitura de configuração: `DESIGN_VARIANCE: 6`, `MOTION_INTENSITY: 3`, `VISUAL_DENSITY: 4`, preservando a composição existente. Não se aplicam as trocas de tipografia, tema, arquitetura ou animação de um redesenho integral.

Comparação com o HTML existente no início da execução (`before.html`) confirmou preservação literal da navegação, contato, imagens, bloco de métricas e seus rótulos, próximo projeto, scripts e IDs de âncoras. O novo parágrafo de resultado apenas situa os dados historicamente.

## Navegador

- Servidor local existente em `http://localhost:8000`, reutilizado.
- Aba própria do T3: `tab_8_ff47e609-afe1-4b1f-8504-1a7b8917e60f`.
- Duas tentativas de captura T3 falharam com `Preview automation snapshot timed out after 15000ms.` O fallback autorizado usou Playwright Python já instalado em `%TEMP%/portfolio-convenios-qa` e Chromium `156.0.8078.4`, sem instalar pacotes no projeto.
- Larguras verificadas: **320, 375, 768 e 1440 px**. `scrollWidth` igual à largura de viewport nas quatro; nenhum elemento ultrapassou os limites laterais.
- Lista com três marcadores visíveis, abaixo da introdução. Nenhum `cs-stakes`, `cs-problem__layout` ou `cs-decision__tradeoff` remanescente.
- Três notas abaixo dos respectivos parágrafos, cada decisão em uma coluna, ícones de 24 × 24 px com máscara válida e `aria-hidden="true"`. O significado permanece no texto acessível.
- Doze respostas HTTP 200 dos ícones, três em cada largura; todas as imagens carregadas. Nenhuma resposta local HTTP de erro ou exceção JavaScript observada.
- Com movimento normal, todas as seções apareceram ao rolar em 375 e 1440 px. Com redução de movimento, permaneceram visíveis.
- Botão de copiar e-mail conferido em 375 e 1440 px: feedback `Copied!` e conteúdo esperado na área de transferência. Nenhum formulário foi enviado.
- `git diff --check -- case-studies/billing.html` passou.

Evidência estruturada em `qa-results.json`; rotina reproduzível em `verify.py`. Capturas inspecionadas de cabeçalho, contexto, decisões, entrega e resultado em desktop/mobile. As capturas recortadas das seções ocultam apenas a navegação fixa durante a captura, evitando sua sobreposição artificial em screenshots de elementos mais altos que o viewport; as capturas `header-*.png` mantêm a navegação real.

## Limites de escrita

Esta execução escreveu somente `case-studies/billing.html`, `assets/css/billing.css`, `assets/icons/tabler/billing/` e `.scratch/billing/`.

Hashes dos estilos compartilhados, contato, scripts de contato, home, Harmony, Convênios e plano permaneceram iguais ao início desta execução. O hash de Enrollment mudou durante o trabalho simultâneo do outro chat; esse arquivo não foi escrito nem revertido por esta execução. Não houve commit, staging ou deploy.

O hook de cinco minutos ainda pode aparecer no card da home e no plano, que ficaram fora dos limites de escrita. A proposta de alinhamento foi registrada em `factual-questions.md` para integração posterior.
