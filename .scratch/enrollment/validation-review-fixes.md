# Enrollment final review fixes and regression verification

Date: 2026-10-24. Single implementer; no nested agents.
Branch: `t3/enrollment-css-review-fixes`.
Worktree: `C:/Users/fplev/.t3/worktrees/Portfolio/t3-8797c47a`.

## Starting point and integration

Started clean at `c356ef26694dfa6f489764b086589a94b572e0bb`, exactly the
`integration/enrollment-visual-narrative` tip and merge base. Read the implementation
and TDD skills, spec, both individual reviews, combined code review, QA README,
domain glossary and analytics ADR before implementation.

Runtime commit: `8011e432ba50dc47fe0ef56d499164b65ddfc5df`.
QA baseline adaptation and executed matrix HEAD:
`bd2db56430cd592c74359805534d52cf92d84f13`.
Merged the latest integration tip into this branch before the full matrix;
Git reported `Already up to date.` Repeated that merge after the matrix and
final checks, then reran the current control smoke check successfully. Integration
still pointed to `c356ef2`. The final evidence/report commit changes no runtime or
QA scripts. Final handoff also checks integration ancestry, validated product
hashes and the clean tree after the last merge attempt. No merge into the parent
integration branch was performed.

## Finding dispositions

All three Standards P3 findings are addressed. Spec had zero actionable findings.

1. **Reuse heading typography:** inspected the actual shared
   `.cs-decision__title` rule in `assets/css/case-study.css`. Its display family,
   24px size, 700 weight, 1.2 line height and primary color exactly match the
   duplicated local declarations. Added that existing primitive to the three
   journey h4s and submission h4, and removed only the duplicated typography.
   Local heading bottom spacing remains `var(--space-16)`; journey/submission
   captions retain `var(--space-24)` bottom spacing. Heading levels, IDs and copy
   remain intact. The shared stylesheet was not modified.
2. **Tokenize the focus gap:** replaced local `outline-offset: 4px` with
   `var(--space-4)`, whose existing computed value is 4px. The native range,
   frame focus rule and 2px accent outline retain their behavior.
3. **Consolidate width ownership:** `.enrollment-decisions` now owns full case
   width in one rule. Its decision prose and all evidence captions share one
   grouped 840px reading-measure rule under that Enrollment scope. Removed the
   competing generic local `.cs-decisions--stacked` / `.cs-decision__left`
   overrides and later duplicate widths. Retained evidence margins, image
   treatment, comparison guidance and responsive outcome grid.

Only `case-studies/enrollment.html` and `assets/css/enrollment.css` changed in
the product. No shared CSS/JS, image, issue, copy, analytics or unrelated file
changed. Current QA uses semantic heading checks and does not count
`.cs-decision__title`, so no selector adaptation was needed.

## Approved seam and maintenance verification

This is behavior-preserving maintenance at the approved rendered-page seam.
No lower-level CSS selector snapshots or artificial failing behavior test were
added. No actual behavioral change was found, so no red/green implementation
cycle was needed. Existing current browser checks were rerun in full.

Before edits, captured rendered measurements in all eight viewport/motion cases:
the four headings' text, dimensions, font family/size/weight/line height/color,
bottom margin; prose/caption dimensions and measure; decisions width; and the
focused comparison frame's style, width, gap and color. Compared after edits:
all string-valued styles match exactly. Numeric measurements match within
0.01 CSS px, with maximum difference **0.00048828125 CSS px** in the completed
comparison. The initial exact floating-point comparison detected only sub-0.001
CSS px differences in transformed element heights; the explicit 0.01 CSS px
tolerance resolves measurement precision rather than masking a behavior change.
Raw before/after readings and the comparison result are retained:

- [rendered-before.json](qa/review-fixes/rendered-before.json)
- [rendered-after.json](qa/review-fixes/rendered-after.json)
- [rendered-comparison.json](qa/review-fixes/rendered-comparison.json)

Compared all six evidence blocks at all four widths in both motion modes against
the untouched `qa/integration-final` screenshots: **48/48 are pixel-identical**,
with identical dimensions and empty difference bounds. The comparison includes
all four headings affected by primitive reuse, prose widths and evidence spacing.
[review-appearance-comparison.json](qa/review-fixes/review-appearance-comparison.json)
records each baseline/current hash and pixel result. These are rendered artifacts,
not CSS selector snapshots.

## Executed QA

Served this exact worktree at
`http://127.0.0.1:8128/case-studies/enrollment.html`. Used fresh output
`qa/review-fixes`; historical output directories were not overwritten.
Environment: Windows 11 `10.0.26300`, Python 3.14.3, Pillow and the existing
Playwright installation under `%TEMP%/portfolio-convenios-qa`, headless Chromium
156.0.8078.4, device scale 1 and emulated touch. No dependency was added.

Current `qa.py` passed **308 checks, zero failures**, plus the independent
protected baseline and comparison/control smoke checks. Normal-motion cases each
passed 38 checks; reduced-motion cases each passed 39.

| Viewport | Motion | Checks | Real wheel events |
| --- | --- | ---: | ---: |
| 320 x 700 | Normal | 38 | 47 |
| 375 x 700 | Normal | 38 | 43 |
| 768 x 700 | Normal | 38 | 38 |
| 1440 x 900 | Normal | 38 | 46 |
| 320 x 700 | Reduced | 39 | 47 |
| 375 x 700 | Reduced | 39 | 43 |
| 768 x 700 | Reduced | 39 | 38 |
| 1440 x 900 | Reduced | 39 | 46 |

