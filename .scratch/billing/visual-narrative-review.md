# Billing — revisão da narrativa visual

Data: 2026-10-24.
Estado: investigação concluída; direção aprovada pelo usuário, com substituição do fluxograma estático por componente interativo. Spec e tickets em [spec.md](spec.md). Página e estilos não alterados nesta rodada.

## Evidência

Inspeção visual dos assets estáticos, do GIF e da página atual. A skill `grilling` solicitou investigação por subagente; a inspeção delegada foi concluída e confrontada com HTML, CSS e capturas locais da página.

O par atual de “What Shipped” é um fluxograma e um dashboard. A legenda do fluxograma o descreve incorretamente como telas do participante. As três decisões atuais não têm imagens estáticas associadas. O texto orientativo atual tem contraste visual baixo.

## Inventário e encaixe proposto

- `billing-digital-platform-flow.jpg`: fluxograma da jornada. Fonte das oito etapas do componente interativo junto da decisão 01; o usuário pediu substituir a imagem por esse componente. Não demonstra permissões por perfil.
- `MFA.png`: seleção de e-mail ou SMS para receber código. Associar à decisão 02. A captura não resolve a classificação técnica de autenticação.
- `tela-inicial.png`: escolha entre regularizar a dívida e negociar com reativação. Associar à decisão 03.
- `oferta-reativação.png`: detalhes e condições da oferta, com opção de seguir sem reativação. Abrir o detalhamento da entrega.
- `pagamento-a-vista.png`: pagamento único no exemplo com reativação. Explicar condições e total antes de avançar.
- `pagamento-parcelado.png`: entrada opcional e quantidade de parcelas no exemplo sem reativação. Dar linha e explicação próprias.
- `resumo.png`: revisão da proposta e código para validar a negociação. Não é comprovante de pagamento ou tela de sucesso.
- `3-boletos.png`: acompanhamento de boletos pendentes e geração de documentos. O trecho inferior sobre contribuição trabalhista não é necessário para esse argumento.
- `tela.png`: detalhe de negociação aprovada e parcelas por situação. Sobrepõe parte do acompanhamento; propõe-se omitir nesta versão.
- `billing-digital-platform-dashboard.jpg`: acompanhamento operacional de negociações, valores e reativações. Linha própria antes dos resultados. A imagem não comprova atualização em tempo real.
- Pares JPG/PNG do fluxograma e dashboard repetem o conteúdo e não precisam aparecer duas vezes.
- `digital-billing-platform.gif`: abertura visual; não substitui a explicação das etapas nas imagens estáticas.

## Proposta de composição

Alternar texto e imagem nas laterais em blocos simples, intercalando telas densas em largura maior, com texto acima. Cada imagem terá explicação própria em inglês, acompanhando o idioma atual do case. No mobile, explicação antes da imagem.

O fluxo interativo substitui a imagem do fluxograma e acompanha a primeira decisão. O dashboard encerra a entrega operacional. A seleção aprovada contempla sete das oito novas imagens, omitindo `tela.png` pela sobreposição com acompanhamento.

## Limites editoriais

As capturas mostram cenários e valores distintos: pagamento à vista está associado à reativação e parcelado está sem reativação. Não narrar como uma única negociação contínua. Oferta, validação, aprovação, boleto pendente e pagamento realizado representam estados diferentes.

Manter as distinções documentadas em `factual-questions.md`: cinco minutos é meta, os resultados são históricos e as imagens não validam novas métricas. As telas sustentam descrições do que é visível; não acrescentar causalidade ou garantias de desempenho.

Todas as novas capturas medem 1920 × 1200. Em meia largura, controles e valores pequenos perdem legibilidade. Recortes de apresentação para reduzir cabeçalhos e rodapés repetidos foram aprovados, preservando contexto e originais.

## Decisões confirmadas

1. Seleção de sete novas telas e omissão de `tela.png` aprovada. A primeira imagem, o fluxograma, será redesenhada como componentes interativos.
2. Ritmo misto aprovado: alternância lateral com pausas em largura maior.
3. Recortes de apresentação aprovados, preservando conteúdo relevante e imagens originais.
4. Usuário confirmou entendimento e pediu specs e tickets para executar no Claude Code, sem implementar nesta sessão. A mecânica concreta do fluxo foi definida no spec como proposta técnica de etapas expansíveis.

Não há decisão arquitetural difícil de reverter que justifique ADR. Nenhum termo novo foi consensuado para inclusão no glossário nesta rodada.

## Navegador

O preview T3 abriu a página, mas duas capturas falharam com `Preview automation snapshot timed out after 15000ms.` A inspeção visual da página atual usou Playwright Python já disponível no ambiente, com capturas em `editorial-current-decisions.png` e `editorial-current-shipped.png`.
