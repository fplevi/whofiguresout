# 02 — Preparar as sete telas para leitura editorial

Status: resolved
Type: task
Dependências: 01 concluído, para manter execução sequencial
Spec: [../spec.md](../spec.md)

## Entrega

Inspecionar as sete capturas selecionadas e o dashboard. Preparar recortes ou derivados onde melhorem a leitura, preservando os originais. Registrar cada escolha em `.scratch/billing/image-manifest.md`.

## Passos

1. Ler “Imagens e textos orientativos” e “Precisão editorial” do spec; conferir visualmente as imagens antes de recortar.
2. Reduzir áreas repetidas de cabeçalho/rodapé quando necessário, preservando o contexto da funcionalidade.
3. Em `3-boletos.png`, focar o acompanhamento de boletos, sem trazer contribuição trabalhista para o argumento.
4. Salvar derivados necessários em `assets/images/billing/editorial/`, com nomes descritivos. Escolher a versão do dashboard que equilibre legibilidade e peso.
5. Registrar no manifesto: original, derivado ou uso integral, dimensões, coordenadas do recorte quando houver, motivo e ponto de integração.

## Aceite

- Manifesto contempla as sete capturas e o dashboard; uso integral também é registrado.
- Originais permanecem intactos e derivados não distorcem conteúdo.
- Seleção de canal, condições de reativação, campos de pagamento, totais, vencimentos, validação e ações de boletos continuam visíveis onde relevantes.
- O recorte não transforma exemplos de cenários diferentes em uma comparação de valores equivalentes.
- `tela.png` fica fora da seleção; versões JPG/PNG equivalentes não aparecem duplicadas.

## Comments

- 2026-10-24: usuário aprovou recortes de apresentação, preservando originais e contexto das telas.
- 2026-10-24 (Claude Code): 7 recortes em `assets/images/billing/editorial/` (JPEG q86, sem redimensionar; 2–4× menores que PNG equivalente). Dashboard usado integralmente em JPG (64 KB vs 212 KB do PNG). `MFA.png` recortado no cartão de identificação, com link para o original; `3-boletos.png` limitado aos boletos, sem contribuição trabalhista. `tela.png` fora da seleção. Detalhes no [manifesto](../image-manifest.md).
- Concluído em: 2026-10-24
