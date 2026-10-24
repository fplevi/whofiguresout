"""Artifact integrity alongside the approved browser seam; no browser substitute."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageChops

BASE = 'f8f9034fb32de4b7839ac0a003db2bb791af883e'
checks = []


def check(name, ok):
    checks.append({'name': name, 'ok': bool(ok)})


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'])


# Every pre-existing file outside the one authorized HTML edit is unchanged.
changed = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=MD', BASE], text=True).splitlines()
check('only authorized existing files changed', set(changed) <= {
    'case-studies/harmony.html', '.scratch/harmony/issues/01-fundamentos-compartilhados.md'})
sources = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'assets/images/harmony'], text=True).splitlines()
for path in sources:
    check(f'original bytes preserved: {path}', Path(path).read_bytes() == original(path))
for path in ['.scratch/harmony/spec.md', '.scratch/harmony/visual-narrative-review.md',
             '.scratch/harmony/validation.md', '.scratch/harmony/copy-draft.md']:
    check(f'historical document preserved: {path}', Path(path).read_text(encoding='utf-8') == original(path).decode().replace('\r\n', '\n'))

before = original('case-studies/harmony.html').decode().replace('\r\n', '\n')
after = Path('case-studies/harmony.html').read_text(encoding='utf-8')
for label, pattern in [
    ('navigation', r'<header>.*?</header>'),
    ('hero and intro', r'<main>.*?<!-- The Problem -->'),
    ('problem and role', r'<!-- The Problem -->.*?<!-- The Decisions -->'),
    ('outcome, work in progress, next project, contact and footer', r'<!-- The Outcome -->.*'),
]:
    # The section marker preceding the new foundations changed; compare the
    # retained problem/role content up to that boundary, excluding the marker.
    if label == 'problem and role':
        old = before.split('<!-- The Problem -->')[1].split('<!-- The Decisions -->')[0].rstrip()
        new = after.split('<!-- The Problem -->')[1].split('<!-- Shared foundations:')[0].rstrip()
    else:
        old, new = re.search(pattern, before, re.S)[0], re.search(pattern, after, re.S)[0]
    check(f'preserved HTML: {label}', old == new)
check('all analytics and other script tags preserved', re.findall(r'<script\b.*?</script>', before, re.S) == re.findall(r'<script\b.*?</script>', after, re.S))
for heading in ['React + Next.js for the product ecosystem', 'Accessibility and content in component design']:
    pattern = r'<h3[^>]*>' + re.escape(heading) + r'</h3>.*?</p>\s*<p.*?</p>'
    check(f'preserved maintenance/accessibility argument: {heading}', re.search(pattern, before, re.S)[0] == re.search(pattern, after, re.S)[0])

manifest = json.loads(Path('.scratch/harmony/image-manifest.json').read_text(encoding='utf-8'))
for record in manifest['derivatives']:
    path = Path(record['derivative'])
    source = Image.open(record['source']).convert('RGB')
    expected = Image.new('RGB', record['dimensions'], record['background'])
    for fragment in record['fragments']:
        expected.paste(source.crop(fragment['crop']), fragment['pasteAt'])
    actual = Image.open(path)
    check(f'manifest and faithful source pixels: {path.as_posix()}',
          list(source.size) == record['sourceDimensions'] and
          hashlib.sha256(Path(record['source']).read_bytes()).hexdigest() == record['sourceSha256'] and
          actual.format == 'PNG' and list(actual.size) == record['dimensions'] and
          path.stat().st_size == record['bytes'] and
          ImageChops.difference(expected, actual.convert('RGB')).getbbox() is None)
check('every derivative used and old pair absent from rendered HTML',
      all(Path(r['derivative']).name in after for r in manifest['derivatives']) and
      'harmony-antes' not in after and 'harmony-depois' not in after)
result = {'baseline': BASE, 'checks': checks,
          'summary': {'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}}
Path('.scratch/harmony/qa/completed-artifact-integrity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result['summary']))
for c in checks:
    if not c['ok']:
        print('FAIL', c['name'])
raise SystemExit(bool(result['summary']['failed']))
