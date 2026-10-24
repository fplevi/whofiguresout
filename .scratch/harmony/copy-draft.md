# Harmony: revisão editorial

Status: entendimento confirmado pelas respostas a Q1–Q4 e pela instrução de atualizar o card da home em 2026-10-24; revisão aplicada e validada.

## Direção aprovada

- O resultado central é a adoção do Harmony nos novos projetos, a migração gradual dos legados e a evolução contínua com desenvolvimento.
- Remover promessas de velocidade sem medição confiável. A maior adoção de IA ocorreu junto da adoção do Harmony, impedindo atribuir a aceleração exclusivamente ao design system.
- Não substituir percentuais por promessas vagas de aceleração ou por “impacto imensurável”. Descrever os resultados observáveis relatados pelo usuário.
- Incluir uma seção curta sobre bibliotecas e skills para prototipação funcional em HTML/CSS/JS, em construção, voltadas à validação com usuários.
- Apresentar a conversão desses protótipos para componentes React do Harmony como uma iniciativa em estudo e desenvolvimento, sem afirmar capacidade entregue ou conversão automática validada.
- Felipe lidera o design e a evolução dos componentes; o time de desenvolvimento implementa a biblioteca React em parceria com ele.
- Retirar o prazo de três meses do destaque e apresentar o sistema como uma iniciativa em evolução contínua.
- Atualizar também o texto do card da home, conforme reforçado pelo usuário.

## Texto aplicado em inglês

Mantidos o idioma e o sistema visual atuais, os assets, a navegação, o contato e as alterações simultâneas existentes. Os textos abaixo substituem os trechos correspondentes; o bloco de estatísticas deu lugar a texto de adoção, e uma seção curta de trabalho em andamento encerra o conteúdo do case. Validação registrada em `validation.md`.

### Home card

Title: Harmony

Tag: Design System

Hook: A shared design system for CASSI's new projects, with existing products migrating gradually.

Highlight: Adopted

Supporting text: in new projects

### Metadados

Meta description: Harmony — Design System case study by Felipe Levi. A shared foundation for new projects at CASSI, with gradual migration of existing products and ongoing component development.

OG description: A shared foundation for new projects at CASSI, with gradual migration of existing products and ongoing component development.

Manter título da página, OG title, imagem, URL e Twitter card existentes.

### Case header

Title: Harmony

Hook: A shared design system for CASSI's new projects, with existing products migrating gradually.

Role: Design Lead

Timeline: Ongoing evolution

Outcome: Adopted in new projects

### The Problem

Title: Separate libraries. Repeated decisions.

CASSI's five platforms had separate Figma libraries and no shared governance. That fragmentation showed up in everyday design work:

- Library updates had to be maintained separately across five platforms.
- Tokens and patterns diverged as each library followed a different update cycle.
- Teams revisited component decisions and repeated design work across products.

### My Role

Title: Leading design, working with development.

I led the design of Harmony, from organizational alignment and governance to components, tokens, and variables. The development team implements the React library in partnership with me. I continue to evolve existing components and design new ones, working with the team to keep the system up to date.

### The Decisions

Title: Building a shared foundation.

Decision 01: One shared library

We chose a unified library rather than maintaining separate foundations for each platform. Shared governance and defined exceptions gave the team a common reference for component decisions, while allowing the system to evolve with product needs.

Note below the paragraph, with a components icon: One shared reference for component decisions.

Decision 02: React + Next.js for the product ecosystem

React and Next.js were chosen with long-term maintenance and hiring in mind. The intent was to give development a shared technical foundation as new projects adopt Harmony and existing products migrate.

Note below the paragraph, with a maintenance icon: Long-term maintenance guided the technology choice.

Decision 03: Accessibility and content in component design

Accessibility and content guidance were included in component design alongside visual tokens and interaction states. Contrast, component semantics, and error messages needed to be considered together, with design and development addressing their respective parts.

Note below the paragraph, with an accessibility icon: Accessibility and content are ongoing component requirements.

### What Shipped

Title: A shared library, with adoption in progress.

Before image caption: Before Harmony: separate Figma libraries across CASSI's platforms.

After image caption: With Harmony: a shared Figma library supporting new projects and the gradual migration of existing products.

### The Outcome

Title: Adopted in new projects. Evolving with the team.

Harmony is now the foundation for new projects at CASSI. Existing products are being migrated gradually, so adoption across the ecosystem remains an ongoing effort.

The work continues through updates to existing components and the design and implementation of new ones. I work with the development team to keep the system aligned as it evolves.

### Work in Progress

Title: Prototyping with AI, exploring the path to React.

I am working with the development team to explore AI-assisted process automation. We are building libraries and skills to support functional HTML, CSS, and JavaScript prototypes for user validation.

We are also developing and evaluating a way to translate those prototypes into Harmony's React components. This work is still in development.

## Entendimento confirmado

Não restam perguntas editoriais abertas após as respostas a Q1–Q4. As confirmações e a instrução adicional de trocar o texto do card da home autorizam a revisão do case e de suas referências. O reforço sobre a home integra o escopo e não reinicia a entrevista.

## Superfícies da revisão

- `case-studies/harmony.html`: cabeçalho, papel, decisões, legendas, resultados e nova seção de trabalho em andamento.
- `index.html`: remover “50% / faster delivery” do card Harmony e alinhar seu resumo à narrativa aprovada.
- `portfolio-dev-plan.md`: atualizar o resumo correspondente para evitar reintroduzir a métrica.
- Rever “zero inconsistencies”, “zero retrofit cost”, “16w → 8w” e afirmações de migração completa como parte da remoção de resultados não sustentados.

## Registro

- 2026-10-24: usuário aprovou adoção e evolução contínua como foco do case (Q1).
- 2026-10-24: usuário aprovou a inclusão do trabalho de prototipação e conversão com seus estágios explícitos (Q2).
- 2026-10-24: usuário confirmou a divisão entre liderança de design e implementação React pelo time em parceria com Felipe (Q3).
- 2026-10-24: usuário aprovou retirar o prazo do destaque e apresentar evolução contínua (Q4).
- 2026-10-24: usuário reforçou que o texto do card da home também deve mudar.
- 2026-10-24: a pedido do usuário, o card lateral de contexto virou três bullets explicativos abaixo da introdução. Os resumos laterais redundantes das decisões foram removidos, com os parágrafos organizados em uma coluna de leitura.
- 2026-10-24: usuário pediu as três mensagens das antigas tags abaixo de cada decisão, acompanhadas de ícones. As mensagens foram reinseridas como notas simples com ícones de componentes, manutenção e acessibilidade, sem formato de pílula.
- A apuração do repositório encontrou as afirmações existentes, mas não documentação de medição ou evidência independente dos resultados. Os fatos sobre adoção e trabalho atual vêm do relato do usuário.
