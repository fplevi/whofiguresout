# Enrollment final integration validation

Date: 2026-10-24. Merger work in the shared checkout
`C:/Users/fplev/.t3/worktrees/Portfolio/integration-enrollment-visual-narrative`,
branch `integration/enrollment-visual-narrative`. No nested agents or other
worktree writes. Worktrees remain available for the parent's two-axis review.

## Merge and checked revision

Started clean at `af687df`. Merged `t3/enrollment-visual-narrative` at
`a09eb9e720f2d4219638d28df858d55ee69a1560` with `--no-ff`, producing
`5581f26fed9fd079c8dd4d4a16a76495b757424c`. Git reported no conflicts. All four
ticket slices and the integration parent's ticket 05 QA URL/output overrides
survived. Product changes from the starting integration are only the incoming
Enrollment HTML/local CSS comparison changes; all shared code remains untouched.

The browser matrix and final checks executed with HEAD
**`74d92fe5e411d2ffaa23cf779cfe76855b0f96e0`**, the merge plus current QA entrypoints.
The final audit received two QA-only corrections described below; no runtime
file changed after merge or during/after validation. The final evidence/report
commit also changes only QA/documentation. Working-file SHA-256 values are:

| Product file | SHA-256 |
| --- | --- |
| `case-studies/enrollment.html` | `9100828d15928ad3b34410fc9fa8bcac7011465bd6c0e864618e55ed6c029fbe` |
| `assets/css/enrollment.css` | `5baa6e61b909b9e48dba39ce084e136b8b4d69365d0635d0075f5246892a64d6` |
| `assets/images/enrollment/submission-analysis.webp` | `30a3cd373457f2712b84b61239af12c2a54a9b66e63ba01f2dd1e86f616172e3` |

[final-checks.json](qa/integration-final/final-checks.json) records all 18 original
asset hashes as well, and verifies every product file against merge `5581f26`
(accounting for Git LF versus Windows CRLF in text).

## Executed matrix

Served this exact checkout at
`http://127.0.0.1:8127/case-studies/enrollment.html`. Environment: Windows 11
`10.0.26300`, Python 3.14.3, headless Playwright Chromium 156.0.8078.4, device
scale 1, browser-emulated touch. Existing Playwright installation under
`%TEMP%/portfolio-convenios-qa`; no project dependency was added.

The final matrix passed **308 browser checks, zero failures**, across eight
cases. Extra baseline/placement/control smoke checks also passed. Final checks
passed six actual navigation destinations, 80 explanation contrast/font
measurements (ten paragraphs in each of eight cases), original/manifest/crop
integrity, historical preservation and 24 normal/reduced screenshot pairs.

| Viewport | Motion | Browser checks | Real wheel events | Result |
| --- | --- | ---: | ---: | --- |
| 320 × 700 | Normal | 38 | 47 | Pass |
| 375 × 700 | Normal | 38 | 43 | Pass |
| 768 × 700 | Normal | 38 | 38 | Pass |
| 1440 × 900 | Normal | 38 | 46 | Pass |
| 320 × 700 | Reduced | 39 | 47 | Pass |
| 375 × 700 | Reduced | 39 | 43 | Pass |
| 768 × 700 | Reduced | 39 | 38 | Pass |
| 1440 × 900 | Reduced | 39 | 46 | Pass |

Every case covers **one discovery process board + four distinct interface
screens + one two-layer comparison**, six evidence blocks and seven image
elements. The board follows the preserved My Role account and precedes The
Decisions. The comparison follows exploration and precedes decision 02. Eligibility,
personal details and portability are separate decision-02 blocks; submission is
beside next steps. What Shipped is absent, with no empty standalone heading or
second simulator. Omitted screens remain outside the presentation.

- Each fresh page starts at scrollY 0. Real wheel input traverses to the bottom
  before any screenshot styling or element jumps. Every narrative heading is
  observed in the viewport with visible ancestors; every section becomes visible.
  Normal motion waits 550 ms per 240 px wheel event for the existing entrance
  animation. No opacity is forced. Reduced-motion sections are immediately visible.
- Fonts settle and all seven images complete with positive natural dimensions
  before evidence capture. Natural/intrinsic dimensions, specific alternatives,
  lazy/async loading, proportional sizing, DOM explanation-first order, copy
  above images, no overlap/text clipping, 16 px guidance, viewport-edge fit and
  zero horizontal overflow pass in all eight cases.
- The native range is named “Compare plan cards before and plan benefits after”.
  Tab enters it, the orange focus frame is visible, Tab exits to next project,
  and Shift+Tab returns. Home/End and both arrows match input value, rendered
  divider and clipping; endpoint screenshots match the independent original
  Before/After rasters. Pointer and CDP-emulated touch operate at an actually
  visible point below fixed navigation, with matching values and reveals.
- Contact name → email → message Tab order and copy-email availability pass;
  submit is never activated. All eight cases record **zero contact POSTs**.
  Actual back, logo, Work, Contact, About and next-project clicks reach their
  expected destinations. Contact submission is not used to test availability.
- Computed foreground/background colors, alpha compositing and WCAG relative
  sRGB luminance measure all ten explanation/instruction paragraphs at every
  setting: minimum **7.55:1**, each 16 px. Labels over their opaque local dark
  background, including a worst-case white underlying image, and dark arrows
  over the white handle measure **19.08:1**. Focus visibility is checked in
  computed style and inspected in viewport screenshots.

[validation.json](qa/integration-final/validation.json) contains every named
check, geometry, wheel-visible headings, image metadata, keyboard results and
pointer/touch values. [contrast-matrix.json](qa/integration-final/contrast-matrix.json)
contains the 80 measurements. All fresh evidence is isolated under
`qa/integration-final/`.

