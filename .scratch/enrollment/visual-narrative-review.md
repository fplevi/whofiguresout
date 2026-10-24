# Enrollment — revisão da narrativa visual

Data: 2026-10-24.
Estado: entrevista concluída; direção editorial, seleção e distribuição aprovadas. Entendimento final confirmado pelo usuário em Q8, em 2026-10-24.

## Referências

- Handoff: `C:/Users/fplev/AppData/Local/Temp/portfolio-cases-visual-narrative-handoff.md`.
- Precisão editorial já confirmada: [copy-decisions.md](copy-decisions.md).
- Inventário visual delegado concluído: [research.md](../cases-visual-narrative/research.md).
- Padrão visual e revisões posteriores do Billing descritos no handoff.

## Decisões confirmadas

- Q1, primeira rodada: selecionar telas pela contribuição para os argumentos de exploração sem cadastro, organização das etapas e acompanhamento. O usuário respondeu “Sim”. Não documentar obrigatoriamente todas as etapas nem incluir uma imagem apenas porque está disponível.
- Q4: manter o comparador antes/depois em bloco largo, com explicação das mudanças a observar. O usuário respondeu “sim”. Ele compara organização/apresentação dos planos; não comprova ausência de cadastro, redução do catálogo ou de preços.
- Q5: usar quatro capturas além do comparador: `parentesco.png`, `dados-parente.png`, `portabilidade-2.png` e `success.png`. O usuário respondeu “Sim”. Omitir desta apresentação `inicio.png`, `simulador.png`, `pagamento.png`, `contrato.png`, `portabilidade-1.png` e `portabilidade-3.png`; preservar todos os originais. Nomear a última imagem por envio para análise, nunca por adesão concluída.
- Q8: distribuição abaixo e entendimento final confirmados com “Sim”.
- Preservar como ponto de partida as preferências do Billing registradas no handoff: explicação própria por imagem, ritmo lateral combinado com blocos largos quando necessário, explicação antes da imagem no mobile, copy em inglês e precisão factual.

## Distribuição aprovada

1. Exploração dos planos: aproximar o comparador da primeira decisão, em largura maior, com texto orientando a leitura da organização antiga e nova. Não acrescentar uma terceira demonstração integral do simulador.
2. Organização das etapas: `parentesco.png` com elegibilidade e sequência lateral preservadas; `dados-parente.png` para orientação de dados/documentos; `portabilidade-2.png` para explicar uma situação específica dentro da jornada. Cada imagem tem argumento e explicação próprios. Não apresentar as imagens selecionadas como documentação exaustiva das sete etapas.
3. Próximos passos: `success.png` junto da terceira decisão, limitada ao envio para análise, protocolo e orientações; não substituir por inferência de uma tela de acompanhamento inexistente no material.

Alternar laterais onde a leitura permitir e usar blocos largos nas imagens densas. Evitar um bloco “What Shipped” que apenas repita o comparador já integrado à decisão. Preservar hero, contexto, papel, resultados e demais elementos externos ao escopo visual/editorial. Recortes concretos e larguras serão definidos por inspeção no render, sem reduzir fontes.

## Encerramento da entrevista

Não restam decisões editoriais abertas para esta revisão. Enquadramentos e composição responsiva são escolhas de execução a validar visualmente, dentro da seleção e dos limites aprovados. Pendências factuais anteriores sobre a métrica continuam no ticket existente; a entrevista não as resolveu nem depende de ampliar essas alegações.

## Limites

O indicador de 171% conta propostas, sem equivalência com adesões concluídas ou atribuição causal exclusiva ao redesenho. Redução de consultas ao atendimento é objetivo sem medição disponível, conforme as decisões anteriores.

## Evidências da inspeção

- `inicio.png` pede dados pessoais, contato e localidade, sem senha; não comprova sozinho ausência de cadastro. `simulador.png` repete o núcleo do comparador e do poster.
- `parentesco.png` mostra elegibilidade e a sequência lateral de sete etapas. `dados-parente.png`, apesar do nome, mostra dados pessoais do proponente e instrução documental; a área de upload está parcialmente fora da captura.
- As três capturas de portabilidade mostram estados/caminhos da mesma etapa. `portabilidade-2.png` explica o conceito e as categorias; `portabilidade-3.png` contém divergência entre dois e três meses de comprovantes. Não transformar os três estados em sequência obrigatória nem reproduzir requisitos contraditórios.
- `pagamento.png` mostra preferências para mensalidades futuras e informa que o primeiro pagamento ocorre após análise documental; não é pagamento realizado. `contrato.png` mostra leitura/download/aceite, sem comprovar assinatura autenticada.
- `success.png` mostra envio para análise, protocolo e próximos passos; não aprovação ou adesão concluída. O link de acompanhamento é placeholder; não mostra uma consulta real de status. As capturas têm dados de exemplo/placeholders e não devem ser chamadas automaticamente de capturas de produção.
- A inspeção abrangeu assets e código, sem nova validação no navegador ou reprodução dos vídeos. Há testes anteriores do comparador em `validation.md`, que não equivalem a revalidação desta rodada.

Esta rodada registra decisões editoriais reversíveis; não surgiu termo novo para o glossário nem decisão que justifique ADR. A sessão concluiu a entrevista e sua documentação; a implementação não foi executada.
