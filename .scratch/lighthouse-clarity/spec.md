# Melhorar Lighthouse preservando Clarity e GA4

Status: approved — entendimento final confirmado pelo usuário em Q6
Data: 2026-10-24
Execução prevista: Claude, em etapa posterior. Esta entrega contém documentação e tickets.

## Problema e resultado esperado

O relatório enviado já apresenta Performance 100 e SEO 100 na home desktop. Acessibilidade está em 96 por contraste; Boas práticas está em 77 por duas auditorias de cookies associadas ao Clarity. Melhorar as páginas sob nosso controle e investigar a configuração suportada dos fornecedores, buscando 100 nas quatro categorias principais e preservando a qualidade da coleta.

Preservar o Clarity significa manter o projeto `wo2llblzgf`, gravações, continuidade do percurso entre páginas e reconhecimento de visitas recorrentes nas condições em que essas funções estão disponíveis e autorizadas. Preservar GA4 significa manter a propriedade `G-C0GC2E2VMN` e sua coleta atual. Carregar o script ou receber HTTP 200 de um endpoint, isoladamente, não comprova esses resultados.

## Decisões confirmadas na entrevista

- Q1: incluir home e todos os estudos de caso, em desktop e mobile.
- Q2: permitir correções de contraste em textos e estados dos controles, preservando a direção visual e verificando as alterações visualmente.
- Q3: continuidade das gravações e visitas recorrentes no Clarity têm prioridade sobre a nota 100 em Boas práticas. Uma limitação residual comprovada do fornecedor é aceitável.
- Q4: manter também o GA4 atual.
- Q5: usar produção HTTPS como referência final, com três medições por página e perfil; localhost continua como apoio ao desenvolvimento.

## Escopo de páginas

Host canônico observado: `https://www.felipelevi.site`, conforme `CNAME` e redirecionamento HTTPS verificado em 2026-10-24. Confirmar novamente na execução.

- `/`
- `/case-studies/billing.html`
- `/case-studies/convenios.html`
- `/case-studies/enrollment.html`
- `/case-studies/harmony.html`

As versões locais e publicadas podem divergir. Toda evidência nova deve identificar a revisão auditada e o ambiente. As alterações locais preexistentes pertencem ao usuário e devem ser preservadas.

## Diagnóstico de referência

Fonte: anexo `pasted-text.txt`, Lighthouse 13.5.0, coleta em `2026-10-24T16:03:25.589Z`, `http://localhost:8000/`, desktop, throttling simulado, emulação de tela desativada. Não é um baseline mobile nem de produção. Ver [evidências e fontes](evidence.md) e [resumo extraído](evidence/report-summary.json).

| Categoria | Nota | Explicação das perdas |
| --- | ---: | --- |
| Performance | 100 | FCP 582 ms, LCP 730 ms, TBT 0 ms, CLS 0,0148, Speed Index 582 ms |
| Acessibilidade | 96 | `color-contrast`: peso 7 de 188 aplicáveis |
| Boas práticas | 77 | `third-party-cookies`: peso 5; `inspector-issues`: peso 1; total aplicável 26 |
| SEO | 100 | Sem falha pontuada |
| Agentic Browsing | 100 | Preservar; não criar WebMCP ou outros recursos para esta entrega |

Contraste: Contact, About e três elementos da legenda do hero apresentam 4,16:1 para texto que exige 4,5:1. O token `--text-secondary` usa opacidade 0,45; a composição de cor e o fundo efetivo precisam entrar na verificação.

Cookies: MR, SM, MUID e CLID aparecem associados ao bootstrap do Clarity. Os avisos do Issues panel também apontam para URLs do Clarity, mas o JSON não inclui o motivo detalhado de cada aviso. Capturar esse motivo antes de definir a mitigação.

Diagnósticos de Performance não descontam pontos diretamente: os 71 KiB estimados de JS não utilizado pertencem ao GA4; há cadeia de fontes por `@import`, reflow próprio no parallax e recomendações de cache/compressão influenciadas pelo servidor local. Priorizar pelo ganho demonstrado, sem assumir que cada aviso precisa desaparecer.

