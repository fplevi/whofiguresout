# Billing — narrativa visual e fluxo interativo

Status: ready-for-agent
Data: 2026-10-24
Executor previsto: Claude Code

## Objetivo

Distribuir as telas de Billing ao longo dos argumentos do case, substituir o fluxograma estático por um componente interativo e variar a composição para dar ritmo à leitura. Cada imagem deve ter uma explicação orientativa própria e aparecer em uma linha independente das demais imagens.

O usuário aprovou a seleção de sete telas novas, a alternância de texto/imagem combinada com blocos largos e os recortes de apresentação que preservem os originais. Alterou a primeira proposta: a imagem do fluxograma deve ser redesenhada como componentes interativos no site. Pediu somente specs e tickets nesta sessão; a implementação será executada pelo Claude Code.

## Execução

Ler este spec, depois executar os tickets na ordem indicada:

1. [01 — Fluxo interativo](issues/01-interactive-flow.md).
2. [02 — Preparação das imagens](issues/02-image-preparation.md).
3. [03 — Narrativa e composição](issues/03-visual-narrative.md).
4. [04 — Validação e entrega](issues/04-validation.md).

Cada ticket usa `Status:` para a triagem e registra progresso e conclusão em `## Comments`. Ao concluir, registrar `Concluído em: <data>` nesse histórico; atualizar o status conforme a convenção vigente do repositório. Dependências indicam ordem de execução, sem autorização para começar trabalho dependente incompleto.

## Escopo e referências

- Página: `case-studies/billing.html`.
- Estilos específicos: `assets/css/billing.css`.
- Assets: `assets/images/billing/`; derivados podem ficar em `assets/images/billing/editorial/`.
- Evidências e relatórios: `.scratch/billing/`.
- Referência factual: [factual-questions.md](factual-questions.md).
- Inventário e investigação: [visual-narrative-review.md](visual-narrative-review.md).
- Consultar `AGENTS.md`, `GLOSSARY.md`, `docs/agents/domain.md` e os estilos/tokens existentes antes de implementar. Aplicar a skill local `design-taste-frontend` ao evoluir a composição existente.

O checkout contém alterações anteriores e simultâneas em outros cases, home e estilos compartilhados. Fazer um inventário inicial e preservar esse trabalho. Concentrar a implementação no Billing e em seus assets. Manter navegação, contato, resultados, metadados, hero e próximo projeto existentes; o escopo é a narrativa visual interna. Alterações em estilos ou scripts compartilhados exigem necessidade demonstrada e validação das páginas afetadas. Sem commit, deploy ou PR solicitado.

## Fluxo interativo

Interpretação de implementação para a nova solicitação: um fluxo editorial com etapas expansíveis. Esta mecânica é a proposta técnica do handoff; o usuário pediu interatividade, sem especificar controles. Implementar esta opção simples, sem reabrir a entrevista por escolhas rotineiras.

O componente acompanha a decisão 01, “One unified flow for all profiles”, substituindo a imagem `billing-digital-platform-flow.jpg`. Usar HTML semântico, CSS e elementos nativos `details`/`summary`, sem adicionar dependências. Cada etapa é um item numerado de uma lista ordenada e contém título sempre visível e explicação expansível. Abrir a primeira etapa inicialmente; permitir abrir/fechar cada etapa de forma independente.

Fonte da sequência: fluxograma estático existente, que continua disponível nos assets. Preservar suas oito etapas e sua ordem:

1. **Access** — Enter the negotiation journey.
2. **Contract identification** — Identify the participant using contract details.
3. **View outstanding debts** — Review the outstanding debt before starting a negotiation.
4. **Start negotiation** — Begin the self-service negotiation.
5. **Choose payment method** — Review the available payment options.
6. **Confirm negotiation** — Review and validate the proposed agreement.
7. **Pay invoice(s)** — Proceed with payment of the agreement's payment documents.
8. **Debts cleared** — The journey reaches debt clearance after the outstanding amounts are paid.

