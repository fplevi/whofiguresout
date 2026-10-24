# Validação da revisão do Harmony

Data: 2026-10-24.

Escopo: decisões Q1–Q4 e instrução adicional de atualizar o card da home, registradas em `copy-draft.md`.

## Conteúdo

- Case e card da home destacam adoção nos novos projetos e migração gradual dos produtos existentes.
- Removidos os percentuais de velocidade, a comparação de 16 para 8 semanas, o prazo de três meses e as promessas de inconsistências/custo de adaptação iguais a zero.
- Distinção explícita entre a liderança de design de Felipe e a implementação React pelo time de desenvolvimento em parceria com ele.
- Nova seção apresenta automação com IA, bibliotecas e skills para prototipação HTML/CSS/JS e conversão para componentes React como trabalho em desenvolvimento.
- Descrições meta e Open Graph do case e resumo do Harmony em `portfolio-dev-plan.md` acompanham a revisão.
- `GLOSSARY.md` registra Harmony como um design system em evolução contínua.

## Verificação no navegador

- Home e case conferidos no Chromium em 375, 768 e 1440 px: seis combinações de rota e largura.
- Nenhum transbordamento horizontal nas páginas ou no card Harmony.
- Nenhuma imagem quebrada ou erro de execução JavaScript observado.
- Ausência das antigas alegações verificada no conteúdo renderizado do case.
- Capturas de desktop e mobile inspecionadas para o card, cabeçalho, resultado e trabalho em andamento.
- Espaçamento de 24 px entre os novos parágrafos consecutivos, usando o token existente em `case-study.css`.

## Ambiente e limites

Site servido pelo servidor local existente na porta 8000. O preview colaborativo abriu e permitiu inspecionar o conteúdo, mas a captura retornou duas vezes `Preview automation snapshot timed out after 15000ms.` A conferência visual foi concluída com o Playwright/Chromium já disponível no diretório temporário do sistema. Nenhuma dependência foi adicionada ao projeto.

Os fatos de adoção e estágio das iniciativas vêm do relato confirmado pelo usuário. Esta validação verifica o portfólio e sua apresentação, sem medir resultados empresariais do Harmony.

Alterações simultâneas preexistentes, incluindo as de contato e demais cases, foram preservadas. Nenhum commit ou deploy foi realizado nesta revisão.

## Ajuste de leitura solicitado após a revisão

- O card “Organizational Cost” foi substituído por uma lista semântica de três consequências concretas, imediatamente abaixo do parágrafo introdutório.
- As decisões passaram a uma coluna com largura máxima de 840 px. As pílulas laterais foram removidas porque repetiam o conteúdo já expresso nos parágrafos.
- Estilos novos restritos à lista e ao modificador `cs-decisions--stacked`; os layouts dos outros cases permanecem preservados.
- Preview colaborativo confirmou lista abaixo do texto e ausência de transbordamento em 375, 768 e 1440 px. Capturas de desktop foram inspecionadas; duas tentativas de captura mobile retornaram o mesmo timeout registrado acima.
- Conferência complementar no Chromium local: lista com marcadores visíveis, três itens, decisões em uma coluna e nenhum erro JavaScript em 375 e 1440 px. Capturas de mobile e desktop inspecionadas.
- Direção aplicada com a skill `design-taste-frontend`: evolução pontual do layout editorial existente, mantendo tipografia, paleta, imagens, navegação e movimento. Sem novas dependências ou animações.

## Notas com ícones abaixo das decisões

- Após nova orientação do usuário, as três mensagens das tags foram reinseridas como notas imediatamente abaixo do parágrafo de cada decisão, sem fundo, borda ou formato de pílula.
- Ícones oficiais Tabler: componentes para a referência compartilhada, ferramenta para manutenção e acessibilidade para os requisitos contínuos. SVGs locais com licença MIT e origem registrada em `assets/icons/tabler/README.md`.
- Ícones de 24 px usam a cor de destaque existente e são decorativos (`aria-hidden="true"`); a mensagem permanece como texto acessível.
- Conferido no Chromium local em 375 e 1440 px: três notas abaixo dos textos, sem transbordamento, seis respostas HTTP 200 dos ícones nas duas larguras e nenhum erro JavaScript. Capturas das três notas em mobile e da primeira em desktop inspecionadas.
- Preview colaborativo confirmou a estrutura, mas a captura mobile voltou a retornar o timeout já registrado. Conferência visual concluída pelo fallback local existente; nenhuma dependência de execução adicionada ao site.
