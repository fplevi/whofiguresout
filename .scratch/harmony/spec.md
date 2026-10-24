# Harmony — narrativa visual por camadas

Status: resolved

## Problem Statement

Quem lê o case Harmony encontra decisões sobre uma base compartilhada, manutenção e acessibilidade, mas a demonstração visual atual se limita a um par de imagens de organização de arquivos. Esse par não explica como fundamentos se relacionam com componentes, templates e documentação, e suas legendas podem sugerir uma ruptura histórica que os pixels não comprovam.

As novas evidências são pranchas densas de um design system. Exibi-las como miniaturas ou galeria deixaria a pessoa responsável por descobrir o argumento de cada imagem. No mobile, a organização precisa manter explicações legíveis e conteúdo alcançável durante a rolagem, inclusive quando as seções ficam altas.

## Solution

Apresentar Harmony como o design system da CASSI em evolução contínua, com uma progressão de leitura: fundamentos compartilhados → aplicação nos componentes → composição em templates → documentação e implementação em parceria com desenvolvimento. Essa ordem explica relações entre camadas; não afirma a cronologia histórica de construção do sistema.

Distribuir sete evidências, cada uma em uma linha própria com título e explicação em inglês antes da imagem no DOM e no mobile. Combinar alternância lateral no desktop com blocos largos para material denso. Integrar o sentido das decisões atuais a essas evidências, substituindo o par antes/depois e evitando uma apresentação paralela redundante.

## User Stories

1. As a portfolio reader, I want to understand Harmony as CASSI's shared design system, so that I can identify its role across products.
2. As a portfolio reader, I want to understand the problem of separate libraries and governance, so that the shared foundation has a clear purpose.
3. As a portfolio reader, I want the visual progression to explain relationships between layers, so that I do not mistake it for a historical timeline.
4. As a portfolio reader, I want to see examples of primitive color scales, so that I understand the foundation's color vocabulary.
5. As a portfolio reader, I want semantic roles explained separately from primitive scales, so that I understand naming by use.
6. As a portfolio reader, I want responsive variables described as Desktop, Tablet, and Mobile modes, so that I understand what the evidence demonstrates.
7. As a portfolio reader, I want to see a readable selection of button variants and states, so that I understand how foundations support component decisions.
8. As a portfolio reader, I want navigation examples connected to their product contexts, so that I can see how shared patterns adapt.
9. As a portfolio reader, I want accessibility and content requirements connected to component design, so that their role is concrete without implying audited compliance.
10. As a portfolio reader, I want to see configurable templates as compositions of patterns, so that I understand their relationship to the preceding components.
11. As a portfolio reader, I want the Storybook Button example explained through its properties, so that I understand its role as a development reference.
12. As a portfolio reader, I want the React and Next.js maintenance rationale connected to documentation and implementation, so that I understand the technical choice in context.
13. As a portfolio reader, I want Felipe's design leadership distinguished from development's React implementation, so that I understand the collaboration accurately.
14. As a portfolio reader, I want each image to have its own explanation, so that I know what to inspect without comparing a gallery.
15. As a desktop reader, I want focal images to alternate with wider evidence blocks, so that the reading rhythm supports the material's density.
16. As a mobile reader, I want the explanation before its image, so that I have context before inspecting the evidence.
17. As a reader on a narrow screen, I want readable text and useful image details without horizontal overflow, so that I can follow the case comfortably.
18. As a reader, I want image crops to retain the context that supports their explanations, so that the presentation does not misrepresent the source.
19. As a reader using assistive technology, I want meaningful headings and image alternatives, so that the argument remains understandable beyond its visual layout.
20. As a keyboard user, I want preserved navigation and visible focus, so that I can continue my percurso no portfólio.
21. As a reader, I want all explanations available without expanding controls or opening raw images, so that I can read the complete narrative in place.
22. As a reader, I want every section to appear during normal scrolling, so that long mobile sections do not conceal the case.
23. As a reader who prefers reduced motion, I want the same content immediately available, so that animation does not gate the explanation.
24. As a reader without JavaScript, I want the static narrative to remain available, so that the case does not depend on enhancement scripts.
25. As a portfolio reader, I want adoption in new projects distinguished from gradual migration of existing products, so that I understand the current scope of adoption.
26. As a portfolio reader, I want AI-assisted prototyping and translation to React clearly identified as work in development, so that exploration is not presented as delivered capability.
27. As a portfolio reader, I want claims to stay within the confirmed account and visual evidence, so that screenshots are not mistaken for measurements of speed, compliance, or parity.
28. As a portfolio maintainer, I want original assets preserved and derivatives documented, so that future editorial changes remain traceable.
29. As a returning visitor, I want the hero, navigation, contact, and surrounding content preserved, so that the revised evidence fits the existing portfolio experience.

## Implementation Decisions

