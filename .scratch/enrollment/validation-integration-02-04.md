# Enrollment integration validation — tickets 02 and 04

Date: 2026-10-24. Merger scope only. All work took place in
`C:/Users/fplev/.t3/worktrees/Portfolio/integration-enrollment-visual-narrative`,
branch `integration/enrollment-visual-narrative`. No other checkout was modified.

The checkout began clean at `fa56b5c740505ab7e46ef04760cd38315a0b245b`.
The independently rendered preservation baseline remains `f8f9034`.

## Integrated changes

Sequential `--no-ff` merges:

1. `5b2669e`: merged `t3/enrollment-discovery-synthesis`, saved tip `13c9ac7`.
2. `501ec0e8c9120c261985719600d45637fb49793c`: merged
   `feature/enrollment-ticket-04`, saved tip `8a6b19d`.

The second merge automatically combined the HTML. The only conflict was the
adjacent insertion of discovery and journey rules in `assets/css/enrollment.css`.
Resolution retained both complete rule sets with separate closing braces. No
additional product correction was needed after browser verification.

The merged page has one discovery board after the preserved My Role section and
before The Decisions, plus the three approved journey figures inside decision 02.
Each explanation precedes its image. The original comparison remains once in
What Shipped, pending ticket 03. Ticket 05's submission image is not present yet.
This is validation of the current integrated slices, not final acceptance of the
future discovery-board/four-interface-screen/relocated-comparison composition.

## Fresh execution on integration

Served this checkout with `python -m http.server 8120 --bind 127.0.0.1`.
Browser URL: `http://127.0.0.1:8120/case-studies/enrollment.html`.
Product files were tested at merged HEAD `501ec0e`; only QA/report files changed
afterward. Product hashes are recorded in [the integration final checks](qa/integration-02-04/final-checks.json).

Environment: Windows 11 `10.0.26300`, Python 3.14.3, headless Playwright Chromium
156.0.8078.4, device scale factor 1. Existing temporary Playwright installation
under `%TEMP%/portfolio-convenios-qa`; no new project dependency. Touch is browser
emulation, not a physical device.

Reused the saved slice scripts. Added optional `ENROLLMENT_QA_URL` and
`ENROLLMENT_QA_OUT` overrides, retaining their original defaults. Local-request
failure filters now follow the selected origin. This permits fresh integration
evidence without overwriting historical runs. These PowerShell commands reproduce
the successful execution, with a server already running from this checkout:

```powershell
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8120/case-studies/enrollment.html'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONIOENCODING='utf-8'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/integration-02-04/discovery'
python .scratch/enrollment/qa-ticket-02.py --matrix
python .scratch/enrollment/final-checks-ticket-02.py
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/integration-02-04/journey'
python .scratch/enrollment/matrix-ticket-04.py
python .scratch/enrollment/final-checks-ticket-04.py
python .scratch/enrollment/final-checks-integration-02-04.py
git diff --check
```

Results:

- Discovery matrix: **8 passed, 0 failed**, in [discovery/matrix.json](qa/integration-02-04/discovery/matrix.json).
- Journey matrix: **166 checks passed, 0 failed**, in [journey/matrix.json](qa/integration-02-04/journey/matrix.json).
- Both final-check suites and integration integrity checks passed.
- Widths/heights: **320 × 700, 375 × 700, 768 × 700, 1440 × 900**;
  each runs normal (`no-preference`) and reduced (`reduce`) motion.
- Fresh pages start at scrollY 0. Real wheel traversal occurs before any element
  jumps or screenshot styling. Journey QA observes every section, decision
  heading and figure while visible in the viewport; no sections remain hidden.
  Normal-motion wheel intervals allow the inherited entrance animation to settle.
  Reduced-motion sections are immediately available. No opacity is forced.
- All images load with positive natural dimensions before captures. The board
  remains 1672 × 661; the three interface originals remain 1920 × 1200. Explanation
  order, proportional sizing, lazy/async loading, 16px body copy, no overlap,
  no horizontal overflow and no main-content clipping pass at all widths.
