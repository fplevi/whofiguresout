# Evidências e fontes

Data da análise: 2026-10-24. Este documento descreve uma análise, não uma nova execução de Lighthouse.

## Relatório fornecido

Nome original: `pasted-text.txt`, anexo desta conversa. O [resumo estruturado](evidence/report-summary.json) contém os scores, configuração e auditorias selecionadas extraídos do JSON, sem valores de cookies ou dumps de rede. O hash do arquivo original permite identificá-lo se for necessário consultar o anexo completo.

- Acessibilidade: `color-contrast`, cinco elementos, relação 4,16:1 para mínimo 4,5:1; peso 7/188.
- Boas práticas: cookies de terceiros MR, SM, MUID e CLID associados ao Clarity; Issues panel contém tipo Cookie e URLs do Clarity. Pesos 5/26 e 1/26. O motivo detalhado dos avisos não está no JSON.
- JavaScript não utilizado: `gtag.js`, aproximadamente 71 KiB, economia FCP/LCP estimada em zero.
- Reflow: próprio `scroll-animations.js`, 11,633 ms; não atribuído, 23,678 ms; atribuição ao Clarity, 0,032 ms. Não atribuir o tempo sem origem ao fornecedor.
- Fontes: cadeia via `@import` em CSS próprio, com conclusão mais longa registrada em aproximadamente 620 ms.
- O servidor local devolve HTTP/1.0 e TTL zero para assets; compressão/cache locais não comprovam a configuração publicada.
- Há atividade de extensão nos diagnósticos; medir novamente com navegador limpo.

## Código verificado

- `index.html:18–34` e início das quatro páginas em `case-studies/`: GA4 e Clarity assíncronos, imediatamente no head, mesmos IDs.
- Não foram encontradas chamadas próprias de eventos, custom IDs, consentimento, CMP ou callbacks de analytics. Isso não comprova a configuração dos painéis externos.
- `assets/css/tokens.css:9`: `--text-secondary` com opacidade 0,45. Consumidores comprovados: `assets/css/nav.css:40` e `assets/css/hero.css:35`.
- `assets/css/global.css:1`: Google Fonts via `@import`.
- `assets/js/scroll-animations.js:87`: leitura de geometria no parallax.
- `assets/js/contact-form.js:84`: submit ao Formspree; testar com simulação.
- README declara HTML/CSS/JS sem framework/build. Não há runner de testes, package.json ou CI de aplicação no estado inspecionado.
- `CNAME`: `www.felipelevi.site`.

As linhas são referências do estado inspecionado e podem mudar durante a execução.

## Produção observada

HEAD em `https://felipelevi.site/` e `https://www.felipelevi.site/` terminou na URL com www, HTTP 200, `Server: GitHub.com`, `Cache-Control: max-age=600`. Esta observação não é um audit de produção. Não testa cookies de navegador, compressão negociada, assets, pontuação ou equivalência entre o código publicado e o checkout.

## Fontes oficiais consultadas

- [Lighthouse: cálculo de Performance](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring): métricas determinam a pontuação; diagnósticos e oportunidades não a alteram diretamente. As condições de execução causam variação.
- [Microsoft: cookies do Clarity](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-cookies): distingue cookies próprios de terceiros e documenta suas funções.
- [Microsoft: Consent Mode](https://learn.microsoft.com/en-us/clarity/setup-and-installation/cookie-consent): configuração no painel é parte da solução; impede cookies até consentimento válido quando corretamente configurada.
- [Microsoft: consentv2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2): API recomendada; configuração sem consentimento usa ID por pageview. Conceder consentimento pode permitir cookies próprios e de terceiros.
- [Microsoft: gerenciamento de consentimento](https://learn.microsoft.com/en-us/clarity/setup-and-installation/consent-management): separa analytics e publicidade; negar publicidade não é uma garantia documentada de eliminar todos os cookies de terceiros.
- [Microsoft: comportamento sem consentimento](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-without-cookie-consent): sessões por página, perda de continuidade e de identificação de recorrência. A página descreve especificamente o comportamento nas regiões sujeitas a consentimento; validar condições concretas do projeto.
- [Microsoft: integração com Google Consent Mode](https://learn.microsoft.com/en-us/clarity/setup-and-installation/cookie-gcm): Clarity reconhece sinais GCM; evitar duas fontes conflitantes caso uma integração venha a ser proposta.

Consultar novamente as fontes ao executar os tickets. Não há comprovação de que uma alteração de consentimento preserve as funções e elimine as duas falhas neste projeto; isso é uma hipótese de investigação.
