# 01 — Estabelecer baseline reproduzível nas cinco páginas

Status: ready-for-agent
Type: task
Blocked by: nenhum
Executor: Claude

## Contexto

O anexo cobre somente home desktop em localhost e contém atividade de extensão. Leia o [spec](../spec.md) e as [evidências](../evidence.md). Não usar essa única coleta como baseline de mobile, cases ou produção.

## Trabalho

- Inventariar o checkout e registrar a revisão de partida, as alterações preexistentes e a diferença entre checkout e versão publicada, sem desfazer trabalho do usuário.
- Definir execução reproduzível com Lighthouse 13.5.0 e Chrome compatível; registrar versão efetiva, presets desktop/mobile, viewport, throttling, política de cookies, extensões e estado de consentimento. Se não for possível usar a versão do anexo, registrar a substituição e gerar todo o baseline na versão escolhida.
- Auditar cinco URLs × dois perfis × três execuções em produção HTTPS, com contextos limpos independentes e estado inicial comparável. Produção é baseline do publicado; quando o candidato for local, medir também o checkout de partida local para uma comparação válida.
- Salvar JSON em `../evidence/baseline/<ambiente>/<pagina>/<perfil>/run-N.json` e um índice `../evidence/baseline.md`, com revisão/URL, scores, métricas, mediana, variação e auditorias reprovadas.
- Registrar carregamentos e endpoints de Clarity/GA4, cookies por nome/domínio e Issues panel com motivo completo, sem valores de cookies nem dados pessoais. Capturar screenshots de referência para a revisão visual.
- Usar ferramentas de desenvolvimento sem transformar o site em uma aplicação com build. Guardar comandos e versões usados; não depender de instalação global não documentada.

## Aceite

- As 30 coletas de produção estão identificadas e resumidas; nenhuma medição com terceiros removidos conta como baseline de aceite.
- Um agente consegue repetir os comandos e obter relatórios com as mesmas condições.
- Atribuições próprias/terceiros/ambiente usam evidências, sem extrapolar a home para os cases.
- A falta de acesso aos painéis é registrada para o ticket 05 e não apresentada como falha ou sucesso de analytics.

## Verificação

Validar formato dos JSONs, presença de todas as células da matriz e consistência da configuração. Não enviar o formulário e não alterar configurações externas.

## Comments

- 2026-10-24: ticket especificado para execução futura, condicionado à confirmação final do spec.
- 2026-10-24: spec confirmado em Q6. Ticket pronto para a etapa futura com Claude.
- 2026-10-24 (Claude): baseline concluído. Lighthouse 13.5.0 fixado em `tools/package.json`, Chrome 156.0.8078.47, Windows 11, headless novo, perfil temporário por execução, sem extensões; comandos em `tools/run-matrix.mjs`. Produção = `d2d74df` (build de Pages 2026-05-08): **24 coletas**, não 30, porque `case-studies/convenios.html` não está publicado (404). Local de partida = HEAD `7c87df3` + alterações do usuário (snapshot fora do repo): 30 coletas. Índice e atribuições em [baseline.md](../evidence/baseline.md). Falhas com peso: contraste (próprio), `errors-in-console` por `/favicon.ico` 404 (próprio), LCP de 19–186 s por GIFs de 23–36 MB (próprio), cookies de terceiros do Clarity (fornecedor). Identificadores de cookies em URLs foram redigidos dos JSON. Painéis não acessíveis pelo agente → ticket 05.
