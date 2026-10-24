# Apuração factual — narrativa visual de Enrollment, Harmony e Convênios

Data: 2026-10-24. Checkout: `D:/Projetos/Portfolio`. Pesquisa individual, sem browser, sem implementação, sem alterações no repositório. Este é um artefato temporário; não substitui o handoff recebido.

## Base e limites

Lidos antes da exploração: `AGENTS.md`, `docs/agents/domain.md`, `GLOSSARY.md` e `docs/adr/0001-preservar-analytics-na-otimizacao-lighthouse.md`. O ADR trata de continuidade de Clarity/GA4, sem decisão específica sobre narrativa visual. Não há conflito com esta pesquisa. Lidos também o handoff `%TEMP%/portfolio-cases-visual-narrative-handoff.md`, os três HTMLs, seus estilos locais existentes, os trechos pertinentes do CSS/JS compartilhado e os documentos Markdown em `.scratch/enrollment/`, `.scratch/harmony/` e `.scratch/convenios/`.

Confrontei os registros anteriores de Billing com seu relatório de validação e comentários posteriores: prevalece o fluxo estático, com conteúdo visível, sem links para screenshots cruas. O spec original de Billing ainda menciona `details`/`summary`, mas isso foi superado pela revisão do usuário. Fontes: `.scratch/billing/visual-narrative-validation.md`, `.scratch/billing/issues/01-interactive-flow.md`.

Inspeção visual feita com `view_image`, individualmente: dez novas telas de Enrollment; oito novas telas de Harmony; dois JPGs do comparador Enrollment; os dois JPGs antes/depois de Harmony; os dois posters dos heroes; seis imagens distintas de Convênios (os quatro WebPs usados e os dois PNGs não usados). Inspecionados também cinco quadros Behance já arquivados no temporário: `portfolio-convenios-behance/board-{03,07,08,12,13}.img`, referenciados por `.scratch/convenios/behance-images.json`.

Não abri nem testei a página no browser. Não reproduzi MP4s; apenas seus posters. Não confirmei os serviços em produção, lojas, pacotes ou Storybook ao vivo. Os estados atuais de adoção/disponibilidade vêm das confirmações do autor já registradas em `.scratch`, não de verificação remota. Não há evidência aqui para resultados mensurados novos. Conteúdo fora das bordas dos PNGs não pode ser recuperado por recorte.

`git status --short` no início confirmou muitas alterações de outras tarefas e assets novos. Nenhum arquivo do checkout foi escrito, revertido, formatado ou staged.

## Enrollment

### Narrativa e decisões existentes

Fonte principal: `case-studies/enrollment.html:93` em diante. O problema é a dificuldade de explorar planos, enviar documentos e acompanhar a proposta sem recorrer ao atendimento. O papel relata discovery, entrevistas, regras de negócio e protótipo Figma com variáveis. As três decisões são: explorar antes de criar conta; reorganizar etapas; explicar status e próximos passos. Atualmente as decisões não têm screenshots próprias. `What Shipped` contém apenas o comparador do simulador (`:168–186`).

O resultado é 408 propostas em jan/2023 e 1.105 em jan/2024, crescimento arredondado de 171%, com lançamento em mar/2023. Não são adesões concluídas, taxa de conversão ou efeito exclusivamente atribuível ao redesign. Reduzir ligações é objetivo sem medição disponível. Fontes: `enrollment.html:189–209`, `.scratch/enrollment/copy-decisions.md`, `.scratch/enrollment/issues/01-metric-definition.md`. Definição exata do evento e fonte original permanecem pendentes; não precisam ser reabertas para decidir composição visual.

O CSS próprio `assets/css/enrollment.css` contém somente máscaras dos ícones e grade dos três resultados no desktop. A comparação é compartilhada: `assets/css/case-study.css:294–382`, `assets/js/scroll-animations.js:104–118`.

### O que as novas imagens mostram

Todas as dez telas abaixo estão em `assets/images/enrollment/` e medem 1920 × 1200.

