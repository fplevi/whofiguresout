# Convênios combined acceptance validation

Executed 2026-10-24 on integration production tree `9dec0e1`, after all three tickets were merged. This records new execution, separately from historical ticket results and acceptance criteria. The later mobile-first review correction has its own focused validation in `review-fix-validation.md`; final handoff below identifies its integration.

## Environment and commands

Windows, Python 3.14, existing Playwright 1.64.1, bundled Chromium 156.0.8078.4, device scale 1. The static server at `http://127.0.0.1:8110` serves `D:/Projetos/Portfolio-convenios-integration`. No dependency installed. T3 preview was tried first: two snapshots returned `Preview automation snapshot timed out after 15000ms.` Continued with the repository's documented Playwright workflow.

```powershell
python -m http.server 8110 --bind 127.0.0.1
python -u .scratch/convenios/integration-matrix-qa.py final-integration
python -u .scratch/convenios/integration-support.py D:/Projetos/Portfolio-convenios-integration http://127.0.0.1:8110 .scratch/convenios/integration-support-evidence D:/Projetos/Portfolio/.scratch/lighthouse-clarity/tools/node_modules/axe-core/axe.min.js
```

`integration-matrix-qa.py` adapts ticket 03/Billing's existing rendered-page QA, using the integration server. Its proportional-painting check accepts `object-fit: cover` for ticket 02's transparent-margin presentation as well as `contain`; neither stretches the source. No internal observer/class assertions or new test architecture.

## Actual results

- Full matrix: **104 passed / 0 failed**, 320/375/768/1440 px × normal/reduced motion, height 900 px. [Results](03-results-final-integration.json), [loaded viewport/image captures and ordinary-wheel logs](03-evidence-final-integration/).
- Supplemental reader, accessibility and artifact checks: **40 passed / 0 failed** at all four widths, height 700 px. [Results and axe findings](integration-support-evidence/support-results.json), [reader viewport captures](integration-support-evidence/).
- Every section was observed visibly during ordinary wheel traversal from the top in all normal-motion contexts, including the tall feature section. Reduced-motion content was immediately available. Captures and any screenshot-positioning jumps occur after this independent traversal.
- All images successfully loaded with nonzero natural dimensions before capture. Intrinsic dimensions, proportional painting, body loading, explanation/image DOM and mobile order, one image per row, no overlap and no horizontal overflow passed. Library remains last, wide, and visible below its explanation, without a raw link or disclosure interaction.
- The four-row sequence is card → provider network → accounts → own library. Factual copy checks passed for available map/list results, account switching without logout, the pre-Harmony product library and supported delivery. No unsupported biometric, location/distance, launch-timing, efficiency, migration or certification wording was introduced.
- Home card keyboard focus and Enter → case, return to Work, Enrollment → Convênios → Harmony, navigation and store destinations passed. Actual Tab traversal confirmed visible focus on the home card, both store links, email-copy control and contact field. Contact presence was checked without submitting the form; external app/store services were not opened.
- **Zero JavaScript page errors, console warnings/errors, failed requests or HTTP errors** in the combined matrix.
- Automated axe-core WCAG 2 A/AA and 2.1 AA: **zero violations at all four widths**, no incomplete checks returned. This is an automated audit, not screen-reader validation or certification.
- Supporting artifact checks confirm preserved metadata/analytics/hero/problem/role prefix, stores/navigation/contact/scripts suffix, home document/card and every original Convênios image. Only the case HTML/CSS and two derived images change in production. Both derivatives decode exactly to the documented source crops, including alpha; the network retains transparency. [Manifest](asset-manifest.md).

The first supplemental artifact execution returned 39/40: its home-document byte comparison mixed Git LF with Windows checkout CRLF. The corrected check compares normalized text and the complete rerun passed 40/40. No production file was changed for that harness correction.

## Visual inspection and limits

Inspected actual integrated captures of the narrow library, accounts and desktop network, plus the 768 px documentation view. Explanatory text is readable at the existing 16 px size and strong secondary contrast. The network map/list control and complete accounts phone remain recognizable; the contiguous library crop includes outlined/filled states, its heading and the full touch-area diagram. Its original small raster is soft when enlarged; no sharper replacement, invented labels or certification claim is implied. Separate loaded-image captures show content that extends below a single viewport; normal scrolling exposes it in the page.

Ticket implementers separately inspected their complete width/motion capture sets. The combined matrix checks all eight final layout/motion combinations. No Firefox, Safari, screen-reader, production app/service, live store or production analytics-continuity audit was performed. Analytics continuity is preserved by unchanged declarations/shared code and the accepted ADR; it was not re-measured in production.
