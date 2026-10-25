# 04 — Otimizar recursos próprios somente com ganho demonstrado

Status: resolved
Type: task
Blocked by: 01
Executor: Claude

## Contexto

Performance já é 100 no anexo desktop. Há fontes por `@import` em `assets/css/global.css:1`, oito folhas CSS na home e reflow de 11,633 ms atribuído ao parallax em `assets/js/scroll-animations.js:87`. Esses diagnósticos não subtraem pontos diretamente. Os 71 KiB de JS não utilizado pertencem ao GA4 e não justificam sua remoção. Leia o [spec](../spec.md).

## Trabalho

- Usar o baseline de cada página/perfil para escolher se há problema próprio relevante a corrigir. Registrar a decisão mesmo que nenhuma alteração adicional se justifique.
- Priorizar a avaliação de substituir a descoberta tardia das fontes via `@import` por carregamento direto adequado no head das cinco páginas. Preservar famílias, pesos, estilos, fallback e licenças; não adicionar preload indiscriminado.
- Investigar o parallax em scroll real antes de alterar: ordenar leituras/escritas ou reduzir trabalho apenas se o perfil confirmar custo relevante. Preservar aparência, responsividade e reduced motion; não remover o efeito apenas para limpar aviso.
- Checar cache/compressão de documentos e assets em produção com requisições GET e negociação de encoding. Separar headers do servidor local, do GitHub Pages e dos fornecedores. Não criar configuração de headers ignorada pelo host.
- Comparar antes/depois sob as mesmas condições; manter apenas mudanças com ganho ou eliminação comprovada do problema próprio sem regressão. Registrar uma decisão de não alterar quando apropriado em `../evidence/resources.md`.
- Não introduzir framework/build obrigatório, migrar hospedagem, reescrever bibliotecas externas, remover GA4/Clarity ou endurecer políticas de segurança incidentalmente.

## Aceite

- Cada alteração retida tem evidência de problema e resultado, identificando ambiente/revisão.
- Mesma tipografia e comportamento; sem fonte, imagem, CSS ou script quebrado nas cinco páginas.
- Performance e estabilidade visual não apresentam regressão reproduzível; custos de terceiros não são apresentados como código próprio corrigido.
- Limitações do host/fornecedor ficam documentadas, sem promessa de zero avisos.

## Verificação

Inspecionar waterfall de fontes e perfil de scroll afetado, executar Lighthouse comparável e revisar capturas. Não ampliar a bateria depois de resultados suficientes sem mudança, falha ou dúvida nova.

## Comments

- 2026-10-24: otimizações condicionadas a evidência; este ticket pode concluir com justificativa de nenhuma mudança necessária.
- 2026-10-24: spec confirmado em Q6; executar após concluir 01.
- 2026-10-24 (Claude): concluído no candidato local, com evidência antes/depois para cada alteração retida: (1) GIFs de topo → MP4 + pôster (−91 % de bytes, SSIM 0,99; LCP desktop dos cases ~20–30 s → ~0,6 s); (2) Google Fonts auto-hospedadas com preload de 2 arquivos — elimina um atraso intermitente de ~1 s no 1º quadro apresentado (reproduzido em 50–75 % das execuções, isolado nas fontes do Google), paridade de pixels 0 diferença; (3) favicon declarado (`errors-in-console`); (4) altura do hero reservada (CLS 0,007–0,030 → 0); (5) `lazy` + dimensões em 4 imagens abaixo da dobra. Parallax, GA4, cache/compressão do Pages avaliados sem alteração. Resultado local: desktop 100 em todas; mobile home 99, cases 97, Convênios 91. Evidência: [resources.md](../evidence/resources.md), [candidate.md](../evidence/candidate.md).
- 2026-10-24 (Claude): revisão após as mudanças do usuário (HEAD `7b29db8`): otimizações anteriores preservadas; GIFs/vídeos de topo substituídos pelo caça-palavras. Corrigido CLS do caça-palavras (até 0,084 no mobile) só em CSS; levantado ganho potencial de 4,4 MB → ~1,2 MB convertendo imagens para AVIF/WebP com `srcset`, pendente de decisão. Evidência: [current/review.md](../evidence/current/review.md).
- 2026-10-24 (Claude): rodada 2 — grade do caça-palavras com tamanho definido só no CSS (JS lê o valor resolvido; override por case sem shift), imagens convertidas para AVIF/WebP responsivos (4,48 MB → 0,82 MB servidos, layout inalterado), protótipo removido a pedido do usuário. Bateria existente + nova passou; Lighthouse local final: desktop 100, mobile 96–99. Evidência: [current/review.md](../evidence/current/review.md#rodada-2--robustez-do-caça-palavras-imagens-protótipo-removido).
- 2026-10-25: fechado a pedido do usuário após a validação em produção (ticket 06).