- `inicio.png`: entrada do simulador, aviso de elegibilidade por parentesco, publicidade e formulário com nome, nascimento, celular, e-mail, estado e município; consentimento de marketing opcional; Avançar desabilitado. Existe botão Fazer login no cabeçalho, mas o formulário não pede senha. Não sustenta a expressão “sem fornecer dados”: a pessoa fornece dados antes de avançar. Não comprova sozinho ausência de cadastro anterior nem que o formulário já cria uma conta. Há placeholder “Lorem Ipsum” no cabeçalho e anúncio com validade até outubro de 2023.
- `simulador.png`: nascimento/localidade, três opções (Família, Essencial, Vida Brasília), linhas comparáveis de benefícios, valores, detalhes, Contratar agora e Quero ser contatado. Repete o núcleo visual do lado novo do comparador e do poster do hero. O topo da captura já está cortado.
- `parentesco.png`: etapa 1, explicação de elegibilidade até quarto grau e opções BB/CASSI recolhidas; plano/mensalidade e sete etapas sempre visíveis na lateral. Não mostra a seleção do parentesco aberta.
- `dados-parente.png`: apesar do nome, mostra etapa 2, Dados pessoais, com CPF, nome, nome social, mãe, sexo, nascimento, estado civil e documento; instruções de cópia do documento e início da área de anexos. O nome do arquivo não deve virar legenda. A área de upload fica parcialmente fora da captura.
- `pagamento.png`: etapa 4; distingue primeiro pagamento após análise documental de preferências das próximas mensalidades; boleto/débito, vencimento, recebimento por e-mail, responsável financeiro. Não é checkout para pagar imediatamente nem confirmação de pagamento.
- `portabilidade-1.png`: etapa 5, pergunta se a pessoa já tem plano e deseja aproveitar carências, com Não selecionado. Mostra a escolha de entrar ou não nesse assunto. Não comprova o fluxo completo de quem escolhe Não.
- `portabilidade-2.png`: mesma etapa 5, explicação do conceito, instruções para solicitar e categorias normal/especial em accordions fechados. Não é etapa posterior à tela 1 numa sequência obrigatória: são estados/caminhos da mesma parte do fluxo.
- `portabilidade-3.png`: mesma etapa 5, redução de carências, requisitos, declaração de atendimento, documentos e uploads. É outro conteúdo da área, não prova de que 1→2→3 seja o único caminho linear. Há divergência interna visível: painel esquerdo fala em comprovantes dos dois últimos meses, rótulo do upload em três últimos meses. Não repetir números específicos na nova copy sem esclarecer. Também contém placeholders para nome e CPF.
- `contrato.png`: etapa 6, leitor do contrato, botão para baixar, declaração de leitura/aceite e Próximo desabilitado. Não mostra assinatura desenhada, biometria ou autenticação de assinatura; preferir descrição de revisão e aceite, se essa for a explicação desejada.
- `success.png`: proposta enviada para análise, protocolo, informação de próximos passos por e-mail e link de acompanhamento. Não confirma aprovação, pagamento ou adesão efetivada. “Contato em até 24 horas” é uma mensagem da interface, não prova de SLA cumprido. O link é um placeholder e há dados de exemplo. Não mostra a tela de consulta de status nem a notificação enviada.

### Comparador: evidência, utilidade e limites

Imagens efetivamente usadas: `old-enrollment-journey-simulator.jpg` e `new-enrollment-journey-simulator.jpg`, ambas 1440 × 1485.

O antigo mostra nove cartões em três colunas com planos nacionais/regionais, preço e descrições próprias. O novo mostra três opções após localidade, tabela de benefícios com linhas alinhadas e filtros de nascimento/estado/município. A diferença de organização é real e oferece um motivo para comparação. Contudo, os conteúdos não estão registrados na mesma posição: nove cartões versus três colunas, cabeçalho/rodapé diferentes e preços/regiões diferentes. Não é um comparador preciso de pixels equivalentes nem evidência de redução do catálogo ou de preço.

O controle é um `input type=range`, 0–100, inicial 50; move o `clip-path` da imagem antiga e o handle. Há inicialização inclusive com reduced motion. O relatório `.scratch/enrollment/validation.md` registra teste anterior por Home/End/setas/ponteiro e várias larguras. Nesta rodada conferi código e imagens, sem repetir teste no browser. Os nomes acessíveis são genéricos (Comparison slider / Before and after comparison), não explicam a mudança editorial. A mesma imagem nova aparece três vezes se se mantiverem poster, comparador e `simulador.png` integral sem funções distintas.