## Requisitos

### Contraste e experiência

Corrigir os pares de contraste comprovadamente insuficientes. Verificar consumidores dos tokens compartilhados nas cinco páginas, inclusive estados de navegação e controles. Texto normal deve atender 4,5:1; texto grande, 3:1 quando a classificação realmente se aplicar. Validar cor composta, fundo, opacidade e estados finais das animações. Não alterar composição, conteúdo ou tipografia para contornar a auditoria.

Preservar navegação, hero, animações, sliders, imagens, formulário, cópia de email, responsividade e reduced motion. Comparar capturas antes/depois nos perfis acordados, com verificação adicional em largura estreita quando houver alteração visual.

### Analytics e cookies

Manter um carregamento por ferramenta em cada documento e os IDs existentes. Investigar o comportamento real do bootstrap, biblioteca e coleta, com perfil limpo e políticas de cookies documentadas. Não inventar eventos, custom IDs ou identificação de usuário: esses recursos não existem no código atual e não são necessários para esta meta.

Avaliar somente alternativas suportadas e documentadas pelo fornecedor. Consent Mode depende também da configuração do projeto no painel; uma chamada de API isolada não deve ser tratada como garantia de impedir cookies emitidos antes dela. `analytics_Storage` e `ad_Storage` são os nomes da API Clarity consentv2; os nomes do Google Consent Mode têm convenção própria. Conferir documentação atual ao executar.

A combinação de consentimento analítico permitido e publicidade negada pode ser investigada como hipótese, em sessão de teste cuja escolha seja real. A documentação não garante que essa combinação elimine todos os cookies de terceiros. Não aplicar a configuração em produção sem demonstrar a preservação das funções e sem uma decisão explícita sobre a política de consentimento.

Modo sem cookies não é uma solução aprovada para esta entrega: muda a unidade da sessão para uma página e compromete a continuidade priorizada. Uma interface nova de consentimento, CMP, política de privacidade, mudança de mascaramento ou integração com publicidade exige decisão própria se a investigação revelar essa necessidade. Registrar a descoberta; não conceder consentimento em nome do visitante.

Não remover ferramentas, trocar IDs, bloquear domínios apenas em auditoria, detectar Lighthouse, atrasar scripts para escapar da janela de medição, simular consentimento ou ocultar avisos. Uma coleta auxiliar sem terceiros pode ajudar a atribuir custos, mas nunca conta como nota de aceite.

### Recursos próprios e hospedagem

Manter HTML/CSS/JS estáticos e o deploy atual. Avaliar a cadeia de carregamento de fontes/CSS e o parallax somente com evidência antes/depois. Assegurar a mesma tipografia, disponibilidade de fontes e comportamento visual. Uma refatoração de infraestrutura, framework, build ou biblioteca de analytics não faz parte desta entrega.

Validar cache e compressão com respostas reais de produção, incluindo negociação de encoding; HEAD sem Content-Encoding não comprova ausência de compressão. Em 2026-10-24 o documento publicado respondeu via GitHub Pages com `Cache-Control: max-age=600`. Esse dado não se estende automaticamente aos assets. Não criar arquivos de headers que o host não interpreta, nem prometer controlar o TTL dos fornecedores.

CSP, HSTS, COOP, framing e Trusted Types não explicam as perdas pontuadas deste relatório. Registrar limitações relevantes descobertas, mas não endurecer políticas incidentalmente e quebrar fontes, scripts, formulário ou Clarity.

## Medição e critérios de aceite

