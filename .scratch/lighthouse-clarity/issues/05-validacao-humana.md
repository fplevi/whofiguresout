# 05 — Disponibilizar candidato HTTPS e confirmar analytics nos painéis

Status: ready-for-human
Type: task
Blocked by: 02, 03, 04
Executor: responsável pelo site e pelas contas

## Contexto

A validação final precisa da revisão candidata publicada e do acesso aos painéis do Clarity/GA4. O usuário autorizou planejar a validação em produção; a preparação destes tickets não autoriza publicação nem mudanças de configurações externas. Leia o [spec](../spec.md).

## Trabalho

- Conferir a revisão candidata e decidir sua publicação pelo fluxo habitual. Registrar a revisão, URL e data efetivamente disponibilizadas em HTTPS; garantir que fontes/arquivos em cache correspondam ao candidato.
- Se produção ainda não estiver pronta, informar a dependência. Não comparar checkout novo contra publicação antiga como se fossem a mesma revisão.
- Verificar as configurações atuais do Clarity e GA4 pedidas pelo ticket 03, incluindo estado de consentimento relevante, apenas para leitura. Registrar conclusão sem credenciais, valores de cookies, identificadores pessoais ou conteúdo de gravações.
- Em uma visita própria de teste, nas condições autorizadas disponíveis, navegar home → case → outro case → home. Confirmar recebimento no projeto `wo2llblzgf`, continuidade entre páginas e reconhecimento de uma visita recorrente em comparação ao comportamento inicial.
- Confirmar coleta no GA4 `G-C0GC2E2VMN`, incluindo pageviews das páginas visitadas e ausência de duplicação nova. Aguardar o processamento normal da ferramenta quando necessário; não usar o atraso do painel como prova de quebra.
- Se houver proposta de mudança de consentimento/configuração, decidir separadamente com base no resultado do ticket 03. Este ticket não exige adotá-la para concluir a entrega com uma limitação residual justificada.

## Aceite

- URL HTTPS e revisão candidata identificadas para o ticket 06.
- Confirmação funcional dos painéis registrada em `../evidence/analytics.md` ou em Comments, com data e condições, sem expor dados pessoais.
- Nenhuma alteração de conta ou publicação atribuída ao agente por inferência; decisões e resultados reais estão claros.
- Se as funções já não estiverem disponíveis no baseline, registrar a divergência e reabrir a decisão, sem alegar preservação comprovada.

## Comments

- 2026-10-24: etapa humana por depender do fluxo de publicação e do acesso às contas. Ainda não executada.
- 2026-10-24: spec confirmado em Q6; dependências de implementação continuam pendentes.
- 2026-10-24 (Claude): candidato pronto **localmente, não commitado e não publicado** (nenhuma publicação feita pelo agente). Para executar este ticket falta: (a) revisar e commitar as alterações listadas em [candidate.md](../evidence/candidate.md) — estão misturadas com alterações não commitadas do próprio usuário nos mesmos arquivos (`case-study.css`, `hero.css`, HTMLs), então o commit precisa incluir os novos arquivos `assets/fonts/`, `assets/css/fonts.css`, `*.mp4`, `*-poster.webp`; (b) publicar pelo fluxo habitual (push para `master` → GitHub Pages) e registrar commit/URL/data; (c) verificações de painel somente leitura listadas em [analytics.md](../evidence/analytics.md#verificações-que-dependem-do-painel-ticket-05): configuração de cookies/Consent Mode do Clarity, sessão única com 4 páginas no percurso home → case → outro case → home, visita recorrente, pageviews no GA4 sem duplicação. Observação: o `max-age=600` do Pages pode servir arquivos antigos por até 10 min após o deploy.
