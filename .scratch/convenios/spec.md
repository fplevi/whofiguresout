# CASSI Convênios — revisão pontual da narrativa visual

Status: resolved
Data: 2026-10-24
Checkpoint de testes: proposta de uma única interface de teste na página renderizada, confirmada pelo usuário nesta conversa com “yes”. A divisão em tickets depende de seu próprio checkpoint antes da publicação.

## Problem Statement

Quem lê o estudo de caso CASSI Convênios encontra uma apresentação concisa do produto, mas ainda não consegue relacionar todas as decisões às evidências com clareza. A rede credenciada disponível não aparece, a linha de contas omite a alternância sem logout e mistura funções que sua imagem não demonstra, e a documentação da biblioteca fica pequena e depende de abrir uma imagem crua para ser examinada.

A leitura precisa melhorar em telas estreitas sem substituir as linhas de funcionalidades que já funcionam, descaracterizar o produto ou transformar objetivos e relatos históricos em resultados comprovados.

## Solution

Fazer uma revisão pontual do corpo do case, preservando sua estrutura e identidade. Manter a home no hero e o cartão com suas ações; acrescentar a rede credenciada em uma linha própria junto dos serviços; explicitar contas sem logout; apresentar por último a biblioteca própria em um recorte legível dos estados e áreas de toque de botões.

Cada evidência terá explicação própria antes da imagem na ordem de leitura. Alternância lateral será usada quando ajudar a leitura, combinada com largura maior para documentação densa. Todo o conteúdo necessário ficará visível no corpo, com copy inglesa factual e sem link para imagem crua.

## User Stories

1. As a portfolio reader, I want the existing case structure to remain recognizable, so that I can follow the product story without unnecessary restructuring.
2. As a portfolio reader, I want the home screen to remain in the hero, so that I can recognize the app and its core services at the start of the case.
3. As a portfolio reader, I want the digital card evidence to retain its own explanation, so that I understand the view, copy and share actions it shows.
4. As a portfolio reader, I want to see provider-network evidence beside the discussion of services, so that I can connect that capability to the app's purpose.
5. As a portfolio reader, I want the network explanation to distinguish map results and the list-view alternative, so that I understand what the image actually supports.
6. As a portfolio reader, I want the provider network described as available without an unsupported launch date, so that I receive an accurate account of delivery.
7. As a portfolio reader, I want account switching without logout stated clearly, so that I understand the confirmed interaction beyond the appearance of saved profiles.
8. As a portfolio reader, I want the account image discussed on its own terms, so that notifications, authorizations and statements are not attributed to an unrelated screen.
9. As a portfolio reader, I want documented facts separated from unknown historical motivations, so that I can assess the case without invented explanations of the author's contribution.
10. As a portfolio reader, I want the component-library evidence to appear last among the feature evidence, so that the case progresses from product capabilities to its own design foundation.
11. As a portfolio reader, I want button states and touch-area documentation to be legible within the page, so that I can understand the design evidence without opening a raw image.
12. As a portfolio reader, I want enough surrounding context retained in each crop, so that I can identify the interface or documentation being explained.
13. As a portfolio reader, I want the library identified as belonging to a product that predates Harmony, so that I do not infer that the app was built on that design system.
14. As a portfolio reader, I want the conclusion to describe concrete delivery without unsupported efficiency claims, so that I can distinguish an available product and documented library from measured impact.
15. As a mobile reader, I want each explanation before its image, so that I know what to look for before examining the evidence.
16. As a portfolio reader, I want one image asset per narrative row with its own explanation, so that I can connect each visual to a specific argument.
17. As a portfolio reader, I want dense documentation to receive enough width, so that the page does not compress the evidence into an unreadable thumbnail.
18. As a portfolio reader, I want explanatory text with readable contrast and adequate type size, so that I can follow the narrative comfortably.
19. As a portfolio reader, I want loaded, proportional images without overlapping content or horizontal overflow, so that the presentation remains usable across screen sizes.
20. As a reader using assistive technology, I want meaningful image alternatives and a coherent reading order, so that the narrative remains understandable beyond the visual layout.
21. As a keyboard user, I want relevant navigation and store links to remain operable with visible focus, so that I can continue my visit through the portfolio.
22. As a reader scrolling on a small screen, I want every section to become visible during ordinary scrolling, so that tall sections do not disappear from the story.
23. As a reader who prefers reduced motion, I want the same content available immediately without entrance movement, so that the narrative respects my preference.
24. As a portfolio reader, I want the existing hero, navigation and contact experience preserved, so that this focused revision does not disrupt the rest of my visit.
25. As a portfolio maintainer, I want derived images documented and originals preserved, so that future editorial changes remain traceable and reversible.

