# Validação do case CASSI Convênios

Escopo aprovado: `copy-draft.md`. Fonte e arquivos baixados: `notion-source.md` e `notion-images.json`.

## Verificações

- Referências locais: 91 links, imagens, estilos, scripts e âncoras verificados nas cinco páginas HTML.
- Imagens: seis PNGs baixados e integridade validada. Quatro WebPs usados na página preservam dimensões, transparência e todos os pixels dos PNGs (`lossless=True, exact=True`).
- Navegação pelo navegador: quarto card da home → CASSI Convênios → Harmony; Enrollment → CASSI Convênios; retorno à seção Work.
- Layout: conferência visual e ausência de overflow horizontal em 375, 768 e 1440 px.
- Movimento reduzido: seções visíveis imediatamente.
- JavaScript: nenhum erro de execução nas rotas verificadas.

## Acessibilidade

Auditoria com axe-core 4.10.2, regras WCAG 2 A/AA e WCAG 2.1 AA. A primeira passagem completa identificou contraste insuficiente no subtítulo de contato; corrigido com token local ao novo case. O foco dos campos recebeu contorno visível local. A auditoria automática não substitui teste com leitor de tela.

Após os ajustes, zero violações nos três tamanhos. A ferramenta deixou o contraste do textarea como verificação manual por detecção de sobreposição. O placeholder usa o mesmo token dos demais campos: 60% de `#F2F2F5` sobre `#121528`, acima do mínimo de 4,5:1. Contorno de foco dos campos confirmado pelo navegador: sólido, 2px.

## Ambiente

Site estático servido por `python -m http.server`. Após dois timeouts de captura e inconsistência de viewport no preview colaborativo, a conferência responsiva usou Chromium com Playwright instalado apenas no diretório temporário do sistema. Nenhuma dependência foi adicionada ao projeto. Não foram executados Lighthouse, Firefox ou Safari.

## Escopo de Git

Alterações simultâneas de cópia de e-mail na área de contato pertencem a outro trabalho. Preservar esses arquivos e hunks na árvore de trabalho; não incluí-los no commit deste case.