### Encaixe editorial recomendado, sujeito à entrevista

- Concentrar a comparação de planos junto da decisão de exploração; manter uma única demonstração estática detalhada do resultado, ou manter o comparador como exceção funcional deliberada. Não adicionar automaticamente `simulador.png` como repetição em What Shipped.
- Associar `parentesco.png` à sequência e à elegibilidade; `dados-parente.png` ao preparo/envio de documentos; `pagamento.png` à explicitação das condições financeiras; `contrato.png` à revisão e aceite. É possível selecionar menos telas para não transformar a página em transcrição de formulário.
- Tratar portabilidade como caso específico com escolha, explicação e documentos, se ela representar uma decisão relevante do trabalho. Se usar mais de um estado, cada um precisa de argumento próprio; preservar a distinção entre caminhos.
- Usar `success.png` junto da decisão de próximos passos com linguagem limitada a envio para análise/protocolo. Não chamá-la de dashboard de status.
- Recortes futuros podem retirar cabeçalho/rodapé repetidos. Preservar stepper ao explicar progressão e preservar avisos de análise junto de pagamento/envio. Formulários e tabelas pedem blocos largos; um recorte não pode recuperar controles que já ficaram fora da screenshot.

### Decisões reais para a entrevista (não feitas nesta pesquisa)

1. O comparador interativo continua como exceção com função própria, ou a comparação deve virar duas imagens com explicações separadas? A mudança a enfatizar é catálogo→comparação por localidade, e não um detalhe visual alinhado.
2. `inicio.png` é exploração sem criação de conta, captura de lead ou outro marco? Qual é a distinção factual entre fornecer dados e criar uma conta nesse fluxo? Isso decide se a tela ajuda ou confunde a decisão 01.
3. Portabilidade merece um argumento próprio? Os estados 1/2/3 correspondem exatamente a quais escolhas? Pode-se selecionar o estado documental mais informativo sem inventar uma sequência?
4. Quais telas são protótipo versus produção e quais são contemporâneas do lançamento? Os placeholders visíveis impedem apresentá-las automaticamente como capturas da produção.
5. Existe imagem de acompanhamento real a incluir posteriormente, ou o texto deve se limitar ao que `success.png` demonstra nesta rodada?

## Harmony

### Narrativa e decisões existentes

`case-studies/harmony.html:92–208` apresenta fragmentação em cinco bibliotecas/plataformas, liderança de design com implementação React pelo time em parceria, biblioteca compartilhada/governança, React + Next.js por manutenção/contratação e acessibilidade/conteúdo como requisitos contínuos. Resultado: adoção em novos projetos e migração gradual de legados. A seção final relata prototipação HTML/CSS/JS com IA e conversão para React ainda em estudo/desenvolvimento.

`.scratch/harmony/copy-draft.md` registra que essas decisões já foram confirmadas. Não reabrir velocidade, prazo de três meses, migração integral ou autoria individual de React. As imagens não autorizam restabelecer essas alegações. Não há CSS próprio do Harmony: o HTML importa `assets/css/case-study.css`; o antes/depois usa `.cs-image-grid`, duas colunas e legendas após as imagens (`harmony.html:172–183`).

### O que as oito novas imagens mostram

Todas em `assets/images/harmony/`, 1920 × 1200.

