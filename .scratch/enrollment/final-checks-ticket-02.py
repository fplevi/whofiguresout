"""Ticket-specific integrity checks adapted from Enrollment final_checks.py.

Browser preservation and behavior run in qa-ticket-02.py --matrix.
"""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('ENROLLMENT_QA_OUT', str(ROOT / '.scratch/enrollment/qa/ticket-02')))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


manifest = json.loads((ROOT / '.scratch/enrollment/presentation-assets-02.json').read_text(encoding='utf-8'))
asset = manifest['assets'][0]
source = (ROOT / asset['source']).read_bytes()
assert source == git('show', f'f8f9034:{asset["source"]}')
assert hashlib.sha256(source).hexdigest() == asset['sha256']
assert struct.unpack('>II', source[16:24]) == (1672, 661)
assert asset['source'] == asset['presentation']
assert asset['cropBounds'] == {'x': 0, 'y': 0, 'width': 1672, 'height': 661}
assert not git('diff', 'f8f9034', '--name-only', '--', 'assets/images/enrollment').strip()
assert not git('diff', 'f8f9034', '--name-only', '--', 'assets/css/case-study.css', 'assets/js',
               '.scratch/enrollment/issues/01-metric-definition.md').strip()
assert git('show', 'fa56b5c:case-studies/enrollment.html') == git('show', 'f8f9034:case-studies/enrollment.html')
subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
matrix = json.loads((OUT / 'matrix.json').read_text(encoding='utf-8'))
assert matrix['summary'] == {'passed': 8, 'failed': 0}
result = {
    'sourceSha256': asset['sha256'], 'sourceAndAllEnrollmentOriginalsUnchanged': True,
    'sharedCssJsAndIssue01Unchanged': True, 'currentPreChangeHtmlEqualsF8f9034': True,
    'gitDiffCheck': 'passed', 'browserMatrix': matrix['summary'],
    'integrationTipAtCheck': git('rev-parse', 'integration/enrollment-visual-narrative').decode().strip(),
    'worktree': str(ROOT), 'branch': git('branch', '--show-current').decode().strip(),
}
(OUT / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
