# 02 — Corrigir contraste e preservar o visual nas cinco páginas

Status: ready-for-agent
Type: task
Blocked by: 01
Executor: Claude

## Contexto

`color-contrast` é a única falha de Acessibilidade pontuada no anexo: Contact, About e três elementos da legenda do hero têm 4,16:1 para mínimo 4,5:1. Fontes: `assets/css/tokens.css:9`, `nav.css:40` e `hero.css:35`. O usuário autorizou ajustes de cor preservando a direção visual. Leia o [spec](../spec.md).

## Trabalho

- Inspecionar os elementos e seus fundos efetivos, inclusive opacidade e estados de animação; mapear consumidores dos tokens afetados nas cinco páginas.
- Escolher a menor alteração coerente no sistema de cores que corrija os pares comprovados e outros pares reprovados no baseline. Decidir entre token compartilhado e aplicação local pelo alcance observado, sem aumentar indiscriminadamente todo texto secundário.
- Verificar navegação normal, ativa, hover, foco e rolada; textos dos cases; formulário, mensagens, botões e sliders quando afetados.
- Garantir 4,5:1 para texto normal e 3:1 para texto classificado como grande. Não usar arredondamento para aprovar valor abaixo do mínimo, esconder texto, mudar seu papel semântico ou alterar conteúdo para passar.
- Registrar cores compostas antes/depois, proporções e capturas desktop/mobile em `../evidence/contrast.md`.

## Aceite

- Falhas de contraste próprias confirmadas são removidas nas cinco páginas.
- Auditoria automática de Acessibilidade chega a 100 nas condições do spec; novas falhas próprias reveladas pelo baseline são corrigidas dentro do escopo, ou explicitamente submetidas a decisão se exigirem expansão.
- Comparação visual preserva hierarquia, composição e tipografia; foco e estados continuam perceptíveis. Verificar largura mobile estreita além dos dois perfis principais se a alteração afetar layout.
- Nenhuma regressão em hero, navegação, formulário ou interações; nenhuma alteração nos analytics.

## Verificação

Rodar axe/Lighthouse no candidato e inspecionar os estados que a navegação inicial não alcança. Revisar screenshots após o carregamento das fontes e a estabilização das animações.

## Comments

- 2026-10-24: escopo e permissão visual confirmados pelo usuário em Q1–Q2; implementação ainda não iniciada.
- 2026-10-24: spec confirmado em Q6; executar após concluir 01.
- 2026-10-24 (Claude): concluído no candidato local. O Lighthouse só via 5 nós porque as seções começam com `opacity: 0`; no estado final todos os consumidores de `--text-secondary`/`--text-muted` (4,12–4,16:1) e `--text-ghost` (1,74:1) reprovavam na home e nos 3 cases (Convênios já passava). Alteração única em `assets/css/tokens.css`: 0,45 → 0,58 e 0,20 → 0,52 (≥ 4,82:1 em todas as superfícies, hovers e tintas). axe 4.14 no estado final: 0 violações em 5 páginas × 3 larguras × 3 estados; Acessibilidade 100 nas 10 células do candidato. Capturas antes/depois sem mudança de composição/tipografia. Evidência: [contrast.md](../evidence/contrast.md). Pendente: confirmação em produção (06).
