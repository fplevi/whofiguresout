# 06 — Validar resultado em produção e fechar o relatório de aceite

Status: ready-for-agent
Type: task
Blocked by: 01, 02, 03, 04, 05
Executor: Claude

## Contexto

O resultado final precisa refletir a experiência publicada, com analytics reais preservados. Leia os [critérios do spec](../spec.md), resultados dos tickets e a confirmação de revisão/analytics do ticket 05.

## Trabalho

- Verificar que o conteúdo servido corresponde à revisão candidata, incluindo assets. Registrar versão do navegador/Lighthouse, ambiente, política de cookies, estado de consentimento e demais condições do baseline.
- Executar cinco páginas × desktop/mobile × três coletas em produção HTTPS, usando as mesmas configurações do baseline. Guardar JSON em `../evidence/final/<pagina>/<perfil>/run-N.json` e resumo em `../evidence/acceptance.md`.
- Comparar mediana e variação de categorias, FCP, LCP, TBT, CLS e Speed Index. Distinguir redução de avisos sem peso de mudança efetiva de nota ou experiência.
- Validar navegação e links, hero, animações, parallax/sliders quando presentes, foco, reduced motion e revisão visual. Testar sucesso/falha do formulário com respostas de rede simuladas, sem enviar mensagens reais.
- Confirmar que há apenas uma inicialização de cada ferramenta por documento, IDs preservados e ausência de erros novos no console. Cruzar evidências de rede com a confirmação funcional do ticket 05.
- Documentar cada falha residual: auditoria, URL, responsável, evidência, motivo de não corrigir e impacto. Se uma falha própria ou regressão impedir o aceite, devolver ao ticket responsável; não mudar silenciosamente os critérios.

## Aceite

- 30 relatórios finais completos e comparáveis; meta 100 nas quatro categorias, aplicando somente as exceções explícitas do spec.
- Falhas próprias de contraste removidas; Acessibilidade/SEO 100 nos cenários aplicáveis; nenhuma regressão reproduzível introduzida.
- Qualquer Boas práticas abaixo de 100 é explicado por evidência residual de fornecedor e pelo trade-off aprovado de preservar analytics, sem exceções que escondam falhas próprias.
- Clarity e GA4 preservados funcionalmente, com a confirmação do ticket 05. Sem essa confirmação, registrar o aceite de analytics como pendente.
- Resultado final distingue concluído, pendente humano/fornecedor e nova decisão necessária. Nenhuma alegação de 100% garantido em todos os navegadores, regiões ou estados de consentimento.

## Comments

- 2026-10-24: ticket para a etapa futura, após candidato correto em HTTPS e validação humana das funções de analytics.
- 2026-10-24: spec confirmado em Q6; executar após satisfazer as dependências.
- 2026-10-24 (Claude): **não executado** — bloqueado pelo ticket 05 (candidato não publicado; produção ainda é `d2d74df`, sem Convênios). Preparado: `tools/run-matrix.mjs production https://www.felipelevi.site ../evidence/final 3`, `tools/summarize.mjs`, `tools/functional-check.mjs`, `tools/contrast-audit.mjs` e `tools/redact.mjs` reproduzem as mesmas condições do baseline. Antes de rodar, conferir que o manifesto publicado corresponde a [candidate/manifest.sha1](../evidence/candidate/manifest.sha1) (ou ao commit registrado no 05).
