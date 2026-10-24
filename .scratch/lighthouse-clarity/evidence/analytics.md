# Cookies do Clarity e preservação dos analytics

Ticket: [03](../issues/03-analytics-cookies.md). Data: 2026-10-24. Revisão auditada: produção `d2d74df` (`https://www.felipelevi.site/`). Ferramenta: `tools/cookie-experiment.mjs` (Chrome 156, contexto novo por cenário, política de cookies padrão). Resultado bruto sem valores: [cookie-experiment.json](cookie-experiment.json).

Para não criar sessões ou gravações de teste nos painéis, o experimento aborta `t.clarity.ms/collect` e os hits `g/collect` do GA4; bootstrap, biblioteca e pixels `c.gif` seguem normalmente. As coletas do Lighthouse (baseline) não bloqueiam nada.

## Reprodução (cenário publicado)

Estado de consentimento reportado pelo próprio Clarity (`clarity('metadata', …)`): `{source: 0, ad_Storage: "granted", analytics_Storage: "granted"}` — sem CMP/API no site; Consent Mode desligado para tráfego fora de EEA/UK/CH (o teste parte do Brasil).

| Cookie | Domínio | Definido por (Set-Cookie) | Momento | Tipo |
| --- | --- | --- | --- | --- |
| `CLID` | `www.clarity.ms` | resposta de `https://www.clarity.ms/tag/wo2llblzgf` (bootstrap) | antes de qualquer JS do Clarity executar | terceiro |
| `MUID`, `SM` | `.clarity.ms`, `.c.clarity.ms` | `https://c.clarity.ms/c.gif` | após a biblioteca carregar | terceiro |
| `MUID`, `MR`, `SRM_B` | `.bing.com`, `.c.bing.com` | `https://c.bing.com/c.gif` (sincronização de MUID) | idem | terceiro |
| `MR`, `ANONCHK` | `.c.clarity.ms` | `https://c.clarity.ms/c.gif?ctsa=mr…` | idem | terceiro |
| `_clck`, `_clsk` | `.felipelevi.site` | JS do Clarity | idem | primeiro (continuidade e recorrência) |
| `_ga`, `_ga_C0GC2E2VMN` | `.felipelevi.site` | JS do GA4 | — | primeiro |

`inspector-issues`: todos os avisos são `CookieIssue` com motivo **`WarnThirdPartyPhaseout`** (cookie de terceiro lido/definido em `s.clarity.ms/collect`, `c.clarity.ms/c.gif`, `c.bing.com/c.gif`). `third-party-cookies` lista os mesmos cookies. O GA4 só usa cookies primários e não aparece em nenhuma das duas auditorias.

## Documentação oficial (consultada em 2026-10-24)

- [Clarity cookies](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-cookies) (atualizado 2026-10-20): `_clck`/`_clsk` são primários; CLID, ANONCHK, MR, MUID, SM são terceiros. Não há opção documentada para desligar só os de terceiros.
- [Consent Mode](https://learn.microsoft.com/en-us/clarity/setup-and-installation/consent-mode): ligado no painel (Settings → Setup), o Clarity não define **nenhum** cookie, primário ou terceiro, até um sinal válido.
- [consentv2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2): com consentimento concedido, o Clarity "set[s] first-party and third-party cookies"; negado, usa ID por pageview.
- [Gerenciamento de consentimento](https://learn.microsoft.com/en-us/clarity/setup-and-installation/consent-management): `ad_storage` negado só impede o compartilhamento com Microsoft Ads; não promete remover cookies de terceiros.
- [Sem consentimento](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-without-cookie-consent): cada pageview vira uma sessão, páginas por sessão = 1, nenhum usuário recorrente — exatamente o que o ADR-0001 proíbe.

## Alternativas avaliadas

| Alternativa | Remove as falhas? | Preserva continuidade/recorrência? | Resultado |
| --- | --- | --- | --- |
| A. Manter como está | Não | Sim | Escolhida: limitação residual |
| B. `consentv2` com `analytics_Storage: granted`, `ad_Storage: denied`, enfileirado **antes** do bootstrap (escolha do testador, só na sessão de teste) | **Não**: CLID, MUID, MR, SM, ANONCHK, SRM_B continuam todos sendo definidos | **Pior** na execução observada (1 execução): `_clsk` (cookie que une pageviews numa sessão) não foi criado; `metadata` não respondeu | Descartada |
| C. Consent Mode no painel + banner/CMP | Só para quem recusa; quem aceita volta a receber cookies de terceiros (consentv2) | Só para quem aceita | Exige CMP, política e decisão nova (fora do escopo); não leva a 100 em Boas práticas para quem aceita |
| D. Modo sem cookies / sem consentimento | Sim | **Não** (sessão = pageview) | Proibida pelo ADR-0001 e pelo spec |
| E. Atrasar o Clarity até depois da medição, remover, detectar Lighthouse | — | — | Proibida pelo spec |

O `CLID` vem no Set-Cookie da resposta do próprio bootstrap: nenhuma chamada JavaScript no site pode evitá-lo ou removê-lo retroativamente. Os demais vêm dos pixels de sincronização de MUID que a biblioteca dispara quando o consentimento está concedido.

## Conclusão

**Limitação residual comprovada do fornecedor.** `third-party-cookies` (peso 5/26) e `inspector-issues` (peso 1/26) são causados exclusivamente por cookies de terceiros do Clarity; a única configuração documentada que os elimina (sem consentimento / Consent Mode sem aceite) fragmenta sessões e elimina a recorrência, o que o ADR-0001 rejeita. Nenhuma alteração de consentimento, publicidade, mascaramento ou configuração de produção foi feita.

Com o favicon corrigido (erro de console próprio, ver [resources.md](resources.md)), a nota esperada de Boas práticas é **(26 − 5 − 1) / 26 ≈ 77**, igual ao anexo; os 23 pontos restantes são esse trade-off aprovado.

Não é necessária decisão nova para fechar o ticket. Uma decisão nova só seria necessária se o usuário quiser adotar a alternativa C (banner/CMP), que muda a política de consentimento e não garante 100.

## Verificações que dependem do painel (ticket 05)

Sem credenciais em arquivos/chat; somente leitura:

1. Clarity `wo2llblzgf` → Settings → Setup: registrar se o "cookie setting" está ligado (cookies por padrão) e se há Consent Mode/integração com Google Consent Mode.
2. Clarity → Recordings: uma visita própria home → case → outro case → home deve aparecer como **uma** sessão com 4 páginas; uma segunda visita no mesmo navegador, horas depois, deve aparecer como usuário recorrente.
3. GA4 `G-C0GC2E2VMN` → Realtime/DebugView: pageviews das 4 páginas, sem duplicação.
4. Fazer 2–3 também após publicar o candidato e comparar.