- Keep the static HTML/CSS architecture. The affected presentation is Harmony's editorial body and its case-specific styling; there is no new product backend, API, state model, framework, or component-library implementation.
- Preserve the existing problem and role, header, hero video and poster, navigation, next-project destination, contact, adoption outcome, and work-in-progress content. Integrate the current decision arguments into the visual progression rather than retaining a second, repetitive decisions/before-and-after narrative. Preserve the meaning of the existing notes about shared reference, maintenance, and accessibility/content; their former standalone layout is not a requirement.
- Use precisely seven static image evidences in the approved order. Source basenames below identify the approved assets, not proposed implementation locations:
  - `color=primitives.png`: examples of primitive color scales; explain a shared vocabulary, not a complete palette or independently verified token total.
  - `semantic-tokerns.png`: semantic roles named by use; distinguish them from the primitive scales without claiming the screenshot resolves aliases or proves contrast compliance.
  - `variables.png`: responsive Desktop/Tablet/Mobile modes for dimensions, spacing, radii, and icons; do not describe light/dark themes or color-token mapping.
  - `buttons.png`: focal selection of button variants, sizes, and states; explain application of patterns without promising that all depicted behavior was executed or audited.
  - `components.png`: navigation adapted to Portal/Intranet and profile contexts; do not present it as an exhaustive component catalog.
  - `templates.png`: configurable compositions in design, preserving enough of the configuration context to support that explanation; do not infer automatic generation.
  - `storybook-2.png`: Button preview and property controls as a reference for implementation in partnership with development; do not describe 96 as a component count or infer passed tests from visible tabs.
- Remove the old organization before/after pair from the rendered demonstration, retaining its original files. Do not add `storybook.png`, which repeats the hero's guide introduction. The old “before” already contains a Harmony file, and the “after” does not show all resources physically merged into a single file; do not restate either unsupported interpretation elsewhere.
- Foundation evidence carries the shared-library and governance argument. Component application carries accessibility and content as continuing requirements, including semantics, contrast, and error messages as considerations, without inventing a documented rule or claiming every requirement is visible in a particular crop. Templates carry composition of patterns. Storybook carries the React/Next.js rationale of long-term maintenance and hiring, and the partnership between Felipe and development.
- Preserve the distinction between a shared reference/governance and a single physical file. Preserve Felipe's leadership of design and ongoing component evolution, with development implementing React in partnership with him.
- Each image receives its own English title and short factual explanation of what to inspect and why it matters. Titles and copy must not invent outcomes, historical sequencing, new governance examples, token/component metrics, measured speed, completed migration, design/code parity, automatic conversion, or audited AA compliance. Text printed inside an asset is not independent verification of its claims.
- One image per editorial row; no paired gallery, carousel, disclosure control, or full-size/raw-image link. All explanations remain visible by default. Screenshots illustrate the system; they do not become interactive replicas of Figma or Storybook.
- Explanation precedes image in DOM order and in the single-column mobile layout. Desktop lateral placement may alternate through presentation styling without changing that reading order. Use generous image width and wide blocks whenever density makes lateral presentation illegible, especially semantic roles, responsive variables, and templates. Focal button/navigation crops can support lateral alternation. Actual crop bounds and widths must be selected against the rendered result, not asserted as validated now.
- Preserve the existing typography system. Do not reduce font sizes to solve line breaks. Resolve wrapping through structure, available width, spacing, or faithful editorial cropping. Orientation text and meaningful captions use the existing stronger secondary text treatment and must remain legible against their rendered backgrounds.
- Create descriptively named derivatives only when needed for presentation, leaving every original intact. Keep the source context needed to identify scales, mode labels, variants/states, navigation context, template configuration, or Button properties. Do not try to recover detail outside source boundaries, enlarge raster text as a substitute for usable detail, fabricate missing UI, or remove context in a way that strengthens a claim beyond the evidence.
- Record every derivative in a Harmony image manifest: original identity, derivative identity, original dimensions, crop rectangle, resulting dimensions, format/quality decision, editorial purpose, and context retained. Choose compression by visual legibility as well as size. Images retain intrinsic dimensions/proportions, lazy loading and asynchronous decoding where appropriate, and specific alternative text describing the evidence.
- Keep new styles specific to Harmony. Reuse established tokens and patterns as references. Shared styling or scripts may change only if a demonstrated need cannot be resolved locally, with validation of every affected page. No broad prefactor is currently justified; any local structure needed to keep long sections visible belongs with the first demonstrable slice that needs it.
- Ensure normal scrolling can reveal every section despite the existing intersection-based animation. Do not place the entire narrative inside an unreachable tall animated section. Choose section boundaries or another narrowly scoped solution based on browser evidence; reduced-motion or programmatic-scroll success alone is insufficient.
- Preserve analytics behavior and the percurso no portfólio in accordance with the accepted continuity ADR. This revision does not authorize changing analytics loading, configuration, consent, or tracking behavior.

## Testing Decisions