## Visual and editorial inspection

Inspected all **24 normal-motion evidence captures**, six blocks at each of
320/375/768/1440 px: `enrollment-discovery`, `evidence` (comparison),
`enrollment-eligibility`, `enrollment-personal-details`,
`enrollment-portability` and `enrollment-submission-title`, using filenames
`<width>-no-preference-<block>.png` in the new evidence directory. Also inspected
reduced-motion focus viewport captures at all four widths, normal focus at
320/375, and the 375 header. All 24 corresponding reduced-motion evidence
captures have identical dimensions and pixels to the inspected normal versions;
[motion-evidence-comparison.json](qa/integration-final/motion-evidence-comparison.json)
records dimensions, hashes and empty difference bounds for every pair.

The English explanations wrap without clipping and remain understandable at
mobile widths. The board's CSD matrix, brainstorming, journey and empathy map
areas remain recognizable with the source's lower-edge truncation; tiny notes
are not promised as readable or reconstructed. The comparison shows cards versus
aligned benefits, with legible labels and focus. Wide journey views retain their
seven-step sidebar and closed categories. Personal details retains the source's
partial attachment area. Submission preserves the notice, protocol and static
placeholder address. No visual correction was needed.

Editorial review confirms discovery synthesis does not establish methods,
participants, sources, verified findings or causation from illegible notes.
Comparison copy does not establish equivalent products/prices, lower prices,
fewer plans or account-free access from the raster. Portability remains a
specific situation rather than mandatory successive states. Submission for
analysis is distinct from approval, completed enrollment, actual status lookup,
sent email or a met deadline. HTML explanation carries these limits without
requiring a gallery, disclosure or raw-image link.

## Preservation

Rendered preserved head/header, hero/media declarations, context, original role,
outcomes, next project and contact match the independent `f8f9034` and pre-change
snapshots in every case. Runtime section-root entrance styles and asynchronously
injected Clarity tags are excluded from that rendered comparison; authored head
and analytics declarations are separately compared exactly to `f8f9034`.
All three original decision paragraphs and decorative notes also match baseline.
The existing 408 January-2023 / 1,105 January-2024 proposals and rounded 171%
growth remain intact; neither completed enrollments nor exclusive causality is
claimed. Support reduction remains an unmeasured objective.

All **18 originals** are byte-identical to `f8f9034`. All four asset manifests
are checked: uncropped original reuse for discovery, comparison and three
journey screens; exact decoded RGBA identity for the declared submission crop
`(0,184,1920,922)`, 1920 × 738. Issue 01 retains `needs-info` and exact working
bytes, SHA-256 `b7d1b0127a8fb45274b3e04c78bba05a46f5c32f5d89827cbfd5eca8309ef2e2`.
Shared CSS/JS and original analytics markup are unchanged.

Historical reports, manifests and evidence remain intact: the audit checks
**303 parent/path records from af687df and 353 from a09eb9e** (overlapping files
are counted against both parents). Binary artifacts require exact bytes; text
allows Git LF/Windows CRLF normalization. The one older incoming ticket-05 report
is retained as the complete unchanged prefix of the newer integration-parent
report, whose existing appendix is also preserved exactly. See
[historical-preservation.json](qa/integration-final/historical-preservation.json).

## Reproduction, diagnostics and limits

The original `qa.py` and `final_checks.py` now dispatch to the current combined
behavior/integrity suites. Their old source is preserved byte-for-byte as
non-executable `.txt` files under `historical-entrypoints/`. Those obsolete
What Shipped/generic-name assumptions are no longer active entrypoints.
[QA-README.md](QA-README.md) documents prerequisites, current reproduction and
the historical status of earlier slice reports/scripts. Commands executed:

```powershell
python -m http.server 8127 --bind 127.0.0.1
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8127/case-studies/enrollment.html'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/integration-final'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONIOENCODING='utf-8'
python -u .scratch/enrollment/qa.py
python -u .scratch/enrollment/final_checks.py
git diff --check
```

The server ran hidden with stdout/stderr redirected, avoiding the earlier
integration's undrained-pipe problem. It was stopped after QA. Future runs should
select a **new** output directory to preserve this execution. The wrapper
automatically creates the independent protected baseline before its first matrix.

The browser matrix completed on its first attempt. The new final historical
audit initially rejected the already-appended ticket-05 report; inspecting both
parents established that no content was lost. The corrected audit specifically
requires the incoming prefix and exact equality to af687df's newer report. Before
that audit ran, a manifest-schema correction accepted ticket 03's
`originalDimensions` alongside the other manifests' `sourceDimensions`.
The final checks then passed in full without rerunning or changing the passed
browser behavior. Both were QA-only corrections. The failure/diagnostic record is
[final-checks-first-attempt.txt](qa/integration-final/final-checks-first-attempt.txt).
A supplementary T3 snapshot timed out after 15000 ms; the requested existing
Playwright workflow supplied the completed browser evidence.

The completed eight-case matrix records **zero page errors, console
warnings/errors, failed requests (local or external), HTTP errors and contact
POSTs**. `git diff --check` passed. No product code was altered to satisfy QA.

This local browser run does not establish physical-device or screen-reader
behavior, MP4 playback, production analytics collection, real enrollment/upload/
portability/status operations, email delivery or service deadlines. Static
screenshot controls remain evidence. No actual contact submit, PR, deployment,
review delegation or worktree cleanup was performed. Parent review remains the
next step; this report certifies the executed final integration matrix.
