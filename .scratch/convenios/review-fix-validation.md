# Convênios review correction

Executed 2026-10-24 in isolated worktree `C:/Users/fplev/.t3/worktrees/Portfolio/t3-a62b262c`, branch `t3/convenios-network-mobile-first`.

## Finding and response

Fixed review point: `f8f9034fb32de4b7839ac0a003db2bb791af883e...9dec0e116e8e679da9f0b8274085f0fe46dad37c`. [Review record](code-review.md): Standards reported one P3; Spec reported no findings, and no baseline smells were identified.

The unconditional desktop placement of the network copy/figure, followed by a mobile reset, violated the mobile-first rule in `portfolio-dev-plan.md:348`. Moved only those grid-column/grid-row declarations into `@media (min-width: 769px)` and removed the redundant mobile reset. Mobile now uses the existing DOM reading order by default. Network figure padding remains `var(--space-16)`; image sizing remains `max-width: 360px` and `max-height: none`. All other production bytes are unchanged. No broader migration of existing styles.

Read implement-spec, TDD and its test/mocking references, AGENTS/tracker/domain docs, glossary/ADR, the spec, all three tickets and their validation records, integration validation and the documented CSS rule. This is review-stage refactoring under TDD, preserving behavior at the already approved rendered-page seam; no artificial failing runtime test was introduced for a standards-only finding.

## Ancestry and integration

- Initial clean HEAD `f8f9034` was confirmed an ancestor of `9dec0e1` with `git merge-base --is-ancestor`; fast-forwarded this branch to integration before editing. No reset.
- Scoped CSS commit: `f72c4d0` (`Make Convenios network grid placement mobile-first`).
- Merged current integration tip `dd3ba9796a51f250fe1db11ea046a3661ce06641` into this branch as `ac225dc9753e50aab41aec35dbdda6e4e0bdef3a`, without conflicts. The integration advance contains only validation/review artifacts. `git diff --exit-code f72c4d0 HEAD -- assets case-studies index.html` passed; merged integration is an ancestor of HEAD.
- Final focused browser execution runs after that merge. Relative to integration, the only production file changed is `assets/css/convenios.css`. `git diff --check` passes.

## Focused rendered validation

Windows; Python 3.14.3; existing Playwright 1.64.1; Chromium 156.0.8078.4; device scale 1; 900 px viewport height. Port 8134 was unused before launching this worktree's own server. Used the explicitly requested existing repository Playwright workflow, adapting `integration-smoke.py` and `03-library-qa.py`; no dependencies installed.

```powershell
python -m http.server 8134 --bind 127.0.0.1
python -u .scratch/convenios/review-fix-qa.py
```

Final result: **45 passed / 0 failed**, 320/375/768/1440 px × normal/reduced motion. [Numeric results and per-step wheel observations](review-fix-evidence/results.json); [reproducible focused script](review-fix-qa.py).

- Actual ordinary 400 px wheel input from the page top, with 550 ms reading pauses, exposed both network explanation and loaded image in every cell. No jumps or visibility overrides precede this traversal. Checks stop after passing the network section; this is not another whole-case acceptance matrix.
- Explanation precedes the image in DOM and mobile layout through 768 px; at 1440 px the image is on the left. No copy/figure overlap or horizontal overflow. Reduced-motion network content is immediately available.
- Network image decoded successfully at intrinsic 430 × 686, paints proportionally and retains its existing size caps/padding. Explanatory text remains 16 px.
- Zero captured JavaScript page errors, console warnings/errors, failed requests or HTTP errors.
- Captured only final network viewport and loaded-image PNGs for all eight cells, after traversal and image decoding. Screenshot-only instantaneous positioning keeps the fixed navigation above the explanation. Inspected all four viewport layouts and the full image; normal/reduced viewport captures are pixel-identical at each width. The mobile map/list control and complete phone remain recognizable, with readable English explanation; desktop separation remains clear. Known source raster softness is unchanged.

An initial harness attempt assumed a semantic `figure`, but the existing image wrapper is a `div`. Corrected the observation to the image's parent; no production change was needed. A complete preliminary execution passed 45/45 while the validation-only integration merge occurred. It was superseded by the full focused post-merge execution above; only final evidence is retained at these paths.

## Limits and handoff

The parent owns the separate combined matrix and axe audit recorded in `final-validation.md`; those historical results are not claimed as new execution here. No new axe, screen-reader, Firefox/Safari, production app/service, live-store or analytics-continuity audit. No new copy/assets or shared presentation/behavior changes.

Original root and integration checkout were not edited. Tickets remain unchanged; no merge into integration, PR, delegation or worktree deletion. Own server is stopped after validation. The single standards finding is addressed; no unresolved correction remains.