- The one existing comparison passes Tab entry/exit, Home, End, both arrow keys,
  reveal correspondence, a visible pointer point and emulated touch in both
  motions. Existing naming/visible-focus limitations remain ticket 03's work.
- No application page errors or failed requests were recorded. Discovery QA also
  recorded zero console warnings/errors and zero Formspree POSTs. Contact fields
  were keyboard traversed without activating submit. No form was submitted.

## Preservation and source integrity

Rendered baseline checks pass at all four widths for navigation/header, hero and
media declarations, context, original role, original three decision arguments,
outcome, next-project destination, contact controls, analytics and script markup.
The proposal metric remains 408 in January 2023, 1,105 in January 2024 and rounded
171% growth. The support-reduction objective is not promoted to a measured result.

All **18 original Enrollment media files** match the baseline hashes. Both asset
manifests still describe uncropped original reuse; the integration helper also
verifies their four selected sources and intrinsic dimensions. Issue 01, tickets
03/05, shared CSS/JS and original media have no diff. Product changes relative to
the pre-merge checkout affect only Enrollment HTML and its local CSS.

Discovery contrast is calculated from browser-computed foreground and ancestor
backgrounds using alpha compositing and sRGB relative luminance. Journey contrast
composites its computed foreground over the actual opaque body background. Both
measure **7.55:1** for explanation text. This is measured color evidence, not an
assumption from a shared token.

The helper verifies **76 historical report, manifest and capture artifacts**
against the saved branch commits (normalizing Git LF versus checkout CRLF only
for text). Existing slice reports and their captures were not rewritten. Tickets
02/04 retain the `resolved` state already present on their saved branches; no new
ticket or spec closure was performed. Final review/closure belongs to the parent.

## Visual and editorial inspection

Inspected these fresh captures at their recorded dimensions:

- `discovery/board-<width>-reduce.png` for all four widths.
- `journey/{eligibility,personal,portability}-<width>-reduce.png` for all four widths.
- `journey/portability-1440-no-preference.png` independently.
- `discovery/page-<width>-reduce.png` for all four widths, plus
  `discovery/page-320-no-preference.png` and `discovery/page-1440-no-preference.png`.

All paths are under [qa/integration-02-04](qa/integration-02-04/). Board orientation
is readable without deciphering the small raster notes; the four artifact groups
remain recognizable and the source's existing lower-edge clipping is retained.
Journey explanations remain readable and above the images. The eligibility
sidebar, partial personal-details attachment area and closed portability categories
remain faithful to their sources. Full-page captures show the expected sequence
through outcomes, next project and contact. Video frames can differ naturally.

Fifteen of the sixteen evidence-capture motion pairs are byte-identical. The
1440px portability pair has equal 1280 × 978 dimensions and differs at one pixel,
in bounds `[0, 181, 1, 182]` at the image edge. Both were inspected; there is no
observable content/layout loss. The integration helper initially asserted exact
byte equality for every pair and failed on this pixel. It now records equality,
hashes, dimensions and difference bounds as evidence rather than treating byte
identity as visual acceptance. No product code or captures were changed for this.

The discovery explanation identifies the CSD matrix, brainstorming, journey and
empathy map without inferring methods, sources, findings or causal links from
unreadable notes. Eligibility does not imply expanded categories or a complete
walkthrough. Personal-details guidance acknowledges the partial upload capture.
Portability remains a specific situation with closed categories, not a mandatory
three-state sequence. No new production, outcome or service-performance claim is
introduced. The original evidence-selection and factual limits remain intact.

## Remaining boundaries

Ticket 03 owns comparator relocation, explanatory limits, accessible name and
visible focus. Ticket 05 owns submission-for-analysis evidence. Neither was
implemented here; their final integrated matrix remains pending. This merge does
not assert final spec acceptance.

The existing QA hides the fixed navigation only in journey figure and preservation
section screenshots. Actual wheel/visibility tests run without that styling;
full-page discovery captures retain the navigation. No forced narrative visibility.

No real screen-reader, physical-device, production-service, MP4-playback, actual
enrollment/upload/portability or analytics-session validation was performed.
Analytics preservation checks cover declarations; they do not establish production
collection continuity. No contact submission, nested agents, PR or deployment.
