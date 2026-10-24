# Enrollment Journey: decisões editoriais

Data: 2026-10-24.

## Referências e escopo

- Handoffs lidos em `%TEMP%/portfolio-case-handoffs-20261024/`, resolvido pela variável de ambiente do Windows para `C:/Users/fplev/AppData/Local/Temp`.
- Referência final: `case-studies/harmony.html`, `.scratch/harmony/copy-draft.md` e `validation.md`.
- Componentes existentes: `.cs-problem__points`, `.cs-decisions--stacked`, `.cs-decision__note` e `.cs-decision__note-icon` em `assets/css/case-study.css`.
- Lidos `AGENTS.md`, `docs/agents/domain.md`, `GLOSSARY.md`, instruções do tracker, origem e licença Tabler. Não há ADR pertinente disponível em `docs/adr/`.
- Skill aplicada: `design-taste-frontend`, limitada à evolução pontual autorizada. Direção: case editorial para avaliação do trabalho de design, mantendo a identidade atual. Variância 5, movimento 3 e densidade 3; nenhuma animação nova.
- Preservados tipografia Fraunces/Inter, tema escuro, cor de destaque, tokens, hierarquia, idioma inglês, imagens, comparador, contato e navegação. As recomendações genéricas da skill sobre redesenho integral, troca tipográfica, tema e cabeçalho cedem ao escopo explícito de preservação.

## Auditoria inicial

O contexto estava em um card lateral com quatro fragmentos. As três decisões tinham pílulas longas à direita, afastadas dos parágrafos. O comparador já era um range nativo. Capturas anteriores estão em `qa/before-*.png` e medições em `qa/baseline.json`.

A página usava três unidades para o mesmo percentual: enrollments, completions e proposals. A redução de demanda do atendimento aparecia como resultado sem medição. “Dropped immediately”, “never left unanswered”, “most enrollments” e “redesign everything” ampliavam as alegações além da evidência disponível.

## Confirmações do usuário neste chat

- O indicador 408 (jan/2023) → 1.105 (jan/2024) conta **propostas criadas ou enviadas; não necessariamente adesões concluídas**.
- A redução de ligações/dependência do atendimento era **um objetivo, sem medição disponível**.

Consequências editoriais: manter 171%, usar “proposal volume”/“proposals” consistentemente em hook, metadados, resumo e resultados; retirar equivalência com adesões/conclusões e atribuição causal exclusiva. O percentual arredondado é `(1105 - 408) / 408 * 100 = 170,8333…%`. Essa conta verifica apenas a variação, não a definição do evento.

## Implementação

- Três obstáculos concretos abaixo da introdução: cadastro antes de explorar planos; envio de documentos com validação e retrabalho; consulta ao atendimento por falta de status.
- Decisões em uma coluna, com notas de exploração antes do cadastro, sequência do percurso e acompanhamento da proposta.
- Ícones oficiais Tabler `lock-open`, `route`, `list-check`, decorativos e acompanhados de texto. Origem registrada em `assets/icons/tabler/enrollment/README.md`; licença compartilhada preservada.
- Removido o card de seta para baixo que sugeria redução medida de dependência. Os três cards restantes reutilizam os estilos existentes, com grade local de três colunas no desktop.
- Redução de consultas ao atendimento descrita como intenção no texto da terceira decisão.
- Resultado informa período, unidade e limite de atribuição. Não cria taxa de conversão nem dado de adesões concluídas.

## Questões ainda abertas

Ver `issues/01-metric-definition.md`. O significado geral de propostas e a ausência de medição de atendimento estão resolvidos. Permanecem pendentes a fonte original, a definição exata do evento (criação ou envio), a comparabilidade dos recortes e eventual evidência de contribuição do redesenho.

## Integração posterior, sem escrita concorrente

`index.html` e a tabela de `portfolio-dev-plan.md` ainda têm a redação antiga de Enrollment. Não foram editados. Proposta para integração pelo responsável:

- Hook: `Redesigning plan exploration, document submission, and status tracking. Proposal volume grew 171% from January 2023 to January 2024.`
- Número: `171%`.
- Rótulo: `more proposals`.

Isso elimina a equivalência com adesões concluídas e a alegação “We fixed that” também nessas superfícies em uma etapa posterior de integração.