The matrix traverses the real page from the top by wheel before element jumps
or isolated evidence screenshots. Every narrative heading is encountered and
every section becomes visible. All seven image elements load with proportional,
declared source dimensions; five single-image evidence blocks and one two-layer
comparison retain explanation-first order. Guidance remains 16px, with no
horizontal overflow, text clipping, overlap or missing selected evidence.

Native-range coverage passes accessible naming, Tab entry/exit and return,
visible frame focus, Home/End/arrows, visible endpoint rasters, pointer and
emulated touch below fixed navigation, and matching value/divider/reveal.
Contact fields and copy-email control remain available, with name/email/message
Tab order preserved. No contact message was submitted.

Current `final_checks.py` also passed in full:

- All six actual navigation/back/next-project destinations.
- Eight contrast cases, ten explanation paragraphs each, all 16px and at least
  **7.55:1**. Computed-color sRGB luminance includes alpha compositing; comparison
  labels over their opaque background and handle arrows measure **19.08:1**.
- All 18 originals byte-identical to `f8f9034`, all presentation manifests valid,
  and the submission derivative exactly matches its declared source crop pixels.
- Hero/media declarations, head/analytics, context, role, outcomes, navigation,
  next project and contact match preserved rendered surfaces. Original decision
  arguments and notes remain exact. Issue 01 retains its exact bytes and
  `needs-info` status. Shared styles and scripts remain unchanged.
- All **1,193 historical parent/path records** preserved: 303 from `af687df`,
  353 from `a09eb9e`, and 537 from pre-review `c356ef2` (overlapping artifacts
  are checked against each reference). The existing ticket-05 appended report
  exception remains narrowly constrained to the already-preserved parent text.
- All 24 current normal/reduced evidence pairs are pixel-identical.

The matrix records zero JavaScript errors, console warnings/errors, failed
requests, HTTP errors and contact POSTs. `git diff --check` passed.
See [qa.log](qa/review-fixes/qa.log),
[validation.json](qa/review-fixes/validation.json),
[final-checks.log](qa/review-fixes/final-checks.log), and
[final-checks.json](qa/review-fixes/final-checks.json).

## Visual inspection and focus

Inspected all 24 normal-motion evidence captures: discovery, comparison,
eligibility, personal details, portability and submission at 320/375/768/1440.
The 24 corresponding reduced-motion captures have identical pixels. Headings
retain their size and line breaks; evidence spacing and desktop reading measure
remain unchanged. Mobile explanations remain readable and complete without
depending on raster microtext. Original screenshot limits, closed categories,
partial upload and submission-for-analysis qualifications remain intact.

Inspected focus viewport captures at all four widths under reduced motion, plus
normal motion at 320 and 1440. The primary 320px reduced-motion focus capture
caught a pale intermediate frame paint despite the passing computed focus
check. A supplementary capture after real wheel traversal, Tab focus and a
150ms paint settle confirms the expected orange frame: solid 2px,
`rgb(244, 168, 124)`, 4px gap and visible section opacity 1. The original matrix
capture is retained; no runtime change was needed. See
[320-reduce-focus-settled.png](qa/review-fixes/320-reduce-focus-settled.png) and
[focus-settled.json](qa/review-fixes/focus-settled.json).

## Explicit runtime hash adaptation

The prior final check asserted every product file against integration merge
`5581f26`. Intentional reviewed maintenance changes the HTML/CSS bytes, so that
assertion could not continue describing the new approved runtime.
`final-checks-integration.py` now pins **only those two files** to reviewed runtime
commit `8011e432ba50dc47fe0ef56d499164b65ddfc5df`. Every other product file keeps
the `5581f26` baseline. `productBaselineByPath` records each choice. There is no
blanket preservation skip, self-derived working-tree baseline or history rewrite.
Historical verification additionally includes the completed pre-review run.

Validated working-file SHA-256:

- HTML: `6e654b5a241dd123e24ef76eab8fb57bf9cf20cd8434720b5bdee25ae8dd2d19`
- Local CSS: `9ee1c1129d2c8e3d990d9bd887cfcc46342b7d22e778231ddfa8ee7f99c2250a`
- Submission derivative: `30a3cd373457f2712b84b61239af12c2a54a9b66e63ba01f2dd1e86f616172e3`

## Reproduction and limits

Commands, following [QA-README.md](QA-README.md), with the requested port/output:

```powershell
python -m http.server 8128 --bind 127.0.0.1
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8128/case-studies/enrollment.html'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/review-fixes'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONIOENCODING='utf-8'
python -u .scratch/enrollment/qa.py
python -u .scratch/enrollment/final_checks.py
git merge integration/enrollment-visual-narrative
python -u .scratch/enrollment/qa.py --control
git diff --check
```

For a future run, choose a new output directory to preserve this evidence.
The post-merge smoke output is retained in
[post-merge-control.log](qa/review-fixes/post-merge-control.log). The server is
stopped after verification. This local QA does not claim physical-device,
screen-reader, MP4 playback, production analytics-session continuity, actual
enrollment/status/upload operations, email delivery or service-deadline testing.
No PR, deployment, parent integration merge or worktree cleanup was performed.
