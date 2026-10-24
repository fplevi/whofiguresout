# Current Enrollment reproduction

`qa.py` and `final_checks.py` now run the combined page checks through the ticket
03 behavior suite and `final-checks-integration.py`. They cover one discovery
process board, four interface screens and one two-layer comparison. The former
pre-visual-narrative entrypoints are retained byte-for-byte as non-executable
`.txt` files in `historical-entrypoints/`; their What Shipped/generic-slider
assumptions are historical and do not describe the current page.

From the integration checkout, run a local server in a separate terminal:

```powershell
python -m http.server 8127 --bind 127.0.0.1
```

Run the matrix and final checks, using a new output directory for each new run:

```powershell
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8127/case-studies/enrollment.html'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/integration-final'
$env:PYTHONDONTWRITEBYTECODE='1'
python -u .scratch/enrollment/qa.py
python -u .scratch/enrollment/final_checks.py
git diff --check
```

The integration-final directory is the saved 2026-10-24 run. For subsequent runs,
change `ENROLLMENT_QA_OUT` to avoid overwriting it. The wrapper creates a fresh
protected-surface baseline by serving `f8f9034` markup and comparing it with the
current preserved surfaces. The matrix records the exact checked commit. The
underlying ticket 03 scripts accept the same environment overrides; their defaults
still reproduce their own historical server/output location. Ticket 02/04/05
scripts and previous integration reports remain slice/historical records.

Prerequisites: Python, Pillow, the existing Playwright Python installation under
`%TEMP%/portfolio-convenios-qa`, and its installed Chromium. No project dependency
is added. The matrix uses 320/375/768 by 700 and 1440 by 900, normal/reduced motion,
real wheel input, native range keyboard/pointer/emulated-touch interaction, image
readiness, order, fit, protected surfaces and contact-field traversal. Final checks
measure computed-color contrast, click navigation destinations, verify original
assets/manifests and historical artifacts, and compare motion-pair screenshots.
Review the six evidence captures at every width after execution. Navigation is
hidden only for isolated evidence captures; wheel/focus captures keep it visible.
No content opacity is forced and no contact message is submitted. Physical-device,
screen-reader, MP4 playback, analytics-session and production-service behavior are
outside this local QA.
