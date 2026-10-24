"""Ticket 02 preservation and manifest integrity, alongside the browser seam.

Ticket 01's original verification and records remain historical and unchanged.
"""
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


def text_at_base(path):
    return original(path).decode('utf-8').replace('\r\n', '\n')


allowed = {'case-studies/harmony.html', 'assets/css/harmony.css',
           '.scratch/harmony/issues/02-aplicacao-nos-componentes.md',
           '.scratch/harmony/visual-narrative-qa.py',
           '.scratch/harmony/image-manifest.json', '.scratch/harmony/image-manifest.md',
           '.scratch/harmony/visual-narrative-validation.md'}
changed = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=MD', BASE], text=True).splitlines()
check('existing changes confined to ticket 02 authorized files', set(changed) <= allowed)
sources = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'assets/images/harmony'], text=True).splitlines()
for path in sources:
    check(f'pre-existing asset bytes preserved: {path}', Path(path).read_bytes() == original(path))
for path in ['.scratch/harmony/spec.md', '.scratch/harmony/visual-narrative-review.md',
             '.scratch/harmony/validation.md', '.scratch/harmony/copy-draft.md',
             '.scratch/harmony/issues/01-fundamentos-compartilhados.md',
             '.scratch/harmony/issues/03-composicao-em-templates.md',
             '.scratch/harmony/issues/04-storybook-parceria-implementacao.md',
             '.scratch/harmony/verify-foundation-artifacts.py']:
    check(f'prior or sibling document preserved: {path}', Path(path).read_text(encoding='utf-8') == text_at_base(path))
for path in ['.scratch/harmony/image-manifest.md', '.scratch/harmony/visual-narrative-validation.md', 'assets/css/harmony.css']:
    check(f'previous record/style preserved as prefix: {path}', Path(path).read_text(encoding='utf-8').startswith(text_at_base(path)))

before = text_at_base('case-studies/harmony.html')
after = Path('case-studies/harmony.html').read_text(encoding='utf-8')
check('head, navigation, hero, problem, role and foundations preserved',
      after.split('    <!-- Component application')[0] == before.split('    <!-- Decision arguments')[0])
check('outcome, work in progress, next project, contact and scripts preserved',
      after.split('    <!-- The Outcome -->')[1] == before.split('    <!-- The Outcome -->')[1])
pattern = r'<h3[^>]*>React \+ Next.js for the product ecosystem</h3>.*?</p>\s*<p.*?</p>'
check('React/Next maintenance and hiring argument preserved for ticket 04',
      re.search(pattern, before, re.S)[0] == re.search(pattern, after, re.S)[0])
check('all analytics and other script tags preserved',
      re.findall(r'<script\b.*?</script>', before, re.S) == re.findall(r'<script\b.*?</script>', after, re.S))

manifest = json.loads(Path('.scratch/harmony/image-manifest.json').read_text(encoding='utf-8'))
prior = json.loads(text_at_base('.scratch/harmony/image-manifest.json'))
check('all prior foundation manifest records preserved', manifest['derivatives'][:len(prior['derivatives'])] == prior['derivatives'])
for record in manifest['derivatives']:
    path = Path(record['derivative'])
    source = Image.open(record['source']).convert('RGB')
    expected = Image.new('RGB', record['dimensions'], record['background'])
    for fragment in record['fragments']:
        expected.paste(source.crop(fragment['crop']), fragment['pasteAt'])
    actual = Image.open(path)
    check(f'manifest dimensions, bytes and unchanged source fragments: {path.as_posix()}',
          list(source.size) == record['sourceDimensions'] and
          hashlib.sha256(Path(record['source']).read_bytes()).hexdigest() == record['sourceSha256'] and
          actual.format == 'PNG' and list(actual.size) == record['dimensions'] and
          path.stat().st_size == record['bytes'] and
          ImageChops.difference(expected, actual.convert('RGB')).getbbox() is None)
    if record.get('ticket') == '02':
        check(f'derivative hash and rendered reference: {path.name}',
              hashlib.sha256(path.read_bytes()).hexdigest() == record['derivativeSha256'] and path.name in after)

result = {'baseline': BASE, 'checks': checks,
          'summary': {'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}}
Path('.scratch/harmony/qa/components-artifact-integrity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result['summary']))
for c in checks:
    if not c['ok']:
        print('FAIL', c['name'])
raise SystemExit(bool(result['summary']['failed']))
