# Passagem para Claude

## Prompt de execução

> Leia `AGENTS.md`, `GLOSSARY.md`, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md` e `docs/adr/0001-preservar-analytics-na-otimizacao-lighthouse.md`. Depois leia `.scratch/lighthouse-clarity/spec.md` e `.scratch/lighthouse-clarity/evidence.md`.
>
> Execute os tickets individuais de `.scratch/lighthouse-clarity/issues/` pela ordem das dependências, somente após o spec estar confirmado. Preserve as alterações preexistentes do checkout. A meta é melhorar Lighthouse na home e nos quatro cases em desktop/mobile, mantendo Clarity `wo2llblzgf` com continuidade entre páginas e visitas recorrentes, e GA4 `G-C0GC2E2VMN`.
>
> Não troque qualidade de dados por nota. Não detecte Lighthouse, não esconda scripts da medição, não conceda consentimento pelo visitante e não remova analytics. Diagnósticos sem peso não são falhas de pontuação. Faça otimizações próprias apenas com evidência. Não adicione eventos, IDs, CMP, políticas ou infraestrutura sem uma nova decisão quando necessária.
>
> Registre resultados e links de evidência em `## Comments` dos tickets, incluindo revisão e ambiente. Quando houver dependência humana ou de painel, descreva exatamente o que falta e conclua o trabalho independente possível. O rótulo `ready-for-agent` significa especificado, não que as dependências estejam concluídas. Não invente status de resolução: use comentário de conclusão com evidências e preserve o vocabulário local.
>
> O ticket 05 é humano e inclui disponibilização da revisão candidata em HTTPS. Não publique por inferência deste prompt. Só execute a validação final do ticket 06 quando o código publicado corresponder à revisão candidata e as confirmações funcionais estiverem disponíveis. Ao terminar, reporte notas medianas e variação, ganhos reais, funções de analytics verificadas e limitações residuais.

## Ordem

`01 → (02, 03, 04) → 05 humano → 06`.

Não há trabalho de implementação autorizado nesta entrega de preparação. O prompt acima é para a etapa futura de execução com Claude.
