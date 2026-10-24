"""Final integration checks; run after qa.py, with the same URL/output overrides."""
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('ENROLLMENT_QA_OUT', str(ROOT / '.scratch/enrollment/qa/integration-final')))
os.environ.setdefault('ENROLLMENT_QA_OUT', str(OUT))
os.environ.setdefault('ENROLLMENT_QA_URL', 'http://127.0.0.1:8127/case-studies/enrollment.html')
runpy.run_path(str(Path(__file__).with_name('final-checks-ticket-03.py')), run_name='__main__')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


result = read_json(OUT / 'final-checks.json')
result['testedHead'] = git('rev-parse', 'HEAD').decode().strip()
result['mergeCommit'] = '5581f26'
result['parents'] = ['af687df', 'a09eb9e720f2d4219638d28df858d55ee69a1560']
result['productHashes'] = {}
originals = git('ls-tree', '-r', '--name-only', 'f8f9034', '--', 'assets/images/enrollment').decode().splitlines()
for rel in ['case-studies/enrollment.html', 'assets/css/enrollment.css',
            'assets/images/enrollment/submission-analysis.webp', *originals]:
    data = (ROOT / rel).read_bytes()
    result['productHashes'][rel] = sha(data)
    # Product bytes were not changed during integration QA.
    committed = git('show', f'5581f26:{rel}')
    assert data == committed or data.replace(b'\r\n', b'\n') == committed, rel

issue = ROOT / '.scratch/enrollment/issues/01-metric-definition.md'
assert sha(issue.read_bytes()) == 'b7d1b0127a8fb45274b3e04c78bba05a46f5c32f5d89827cbfd5eca8309ef2e2'
assert b'Status: needs-info' in issue.read_bytes()
result['issue01WorkingSHA256'] = sha(issue.read_bytes())

# Preserve the established decision arguments independently of relocated markup.
baseline = git('show', 'f8f9034:case-studies/enrollment.html').decode('utf-8')
current = (ROOT / 'case-studies/enrollment.html').read_text(encoding='utf-8')
for class_name in ['cs-decision__body', 'cs-decision__note']:
    pattern = rf'<p class="{class_name}">[\s\S]*?</p>'
    old = re.findall(pattern, baseline)
    new = re.findall(pattern, current)
    assert len(old) == len(new) == 3 and old == new, class_name
result['originalDecisionArgumentsAndNotesUnchanged'] = True

result['manifests'] = []
for ticket in ['02', '03', '04']:
    rel = f'.scratch/enrollment/presentation-assets-{ticket}.json'
    manifest = read_json(ROOT / rel)
    for item in manifest['assets']:
        source, presentation = ROOT / item['source'], ROOT / item['presentation']
        assert source.read_bytes() == presentation.read_bytes()
        actual = list(Image.open(source).size)
        declared = item.get('sourceDimensions', item.get('originalDimensions'))
        if isinstance(declared, dict):
            declared = [declared['width'], declared['height']]
        assert actual == declared
        if 'sha256' in item:
            assert sha(source.read_bytes()) == item['sha256']
    result['manifests'].append({'path': rel, 'assetsVerified': len(manifest['assets'])})

# Check immutable QA captures/reports from both inputs, including recovered evidence.
history = []
for ref in result['parents']:
    paths = git('ls-tree', '-r', '--name-only', ref, '--', '.scratch/enrollment').decode().splitlines()
    for rel in paths:
        if not (rel.startswith('.scratch/enrollment/qa/') or '/validation' in rel
                or '/presentation-assets-' in rel):
            continue
        expected = git('show', f'{ref}:{rel}')
        actual = (ROOT / rel).read_bytes()
        text = Path(rel).suffix in {'.md', '.json', '.txt', '.log'}
        normalized = actual.replace(b'\r\n', b'\n') if text else actual
        # The integration parent already appended its merger note to the older
        # incoming report. Preserve that entire newer file and the older prefix.
        extended_report = (rel == '.scratch/enrollment/validation-ticket-05.md'
                           and normalized.startswith(expected)
                           and normalized == git('show', f'af687df:{rel}'))
        assert actual == expected or normalized == expected or extended_report, (ref, rel)
        history.append({'ref': ref, 'path': rel, 'workingSHA256': sha(actual),
                        'olderReportRetainedWithExistingIntegrationAppendix': extended_report and normalized != expected})
(OUT / 'historical-preservation.json').write_text(json.dumps(history, indent=2), encoding='utf-8')
result['historicalArtifactsVerifiedByParent'] = {ref: sum(h['ref'] == ref for h in history) for ref in result['parents']}

matrix = read_json(OUT / 'validation.json')
assert len(matrix['cases']) == 8 and matrix['summary']['failed'] == 0 and not matrix['errors']
assert matrix['testedCommit'] == result['testedHead']
result['matrixSummary'] = matrix['summary']
result['renderedSelection'] = {'processBoards': 1, 'interfaceScreens': 4, 'twoLayerComparisons': 1, 'evidenceBlocks': 6}
result['errors'] = {key: [e for case in matrix['cases'] for e in case[key]]
                    for key in ['javascriptErrors', 'console', 'failedRequests', 'httpErrors', 'contactPosts']}
assert not result['errors']['javascriptErrors'] and not result['errors']['contactPosts']

paired = []
for width in [320, 375, 768, 1440]:
    for suffix in ['evidence', 'enrollment-discovery', 'enrollment-eligibility',
                   'enrollment-personal-details', 'enrollment-portability', 'enrollment-submission-title']:
        normal = OUT / f'{width}-no-preference-{suffix}.png'
        reduced = OUT / f'{width}-reduce-{suffix}.png'
        a, b = Image.open(normal).convert('RGB'), Image.open(reduced).convert('RGB')
        assert a.size == b.size, (normal, reduced)
        diff = ImageChops.difference(a, b)
        paired.append({'width': width, 'block': suffix, 'dimensions': list(a.size),
                       'identicalPixels': diff.getbbox() is None, 'differenceBounds': diff.getbbox(),
                       'meanDifference': ImageStat.Stat(diff).mean,
                       'normalSHA256': sha(normal.read_bytes()), 'reducedSHA256': sha(reduced.read_bytes())})
(OUT / 'motion-evidence-comparison.json').write_text(json.dumps(paired, indent=2), encoding='utf-8')
result['motionPairs'] = {'count': len(paired), 'identical': sum(p['identicalPixels'] for p in paired)}
git('diff', '--check')
(OUT / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('PASS final integration: hashes, historical artifacts, manifests, decisions, issue01, eight cases and 24 evidence pairs')
