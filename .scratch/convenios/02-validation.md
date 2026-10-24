# Ticket 02 — accounts without logout

Executed 2026-10-24 in the isolated checkout `C:/Users/fplev/.t3/worktrees/Portfolio/t3-497a9714`, branch `t3/accounts-no-logout`.

## Scope and factual basis

The accounts row now states: “Multiple accounts can stay signed in on one device. Members can switch between them without logging out.” Removed the unrelated notifications, authorization and statement claims. The recorded author confirmation and Behance board 12 support persistence without logout; the static mockup alone does not. No historical requirement, motivation or individual authorship is asserted. The alt describes the three saved profiles, selection and add/switch controls actually visible.

The accounts-only portrait frame crops transparent side margins in CSS. No source asset changed and no derivative was generated. Initial loaded captures at 320/375 showed the phone occupying only about 115/143px of width; the frame increases that to about 211/254px while retaining the entire phone. See `02-evidence-matrix-before/02-accounts-320-no-preference.png` and the corresponding `02-evidence-final` captures. All nontransparent source pixels remain inside the presentation crop. Source, format, dimensions, bounds and checksum: `assets/02-accounts.json`.

The seam was explicitly approved by the user: rendered page and externally observable browser behavior. This reuses `.scratch/billing/visual-narrative-qa.py` and the previous `validation.md` approach; no unit seam, app implementation or dependency architecture was introduced.

## RED → GREEN

1. Before editing the row, `02-results-red-copy.json`: **0 passed / 2 failed**. The rendered copy omitted switching without logout and attributed unrelated services to this evidence.
2. After the factual copy correction, `02-results-green-copy.json`: **2 passed / 0 failed**. These initial copy-only captures were not used to assess image loading or crop quality.
3. `02-results-matrix-before.json`: **81 passed / 4 failed**. This exploratory run used 100ms pauses between 350px wheel steps and required fully settled opacity while each section was onscreen. All sections ultimately reached opacity 1; the 500ms existing fade had not finished during some samples. This was a sampling error, not evidence of permanently hidden sections. The script now allows 650ms reading pauses. No observer, shared script or visibility override was changed.
4. After visual inspection of the loaded mobile images, added only the accounts-specific frame. `02-results-final.json`: **85 passed / 0 failed**. All sections became visible during actual ordinary wheel traversal at every width. No case-local animation remedy was necessary.

## Current browser evidence

- Windows, Python, existing Playwright **1.64.1**, bundled headless Chromium **156.0.8078.4**, device scale 1, viewport height 700 CSS px.
- Own Python HTTP server: `python -m http.server 8112 --bind 127.0.0.1`, launched from this checkout only after confirming port 8112 was unused. All QA targeted `http://127.0.0.1:8112/case-studies/convenios.html`.
- Checked T3 `preview_status`, opened a private agent-owned tab and navigated successfully. Two `preview_snapshot` attempts returned `Preview automation snapshot timed out after 15000ms.` Continued with the explicitly named repository Playwright workflow.
- Matrix: **320, 375, 768, 1440 × normal/reduced motion**. All images loaded with nonzero intrinsic dimensions before capture. No horizontal overflow; accounts explanation precedes one image in DOM and mobile; no overlap or disclosure interaction. Body copy stays 16px with measured composited contrast **7.55:1**. Image fitting preserves proportions; the portrait crop preserves transparency and the entire phone.
- Normal motion: real 350px wheel input from page top to bottom, 650ms reading pauses, recording section positions and actual opacity along the way. Every section was seen at full opacity within the viewport. Reduced motion: sections immediately visible with no entrance transform, then the same content was traversed.
- Home card → case, case → Work, case → Harmony, Enrollment → case passed. Preserved nav URLs, Google Play/App Store destinations, launch message and hero home image. Actual keyboard Tab/Shift+Tab checks confirmed visible focus for back, stores, next case, email and copy-email controls. Contact form presence checked; **not submitted**. Store/service destinations were not opened to validate production behavior.
- **No JavaScript errors or failed requests** in the eight matrix contexts.
- Captures: `02-evidence-final/02-accounts-<width>-<motion>.png`, `02-loaded-image-*`, `02-viewport-*`, `02-page-*`; focus captures `02-focus-back.png` and `02-focus-store.png`. Inspect loaded element/viewport captures for detail, rather than reduced full-page thumbnails.
- Supplemental recapture: **10 passed / 0 failed**. It uses the same loaded page and traversal, and hides the fixed nav only for element/full-page screenshots to reduce the stitched-image overlay artifact. Real viewport screenshots keep the nav and position the row 80px below the top. Results are in `02-results-recapture.json`. This is capture-only styling, never a shipped style or a substitute for visibility checks.
- Inspected the final accounts-row captures at all eight width/motion combinations, full-page context at all eight combinations, loaded-image details, mobile viewport samples and both keyboard-focus captures. The full phone and account-switcher sheet remain visible with useful surrounding context; copy and image keep a clear reading order. Fixed-navigation stitching in full-page captures is a capture artifact; the real viewport samples show the actual reading experience.

Reproduce the matrix while this checkout's server is running:

```powershell
python -u .scratch/convenios/02-accounts-qa.py .scratch/convenios/02-evidence-final .scratch/convenios/02-results-final.json
python -u .scratch/convenios/02-accounts-qa.py .scratch/convenios/02-evidence-final .scratch/convenios/02-results-recapture.json --recapture
python .scratch/convenios/02-preservation.py
```

## Preservation and limits

`02-preservation.json`: **20 passed / 0 failed** supporting source/asset checks. HTML outside the accounts row is identical to integration, including metadata, analytics snippets, hero, card, library, conclusion, nav and contact. CSS outside the accounts-only rules is identical. Home, shared styles/scripts and every Convênios original image are unchanged. Accounts PNG/WebP decode to identical RGBA pixels; only the WebP remains in the row. No extra evidence, source link, label or interactive switcher was added.

Manual visual review checks layout, readable explanatory copy, saved-profile structure, full-phone context, transparency and proportional rendering. It does not claim that every tiny profile label is independently readable at 320px. No screen-reader, Firefox, Safari, production app/service or accessibility-certification audit was performed. Existing library raw-image link, small documentation and unsupported conclusion text belong to ticket 03; provider-network insertion belongs to ticket 01. They were preserved exactly in this independently validated ticket state.

Ticket remains **claimed** for integration final review. No PR, delegation, integration-checkout write, original-root write or worktree deletion.

## Final integration sync

Initial HEAD `f8f9034` was an ancestor of integration `78a853d`; merged integration by fast-forward before implementation. Implementation/evidence commit: `ca360f8107b5ef33cd546f48897d24698ba6dc26`.

After committing, ran `git merge integration/convenios-visual-narrative` again: **Already up to date**, current integration tip `78a853df61a4de9cce4c67d23f4e77880daeb31a`. `git merge-base --is-ancestor integration/convenios-visual-narrative HEAD` succeeded. No conflicts or other-ticket changes were present to resolve. Rechecked preservation: **20 passed / 0 failed**. Post-merge rendered-copy smoke: **2 passed / 0 failed**, `02-results-postmerge.json` and `02-evidence-postmerge/02-copy.png`. The full matrix remains applicable because integration introduced no additional code after that run.
