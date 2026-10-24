# Ticket 03 — own-library evidence and outcome

## Scope and environment

- Isolated worktree: `C:/Users/fplev/.t3/worktrees/Portfolio/t3-988d206e`, branch `t3/library-row-mobile-legibility`.
- Clean initial HEAD `f8f9034` was an ancestor of integration `78a853d`; merged integration by fast-forward before implementation. No reset or edits to the root/integration checkouts.
- Read implement-spec, TDD and its tests/mocking references, AGENTS/tracker/domain pointers, glossary, ADR-0001, spec/ticket, visual review, Behance analysis, factual research, previous Convênios validation and Billing QA.
- Approved seam: rendered page and externally observable browser behavior. No unit seam, dependency installation, shared architecture or delegated work.
- Python 3.14, Pillow, Playwright Chromium `156.0.8078.4`; own static server on `127.0.0.1:8113`, launched from this worktree after confirming the port was unused.
- T3 `preview_status` initially had no tab. Opened own background tab `tab_5_f4360451-cc0a-4867-8add-b566bd6f135a` and navigated it successfully to port 8113. The first open rejected `about:blank`; retry without a URL succeeded. Used the explicitly named existing Playwright QA workflow for the reproducible viewport matrix.

## RED → GREEN at the browser seam

1. `python .scratch/convenios/03-library-qa.py red`: **0 passed, 1 failed**. At 320 px the original 1024 px-wide sheet was painted at 224 px (21.875% source scale), making states and touch-area detail unreadable. Actual loaded capture: `03-evidence-red/03-library-320.png`; numeric evidence: `03-results-red.json`.
2. Changed only the library row's presentation and source. `... green`: **1 passed, 0 failed**. Focused contiguous 173 × 263 crop renders at 272 px (157.2% source scale) at 320 px. Actual loaded capture: `03-evidence-green/03-library-320.png`.
3. Added the next reader-facing acceptance check: complete in-page explanation, own-library/Harmony distinction and supported outcome. `... red-copy`: **1 passed, 1 failed** while the raw-image link and old claims remained. `... green-copy`: **2 passed, 0 failed** after removing the link and updating only the library and outcome copy. JSON results and loaded captures retain both stages.

## Implementation and visual inspection

- Inspected the actual 1024 × 1322 source before cropping. Crop `(35,560)–(208,823)` retains **Botões ícone**, component-final label, all outlined/filled state examples and the full **Área de clique** diagram. It does not crop out touch areas to obtain a narrow states-only image. No content beyond the source boundaries, montage, retouching or generated pixels.
- Full-width library row, explanation first, focused image capped at 480 px and no 480 px height cap. Other rows are untouched. Source raster softness remains visible when enlarged; this is an honest excerpt, not newly typeset documentation. The larger in-page examples and full diagram can be distinguished without opening another surface. English prose explains the Portuguese source.
- Original PNG/WebP are untouched. Decoded RGBA output exactly equals the source crop, including alpha. The selected rectangle is fully opaque; no background was flattened. Exact bounds, original/output hashes, dimensions, format and rationale: `assets/03-button-documentation.json`.
- Copy states that the app predates Harmony and uses its own component library and visual language. No construction on Harmony, migration, reuse, certification, or efficiency claim. Outcome describes the dedicated shipped app and documented product library.
- Existing 16 px explanation text remains at `rgba(242,242,245,.65)` over `rgb(13,15,26)`; visual inspection accompanies the computed contrast check. No typography was reduced.

## Executed regression checks

`python .scratch/convenios/03-library-qa.py final-premerge`: **104 passed, 0 failed**; `03-results-final-premerge.json`. Widths 320/375/768/1440, 900 px height, normal and reduced motion:

- Ordinary wheel traversal starts at the top for every matrix cell; all sections were observed visibly in the viewport. Per-step section geometry and opacity: `03-evidence-final-premerge/03-wheel-*.json`. Reduced-motion content is immediately available. No tall-section animation remedy was needed.
- All images loaded with nonzero intrinsic dimensions, correct declared dimensions, meaningful alternatives and proportional painting; body images lazy/asynchronous. One asset per row, explanation before evidence, no copy/image overlap or horizontal overflow. Library is last, wide, below its explanation, and has no raw link or disclosure.
- Home card keyboard focus and Enter → case, return to Work, Enrollment → Convênios → Harmony, nav/store hrefs, keyboard focus on both store links, contact email-copy button and name field all passed. Contact form remains present and was not submitted. External stores/services were not opened or verified.
- No JavaScript page errors, console warnings/errors or failed requests in this execution.
- Initial matrix instrumentation sampled short sections only during their entrance fade and compared the letterboxed hero element's box ratio to its image ratio. Corrected the wheel cadence/final settled sample and recognized undistorted `object-fit: contain` painting. An initial terminal print also hit Windows cp1252 on the store-link arrow; stdout is now UTF-8. Those harness issues required no production changes.
- Initial tall-element screenshots could include the fixed navigation over offscreen text. Final capture workflow uses a real viewport with the explanation below the fixed nav plus a separate fully loaded crop capture. Wheel verification precedes all screenshot positioning.

## Preservation and limits

Only the library article, outcome heading/paragraph, and library-specific rules in `assets/css/convenios.css` change. Hero, home card, card/accounts rows, navigation, store/contact destinations, metadata, analytics and shared CSS/JS remain as found. Ticket remains **claimed**, pending integration final review.

Manual inspection is of real Chromium captures, not a screen-reader audit or new axe run. No production app/service validation, Firefox, Safari, Lighthouse or accessibility certification is claimed. Other tickets' editorial changes remain outside this ticket.

## Final integration recheck

Pending final merge and recheck; this section will be completed before handoff.
