---
status: accepted
---

# A página para de crescer em 1920px

Em 2026-10-25, decidimos que o layout tem uma largura máxima de 1920px (`--frame-width`): até essa largura nada muda, e acima dela o `<main>` fica centralizado e só o fundo da página se estende. Assim, telas ultrawide (3440px, 5120px) não esticam o hero, a foto e as divisórias. A faixa da `.nav` continua ocupando a tela toda, mas o logo e os links se alinham às bordas do conteúdo dentro dos 1920px. Dentro do limite vale a estratégia híbrida: textos e colunas dos cases mantêm seus limites (840, 900 e 1440px), e só o hero, a foto e o nome do footer chegam a 1920px. Fundos e divisórias de seção param na borda dos 1920px.

O caça-palavras também é limitado pela altura: em telas mais largas do que altas, a largura de `.wsh__game` é calculada para que a grade, a nav e a linha de chips (`--wsh-reserve`) caibam numa tela só; no hero da home ele fica centralizado, e nos cases segue alinhado ao título. Imagens que ocupam a largura toda declaram `sizes="(max-width: 1920px) 100vw, 1920px"`. Elementos novos não devem usar `100vw` nem truques de full-bleed que escapem do `<main>`. O critério de validação é 1920×1080; larguras maiores só precisam provar que o limite se mantém.
