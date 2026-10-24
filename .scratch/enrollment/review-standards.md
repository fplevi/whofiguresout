# Standards review

Reviewed `git diff f8f9034fb32de4b7839ac0a003db2bb791af883e...HEAD` at `3b7074d897967924c869c2ba7ce46bd8be07a30f`. Standards sources and the complete supplied smell baseline were considered. No product edits or nested agents.

## Documented-standard violations

- **P3 — Reuse the existing heading style:** `assets/css/enrollment.css:46–53` introduces `font-size: 24px` and repeats the existing `.cs-decision__title` typography for journey/submission headings. README.md, “Key decisions / Design tokens as the foundation,” requires typography values to live in `tokens.css`; `portfolio-dev-plan.md:348` requires custom properties for tokens. Reuse the established title primitive on these headings and keep only evidence-specific spacing locally, rather than adding another hardcoded heading size. This preserves the approved typography without changing shared CSS.
- **P3 — Tokenize the focus gap:** `assets/css/enrollment.css:104`, `outline-offset: 4px`, bypasses the existing `--space-4`. `portfolio-dev-plan.md:355` requires “All spacing from --space-N tokens only.” Use `outline-offset: var(--space-4)` so focus spacing follows the token system.

## Baseline smells — judgment calls

- **P3 — Possible Duplicated Code:** `assets/css/enrollment.css:26–32` and `82–88` independently implement the same full-width-decisions/840px-prose arrangement: `.cs-decisions--stacked { max-width: none; }` versus `.enrollment-decisions { max-width: none; }`, and `.cs-decision__left { max-width: 840px; }` versus `.enrollment-decisions .cs-decision__left { max-width: 840px; }`. Both container classes occur on the same element. Consolidate the width ownership under the Enrollment selector and group the relevant captions. Otherwise, changing the earlier prose-width rule alone silently loses to the later, more specific duplicate. This is a local cleanup, not a shared-component extraction.

Historical slice scripts/reports are intentionally retained; their repeated checks are not treated as maintenance findings. Spec.md:76 explicitly permits uncropped-original reuse, so reused PNG/JPEG sources are not flagged against the older WebP preference. Authorized implementation/commits are not scope findings.

Evidence check: saved final matrix contains eight cases and 308 passes/zero failures; all recorded product hashes match reviewed HEAD. Full browser matrix was not rerun.

**Total:** two documented-standard violations and one smell judgment; highest severity P3. No blocking standards finding.
