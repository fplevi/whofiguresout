"""Current combined Enrollment integrity/contrast checks; see QA-README.md."""
import os
from pathlib import Path
import runpy

root = Path(__file__).resolve().parent
os.environ.setdefault('ENROLLMENT_QA_URL', 'http://127.0.0.1:8127/case-studies/enrollment.html')
os.environ.setdefault('ENROLLMENT_QA_OUT', str(root / 'qa/integration-final'))
runpy.run_path(str(root / 'final-checks-integration.py'), run_name='__main__')