## Implementation Decisions

- Modify only the case's narrative rows, their specific presentation and the conclusion where needed for factual coherence. Preserve the problem and role narrative outside that scope; do not expand the leadership or process investigation.
- Preserve the home mockup in the hero and the existing home card. The typographic cover remains unused. Preserve the digital-card row and the actions it demonstrates; its existing composite mockup is one asset, not a gallery of independent images.
- Add one provider-network row alongside access to services, after the card and before accounts. Use the existing network mockup as the source, with a presentation crop that makes better use of its transparent margins while retaining useful context.
- Explain results on a map and the available list-view alternative. Availability is already confirmed by the author; the old pending status is historical. Do not claim automatic geolocation, sorting by distance, a tested live service, or inclusion in the initial launch.
- Keep the account row and explicitly describe switching between accounts without logout, supported by the recorded author confirmation and Behance material. Do not invent the motivating requirement, an alternative considered, or Felipe's specific historical contribution to that choice.
- Remove unrelated notifications, authorizations and statements from the account explanation. Do not add replacement process material or broaden claims about delivery of those functions. The digital-card image does not demonstrate biometric login; do not use it as visual proof of that capability.
- Keep the library as the last feature evidence. Use a focused, legible crop of button documentation showing states and touch areas, with enough context to understand the example. Give dense documentation adequate width rather than retaining a height constraint that makes it unreadable.
- State that CASSI Convênios predates Harmony and uses its own component library and visual language. Do not imply construction on Harmony, migration to it, or later reuse of components. Preserve the product's own identity.
- Align the conclusion with concrete delivery and the documented product library. Remove or qualify the unsubstantiated assertion of reduced rework so that it is not presented as demonstrated impact; do not introduce metrics, certification, or expanded efficiency claims. Clarify any ambiguous shared-foundation wording as referring to this product's library.
- Use one image asset per row and an explanation specific to that evidence. Preserve functioning rows; apply lateral alternation only where it improves rhythm without compromising legibility, and use a wider block for dense documentation. Do not reproduce Billing's section architecture mechanically.
- Put the explanation before the image in the DOM and mobile layout. Use strong, readable explanatory text, consistent with the existing higher-contrast secondary text. Resolve wrapping and legibility structurally, without reducing fonts.
- Keep evidence and explanations visible in the page. Remove the library's raw-image link; do not replace it with a gallery, accordion, modal or interaction whose purpose is to hide essential content. Do not add extra section labels.
- Preserve original images. Derivatives must retain transparency where present and preserve proportions and relevant context. Choose a suitable transparent format rather than imposing JPEG. Existing equivalent PNG/WebP pairs are alternate encodings, not additional evidence.
- Record each derived image's source, crop bounds, output dimensions, format and editorial purpose in a case-specific manifest; state any use of an unchanged source. Include intrinsic dimensions and meaningful alternative text; preserve appropriate loading priority for the hero and lazy/asynchronous loading for body evidence.
- Keep styles specific to Convênios. Shared styles or scripts may change only with demonstrated necessity and regression validation of every affected page. Preserve simultaneous edits in the shared checkout.
- Preserve navigation, store destinations, contact behavior, existing metadata and analytics. Respect the accepted decision to preserve Clarity/GA4 continuity across the portfolio visit; analytics optimization is outside this revision.

## Testing Decisions