- `color=primitives.png`: prancha Color Primitives; afirma 13 famílias/134 tokens na coleção Colors e vínculo das amostras a variáveis; a captura mostra escalas Primary e Secondary (50–900), com início de Tertiary. Os totais são texto da prancha, não contagem independente das variáveis. Não chamar a imagem de paleta completa.
- `semantic-tokerns.png`: prancha Semantic Tokens; coleção Backgrounds, com grupos Surface, Border e início de Content. Roles Default, Soft, Hard, Disabled, Emphasis, Highlight, Success, Warning e Critical visíveis. Demonstra nomes por uso, sem exibir a resolução dos aliases para primitivos. O texto “sempre contraste AA” da prancha não é auditoria de conformidade. Parte inferior cortada.
- `variables.png`: painel Figma da coleção Breakpoints, modos Desktop/Tablet/Mobile, ScreenSize 1440/768/390 e grupos Gap/Padding/Radius/Icons. Mostra valores/aliases nos três modos e a coleção Scale na lateral. Não é demonstração de tema claro/escuro, nem mapeamento de tokens de cor.
- `buttons.png`: matriz Figma de botões Standard/Alternative/Critical, NormalSize/SmallSize, Solid/Outline/Ghost, variantes de texto/dropdown/ícone e estados visuais. Nomes de componentes sobrepostos e texto interno minúsculo limitam leitura; contém variedade, sem explicar por si cada estado e sua implementação.
- `components.png`: headers de Portal autenticado/visitante e Intranet, botões/menus de perfil e versões de navegação estreitas. Melhor evidência de padrões de navegação compartilhados/adaptados entre contextos do que de um catálogo genérico de todos os componentes. Há conteúdo truncado na borda inferior e labels pequenos.
- `templates.png`: canvas Figma com Form/Add, Form/Resume, Form/AddItem, Form/Success, List/CardView, List/TableView e Loading; painel de propriedades de instância selecionada, com SwitchProfile, breadcrumb e alternâncias de linhas/conteúdo. Evidência de composições configuráveis em design. Não prova geração automática de telas nem valida a iniciativa de conversão de protótipos para React. Texto das telas muito pequeno.
- `storybook.png`: introdução ao guia, catálogo lateral de componentes e nomes dos pacotes `@cassi/harmony`, `@cassi/next`, `create-cassi-next-app`. O texto visível descreve React, utilitários Next.js e CLI. A screenshot corta a direita; não prova publicação pública, instalação bem-sucedida ou status de todos os itens listados. Repete o conteúdo do poster do hero.
- `storybook-2.png`: preview de Button e painel Controls (contador 96) com onPress, children, variant solid e tamanhos sm/md. Abas Actions, Interactions, Accessibility e Performance visíveis. O contador é de controles, não componentes. A presença da aba Accessibility não comprova testes aprovados; screenshot estática não comprova interação executada.

### Antes/depois existente

`harmony-antes.jpg` (1216 × 724) é lista de arquivos Figma com vários guias separados, incluindo um arquivo já chamado Harmony [Design System]. Portanto, “antes de Harmony existir” seria uma cronologia mais forte do que a imagem permite. `harmony-depois.jpg` é organização em quatro cartões: Logos, Harmony, Paleta e Ícones. Não mostra todos os recursos fisicamente fundidos num único arquivo nem prova migração de plataformas. As legendas atuais comunicam uma história relatada pelo autor, mas os pixels mostram organização de bibliotecas. Fontes: inspeção das imagens e `harmony.html:172–183`.

### Encaixe editorial recomendado

- Usar organização antiga/atual como contexto da fragmentação, em linhas separadas caso ambas sejam mantidas. Evitar chamá-las de prova de migração concluída.
- Narrativa por camadas: primitivos → papéis semânticos → variáveis responsivas → componentes → templates → documentação/implementação com desenvolvimento. É uma proposta de leitura, não uma nova decisão histórica confirmada.
- Aproximar `storybook.png` da decisão React/Next e `storybook-2.png` da colaboração design/desenvolvimento. Dar funções diferentes às duas; a primeira explica acesso/documentação, a segunda configuração do componente.
- Preferir recorte focal de `buttons.png` ou `components.png` a duas visões panorâmicas pouco legíveis. Cada uma pode permanecer se explicar respectivamente estados/variantes e adaptação por contexto.
- Não usar templates/Storybook como prova da iniciativa de IA entregue. A seção Work in Progress deve continuar explicitamente em desenvolvimento.
- Pranchas semânticas, variáveis e templates merecem largura maior. Alternância lateral pode ser aplicada onde o recorte conserve leitura; oito screenshots não precisam ser oito argumentos de igual peso.

### Decisões reais para a entrevista

