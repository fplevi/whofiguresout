# Enrollment ticket 03 validation

Date: 2026-10-24. Current branch: `t3/enrollment-visual-narrative` (the checkout was initially named `t3/6485afe7`). Worktree: `C:/Users/fplev/.t3/worktrees/Portfolio/t3-6485afe7`. Local server: `http://127.0.0.1:8123/case-studies/enrollment.html`.

## Recovery and scope

The clean starting checkout was `fa56b5c740505ab7e46ef04760cd38315a0b245b`, the integration tip at the initial ancestry check. `git merge-base --is-ancestor integration/enrollment-visual-narrative HEAD` succeeded before work. The existing `t3/enrollment-plan-comparison` branch at `66ebc772bd3b37cbd804b0b589f13eb2390cf444` was merged here, preserving its original worktree and history. Its uncommitted changes were all QA evidence: 28 PNGs and a newer eight-case JSON with 220 passing checks. Those 29 files are preserved in [qa/ticket-03-recovery](qa/ticket-03-recovery/README.md), with their provenance distinguished from fresh validation.

The discovery and journey slices were subsequently merged from integration tip `501ec0e8c9120c261985719600d45637fb49793c`; the resulting tested runtime commit was `65ded778735c78414e788d37d99582a0d17c5fde`. No other checkout was written. Ticket 05 was not implemented. This report covers ticket 03 and the complete page currently containing discovery, three journey screenshots and the comparison. It does not claim the final five-new-image matrix, which still needs submission-confirmation evidence.

## Delivered behavior and editorial review

The original two-image native-range comparison appears once, within the first exploration decision and before the second decision. The old What Shipped section is removed. The hero and its related poster remain intact. Guidance precedes the comparison in the DOM and on screen, explaining separate plan cards versus aligned benefit rows. It explicitly distinguishes that organization from equivalent products/prices, cheaper prices, a smaller catalog, or proof that no account or personal data is required. The established account-free-exploration decision remains unchanged above it.

The control is named “Compare plan cards before and plan benefits after”, references visible instructions, and has a visible orange frame when keyboard-focused. Home reveals After and End reveals Before, as stated in the page. The original range behavior and both 1440 × 1485 JPEGs are retained. Opaque local label backgrounds and dark arrows on the white handle correct the measured inherited contrast failures. All presentation styles remain in Enrollment's stylesheet. [presentation-assets-03.json](presentation-assets-03.json) records uncropped source reuse, full bounds, dimensions, format, rationale and hashes. No derivatives, raw-image links, galleries or disclosure controls were introduced.

Editorial review also checked the merged discovery and journey copy: discovery artifact organization is distinguished from verified research methods/findings; eligibility retains its sidebar and closed-category context; personal details acknowledges the partial upload capture; portability remains a particular situation with closed categories. The HTML explanations carry the argument on mobile, independently of tiny raster text. No new result or production claim was added. The outcome still reports 408 proposals in January 2023 and 1,105 in January 2024, a rounded 171% increase, without equating proposals to completed enrollments or assigning exclusive causality. Support reduction remains an unmeasured objective.

## Executed checks

The repository TDD skill was read and used at the user-approved rendered Enrollment page seam. Existing Enrollment `qa.py` / `final_checks.py` and Billing narrative QA were adapted into ticket-specific scripts; no project dependencies were added.

Recovered red/green evidence remains under `qa/ticket-03`: placement initially failed because the comparison followed the decisions; the named-control test failed on the generic slider name; the focus test failed on the invisible native input outline; contrast failed at 3.35:1 for labels over a white raster. The original implementation fixes and its passing evidence are preserved, rather than recreated or discarded during recovery.

Fresh commands on port 8123:

```text
python -u .scratch/enrollment/qa-ticket-03.py --control --matrix
python .scratch/enrollment/final-checks-ticket-03.py
git diff --check
```

The fresh matrix passed **244 checks, zero failures**, across 320 × 700, 375 × 700, 768 × 700 and 1440 × 900, each with `no-preference` and `reduce`. Environment: Windows, Python 3.14.3, headless Playwright Chromium 156.0.8078.4, device scale 1, existing `%TEMP%/portfolio-convenios-qa` installation, emulated touch.