As explicações acima são copy inicial editável, limitada ao que o case e o desenho sustentam. A última etapa representa o destino conceitual do fluxo, não uma afirmação de que todo acordo aprovado já foi pago. O componente explica uma estrutura compartilhada e não comprova as permissões de cada perfil.

Requisitos de interação e apresentação:

- Clique/toque e Enter/Espaço expandem/recolhem a etapa com comportamento nativo. Foco visível e nome acessível em todos os controles.
- A sequência inteira permanece identificável com etapas recolhidas, com JavaScript desativado e com movimento reduzido.
- Organizar etapas para leitura em ordem no desktop e em coluna no mobile. Se houver conectores, devem ser decorativos e indicar a ordem correta também nas quebras de linha; numeração e texto carregam o significado.
- Copy e rótulos em inglês, como o restante da página. Instrução curta sugerida: “Select a step to explore the shared journey.”
- Estilo coerente com a paleta escura, acento pêssego, Fraunces/Inter e tokens existentes. Estados de foco, aberto e hover devem ser distinguíveis, sem depender apenas de cor.
- Sem autoplay ou avanço automático. O conteúdo expandido deve ter espaço suficiente e acompanhar o fluxo natural da página.

## Sequência editorial

Manter “The Problem” e “My Role” como abertura textual: os assets mostram a solução e não documentam o processo anterior por telefone. Manter as três decisões e suas notas junto dos respectivos parágrafos.

1. **Decisão 01:** texto e fluxo interativo, cada um com espaço suficiente. A imagem do fluxograma deixa de ser exibida.
2. **Decisão 02:** `MFA.png`, imagem à esquerda e texto à direita no desktop. Explicar seleção de e-mail ou SMS para receber código.
3. **Decisão 03:** `tela-inicial.png`, texto à esquerda e imagem à direita. Explicar escolha entre regularização da dívida e negociação com reativação.
4. **What Shipped — reativação:** `oferta-reativação.png`, imagem à esquerda e texto à direita. Explicar condições da oferta e opção de seguir sem reativação.
5. **Pagamento único:** `pagamento-a-vista.png`, texto à esquerda e imagem à direita. Identificar o exemplo como negociação com reativação.
6. **Parcelamento:** `pagamento-parcelado.png`, imagem à esquerda e texto à direita. Identificar o exemplo como negociação sem reativação.
7. **Revisão e validação:** `resumo.png` em largura maior, com texto acima. Explicar conferência de valores/vencimentos e validação por código.
8. **Acompanhamento:** `3-boletos.png`, imagem à esquerda e texto à direita, focando parcelas pendentes e geração de documentos.
9. **Operação:** dashboard em largura maior, texto acima, antes de “The Outcome”. Explicar acompanhamento operacional de negociações, valores e reativações.

Essa alternância é a direção inicial. Dar mais largura a qualquer tela que fique ilegível na posição lateral, mantendo variedade no conjunto. No mobile, ordenar no DOM a explicação antes da respectiva imagem; usar CSS para alternar o desktop, mantendo a leitura assistiva coerente.

Desfazer o par fluxograma/dashboard de `.cs-image-grid`. Cada imagem estática passa a ter linha própria, título ou texto introdutório e, quando útil, legenda. Não criar pares de screenshots, carrossel ou uma galeria isolada do texto.

## Imagens e textos orientativos

Usar sete das oito novas capturas: `MFA.png`, `tela-inicial.png`, `oferta-reativação.png`, `pagamento-a-vista.png`, `pagamento-parcelado.png`, `resumo.png`, `3-boletos.png`. Omitir `tela.png`, que sobrepõe o acompanhamento. Usar uma versão do dashboard existente, selecionando JPG/PNG pela legibilidade e peso. Não duplicar suas versões.

Todas as capturas novas têm 1920 × 1200. Cabeçalhos e rodapés repetidos podem ser reduzidos por recortes de apresentação aprovados pelo usuário. Preservar imagens originais, valores, controles e contexto necessários para o argumento. Para `3-boletos.png`, destacar o trecho superior de boletos: o conteúdo inferior de contribuição trabalhista é outro assunto.