1. Aprovar organização por camadas ou manter as três decisões atuais como eixo para distribuir evidências?
2. Manter ambas as imagens de organização antiga/atual, ou reduzir seu protagonismo diante das evidências mais concretas? A presença de Harmony na imagem antiga deve orientar a legenda.
3. Qual exemplo demonstra uma regra real de acessibilidade/conteúdo ou exceção governada? O material atual mostra variantes, mas não sustenta nova alegação de conformidade ou governança medida.
4. Os números escritos nas pranchas são atuais e relevantes? Se não forem necessários, descrever papéis e exemplos sem transformar 134 tokens/96 controles em métricas de impacto.
5. Quais imagens representam o estado vigente do sistema e qual a contribuição de Felipe versus desenvolvimento em cada evidência? A divisão geral já foi respondida; só perguntar pelo exemplo concreto ainda desconhecido.

## CASSI Convênios

### Narrativa e decisões existentes

`case-studies/convenios.html:92–144`: ausência de canal digital dedicado para participantes de reciprocidade; liderança de produto/design até pós-lançamento; essenciais/cartão; múltiplas contas; biblioteca própria. Quatro imagens usadas: home no hero, cartão, contas e componentes junto das escolhas. A página não tem comparador.

`assets/css/convenios.css` já ordena texto antes da imagem no DOM/mobile, mas todas as três linhas desktop mantêm texto à esquerda/imagem à direita em 1fr/1fr; não há alternância. A figura tem padding e `max-height:480px` para a imagem, comprimindo especialmente a documentação densa. O link da biblioteca abre o WebP cru (`convenios.html:131`), em desacordo com a preferência atual do handoff.

O glossário e `.scratch/convenios/behance-analysis.md` já confirmam que Convênios precede Harmony, tem biblioteca/linguagem próprias e não pode ser apresentado como aplicação ou variante do Harmony. Não há confirmação de migração ou reutilização posterior de componentes. A intenção original de referência visual corporativa foi substituída por outra direção durante revisão de marca; é contexto documentado, não motivo para fazer as telas antigas parecerem Harmony.

### O que cada imagem mostra e o que ainda não é usado

- `convenios-home.webp` (818 × 1025): telefone inclinado com dados/status/validade do cartão, copiar número, Exibir cartão, serviços em destaque (extrato/rede/cartão) e notificações. Já está no hero. Não mostra o login biométrico nem telas completas de autorização/extrato.
- `convenios-card.webp` (758 × 1031): composição de dois telefones com frente e verso do cartão e ações de virar/copiar/compartilhar. É um único asset composto, não duas screenshots independentes no HTML. O mockup isolado não demonstra biometria.
- `convenios-accounts.webp` (1024 × 844): sheet Trocar conta com três perfis salvos, um selecionado, remoção, Adicionar outra conta e Trocar conta. A imagem isolada não comprova persistência de autenticação; essa explicação está explícita no quadro Behance 12 e foi aprovada nos esclarecimentos do autor.
- `convenios-components.webp` (1024 × 1322): documentação Button com botões padrão, ícone e link; estilos/funções/estados; áreas de toque; aplicações em telas. Boa evidência para explicar consistência/acessibilidade como decisões documentadas, sem prometer certificação. Visão integral na coluna atual é pequena; um recorte de uma seção pode sustentar um argumento concreto.
- **`convenios-provider-network.png` (1024 × 768): útil e ainda não usado no HTML.** Telefone com Rede credenciada, Dermatologia, 07 resultados encontrados, marcadores num mapa, Voltar para lista e Realizar nova busca. Mostra resultado geográfico, não o formulário de pesquisa nem ordenação por distância ou geolocalização automática. Tem grandes margens transparentes; recorte de apresentação do mockup pode melhorar aproveitamento. Preservar transparência, sem copiar mecanicamente o JPEG do Billing.
- `convenios-cover.png` (2048 × 1059): capa tipográfica “APP FROM SCRATCH” com ilustrações; não mostra função do produto. Também não usada. O rascunho aprovado já preferiu home no hero; não há motivo factual novo para substituir pela capa.

Verificação adicional com Pillow: os quatro pares PNG/WebP usados têm dimensões e bytes RGBA decodificados idênticos. Não são quatro imagens inéditas a acrescentar. Os mockups têm canal alfa; um JPEG perderia transparência. Fonte da equivalência: comparação local desta pesquisa, consistente com `.scratch/convenios/validation.md`.

