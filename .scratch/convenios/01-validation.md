# Ticket 01 — provider-network evidence

Executed 2026-10-24 in the isolated worktree `C:/Users/fplev/.t3/worktrees/Portfolio/t3-faceaf1e`, branch `t3/add-network-visual-row`. Integration checkout was not edited. Initial clean HEAD `f8f9034` was an ancestor of `integration/convenios-visual-narrative`; merged by fast-forward to `78a853d` before implementation. A second merge before final GREEN reported `Already up to date.`

## Scope and test seam

Approved seam: the rendered page and externally visible browser behavior. Adapted `.scratch/billing/visual-narrative-qa.py` and the previous `.scratch/convenios/validation.md`; no new unit seam, dependency or app architecture. Tests use accessible headings, articles, images and links. Geometry, loaded-image state and screenshots are observations of the rendered page.

Added the network row between card and accounts, factual English map/list copy, a transparent presentation crop and case-local styling. Removed only the unsupported biometric-login phrase from the card. Accounts, library and conclusion remain owned by tickets 02/03. Shared CSS/JS, hero, home card, navigation, contact, metadata and analytics were not edited.

## RED → GREEN

Commands (from this worktree; port 8111 was unused before starting this server):

```powershell
python -m http.server 8111 --bind 127.0.0.1
python .scratch/convenios/01-network-qa.py red
python .scratch/convenios/01-prepare-network.py
python .scratch/convenios/01-network-qa.py green
```

- RED before implementation: **44 passed, 16 failed**, process exit 1. The failures were the missing network explanation and unsupported biometric phrase in all eight viewport/motion combinations. [Actual RED results](01-evidence/01-red-results.json), [pre-change features](01-evidence/01-red-features-320.png).
- An early exploratory wheel check moved faster than the 500 ms entrance transition and incorrectly counted sections before they finished appearing. The retained RED run waits 550 ms after each 300 px normal-motion wheel input; all section visibility checks passed before implementation. An image `object-fit: contain` also preserves painted proportions when its element box has a height cap; the retained check accounts for that existing behavior.
- First GREEN matrix passed; a Windows cp1252 stdout error interrupted the subsequent adjacent-case reporting. Explicit UTF-8 stdout fixed the QA harness. The complete final execution then exited 0: **109 passed, zero failed**, with **zero captured page errors, failed requests or HTTP errors**. [Final GREEN results](01-evidence/01-green-results.json).
- Final matrix: **320 / 375 / 768 / 1440 × normal / reduced motion**, 700 px viewport height. Ordinary wheel traversal starts at the top and reaches the bottom before any capture scrolling. Every section became visible in normal motion; reduced-motion content was immediately available. No case-local animation remedy or shared script change was necessary.
- Network explanation precedes its image in DOM and at widths through 768; desktop places the image on the left. One static image, no extra label, raw-image link or disclosure. Loaded images have nonzero natural dimensions and preserve their painted proportions. Network alt text, intrinsic dimensions and lazy/asynchronous loading were checked. No horizontal overflow or copy/image overlap.
- Home card → case → Work and Enrollment → Convênios → Harmony were exercised. Navigation/store hrefs, hero, metadata, analytics declarations and contact form presence were checked. Keyboard traversal reached navigation, stores, adjacent project, email-copy button and contact fields with visible outlines. [Store focus](01-evidence/01-keyboard-store-1440.png), [contact focus](01-evidence/01-keyboard-contact-1440.png). Form not submitted; external store destinations not opened.

## Visual inspection and assets

Inspected the original PNG, resulting WebP, loaded network images and all eight network-row captures. At 320/375 the map, pins, header and list-view control remain recognizable; app microcopy is naturally small, while the adjacent 16 px explanation states the map/list meaning explicitly. No phone edges or relevant controls are cut. At 768 the image is centered below its explanation; at 1440 the lateral composition has clear separation. Explanatory text uses the existing strong secondary color, with calculated contrast approximately **7.55:1** against the actual page background; font size is unchanged.

Inspected loaded-page captures as preservation evidence for the hero, card, other rows and contact. Library legibility and its raw link are pending ticket 03, and account wording is pending ticket 02; this ticket does not claim those fixes. Existing documentation remains the last feature evidence.

Evidence naming: `01-evidence/01-network-{width}-{no-preference|reduce}.png` records complete network rows; `01-network-image-*` records the real loaded image; `01-loaded-page-*` records the complete loaded page. Final full-page captures were taken after wheel traversal and all images reported loaded, then network rows cropped from them with no fixed-nav overlay. The historical RED section capture includes a fixed-nav overlay and is only evidence of the pre-change wording/absence.

The crop is lossless RGBA WebP, **430 × 686**, source bounds **[330, 48, 760, 734]** (right/bottom exclusive). Decoded output pixels equal the source crop, including transparent pixels. The source PNG is unchanged. [Asset record](assets/01-network.json) includes source hash, bounds, dimensions, format, purpose and unchanged hero/card records; [reproduction script](01-prepare-network.py) writes only ticket 01's derivative and record.

## Environment and limits

Windows; Python 3.14.3; Playwright 1.64.1; Chromium 156.0.8078.4; Pillow 12.3.0. The T3 preview status was inspected, an own tab opened and navigation succeeded. Two snapshot calls returned `Preview automation snapshot timed out after 15000ms.`; browser QA used the explicitly authorized repository Playwright workflow. No dependencies installed.

No new axe, screen-reader, Safari/Firefox, live app/service, production analytics continuity or live-store validation. Analytics preservation is supported by unchanged source declarations, not a new production audit. No PR created. Ticket remains `claimed` for integration review.
