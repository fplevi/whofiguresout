"""Current combined Enrollment QA. Historical entrypoints are preserved as .txt files.

See QA-README.md for the server, environment overrides and evidence boundaries.
"""
import os
from pathlib import Path
import runpy
import subprocess
import sys

root = Path(__file__).resolve().parent
os.environ.setdefault('ENROLLMENT_QA_URL', 'http://127.0.0.1:8127/case-studies/enrollment.html')
os.environ.setdefault('ENROLLMENT_QA_OUT', str(root / 'qa/integration-final'))
script = root / 'qa-ticket-03.py'
if len(sys.argv) == 1:
    sys.argv.extend(['--control', '--matrix'])
if '--baseline' not in sys.argv and not (Path(os.environ['ENROLLMENT_QA_OUT']) / 'protected-before.json').exists():
    subprocess.run([sys.executable, str(script), '--baseline'], check=True)
runpy.run_path(str(script), run_name='__main__')