Gerar derivados apenas quando houver ganho claro de leitura ou tamanho. Registrar origem, área de recorte e dimensões em `.scratch/billing/image-manifest.md`. Exibir imagens proporcionais, com dimensões intrínsecas, sem distorção ou corte acidental de controles. Aplicar lazy loading às imagens abaixo da dobra e alt text específico. Se o conteúdo essencial continuar pequeno em uma tela larga no mobile, fornecer acesso acessível à versão maior, por exemplo link “View full-size screen”; manter o controle junto à sua imagem.

Copy inicial para os novos trechos, adaptável sem acrescentar alegações:

- Acesso: “Participants selected an email or SMS channel to receive a verification code.”
- Escolha: “Participants could review their outstanding debt and choose whether to negotiate with plan reactivation.”
- Reativação: “The offer showed the plan, monthly fee, and debt conditions, with an option to continue without reactivation.”
- À vista: “In this reactivation example, participants could review the single-payment total and the displayed interest and penalty conditions before continuing.”
- Parcelado: “In this example without reactivation, participants could set an optional down payment and select the number of installments while reviewing the total.”
- Revisão: “Before validating the negotiation, participants reviewed the debt breakdown, installment amounts, and due dates, then entered a verification code.”
- Acompanhamento: “Participants could return to view pending installments and generate payment documents.”
- Operação: “The operations dashboard brought together negotiation status, recovery figures, and plan reactivation indicators.”

## Precisão editorial

- Os assets mostram exemplos distintos, com valores e condições diferentes. À vista inclui reativação e parcelado não inclui; apresentar como cenários, sem sugerir uma negociação numericamente contínua.
- Oferta de reativação, negociação validada/aprovada, boleto pendente e pagamento realizado são estados distintos. `resumo.png` é revisão/validação, não tela de sucesso ou comprovante de pagamento.
- Manter cinco minutos como meta de design e Clarity como acompanhamento histórico. Nenhuma duração observada foi fornecida.
- Manter os números existentes e seu contexto histórico, distinguindo dinheiro pago, valores parcelados, contratos reativados e negociações autônomas.
- Manter a descrição do mecanismo de acesso por dados contratuais e código via e-mail/SMS; o nome `MFA.png` e o rótulo da interface não resolvem a classificação técnica pendente.
- Corrigir a legenda atual que chama o fluxograma de “participant-facing screens”. Retirar “in real time” do texto do dashboard, pois a imagem não sustenta essa propriedade.
- Usar texto orientativo com contraste de leitura, sem herdar a baixa opacidade atual de `.cs-image-caption` para conteúdo essencial.

## Aceite global

- Sete novas capturas aparecem nas etapas correspondentes; `tela.png` e o fluxograma estático ficam fora da apresentação.
- O fluxo interativo contém as oito etapas em ordem, funciona por mouse/toque/teclado e sem JavaScript, e preserva leitura com movimento reduzido.
- Há alternância lateral e blocos largos; nenhuma linha contém duas screenshots lado a lado. No mobile, explicação precede a imagem.
- Revisão, pagamento e acompanhamento têm textos próprios, respeitando os limites factuais acima.
- Em 320, 375, 768 e 1440 px, não há overflow horizontal, sobreposição, imagem deformada, controles cortados ou conteúdo essencial inacessível. Todas as imagens carregam.
- Navegação, contato, métricas, hero e próximo projeto preservam seu funcionamento e conteúdo fora das mudanças autorizadas. Validar também com movimento normal: as novas seções devem aparecer ao rolar, considerando o `IntersectionObserver` existente.
- Evidências desktop/mobile e relatório de validação salvos em `.scratch/billing/`. Documentar o que foi efetivamente verificado e eventuais limites.

## Prompt de início para Claude Code

> Implemente `.scratch/billing/spec.md`, executando os tickets de `.scratch/billing/issues/` em ordem de dependência. O usuário já aprovou a direção visual e os recortes. Substitua o fluxograma estático por etapas interativas conforme o spec. Preserve alterações existentes no checkout e mantenha as mudanças no escopo do Billing. Registre conclusão e evidências por ticket. Entregue a implementação validada localmente; sem commit ou deploy.