- Approved interface: the rendered case page and externally observable browser behavior. Prefer this single, high-level interface over new internal unit-test seams or assertions tied to class names, CSS implementation or observer configuration.
- Good checks demonstrate what a reader can see, understand and operate. Combine browser assertions with visual inspection; image loading or a color token alone does not establish legibility or adequate contrast.
- Reuse and adapt the existing Billing visual-narrative QA approach and the previous Convênios validation as prior art. Reuse viewport captures, image readiness checks, reading-order and overflow checks, real scrolling and preserved-surface checks; do not inherit Billing-specific counts, classes, flow controls or exact alternation patterns.
- Validate 320, 375, 768 and 1440 px with both normal and reduced motion. Check explanation/image order, readable text and evidence, appropriate wide documentation, no overlaps, no horizontal overflow, and proportional rendering of every loaded image.
- Verify the intended evidence sequence: home in the hero; card, network, accounts and own-library evidence in the body, each with its explanation. Check that no raw-image link or content-hiding interaction remains.
- Review English copy against confirmed evidence: map/list without geolocation or distance-order claims; available network without a launch-date claim; accounts without logout without invented authorship; library before Harmony without migration/reuse claims; no demonstrated efficiency or accessibility certification implied by the documentation.
- Scroll from the top through the full page with ordinary wheel or equivalent input in normal motion at every target width. Verify that all sections actually become visible, including the tallest mobile section. A scroll-into-view shortcut or a calculated observer threshold alone is insufficient. With reduced motion, content must be available immediately.
- Check image readiness before capture using successful loading and nonzero intrinsic dimensions. Use element or viewport evidence where full-page captures produce lazy-loading artifacts. Inspect the actual captures; automation alone cannot approve crop quality or tiny interface text.
- Check explanatory contrast, meaningful alternatives, heading/reading order and relevant keyboard navigation with visible focus. Reuse accessibility auditing where available and distinguish automated findings from manual inspection; do not claim a screen-reader audit unless one is performed.
- Confirm the preserved portfolio visit through the home card, return to Work and adjacent-case links, plus navigation and store destinations. Check contact's preserved presence and keyboard access without submitting the form. Distinguish link preservation from live app/store or production-service validation.
- Compare originals and derived assets and inspect the manifest as supporting artifact checks, without introducing another runtime interface. Confirm transparency, traceability, preserved context and no duplicated evidence from equivalent encodings.
- If shared presentation or behavior must change, demonstrate the reason and validate all affected pages in addition to Convênios. Otherwise keep regression scope on the case and its immediate navigation surfaces.
- Record actual execution results, captures, environment and limitations separately from acceptance criteria. Historical validation is prior art, not proof that this revision passes. No browser tests, crops or implementation were performed while producing this spec.

## Out of Scope

- Rebuilding the case to match Billing, changing the hero or home card, using the typographic cover, or changing unrelated narrative, navigation, contact or other cases.
- Adding process canvases, interviewing again about account motivation or authorship, investigating efficiency, or rechecking whether the network is available.
- Building live app features, reproducing an interactive account switcher or provider map, or verifying the app, stores and services in production.
- Adding raw-image links, paired-image galleries, unnecessary interactive disclosure or additional labels.
- Claiming a launch date for the network, automatic geolocation, distance sorting, new measured results, accessibility certification, or a Harmony migration/reuse relationship.
- Refactoring shared presentation without necessity, changing analytics, installing a new test architecture, or editing glossary/ADRs without a new domain or architectural decision.
- Executing tickets, editing HTML/CSS/JavaScript, generating crops during this specification conversation, closing existing issues, commits, PRs or deployment.

## Further Notes

- The completed visual-narrative review is the final interview source; Q3, Q7 and Q8 were approved. Later author clarifications in the Behance analysis supersede the historical pending-network wording in the original editorial draft and Notion source.
- The factual research establishes the inspected image content and encoding equivalence. It does not validate rendered pages, MP4s or production services. The previous validation describes an older version and does not establish current results.
- Billing's later validation and user comments supersede its original expandable-flow and full-size-image-link proposals. Its applicable reference is clarity, visible content and responsive evidence, adapted to this case.
- No existing Convênios spec or issue directory was present when this spec was created. Existing sources and validation records remain preserved. Ticket publication will follow the separate confirmation of granularity and genuine blocking edges required by the tickets skill.

## Comments

- 2026-10-24: após a confirmação da interface de teste, o usuário aprovou com “Sim” a divisão em três tickets: rede credenciada junto dos serviços; alternância de contas sem logout; biblioteca própria legível e fechamento. Todos sem bloqueadores, pois cada entrega é demonstrável independentemente, incluindo sua própria validação. Tickets publicados com status ready-for-agent. A aprovação trata da especificação e da divisão; não foram executados tickets, implementação, recortes ou testes de navegador nesta conversa.

- 2026-10-24: Implementa??o conclu?da na branch `integration/convenios-visual-narrative`; tickets 01, 02 e 03 resolvidos ap?s integra??o e revis?o. Matriz conjunta 104/104, suporte/axe/assets 40/40, corre??o de padr?es 45/45. [Valida??o final](final-validation.md), [revis?o](code-review.md), [manifesto](asset-manifest.md). Sem PR ou deploy; checkout principal e trabalhos simult?neos preservados.
