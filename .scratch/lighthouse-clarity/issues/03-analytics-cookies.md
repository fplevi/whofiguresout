# 03 — Investigar cookies do Clarity sem degradar Clarity ou GA4

Status: ready-for-agent
Type: research
Blocked by: 01
Executor: Claude

## Contexto

`third-party-cookies` e `inspector-issues` explicam os 23 pontos perdidos em Boas práticas. O usuário priorizou continuidade entre páginas e visitas recorrentes no Clarity e preservação do GA4. Leia [spec](../spec.md), [evidências](../evidence.md) e [ADR-0001](../../../docs/adr/0001-preservar-analytics-na-otimizacao-lighthouse.md).

Os bootstraps estão no head de `index.html` e dos quatro cases. IDs existentes: Clarity `wo2llblzgf`; GA4 `G-C0GC2E2VMN`. Não há API de consentimento, CMP, eventos ou custom IDs próprios no código inspecionado. Configurações dos painéis são desconhecidas.

## Trabalho

- Reproduzir cookies/Issues no navegador limpo em produção; registrar origem, momento, domínio, política do navegador, estado de consentimento e motivo exato do aviso. Diferenciar cookie da resposta inicial do bootstrap, biblioteca e coleta.
- Consultar a documentação oficial atual de cookies, Consent Mode e consentv2. Explicitar que o painel também controla o comportamento e que JavaScript não cancela retroativamente um Set-Cookie já recebido.
- Avaliar hipóteses suportadas que possam remover a causa sem fragmentar sessões. Se investigar analytics permitido/publicidade negada, usar escolha explícita do próprio testador e configuração isolada apropriada; não assumir que essa combinação elimina cookies de terceiros.
- Separar o que pode ser demonstrado no navegador do que exige painel. Registrar exatamente as verificações externas necessárias no ticket 05, sem pedir credenciais em arquivos ou chat.
- Não mudar consentimento, publicidade, mascaramento ou configurações de produção como parte desta investigação. Se uma solução precisar disso, apresentar proposta concreta com benefícios, perda de dados, dependências e rollback para decisão própria.
- Salvar `../evidence/analytics.md` com alternativas, resultados, referências oficiais e conclusão: mitigação viável a especificar, ou limitação residual comprovada. Se exigir decisão nova, indicar `needs-info` neste ticket e registrar a pergunta em Comments; não declarar a investigação aprovada como implementação.

## Aceite

- Causa completa das duas auditorias e condições de reprodução documentadas; a lista de URLs do anexo não é tomada como diagnóstico suficiente.
- Nenhuma remoção, troca de ID, consentimento fabricado, fragmentação de sessões ou adiamento para escapar da medição.
- Uma alternativa só é recomendada como preservando analytics com evidência das funções, não apenas script carregado ou coleta HTTP 200. A confirmação de painéis pode permanecer dependente do ticket 05.
- Se não houver mitigação que cumpra as restrições, registrar a limitação e suas evidências é um resultado válido. Não prometer 100 e não implementar um modo sem cookies para atingir a nota.

## Verificação

Comparar estados reais documentados no mesmo navegador/revisão. Identificar eventual ensaio sem terceiros como atribuição diagnóstica, sem usá-lo para aceite. Preservar as preferências de quem recusa/bloqueia e não exportar valores de cookies ou dados de gravações.

## Comments

- 2026-10-24: preservar as duas ferramentas e a continuidade do Clarity foi confirmado em Q3–Q4. Nenhuma nova política de consentimento foi aprovada.
- 2026-10-24: spec confirmado em Q6; executar após concluir 01.
- 2026-10-24 (Claude): investigação concluída — **limitação residual comprovada do fornecedor**. Em produção, sem CMP, Clarity reporta consentimento concedido por padrão; `CLID` vem no Set-Cookie da resposta do bootstrap `www.clarity.ms/tag/wo2llblzgf` (antes de qualquer JS), MUID/MR/SM/ANONCHK/SRM_B vêm dos pixels `c.gif` de `c.clarity.ms`/`c.bing.com`; motivo de todos os avisos: `WarnThirdPartyPhaseout`. Hipótese `analytics_Storage: granted` + `ad_Storage: denied` (enfileirada antes do bootstrap, só na sessão de teste, com `/collect` abortado): não removeu nenhum cookie de terceiro e o `_clsk` não foi criado. A única via documentada sem cookies de terceiros fragmenta sessões (ADR-0001). Nada foi alterado em consentimento/painel/produção. Não há decisão nova necessária para seguir; adotar banner/CMP seria decisão própria e não garante 100. Evidência: [analytics.md](../evidence/analytics.md). Verificações de painel listadas para o ticket 05.
