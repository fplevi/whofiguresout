# Enrollment ticket 02 — discovery synthesis

Implemented only the discovery-synthesis slice in worktree `C:/Users/fplev/.t3/worktrees/Portfolio/t3-dde0ded8`, branch `t3/enrollment-discovery-synthesis`. Starting HEAD and integration tip were `fa56b5c740505ab7e46ef04760cd38315a0b245b`; the integration ancestry check passed before edits. Server: `http://127.0.0.1:8102/case-studies/enrollment.html`.

## Delivered behavior

One wide discovery board follows the unchanged My Role account and precedes The Decisions. Its English heading and two explanatory paragraphs precede the image in the DOM and on screen. The copy identifies the CSD matrix, brainstorming areas, user/customer journey, and empathy map. It distinguishes the supplied Desk Research label from established methods/sources, and does not infer findings, participants, workshop authorship or note-to-decision causality. The source's existing lower-edge clipping is acknowledged. The original discovery account remains verbatim.

The composite PNG is reused at its full 1672 × 661 extent, with a specific alternative, intrinsic dimensions, lazy loading and asynchronous decoding. No image manipulation, reconstruction, new controls or raw-image links. Local rules in `assets/css/enrollment.css` supply the strong secondary text color and proportional wide image. Shared CSS/JS and all original assets remain unchanged. See `presentation-assets-02.json` for source, bounds, dimensions, format, rationale and SHA-256.

## Executed QA

The existing Enrollment `qa.py` and `final_checks.py` were adapted into ticket-specific scripts; Billing's visual-narrative QA supplied image-readiness and wheel-traversal patterns. No project dependencies were added. The user-approved seam is the rendered Enrollment page.

- `python .scratch/enrollment/qa-ticket-02.py`: red before implementation, failed with “Expected one dedicated discovery-synthesis region”; then green after implementation. Recorded in `qa/ticket-02/red.json` and `green.json`.
- `python .scratch/enrollment/qa-ticket-02.py --matrix`: eight viewport/motion combinations passed. Widths 320, 375 and 768 use height 700; width 1440 uses height 900. Each width runs `no-preference` and `reduce`, at device scale 1.
- Every matrix run starts at scrollY 0 and traverses the entire current page with real `mouse.wheel(0, 300)` input. Every narrative section, next project and contact becomes visible. No forced opacity or element jumps replace this path. Reduced-motion sections are also checked immediately after load.
- Fonts and all images are ready before captures. The board loads at positive natural dimensions, retains its intrinsic ratio, fits the viewport, follows its explanation, and adds no controls. Body copy remains 16 px; headings retain the existing 48 px system. Explanatory text has no clipping or overlap and the page has no horizontal overflow. Outcome numbers fit.
- Contrast is calculated from browser-computed sRGB colors, alpha-compositing foreground over actual ancestor backgrounds and applying relative luminance. Explanation: `rgba(242, 242, 245, 0.65)` over `rgb(13, 15, 26)`, **7.55:1**. Heading contrast also exceeds 4.5:1. This measures rendered colors rather than assuming token compliance.
- Existing comparison: Tab entry/exit, Home/End and both arrow keys, reveal position/clipping, pointer click and emulated touch tap pass in all eight combinations. Contact fields and submit button are present; no real message is sent.
- Current rendered navigation/header, hero/video/poster, context, original role, outcome, next project, contact and analytics/script markup match an independently served `git show f8f9034:case-studies/enrollment.html` baseline. Runtime entrance styles on section roots are excluded from markup equality and checked separately through the wheel path. The pre-change `fa56b5c` HTML equals `f8f9034`.
- `python .scratch/enrollment/final-checks-ticket-02.py`: original source byte/hash/dimension fidelity, all Enrollment originals unchanged, issue 01 unchanged, shared CSS/JS unchanged, baseline equivalence and `git diff --check` pass.
- No JavaScript page errors, console warnings/errors, failed requests, failed local assets or Formspree submissions were recorded in the successful matrix.

Environment: Windows 11 `10.0.26300`, Python 3.14.3, headless Playwright Chromium `156.0.8078.4`, using the existing temporary installation under `%TEMP%/portfolio-convenios-qa`. Machine-readable results and wheel positions are in `qa/ticket-02/matrix.json` and `final-checks.json`.

## Review, failures and limits

Editorial review: the HTML explanation is self-contained without reading the tiny sticky notes. No new research findings, source review, sample, workshop participation or causal claim is introduced. The established discovery activities remain in My Role. Proposal-growth and unmeasured support-reduction wording are untouched. The four named areas stay within the uncropped original; nothing missing below the source edge is reconstructed.

The initial broader QA compared reduced-motion runtime styles to normal-motion styles and rejected otherwise unchanged sections. The check now compares authored content and tests animated visibility separately. A second harness issue read the native comparison's reveal before the browser settled; an 80 ms wait resolves it without product changes. The diagnostic `matrix-before-settle-fix.json` records the latter failed run. Element screenshots initially let the fixed nav overlap the heading; the final capture workflow returns to top after the wheel test and clips the full-page render at document coordinates, without hiding the nav or altering content.

The existing comparison's transparent range focus and generic accessible name are preserved baseline limitations assigned to ticket 03. This slice does not claim their remediation. Browser automation and emulated touch are not real screen-reader or physical-device validation. Local screenshots and preserved media markup do not establish MP4 playback or production-service behavior. No contact submission or real enrollment operation was performed.

This is the current complete page for ticket 02, not the final future-slice matrix: the four interface images and comparison relocation belong to tickets 03–05. Their acceptance is not claimed here. Issue 01 remains open and unmodified.

## Final integration check

Final screenshots, inspected evidence list, merge result and post-merge rerun are recorded below after execution.