- User approved the proposed test interface and coverage in this conversation after inspection of the approved narrative and current code. Use one principal seam: Harmony rendered and exercised in the browser through its externally observable behavior. Do not couple acceptance to internal CSS class names, exact DOM nesting, observer thresholds, or screenshot pixel equality.
- Reuse the existing Billing visual-narrative browser QA approach and Harmony's prior editorial validation as prior art, adapting expectations to the seven Harmony evidences. Keep browser checks and human visual inspection together; machine checks cannot establish raster-detail legibility or factual adequacy of a crop on their own. No new low-level test seam or project dependency is required by this spec.
- At 320, 375, 768, and 1440 px, verify the complete reading order; seven evidence images, one per row; explanation/image association; loaded images with positive intrinsic size; preserved proportions; no horizontal overflow, overlap, or clipped meaningful text; readable orientation text; suitable wide versus lateral treatment. Inspect viewport or element captures after confirming lazy images have loaded, rather than treating blank full-page captures as proof of a broken image.
- In all four widths, cover normal and reduced motion. Start normal-motion checks at the page top and scroll with real wheel/scroll input through the whole document, including a 700 px-high viewport. Observe each section as it is reached, not only its final state. All meaningful content must appear during reading; direct jumps to elements cannot substitute for this check. Reduced motion must expose the same narrative without reveal-animation gating.
- With JavaScript disabled, verify that the static narrative, images, and explanations remain available. No explanation should require a script or disclosure action to read.
- Exercise relevant preserved navigation with keyboard and inspect visible focus, accessible names, heading hierarchy, alternative text, and reading order. Verify back/home, work/about/contact, and next-project destinations; check contact presence without sending a message. No new image links or screenshot controls are expected.
- Review rendered copy against the approved seven-image mapping and factual limits. Check adoption/migration language, role attribution, the responsive meaning of variables, the limited scope of the Storybook evidence, and the explicitly unfinished status of AI prototyping/React conversion. Confirm that neither the old image pair nor the redundant Storybook introduction appears as static evidence.
- Confirm preservation of hero media configuration, navigation, contact, analytics, and out-of-scope content against the pre-implementation baseline. If shared code becomes necessary, add browser regression coverage for all pages it affects; do not treat a diff alone as evidence that behavior is preserved.
- Alongside the browser seam, perform artifact-integrity checks: source assets unchanged, manifest consistent with the derivatives actually used, and existing local changes preserved. These are document/asset checks, not a second product test interface.
- Each implementation slice includes its own browser verification and evidence for the behavior it introduces. The final slice also verifies the complete composed case, with all seven images and surrounding preserved surfaces. Do not defer all validation to a separate horizontal QA ticket.
- Record environment, browser, viewport/motion combinations, actual observations, failures/fixes, evidence captures, and remaining limits in a new Harmony narrative validation record. Preserve the earlier editorial validation as historical evidence. A token check alone must not be reported as measured contrast compliance; a DOM inspection must not be reported as a real screen-reader test.
- No browser, MP4, production Storybook, or live service tests were performed while authoring this spec. Previous validation reports describe earlier editorial work, not validation of the future seven-image implementation. Implementation acceptance remains pending execution.

## Out of Scope

- Implementing or executing any ticket during this specification conversation; editing HTML/CSS/JavaScript; generating image derivatives now; creating a commit, PR, or deploy.
- Reopening the completed narrative interview or adding unsupported factual claims and metrics.
- Altering the home, other cases, shared identity, typography system, hero assets, navigation, contact behavior, or analytics as independent work.
- Rebuilding Harmony components, tokens, templates, Storybook, React/Next.js packages, or production systems themselves.
- Delivering AI automation, automatic screen generation, or prototype-to-React conversion.
- Auditing or certifying the actual Harmony design system for accessibility, performance, parity, adoption, or business impact; verifying public package or production-service availability.
- Deleting originals, repairing missing source pixels, adding raw-image links, galleries, or interactions whose only function is hiding content.

## Further Notes

- The completed Harmony visual-narrative review is the final editorial authority for this revision. It records affirmative Q2, Q6, and Q8 responses. The copy draft and prior validation provide confirmed adoption, role, and work-in-progress context, but their former before/after captions do not override the later seven-image decision.
- The full cross-case factual research was read, with Harmony's limits applied. Its earlier interview recommendations have been resolved by the final review and must not reopen the interview. The handoff provides inherited presentation preferences; later approved revisions prevail over its older suggestions and the original Billing disclosure/full-size-link spec.
- Repository exploration found substantial pre-existing local modifications. Harmony had the visual review, copy draft, and prior validation, with no existing spec or ticket files at authoring time. This spec adds a document without modifying or closing earlier records. Shared-checkout work from other specification conversations must remain untouched.
- Ticket publication follows the separate granularity/dependency checkpoint in the local to-tickets skill. Tickets will be ready-for-agent with explicit blocking edges, one document per vertical behavior slice; this status is not authorization to execute them in this conversation.

## Completion

2026-10-24: All four tickets and implement-spec step 7 are resolved. See [code review](code-review.md) and [CSS grouping validation](visual-narrative-validation.md#code-review-css-grouping--2026-10-24) for the r1 resolution, checks and limits.
