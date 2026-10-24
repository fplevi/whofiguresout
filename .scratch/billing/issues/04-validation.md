# 04 — Validar interação, legibilidade e regressões

Status: resolved
Type: task
Dependências: 01, 02 e 03 concluídos
Spec: [../spec.md](../spec.md)

## Entrega

Validar o aceite global do spec e corrigir problemas encontrados. Salvar evidências e um relatório específico em `.scratch/billing/visual-narrative-validation.md`, preservando relatórios anteriores.

## Verificações

- Conferir a página em 320, 375, 768 e 1440 px: ordem de leitura, largura disponível, overflow, sobreposição, proporção e carregamento das imagens.
- Inspecionar visualmente todas as novas telas em desktop e mobile, incluindo detalhes essenciais preservados nos recortes. Conferir os acessos a versões maiores quando necessários.
- Exercitar todas as etapas do fluxo por clique e teclado; confirmar abertura/fechamento independente, foco visível e comportamento sem JavaScript.
- Conferir movimento reduzido e rolagem com movimento normal. As seções devem aparecer por inteiro, inclusive após expandir etapas, considerando a animação existente por `IntersectionObserver`.
- Conferir precisão da copy, separação dos cenários de pagamento, ausência de alegações novas e remoção das legendas incorretas.
- Verificar navegação, próximo projeto e contato sem enviar o formulário. Conferir que métricas e seus rótulos foram preservados.
- Checar erros locais de console/rede e executar `git diff --check` nos arquivos alterados. Rever o diff para preservar trabalho anterior e mudanças externas.

## Ferramentas e evidências

Seguir o workflow de navegador disponível no ambiente do Claude Code. Há um verificador anterior em `../verify.py`, mas suas asserções preservam a estrutura e o conjunto antigos de imagens: não o executar como critério final sem adaptá-lo ao novo escopo. Preferir uma rotina nova para esta revisão, caso automatizar seja útil. Reaproveitar dependências de QA disponíveis sem adicionar dependências de runtime ao site.

Na investigação anterior, `http://localhost:8000` estava ativo. Verificar sua disponibilidade antes de reutilizar. Duas capturas do preview T3 falharam com `Preview automation snapshot timed out after 15000ms.` O fallback então usou Playwright Python disponível em `%TEMP%/portfolio-convenios-qa`; isso é contexto histórico, não garantia de disponibilidade atual.

## Aceite

- Todos os critérios globais do spec passam; falhas encontradas foram corrigidas e revalidadas.
- Há capturas representativas de desktop/mobile para fluxo, acesso, pagamentos, revisão, acompanhamento e dashboard.
- O relatório registra larguras, interações testadas, resultado das verificações, arquivos alterados e limites reais da validação.
- Manifesto de imagens e comentários dos tickets refletem a entrega final.
- Entrega final informa o que mudou e onde abrir o case localmente, sem declarar deploy ou commit que não ocorreu.

## Comments

- 2026-10-24: ticket preparado para validação da futura implementação pelo Claude Code. Nenhuma implementação foi executada na sessão de especificação.
- 2026-10-24 (Claude Code): rotina nova [visual-narrative-qa.py](../visual-narrative-qa.py), 74/74 verificações aprovadas em 320/375/768/1440, sem erros de console/rede. Correções durante a validação: largura das telas laterais e cor explícita do foco do `summary`. Relatório em [visual-narrative-validation.md](../visual-narrative-validation.md), evidências `narrative-*.png`. Limites: só Chromium headless, sem leitor de tela real. Sem commit/deploy.
- Concluído em: 2026-10-24
- 2026-10-24 (revisão do usuário): rotina adaptada ao fluxo estático e à remoção dos links; 71/71 aprovadas, sem erros de console/rede; evidências recapturadas.