- Every case starts at scrollY zero and traverses the complete page with actual wheel events before screenshots or element jumps. Normal-motion scrolling waits 550ms per 240px event for the existing entrance fade. All narrative headings are encountered with visible ancestors, every section becomes visible, and no opacity override is used. Reduced-motion sections are immediately available.
- Fonts and all images are ready with positive natural dimensions before captures. Images retain their source proportions; comparison dimensions, specific alternatives, lazy loading and async decoding pass. Guidance remains 16px, precedes the wide comparison, and does not overlap it. The discovery and three journey blocks each retain one image, explanation-first order, 16px orientation, specific alternatives and viewport fit. No horizontal page overflow occurs.
- Tab enters the named comparison and exits to the next project; Shift+Tab returns. Focus is visibly framed. Home, End, ArrowLeft and ArrowRight update the input and rendered handle/clipping. Endpoint screenshots are compared to the independent source JPEG rasters. Pointer clicks and emulated touch drags operate below the fixed navigation, and their resulting values match the visible reveal.
- Contact fields and the copy-email control are visible; no real message was submitted. Actual clicks verify the logo, back link, Work, Contact, About and next-project destinations. Preserved rendered head/header, hero/media, context, original role, outcome, next-project and contact surfaces match the independent `f8f9034` / pre-change snapshots after excluding section-root animation styles and runtime-injected Clarity scripts. Authored head and analytics declarations are separately compared exactly with `f8f9034`.
- Source bytes/hashes and the manifest match baseline. There is no Git diff for any Enrollment original, shared CSS/JS or issue 01. Issue 01 retains `needs-info`; its working-file SHA-256 also matches the untouched recovery checkout: `b7d1b0127a8fb45274b3e04c78bba05a46f5c32f5d89827cbfd5eca8309ef2e2`.
- WCAG relative sRGB luminance uses browser-computed colors and alpha compositing. Guidance `rgba(242,242,245,.65)` over `rgb(13,15,26)` measures **7.55:1**. White labels over the opaque dark background and dark arrows over the white handle each measure **19.08:1**. The label calculation also checks a worst-case white underlying image. See `contrast.json` and `final-checks.json`.

No page errors, console warnings/errors, failed requests or HTTP errors were recorded in the passing eight-case run. Fresh machine-readable evidence is [qa/ticket-03/validation.json](qa/ticket-03/validation.json).

## Visual inspection, failures and limitations

Inspected the `*-no-preference-evidence.png`, `*-no-preference-focus.png` and all four `*-no-preference-enrollment-*.png` evidence blocks at each of the four widths. Also inspected the four reduced-motion comparison evidence captures. All 20 static comparison/discovery/journey evidence pairs across normal and reduced motion have identical dimensions and pixels: `motion-evidence-comparison.json`. Explanations wrap without clipping, comparison labels and focus remain visible, the discovery board's artifact groups remain recognizable, and journey sidebars/source bounds are retained. Raster microtext remains small at narrow widths; the HTML orientation remains readable without enlarging raw images. The screenshot workflow hides the fixed nav only for isolated element captures; viewport/focus captures and wheel traversal retain it. This styling does not force narrative visibility.

The recovered first matrix attempt read a keyboard reveal before rendering settled; its diagnostic is retained as `matrix-first-attempt.json`. The recovered code waits for the corresponding handle state before assertions. The first fresh post-merge attempt passed all four normal-motion cases, then failed a whole-head preservation equality check at 320px reduced motion. Three diagnostic reloads passed. Inspection showed the saved baseline contained asynchronously injected vendor scripts; whole-head equality was timing-sensitive. QA now removes only those injected Clarity tags from both snapshots and separately asserts exact authored head/analytics source equality. The failed attempt remains in `postmerge-before-preservation-settle.json`. No product code changed to satisfy that harness correction.

Browser automation and emulated touch do not establish physical-device or screen-reader behavior. Local captures do not validate MP4 playback, real enrollment services, uploads, production availability or analytics session continuity. No actual contact submission or enrollment operation was performed. Ticket 05 and the final discovery/four-interface-screen/comparison matrix remain pending with the integration owner.

## Latest integration check

Integration advanced to QA/documentation commit `9b86741d7791c08fa0b7f043092e94a049095926` during this run; its HTML/CSS runtime is unchanged. Own validation/evidence was committed as `5679d50`, then that integration tip was merged into this branch as `61a19d397102dd224cf637724c900a78f5f74f89`. The ancestry check passed. Post-merge final checks passed again: measured contrast, actual navigation, authored head/analytics equality, originals/manifest, shared source and issue 01 preservation. `git diff --check` passed.

The complete currently integrated page was rerun after that merge on port 8123: **eight cases, 244 passing checks, zero failures**. Every case completed wheel traversal from the top and all comparison/evidence/preservation checks. No page errors, console warnings/errors, failed requests or HTTP errors were recorded. `validation.json` identifies tested commit `61a19d3` and integration tip `9b86741`. The later handoff commit changes only this report, the ticket completion note and QA evidence; runtime HTML/CSS is unchanged. Ticket 03 is resolved. Ticket 05 remains ready for its independent implementation and final integration validation.
