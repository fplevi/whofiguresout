# Enrollment desktop composition correction

Date: 2026-10-24. Implemented directly on local `master`, runtime commit `bc79a8d`.
This follows the user's request to make text and images alternate side by side
as in Billing, superseding the former wide-image presentation choices.

## Design and scope

Reading this as a targeted portfolio correction for people evaluating the design
work, preserving its existing editorial language and Billing's copy/media pattern.
Existing dark background, orange accent, Inter/Fraunces type, spacing tokens,
radii, routes, headings, wording, navigation, hero and interactions are preserved.
Design variance, motion intensity and density stay at their existing levels;
only evidence composition changes. No new library, generated image or motion.

All six rows use CSS Grid. Above 1024 px, copy occupies approximately one third
and media two thirds, with the existing 64 px gap. Discovery, eligibility and
portability have media on the right; the comparator, personal details and
submission confirmation have media on the left. Rows are capped at 1440 px.
At 1024 px and below, copy precedes the image in a single column. DOM order
always remains copy first. Original images and their aspect ratios are unchanged.

## Executed validation

The existing rendered-page QA was adapted to check alternating desktop placement,
bounded media size and copy-first mobile stacking. The complete normal/reduced
motion matrix passed **316 checks, zero failures**, at 320 × 700, 375 × 700,
768 × 700 and 1440 × 900. It covers real wheel traversal from the top, all evidence
loading and proportional sizing, no overflow or clipping, native range keyboard,
pointer and emulated-touch operation, visible focus, protected surfaces and
contact fields without submitting the form.

Supplementary layout checks passed at 375, 1024, 1280, 1440, 1920 and 2560 px
with a 900 px viewport height and reduced motion. Media widths were respectively
327, 976, 704, 811, 917 and 917 px. Desktop media stays below native image width,
alternates correctly and no longer occupies the entire row. All six evidence
blocks were captured at 375, 1440 and 1920 px. Visually inspected discovery,
eligibility, personal-details, comparator and submission captures at 1440 px,
plus mobile discovery. No source text was reconstructed or image sharpened.

Evidence is under [qa/desktop-alternation](qa/desktop-alternation/): the matrix is
`validation.json`, supplementary geometry is `desktop-layout.json`, and captures
are `layout-<width>-<row>.png` plus the existing matrix capture names. Historical
evidence was not overwritten. The machine report records its base `b5e9f6b`;
the runtime working files already contained this correction throughout that run
and were committed as `bc79a8d` without further product changes.

Computed-color contrast remains at least **7.55:1** for 16 px guidance. Actual
navigation clicks, all 18 original assets, source manifests, submission crop pixel
identity, the pending metric issue, authored head/analytics declarations and
unrelated shared code passed preservation checks. Shared code uses pre-correction
master `b5e9f6b` as its baseline so other completed projects are retained.

The complete final integrity suite also passed, including historical artifact
preservation and 24 normal/reduced evidence pairs. Twenty-three pairs are pixel
identical; the desktop comparator pair differs only within a 5 × 1 px edge region
in the blue channel, with unchanged dimensions and no visible content change.

Reproduce with a server from the root checkout on port 8130:

```powershell
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8130/case-studies/enrollment.html'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/a-new-desktop-run'
$env:ENROLLMENT_RUNTIME_REVISION='bc79a8d'
$env:ENROLLMENT_PRESERVATION_REVISION='b5e9f6b'
$env:PYTHONDONTWRITEBYTECODE='1'
python -u .scratch/enrollment/qa.py
python -u .scratch/enrollment/final_checks.py
```

Environment: Windows, Python/Playwright Chromium from the existing temporary QA
installation; exact browser/OS versions are in `validation.json`. Browser touch is
emulated. No physical-device, screen-reader, production-service or MP4-playback
validation, deployment, push or contact submission is claimed.

## Harness limitations corrected

The collaborative preview timed out twice with “Preview automation snapshot timed
out after 15000ms”; validation used the repository's documented Playwright workflow.
The initial matrix metadata referenced a deleted integration branch; it now records
the current branch. The old desktop assertions required full-width images and
copy above them, so they now check the requested responsive layout. Integrity
checks accept an explicit authorized runtime revision and current shared-code
baseline. The metric issue comparison now normalizes Git/Windows line endings,
preserving its actual content rather than relying on one checkout's byte hash.
