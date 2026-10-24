# Enrollment integration validation — tickets 02, 04 and 05

Date: 2026-10-24. Merger work only, in the shared integration checkout
`C:/Users/fplev/.t3/worktrees/Portfolio/integration-enrollment-visual-narrative`,
branch `integration/enrollment-visual-narrative`. No other worktree or agent was used.

The checkout began clean at `9b86741d7791c08fa0b7f043092e94a049095926`.
Merged `t3/enrollment-submission-next-steps` at
`16aa46513ce379b139e40d224f4aba7ee7e40790` with `--no-ff`, producing
`07b1a14f419d27ec121d6d324598e9d9d54da297`. No conflicts or product corrections
were necessary. The merged HTML, local CSS and submission derivative equal the
incoming branch exactly; discovery and journey evidence remain present.

## Execution

Reused the existing ticket 05 story, matrix and integrity scripts. Added the same
`ENROLLMENT_QA_URL`/`ENROLLMENT_QA_OUT` overrides already supported by tickets 02/04;
the matrix now derives its origin for navigation and local-request checks.
No shared code or dependencies changed. Served this checkout with
`python -m http.server 8126 --bind 127.0.0.1`, redirecting server logs to a file.

PowerShell reproduction, with the server running from this checkout:

```powershell
$env:ENROLLMENT_QA_URL='http://127.0.0.1:8126/case-studies/enrollment.html'
$env:ENROLLMENT_QA_OUT='.scratch/enrollment/qa/integration-02-04-05'
python .scratch/enrollment/qa-ticket-05.py green-integration
python .scratch/enrollment/matrix-ticket-05.py
python .scratch/enrollment/final-checks-ticket-05.py
```

Fresh evidence is in [integration-02-04-05](qa/integration-02-04-05/); the existing
ticket evidence and earlier integration evidence were preserved. A separate
[preservation record](qa/integration-02-04-05/merge-preservation.json) verifies
167 protected/historical files and 57 incoming historical artifacts, including
issue 01, tickets 02/04, all shared JS and the shared case-study stylesheet.

The first matrix attempt completed the six 320/375/768 combinations, then timed
out waiting for desktop images (`Page.wait_for_function: Timeout 30000ms exceeded`).
The verbose local server was writing into an undrained process-output pipe.
Restarted it with logs redirected and reran without product changes. Initial
captures and the interruption note remain separately under this fresh evidence
directory; they are not a completed matrix.

## Results and inspection

- Submission story passed. The complete rerun passed **199 checks, 0 failures**:
  320×700, 375×700, 768×700 and 1440×900, each in normal and reduced motion.
  Environment: Windows 11, Python 3.14.3, headless Chromium 156.0.8078.4,
  device scale 1, emulated touch. [Matrix](qa/integration-02-04-05/matrix.json).
- Real wheel traversal began at the top and reached every current narrative
  region and the bottom at all eight settings. Font/image readiness, positive
  natural dimensions, proportional/intrinsic dimensions, alternatives, copy-first
  order, text fit, viewport bounds and horizontal overflow checks passed.
- Comparison Tab entry/exit, Home/End/arrows, rendered reveal values/extremes,
  pointer and emulated touch passed in both motion settings. Navigation to the
  next project and back to work, navigation destinations and contact-field Tab
  order passed. Protected hero, header, context, role, outcome, contact, decision
  arguments and authored analytics/scripts matched baseline `f8f9034` in all runs.
- Measured computed foreground/background colors with alpha compositing and
  relative luminance: minimum orientation-text contrast **7.55:1**, body text
  at least 16 px. No application errors, failed requests (local or external), or
  contact POSTs were recorded in the completed run.
- Existing final checks passed: all **18 original files** unchanged, issue 01
  byte-identical in its CRLF checkout with `needs-info`, shared files unchanged,
  exact decoded RGBA crop identity and manifest mapping, and the exact one-board,
  four-screen, one-comparison selection in every run. Omitted screens remain out.
  [Integrity results](qa/integration-02-04-05/final-checks.json).
- Visually inspected submission captures at all four widths in normal motion and
  320 px reduced motion; discovery at 320/768/1440; personal details at 320/1440;
  portability at 375; eligibility at 768; and current header/outcome at 375/1440.
  Copy fits and remains independently understandable. Submission framing retains
  the protocol, notice and placeholder address; small embedded text is not fully
  readable on narrow screens. Journey sidebars and the board's organization retain
  context without reconstructing missing content. No visual correction needed.

Editorial inspection confirms submission for analysis is distinct from approval,
completed enrollment and live status consultation. Email delivery/deadline and
support reduction are not claimed as measured facts. Discovery remains synthesis
evidence; personal-details copy acknowledges the partial upload, and portability
does not become a compulsory sequence. Product files tested at merge `07b1a14`
remain unchanged by this QA/documentation follow-up. `git diff --check` passed.

## Boundary

This validates the currently merged discovery board, four interface screens and
existing comparison. Ticket 03 recovery runs separately and is not merged here.
The comparison still appears once in What Shipped, with its baseline generic
name and transparent-range focus limitation. Relocation, explanatory copy,
improved accessible naming/focus and the final all-four-ticket matrix remain
pending. This report does not certify final spec acceptance.

Screenshot capture hides fixed navigation only for isolated evidence/preservation
captures; real wheel visibility checks do not force opacity or hide navigation.
Emulated touch and browser automation are not physical-device or screen-reader
testing. Local QA does not verify production services, analytics collection,
MP4 playback, sent email, deadlines or actual enrollment/status operations.
No contact form was submitted; no PR, deployment or unrelated product edit.