1. Fixar Lighthouse 13.5.0 para comparação quando disponível e compatível. Registrar Chrome, SO, URL, revisão, viewport, throttling, política de cookies, extensões e estado de consentimento. Se a versão mudar, recriar o baseline; não comparar categorias de versões distintas como equivalentes.
2. Gerar baseline atual para cinco páginas × dois perfis × três execuções, em navegador limpo. Usar presets desktop/mobile documentados, idênticos antes/depois. Não reutilizar o perfil estranho do anexo como suposta medida mobile.
3. Fazer a comparação final em produção HTTPS da revisão candidata: 30 relatórios, com mediana por categoria e métricas, além da variação entre as três execuções. Guardar JSON e resumo por página/perfil. Comparações de performance devem usar baseline e candidato do mesmo tipo de ambiente.
4. Meta: 100 em Performance, Acessibilidade, Boas práticas e SEO. Aceite obrigatório: remover as falhas próprias confirmadas, atingir 100 nas auditorias automáticas de Acessibilidade e SEO aplicáveis, e não introduzir regressão reproduzível nas métricas ou nas categorias previamente aprovadas. Uma nota automática de Acessibilidade não substitui a revisão visual e funcional.
5. Boas práticas abaixo de 100 só pode ser aceita com auditoria/URL/causa residual documentadas, atribuição demonstrada e justificativa de que a alternativa prejudicaria a coleta priorizada ou depende do fornecedor. Não aceitar falhas novas próprias sob essa exceção.
6. Se houver nova limitação própria que impeça os critérios, registrar e abrir uma decisão de escopo; não declarar o trabalho concluído nem rebaixar a meta silenciosamente. Distinguir oscilação entre execuções de regressão reproduzível; repetir a célula afetada apenas se houver dúvida concreta.
7. Confirmar ausência de erros novos de console, recursos quebrados e inicializações duplicadas. Verificar navegação home → case → outro case → home e revisão visual dos controles afetados.
8. Confirmar o recebimento de dados no mesmo projeto Clarity e propriedade GA4, continuidade do percurso e visita recorrente em condições comparáveis ao baseline. Evidência de rede é necessária, mas a confirmação funcional do painel fica com o responsável com acesso. Respeitar bloqueio/negação real quando aplicável; não usar perfis consentidos como prova do comportamento sem consentimento.
9. Testar o formulário com respostas simuladas, sem enviar mensagens reais. Não armazenar valores de cookies, identificadores pessoais, conteúdo de gravações ou campos do formulário nos artefatos de evidência.

## Plano de execução com Claude

Os tickets usam o tracker local e preservam as dependências mesmo quando estão rotulados `ready-for-agent`. Esse rótulo não autoriza iniciar antes da confirmação deste spec nem antes de satisfazer as dependências.

1. [01 — Baseline reproduzível](issues/01-baseline.md).
2. [02 — Contraste e revisão visual](issues/02-contraste.md), [03 — Cookies e preservação dos analytics](issues/03-analytics-cookies.md) e [04 — Recursos próprios](issues/04-recursos-proprios.md), após o baseline. Podem ser executados sequencialmente; paralelismo não é necessário.
3. [05 — Candidato HTTPS e confirmação dos painéis](issues/05-validacao-humana.md), pelo responsável humano. A entrega atual não autoriza publicação.
4. [06 — Validação final e relatório de aceite](issues/06-validacao-final.md), após disponibilizar a revisão correta em HTTPS.

Instruções de passagem: [handoff para Claude](claude-handoff.md). Decisão persistente: [ADR-0001](../../docs/adr/0001-preservar-analytics-na-otimizacao-lighthouse.md).

## Fora do escopo

Mudança de hospedagem; framework ou build obrigatório; substituição de Clarity/GA4; eventos ou IDs novos; redesign; alterações editoriais nos cases; objetivo de zerar todo diagnóstico informativo; publicação ou início automático da implementação nesta conversa.

## Confirmação final

Em 2026-10-24, o usuário confirmou em Q6 o entendimento consolidado, os critérios de aceite e as fronteiras da execução. Spec e tickets finalizados para a etapa futura com Claude; nenhuma implementação ou publicação iniciada.

## Comments

- 2026-10-24: spec elaborado a partir do relatório anexado, código local, documentação oficial e respostas Q1–Q5. Nenhum código de aplicação alterado.
- 2026-10-24: Q6 confirmada: “Sim, finalizar o spec e os tickets”. Pacote documental aprovado.