### Conflito documental resolvido: rede credenciada

`.scratch/convenios/notion-source.md` registra provider network pendente; `copy-draft.md` por isso deixa imagem de fora. Porém `.scratch/convenios/behance-analysis.md`, em Fatos 6 e Esclarecimentos do autor, atualiza explicitamente: a busca já está disponível, sem data de entrada informada. O quadro 13 arquivado mostra a mesma função. Para a nova narrativa, é possível apresentá-la como função disponível segundo o autor; não afirmar que integrou o lançamento inicial, nem voltar a perguntar se já existe. Perguntar só data se essa temporalidade for necessária à narrativa.

### Material de processo fora de assets

O quadro 08 já arquivado em `%TEMP%/portfolio-convenios-behance/board-08.img` mostra grupos de fluxos (login/primeiro acesso/onboarding/senha, home/menu/notificações/cartão, autorizações/rede/extrato, perfil etc.). É evidência de escopo projetado, não de entrega de cada função. Há texto/telas minúsculos e trechos cortados no topo. Não existe como asset pronto na pasta pública; não prometer detalhe legível apenas ampliando essa rasterização. Quadro 07 repete a documentação de botões. Quadro 03 lista gerente de serviços, Design Lead, designer sênior, designer júnior e estagiária, mas não a divisão concreta de decisões. Quadro 12 documenta explicitamente alternância entre contas simultâneas sem logout.

### Limites e encaixe editorial recomendado

- Há valor novo suficiente para uma linha própria de rede geográfica. Não tratar Convênios como caso sem material adicional útil.
- Separar a argumentação de contas da frase genérica sobre notificações, autorizações e extratos; essas funções não são mostradas pelo mockup de troca. A home sustenta uma explicação de comunicação, e o quadro de fluxos sustenta escopo projetado, sem provar produção.
- Dar destaque à alternância sem logout com base nas fontes já confirmadas. A motivação concreta e contribuição direta de Felipe continuam em aberto, conforme `behance-analysis.md`.
- Biblioteca própria pode receber um recorte legível de Button, preservando exemplos de estado/área de toque/aplicação. Substituir futuramente o recurso de abrir imagem crua por conteúdo legível no corpo, seguindo o padrão já aprovado, não por nova interação.
- A frase atual “The component library reduced rework” (`convenios.html:140`) vem do relato do Notion, sem exemplo/medição. A nota editorial mais recente recomenda fechar com entregas concretas. Não converter esse relato em resultado medido. “A shared foundation” precisa deixar claro que se trata da base do produto, não de Harmony.
- Manter a identidade própria e a ausência de etiquetas extras aprovada para este case. Adotar o ritmo do Billing sem exigir mesma arquitetura de seções ou converter mockups transparentes em JPEG.

### Decisões reais para a entrevista

1. Incluir rede como quarta evidência junto de acesso aos serviços, ou focar só contas/cartão/biblioteca? A disponibilidade já foi confirmada; falta escolher seu papel editorial.
2. Qual situação concreta levou a manter várias contas simultaneamente e qual decisão Felipe conduziu? Houve alternativa/restrição importante? É a principal lacuna para transformar uma capacidade em narrativa de liderança.
3. O escopo de processo merece entrar? Há imagem mais próxima/exportável do fluxo que permita explicar uma escolha sem depender de miniaturas do quadro 08?
4. Qual exemplo documentado explica redução de retrabalho? Sem ele, manter entrega/biblioteca e intenção de evolução, sem alegação nova de eficiência.

## Prioridades para conduzir a entrevista

1. Enrollment: papel do comparador e distinção entre exploração, dados iniciais e criação de conta; seleção da portabilidade como argumento próprio.
2. Harmony: organização por camadas, seleção de exemplos e estágio de cada evidência, preservando evolução contínua e autoria compartilhada já confirmadas.
3. Convênios: incorporar rede disponível, aprofundar a escolha de contas simultâneas e dar legibilidade à documentação própria.

Não é necessário pedir novamente preferências já aprovadas: uma imagem por linha com explicação própria, alternância com blocos largos, explicação antes da imagem no mobile, originais intactos, ausência de links crus, copy inglesa factual e conteúdo visível sem interações criadas apenas para escondê-lo.
