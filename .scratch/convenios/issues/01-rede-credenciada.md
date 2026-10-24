# 01: Apresentar a rede credenciada junto dos serviços

**What to build:** quem lê o estudo de caso CASSI Convênios encontra a rede credenciada em uma linha própria junto do acesso aos serviços, depois do cartão e antes de contas, com explicação inglesa factual de resultados no mapa e alternativa de lista. O mockup ganha um recorte de apresentação legível, mantendo transparência e contexto. Home e cartão permanecem preservados.

**Blocked by:** None (can start immediately).

**Status:** claimed

- [x] A rede possui título e explicação próprios, uma imagem na linha e posição depois do cartão e antes de contas. As linhas existentes que funcionam são preservadas, sem reconstruir a arquitetura do case para imitar Billing.
- [x] A copy descreve a função como disponível, conforme confirmação já registrada do autor, sem repetir o status pendente histórico nem afirmar que participou do lançamento inicial. Descreve resultados no mapa e alternativa de lista, sem alegar geolocalização automática, ordenação por distância ou verificação do serviço em produção.
- [x] O derivado do mockup de rede aproveita melhor as margens transparentes, preserva a transparência, a proporção e o contexto necessário para reconhecer os resultados e a alternativa de lista. O original fica intacto; não se impõe JPEG.
- [x] O manifesto do case registra fonte, limites do recorte, dimensões, formato e motivo editorial do derivado, preservando entradas anteriores. Pares PNG/WebP equivalentes não são apresentados como novas evidências.
- [x] A explicação antecede a imagem no DOM e no mobile, com contraste legível. A composição lateral só é usada se mantiver leitura adequada; quebras são resolvidas por composição, sem reduzir fontes. A linha não acrescenta etiquetas extras, link de imagem crua, galeria ou interação para esconder conteúdo.
- [x] A imagem carrega, mantém proporção e dimensões intrínsecas, tem alternativa textual específica e carregamento apropriado para evidência no corpo. O mapa é apresentado como evidência estática, sem simular busca ou navegação do aplicativo.
- [x] A página renderizada é verificada em 320, 375, 768 e 1440 px com movimento normal e reduzido, reaproveitando o QA existente. Inspeção visual confirma legibilidade, ordem da explicação, ausência de sobreposição e overflow horizontal; capturas aguardam o carregamento real das imagens.
- [x] Rolagem real desde o topo, por roda ou entrada equivalente, confirma que todas as seções se tornam visíveis nas quatro larguras com movimento normal, incluindo a seção de funcionalidades mais alta. Com movimento reduzido, o conteúdo está imediatamente disponível. Saltar para elementos não substitui essa verificação.
- [x] São conferidos o percurso pela home até o case, retorno a Work, navegação adjacente, destinos das lojas e acesso por teclado com foco visível nos links relevantes. Hero, home card, cartão, contato, metadados e analytics permanecem preservados; o formulário não é enviado.
- [x] Estilos permanecem próprios do case. Qualquer necessidade comprovada de alterar apresentação ou comportamento compartilhados é registrada e acompanhada de validação das páginas afetadas. Alterações simultâneas e conteúdo fora do escopo são preservados.
- [x] Resultados reais, capturas, ambiente e limites da validação são registrados separadamente dos critérios de aceite, sem apresentar a validação histórica ou a inspeção dos assets como teste desta revisão.


## Comments

- 2026-10-24: implementação do ticket 01 concluída no worktree isolado. RED 44/16 e GREEN 109/0 na seam de página renderizada; matriz completa, roda normal e preservação de navegação/foco. Evidências e limites em [01-validation.md](../01-validation.md); asset em [01-network.json](../assets/01-network.json). Status mantido claimed para revisão final da integração.
