---
status: accepted
---

# Só controles interativos têm cantos arredondados

Em 2026-10-25, decidimos que apenas controles interativos — botões, campos de formulário, a cápsula e os chips do caça-palavras (`--radius-control`) e a alça do slider de comparação (`--radius-full`) — têm cantos arredondados. Todas as superfícies de conteúdo — imagens, vídeos, cards de métrica, blocos, tags e a moldura do minigame — usam `--radius-surface` (0), para uma apresentação de formas mais duras. Assim o arredondamento passa a sinalizar o que é clicável: uma pílula ao lado de um botão parecia interativa sem ser. Componentes novos de case devem usar `--radius-surface`, a menos que sejam controles; o valor das superfícies é um token só para que a forma possa ser reavaliada em uma linha.
