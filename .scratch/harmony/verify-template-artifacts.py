"""Ticket 03 artifact integrity; complementary to rendered-browser acceptance."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageChops

BASE = '2a58eb63b2ca1d5cad14ee3047370be4e826f436'
checks = []


def check(name, ok):
    checks.append({'name': name, 'ok': bool(ok)})


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'])


sources = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'assets/images/harmony'], text=True).splitlines()
for path in sources:
    check('pre-existing image bytes preserved: ' + path, Path(path).read_bytes() == original(path))
shared = subprocess.check_output(['git', 'diff', '--name-only', BASE, '--', 'assets/js', 'assets/css', 'index.html'], text=True).splitlines()
check('shared styles/scripts and home unchanged', set(shared) <= {'assets/css/harmony.css'})
for path in ['.scratch/harmony/spec.md', '.scratch/harmony/visual-narrative-review.md', '.scratch/harmony/validation.md', '.scratch/harmony/copy-draft.md', '.scratch/harmony/visual-narrative-qa.py']:
    check('existing document/helper preserved: ' + path, Path(path).read_text(encoding='utf-8') == original(path).decode().replace('\r\n', '\n'))
for path in ['.scratch/harmony/image-manifest.md', '.scratch/harmony/visual-narrative-validation.md']:
    check('prior record preserved: ' + path, Path(path).read_text(encoding='utf-8').startswith(original(path).decode().replace('\r\n', '\n')))

before = original('case-studies/harmony.html').decode().replace('\r\n', '\n')
after = Path('case-studies/harmony.html').read_text(encoding='utf-8')
check('header, hero, problem and role preserved', before.split('<!-- Shared foundations:')[0] == after.split('<!-- Shared foundations:')[0])
check('outcome, in-development work, next project and contact preserved', before.split('<!-- The Outcome -->')[1] == after.split('<!-- The Outcome -->')[1])
check('analytics and all other script tags preserved', re.findall(r'<script\b.*?</script>', before, re.S) == re.findall(r'<script\b.*?</script>', after, re.S))
check('template positioned after foundations and before maintenance', after.index('id="harmony-responsive"') < after.index('id="harmony-templates"') < after.index('React + Next.js'))
manifest = json.loads(Path('.scratch/harmony/template-image-manifest.json').read_text(encoding='utf-8'))
for record in manifest['derivatives']:
    path = Path(record['derivative'])
    source = Image.open(record['source']).convert('RGB')
    expected = Image.new('RGB', record['dimensions'], record['background'])
    for fragment in record['fragments']:
        expected.paste(source.crop(fragment['crop']), fragment['pasteAt'])
    actual = Image.open(path)
    check('manifest identity and faithful crop pixels: ' + path.name,
          list(source.size) == record['sourceDimensions'] and
          hashlib.sha256(Path(record['source']).read_bytes()).hexdigest() == record['sourceSha256'] and
          hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'] and
          list(actual.size) == record['dimensions'] and actual.format == 'PNG' and
          path.stat().st_size == record['bytes'] and
          ImageChops.difference(expected, actual.convert('RGB')).getbbox() is None)
    check('derivative used in rendered page: ' + path.name, path.name in after)
check('old organization pair and redundant Storybook intro remain absent', all(name not in after for name in ['harmony-antes', 'harmony-depois', '/storybook.png']))
result = {'baseline': BASE, 'checks': checks, 'summary': {
    'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}}
Path('.scratch/harmony/qa/template-artifact-integrity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(result['summary'])
for c in checks:
    if not c['ok']:
        print('FAIL', c['name'])
raise SystemExit(bool(result['summary']['failed']))
