# Enrollment ticket 05 — submission and next steps

Implemented in `t3/enrollment-submission-next-steps`, worktree `C:/Users/fplev/.t3/worktrees/Portfolio/t3-c1fde48d`.

## Delivery

- Claimed ticket 05 before implementation. Read the tracker, approved spec, TDD skill and its testing references, glossary, analytics ADR, Enrollment QA/final checks, Billing narrative QA, and local conventions on the three sibling branches without merging those branches directly.
- The initial worktree was clean at `fa56b5c`; `integration/enrollment-visual-narrative` was an ancestor before work began. Own implementation commit: `bde0626`. Integrated discovery/journey work by merging the integration branch, resolving only local Enrollment CSS conflicts while retaining both evidence styles. No parent checkout or unrelated worktree was modified.
- One static confirmation figure now sits within decision 03. Its English heading, two explanatory paragraphs and specific alternative precede the image. Dense evidence uses the case width; paragraph measure remains 840 px and body type remains 16 px. Styling is local to Enrollment.
- Inspected the actual `success.png` before implementation. Its lossless presentation crop removes site navigation/footer, retaining the submission message, applicant context, protocol, next-step notice, placeholder address and return button. Source and crop mapping: [presentation-assets-05.json](presentation-assets-05.json). All 18 baseline Enrollment originals remain intact.

## Editorial review

The source says the proposal was sent for analysis. The explanation distinguishes this from approval and completed enrollment, identifies the protocol as a reference, and describes the waiting/contact instructions. It explicitly identifies the tracking address as a placeholder inside the image. No screenshot control becomes a portfolio operation or raw-image link.

The capture describes email contact within 24 hours; neither delivery nor an achieved deadline is asserted. The copy distinguishes this submission moment from the established broader status-messages/notifications argument and calls support reduction an unmeasured objective. There is no payment, production availability, live status consultation, or added impact claim. Existing 408 → 1,105 proposal figures, rounded 171%, attribution limits and original decision arguments are preserved.

## Executed validation

Primary seam: the previously approved rendered Enrollment page and observable browser behavior. Adapted `.scratch/enrollment/qa.py`, `final_checks.py` and Billing prior art into ticket-specific scripts and outputs; no new project dependencies.

- `python .scratch/enrollment/qa-ticket-05.py red` failed because the submission evidence was absent; `green` passed after implementation.
- The next dimension check failed on the authored width, then passed after correcting it to the actual 1920 px. `red-intrinsic.json` and `green-intrinsic.json` retain that cycle. The merged-page story also passed.
- `python .scratch/enrollment/matrix-ticket-05.py`: **199 checks passed, 0 failed**, across 320×700, 375×700, 768×700 and 1440×900, each with `no-preference` and `reduce`. Headless Playwright Chromium 156.0.8078.4 on Windows, device scale 1, emulated touch. Exact environment is in [matrix.json](qa/ticket-05/matrix.json).
- Every run began at `scrollY=0` and traversed the real page with `mouse.wheel(0,300)` before element jumps/captures. Visibility observations include ancestor opacity during passage, every currently integrated narrative region/figure and reaching the bottom. No forced opacity was used. Reduced-motion content was immediately available.
- Waited for fonts and positive natural dimensions after lazy loading. Verified proportional, correctly dimensioned, lazy/async images, descriptive alternatives, explanation-before-image order, no overlap or horizontal overflow, and fitting explanation/metric text at all eight combinations.
- Confirmed the currently integrated selection: one process board, three journey captures, one submission capture and one two-layer comparison. Omitted screens remain absent. Capture files cover every current evidence block at each width/motion preference.
- Tested comparator Tab entry/exit, Home, End, ArrowLeft/Right, values and rendered reveal boundaries/extremes, pointer at 25% and emulated touch at 75%, using a visible interaction point below the fixed navigation in both motion preferences.
- Compared authored browser markup for hero/header/video/poster, navigation, problem/context, existing role, outcome, next project, contact and analytics/scripts against `f8f9034` in every run. Original decision arguments also match. Actually navigated next-project and back-to-work destinations; traversed contact fields by keyboard. No contact submission or Formspree POST occurred.
- Contrast was measured from computed sRGB foreground values, alpha-composited over the ancestor background chain, then evaluated using relative luminance. Minimum explanatory-text ratio: **7.55:1**, exceeding 4.5:1; body copy remains 16 px. This is a computed rendered-color measurement, not an inference from a token name.
- Integrity checks compare all baseline original bytes, issue 01's exact CRLF checkout bytes and `needs-info` status, shared CSS/JS preservation, and decoded crop RGBA pixels against the declared source rectangle. Results: [final-checks.json](qa/ticket-05/final-checks.json).

## Inspection and failures

Inspected the source, crop, all four submission widths in normal motion, the narrow discovery/journey captures, and preserved header/outcome captures. The explanation remains readable and the image keeps the entire protocol/notice context. On narrow screens, embedded interface microtext is too small for full reading; the HTML explanation supplies the argument independently. No reconstructed or sharpened text was introduced.

The first crop-integrity check found WebP's default handling had changed invisible RGB values in the source's two transparent edge columns. Re-encoded with `lossless=True, exact=True`; decoded RGBA pixels now match the crop exactly. The visible composition was unchanged. A later integrity run correctly refused to certify a newly advanced integration tip before it was merged; the tip contained QA/documentation updates, with no page/CSS change.

No application errors or failed local assets were recorded. One run recorded an external Clarity HTTP 400 and `net::ERR_ABORTED`; the analytics markup is preserved and the external failure remains separately recorded in `matrix.json`.

## Integration boundary and limitations

This matrix includes the integrated discovery and journey slices plus ticket 05. At execution, ticket 03 had not yet reached integration: the single comparator remained in its baseline location with the baseline generic name and transparent-range focus limitation. Its keyboard/pointer/touch behavior passed. Comparator relocation, improved name/focus and removal of the old standalone section belong to ticket 03; this report does not certify them as delivered. The merger should execute the final combined matrix after all four slices arrive.

Browser automation and emulated touch do not constitute real-device or screen-reader testing. Local captures do not validate production services, analytics session collection, MP4 playback, sent email, response timing, enrollment or status services. No real contact message was sent. The final integrity record names the latest integration ancestor and tested head; ticket-specific evidence is separate from historical reports.

Post-merge closure: merged integration tip `9b86741d7791c08fa0b7f043092e94a049095926` into this branch at `25c3b737f3501d0ef7f47d6988fd04fad411bd31`. That tip changed only supporting QA/documents; page HTML and local CSS were unchanged from the full matrix run. After merging, the submission browser story and final integrity/baseline checks passed again. The final check certifies all 18 original files, byte-preserved issue 01, exact decoded RGBA crop identity, all-eight-run selection and integration ancestry.

Integration merger validation (2026-10-24): source tip `16aa465` merged without
conflicts using `--no-ff` at `07b1a14`. Fresh port-8126 QA passed the submission
story, all 199 matrix checks and integrity checks, with screenshots inspected.
An interrupted first attempt and its successful rerun are documented in the
[tickets 02/04/05 integration report](validation-integration-02-04-05.md), with
separate evidence preserving the historical ticket outputs. Ticket 03 is still
unmerged; final all-four-ticket acceptance remains pending.
