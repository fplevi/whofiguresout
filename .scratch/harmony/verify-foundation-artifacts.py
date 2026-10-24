"""Final composed artifact integrity alongside the approved browser seam.

Keeps the original foundation/protected-surface checks, with integrated decision
arguments and all seven evidence manifests. Historical results are not overwritten.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageChops

BASE = 'f8f9034fb32de4b7839ac0a003db2bb791af883e'
REVIEW_TIP = '3a466dbb17c20b7522a62128503281fdc0f48a7f'
COMPLETION = '\n## Completion\n\n2026-10-24: All four tickets and implement-spec step 7 are resolved. See [code review](code-review.md) and [CSS grouping validation](visual-narrative-validation.md#code-review-css-grouping--2026-10-24) for the r1 resolution, checks and limits.\n'
checks = []


def check(name, ok):
    checks.append({'name': name, 'ok': bool(ok)})


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'])


# Every pre-existing file outside the one authorized HTML edit is unchanged.
changed = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=MD', BASE], text=True).splitlines()
check('only authorized existing files changed', set(changed) <= {
    'case-studies/harmony.html', '.scratch/harmony/spec.md', *[
        '.scratch/harmony/issues/' + name for name in [
            '01-fundamentos-compartilhados.md', '02-aplicacao-nos-componentes.md',
            '03-composicao-em-templates.md', '04-storybook-parceria-implementacao.md']]})
sources = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, 'assets/images/harmony'], text=True).splitlines()
for path in sources:
    check(f'original bytes preserved: {path}', Path(path).read_bytes() == original(path))
for path in ['.scratch/harmony/spec.md', '.scratch/harmony/visual-narrative-review.md',
             '.scratch/harmony/validation.md', '.scratch/harmony/copy-draft.md']:
    previous = original(path).decode().replace('\r\n', '\n')
    allowed = [previous]
    if path == '.scratch/harmony/spec.md':
        # Only the authorized completion status and exact pointer may change.
        allowed.append(previous.replace('Status: ready-for-agent', 'Status: resolved', 1) + COMPLETION)
    check(f'historical document preserved (spec permits completion only): {path}', Path(path).read_text(encoding='utf-8') in allowed)

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
check('maintenance and hiring rationale integrated without standalone decisions',
      'React and Next.js were chosen with long-term maintenance and hiring in mind.' in after and
      'The intent was to give development a shared technical foundation as new projects adopt Harmony and existing products migrate.' in after and
      'harmony-decisions' not in after and 'The Decisions' not in after)
check('shared governance and accessibility/content arguments integrated',
      all(text in after for text in ['shared library as the common reference',
          'Shared governance and defined exceptions', 'Accessibility and content guidance',
          'Contrast, component semantics, and error messages remain ongoing component requirements']))

TIP = '6f1a19349e10e602683c68a8166544f12dad5724'
changed_in_final = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=MD', TIP], text=True).splitlines()
check('ticket 04 only edits its authorized existing files at integration tip', set(changed_in_final) <= {
    'case-studies/harmony.html', 'assets/css/harmony.css', '.scratch/harmony/spec.md',
    '.scratch/harmony/issues/04-storybook-parceria-implementacao.md',
    '.scratch/harmony/image-manifest.md', '.scratch/harmony/visual-narrative-validation.md',
    '.scratch/harmony/visual-narrative-qa.py', '.scratch/harmony/verify-foundation-artifacts.py'})
for path in ['.scratch/harmony/issues/01-fundamentos-compartilhados.md',
             '.scratch/harmony/issues/02-aplicacao-nos-componentes.md',
             '.scratch/harmony/issues/03-composicao-em-templates.md',
             '.scratch/harmony/image-manifest.json', '.scratch/harmony/template-image-manifest.json',
             '.scratch/harmony/template-narrative-qa.py']:
    previous = subprocess.check_output(['git', 'show', f'{TIP}:{path}']).decode().replace('\r\n', '\n')
    check(f'resolved sibling ticket/manifest/helper preserved: {path}', Path(path).read_text(encoding='utf-8') == previous)
for path in ['.scratch/harmony/image-manifest.md',
             '.scratch/harmony/visual-narrative-validation.md']:
    previous = subprocess.check_output(['git', 'show', f'{TIP}:{path}']).decode().replace('\r\n', '\n')
    check(f'integrated prior record/style preserved as prefix: {path}', Path(path).read_text(encoding='utf-8').startswith(previous))

# The review permits exactly the common figure/image/caption grouping, replacing
# the inherited CSS-prefix assertion. Everything else remains text-identical.
review_css = subprocess.check_output(['git', 'show', f'{REVIEW_TIP}:assets/css/harmony.css']).decode().replace('\r\n', '\n')
prior_css = subprocess.check_output(['git', 'show', f'{TIP}:assets/css/harmony.css']).decode().replace('\r\n', '\n')
check('review baseline retains prior CSS prefix', review_css.startswith(prior_css))
grouped_css = review_css
for element in ['figure', 'img', 'figcaption']:
    selector = f'.harmony-case .harmony-evidence {element}'
    block = re.search(re.escape(selector) + r' \{[^}]*\}\n\n', review_css)[0]
    for section in ['templates', 'storybook']:
        duplicate = block.replace('harmony-evidence', f'harmony-{section}', 1)
        check(f'baseline duplicate is identical: {section}/{element}', grouped_css.count(duplicate) == 1)
        grouped_css = grouped_css.replace(duplicate, '', 1)
    selectors = ',\n'.join([selector, f'.harmony-case .harmony-templates {element}',
                            f'.harmony-case .harmony-storybook {element}'])
    grouped_css = grouped_css.replace(selector + ' {', selectors + ' {', 1)
check('CSS differs only by authorized identical-rule grouping', Path('assets/css/harmony.css').read_text(encoding='utf-8') == grouped_css)
review_changes = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=MD', REVIEW_TIP], text=True).splitlines()
check('review only edits authorized existing files', set(review_changes) <= {
    'assets/css/harmony.css', '.scratch/harmony/verify-foundation-artifacts.py',
    '.scratch/harmony/spec.md', '.scratch/harmony/visual-narrative-validation.md'})
check('all inherited QA evidence and source/derived assets preserved at reviewed tip',
      not subprocess.check_output(['git', 'diff', '--no-renames', '--name-only', '--diff-filter=MD', REVIEW_TIP,
                                   '--', '.scratch/harmony/qa', 'assets/images/harmony']))
for path in ['.scratch/harmony/visual-narrative-validation.md', '.scratch/harmony/image-manifest.md']:
    previous = subprocess.check_output(['git', 'show', f'{REVIEW_TIP}:{path}']).decode().replace('\r\n', '\n')
    check(f'review retains full historical record prefix: {path}', Path(path).read_text(encoding='utf-8').startswith(previous))
for path in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', TIP, '.scratch/harmony/qa', 'assets/images/harmony'], text=True).splitlines():
    expected = subprocess.check_output(['git', 'show', f'{TIP}:{path}'])
    actual = Path(path).read_bytes()
    if Path(path).suffix in ['.json', '.md']:
        actual, expected = actual.replace(b'\r\n', b'\n'), expected.replace(b'\r\n', b'\n')
    check(f'historical evidence/asset preserved: {path}', actual == expected)

manifest = json.loads(Path('.scratch/harmony/image-manifest.json').read_text(encoding='utf-8'))
for name in ['template-image-manifest.json', 'storybook-image-manifest.json']:
    manifest['derivatives'].extend(json.loads(Path('.scratch/harmony', name).read_text(encoding='utf-8'))['derivatives'])
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
          (not (record.get('sha256') or record.get('derivativeSha256')) or
           hashlib.sha256(path.read_bytes()).hexdigest() == (record.get('sha256') or record.get('derivativeSha256'))) and
          ImageChops.difference(expected, actual.convert('RGB')).getbbox() is None)
check('every derivative used and old pair absent from rendered HTML',
      all(Path(r['derivative']).name in after for r in manifest['derivatives']) and
      'harmony-antes' not in after and 'harmony-depois' not in after and '/storybook.png' not in after)
result = {'baseline': BASE, 'reviewedTip': REVIEW_TIP, 'checks': checks,
          'summary': {'passed': sum(c['ok'] for c in checks), 'failed': sum(not c['ok'] for c in checks)}}
Path('.scratch/harmony/qa/code-review-artifact-integrity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result['summary']))
for c in checks:
    if not c['ok']:
        print('FAIL', c['name'])
raise SystemExit(bool(result['summary']['failed']))
