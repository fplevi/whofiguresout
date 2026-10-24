# Enrollment ticket 04 validation

Date: 2026-10-24. Scope: the three journey-organization evidence blocks only.
Branch: `feature/enrollment-ticket-04`.
Worktree: `C:/Users/fplev/.t3/worktrees/Portfolio/t3-0486efba`.
Server: `http://127.0.0.1:8104/case-studies/enrollment.html`.

## Implementation and editorial review

The second decision contains three named figures, each with one image, an English explanation before the image, and a specific alternative. Each image has its actual 1920 × 1200 intrinsic dimensions, lazy loading, and async decoding. All three originals are reused without cropping or modification; see [the manifest](presentation-assets-04.json).

Rendered inspection favored full-width blocks for all three dense screens. Putting the sidebar and main content in a narrower alternating column would reduce their useful detail. The full seven-stage sidebar remains in the eligibility image. HTML orientation stays at 16px, independently of screenshot scaling, at every width. Small raster text cannot all be read at mobile widths; the English explanations carry the argument without requiring that text to be deciphered.

Editorial review against the approved source captures and spec:

- Eligibility describes the visible guidance, seven-stage sidebar and closed relationship categories. It does not claim an expanded selection or a complete seven-screen walkthrough.
- Personal details identifies the applicant, independent of the source filename. It explains the visible document guidance and explicitly limits the partly off-screen upload area. No upload, successful submission or validation is claimed.
- Portability uses only `portabilidade-2.png`, the approved explanation/category state. It describes a particular applicant situation and closed categories, without claiming visible expanded requirements or mandatory progression through three portability states.
- No new result, production, legal eligibility, causal or service-performance claim is introduced. The images remain static evidence with no enrollment controls. No omitted screen is added. All original media, including omitted screens, remain untouched.

## Executed browser evidence

Environment: Windows, headless Chromium 156.0.8078.4, device scale factor 1. Touch is browser emulation (`hasTouch`), not a physical device. Python Playwright comes from the existing temporary `portfolio-convenios-qa` installation. No project dependency was added.

Executed commands:

```text
python .scratch/enrollment/qa-ticket-04.py eligibility red
python .scratch/enrollment/qa-ticket-04.py eligibility green
python .scratch/enrollment/qa-ticket-04.py personal red
python .scratch/enrollment/qa-ticket-04.py personal green
python .scratch/enrollment/qa-ticket-04.py eligibility regression
python .scratch/enrollment/qa-ticket-04.py portability red
python .scratch/enrollment/qa-ticket-04.py portability green
python .scratch/enrollment/matrix-ticket-04.py
python .scratch/enrollment/final-checks-ticket-04.py
git diff --check
```

The three initial story tests failed because their named evidence was absent; each passed after its corresponding implementation. Results are retained as `*-red.json` and `*-green.json` in [qa/ticket-04](qa/ticket-04/).

The complete current-page matrix passes **166 checks, zero failures**: [matrix.json](qa/ticket-04/matrix.json). It covers 320 × 700, 375 × 700, 768 × 700 and 1440 × 900, each with `no-preference` and `reduce` motion. For every combination it verifies:

- A fresh page starts at scroll position zero, then real wheel events traverse the page before any element jumps. Every narrative section, decision heading and evidence figure is observed in the viewport with visible ancestors. No section remains hidden. Normal-motion scrolling pauses 600ms after each 250px wheel event to let the existing 500ms entrance complete. Reduced-motion content is available immediately.
- All images have loaded and have positive natural dimensions before captures. Each selected image retains its ratio, with explanation before image in the DOM and on screen. Text remains 16px. Neither the page nor any main-content element overflows horizontally; caption and image do not overlap.
- The single existing comparison supports Tab entry/exit, Home, End, both arrow keys, a visible pointer interaction point and emulated touch. The input values match the visible clipping extremes and handle position. Motion/render updates settle before readings.
- There are no application `pageerror` events, failed local image requests, or other failed requests recorded in this run. This is local browser evidence, not production-service validation.

For each width, I inspected all three `eligibility-*-reduce.png`, `personal-*-reduce.png` and `portability-*-reduce.png` captures (12 figure captures). The corresponding 12 normal-motion captures are byte-identical: [motion-capture-comparison.json](qa/ticket-04/motion-capture-comparison.json). This provides the same inspected composition in both modes. Full current-page captures are `page-<width>-<motion>.png`. The fixed portfolio navigation is hidden only during figure/section evidence screenshots, following the existing QA pattern; visibility is never forced on narrative content. Wheel checks run beforehand without that screenshot styling.

## Preservation and contrast

[final-checks.json](qa/ticket-04/final-checks.json) compares the current rendered markup with an independently served `f8f9034` version of Enrollment at all four widths. Header/navigation, hero/header copy and media, problem/context, original role account, all three decision arguments, outcome/metric, next project, contact controls, analytics and other script declarations match exactly. Contact inputs were keyboard-traversed; the form was never submitted. The comparison's inherited naming/focus style also matches baseline.

All **18 original Enrollment media files** have matching SHA-256 hashes against `f8f9034`. Issue 01 matches baseline with checkout newline normalization and has no Git diff. Shared CSS/JS, home and other case pages have no changes from this ticket.

Contrast is measured from browser-computed colors, not inferred from a token name. Orientation foreground `rgba(242, 242, 245, 0.65)` is composited over its actual `rgb(13, 15, 26)` body background to `[161.85, 162.55, 168.35]`, then checked using sRGB linearization and WCAG relative luminance. The resulting ratio is **7.55:1** at all four widths.

## Failures corrected and limits

- The initial matrix retained in [matrix-initial.json](qa/ticket-04/matrix-initial.json) reported 18 harness timing failures: 110ms wheel intervals outran entrance fades, and immediate reduced-motion reads preceded range rendering. No sections remained hidden after that run. Corrected waits produce the passing matrix without changing shared animation/comparison code or forcing opacity.
- Initial QA also encountered Windows console Unicode encoding and CRLF-versus-Git-LF comparison problems. The harness now emits UTF-8 and normalizes the issue-document comparison. No issue 01 content changed.
- The inherited comparison input has opacity zero, making its own focus outline invisible; there is no parent focus outline/shadow. The existing generic name is `Comparison slider`. These are baseline limitations for the exploration/comparison ticket 03, not changes introduced by ticket 04. Keyboard/pointer/touch operation passes; visible-focus acceptance for the final combined page is not claimed here.
- Discovery, relocation/editorial enhancement of the comparison, and submission-confirmation evidence are other tickets. This slice tests the whole current page, which contains these three new interface figures and the original comparison. It does not claim the future five-new-image final integration matrix.
- No real screen-reader, physical-device, production, MP4-playback, enrollment-service, upload, portability-service or contact-submission validation was performed. Analytics declarations and local loading are preserved; real session continuity was not newly tested.

## Integration handoff

Before editing, `git merge-base --is-ancestor integration/enrollment-visual-narrative HEAD` succeeded with both at `fa56b5c740505ab7e46ef04760cd38315a0b245b`. Work remained confined to this worktree. The latest integration merge and post-merge verification will be recorded before final handoff; this branch must be merged by the integration owner, not by this ticket's implementation agent.
