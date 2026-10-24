"""Collect freshly rerun integration QA and verify saved slice evidence stays historical.

Run after both existing matrices/final checks with ENROLLMENT_QA_URL on port 8120
and ENROLLMENT_QA_OUT pointing to integration-02-04/discovery or /journey.
"""
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.scratch/enrollment/qa/integration-02-04'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def read(relative):
    return json.loads((OUT / relative).read_text(encoding='utf-8'))


discovery = read('discovery/matrix.json')
journey = read('journey/matrix.json')
assert discovery['url'] == journey['environment']['url'] == 'http://127.0.0.1:8120/case-studies/enrollment.html'
assert discovery['summary'] == {'passed': 8, 'failed': 0}
assert journey['summary']['failed'] == 0 and len(journey['matrix']) == 8
assert not discovery['pageErrors'] and not discovery['localFailedRequests'] and not discovery['formSubmissions']
assert not journey['errors'] and not journey['requests']
assert read('discovery/final-checks.json')['sourceAndAllEnrollmentOriginalsUnchanged']
assert read('journey/final-checks.json')['issue01Unchanged']

historical = []
for ref, ticket in [('13c9ac7', '02'), ('8a6b19d', '04')]:
    subprocess.run(['git', 'merge-base', '--is-ancestor', ref, 'HEAD'], cwd=ROOT, check=True)
    paths = git('ls-tree', '-r', '--name-only', ref, '--',
                f'.scratch/enrollment/qa/ticket-{ticket}',
                f'.scratch/enrollment/validation-ticket-{ticket}.md',
                f'.scratch/enrollment/presentation-assets-{ticket}.json').decode().splitlines()
    for path in paths:
        saved, current = git('show', f'{ref}:{path}'), (ROOT / path).read_bytes()
        # Git LF and Windows checkout CRLF are equivalent for text artifacts.
        if not path.endswith('.png'):
            saved, current = saved.replace(b'\r\n', b'\n'), current.replace(b'\r\n', b'\n')
        assert saved == current, f'Historical evidence changed: {path}'
        historical.append(path)

assets = []
for ticket in ['02', '04']:
    manifest = json.loads((ROOT / f'.scratch/enrollment/presentation-assets-{ticket}.json').read_text(encoding='utf-8'))
    for asset in manifest['assets']:
        data = (ROOT / asset['source']).read_bytes()
        assert data == git('show', f'f8f9034:{asset["source"]}')
        assert asset['source'] == asset['presentation']
        dimensions = struct.unpack('>II', data[16:24])
        expected = asset['sourceDimensions']
        if isinstance(expected, dict):
            expected = [expected['width'], expected['height']]
        assert list(dimensions) == expected
        assets.append({'path': asset['source'], 'dimensions': dimensions, 'sha256': hashlib.sha256(data).hexdigest()})

assert not git('diff', 'fa56b5c', '--name-only', '--', 'assets/images/enrollment', 'assets/js',
               'assets/css/case-study.css', '.scratch/enrollment/issues/01-metric-definition.md',
               '.scratch/enrollment/issues/03-plan-exploration-comparison.md',
               '.scratch/enrollment/issues/05-submission-next-steps.md').strip()
subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)

capture_pairs = []
for folder, names in [('discovery', ['board']), ('journey', ['eligibility', 'personal', 'portability'])]:
    for width in [320, 375, 768, 1440]:
        for name in names:
            a = (OUT / folder / f'{name}-{width}-no-preference.png').read_bytes()
            b = (OUT / folder / f'{name}-{width}-reduce.png').read_bytes()
            capture_pairs.append({'folder': folder, 'name': name, 'width': width,
                                  'normalAndReducedIdentical': a == b,
                                  'normalSha256': hashlib.sha256(a).hexdigest(),
                                  'reducedSha256': hashlib.sha256(b).hexdigest()})
            if a != b:
                from PIL import Image, ImageChops
                normal = Image.open(OUT / folder / f'{name}-{width}-no-preference.png').convert('RGB')
                reduced = Image.open(OUT / folder / f'{name}-{width}-reduce.png').convert('RGB')
                capture_pairs[-1]['normalSize'] = normal.size
                capture_pairs[-1]['reducedSize'] = reduced.size
                if normal.size == reduced.size:
                    capture_pairs[-1]['differenceBounds'] = ImageChops.difference(normal, reduced).getbbox()

result = {
    'validatedProductHead': git('rev-parse', 'HEAD').decode().strip(),
    'branch': git('branch', '--show-current').decode().strip(), 'worktree': str(ROOT),
    'baseline': 'f8f9034', 'preMergeHead': 'fa56b5c',
    'mergeCommits': git('log', '--merges', '--format=%H %P', 'fa56b5c..HEAD').decode().splitlines(),
    'discoveryMatrix': discovery['summary'], 'journeyMatrix': journey['summary'],
    'historicalArtifactsUnchanged': historical, 'manifestSourcesUnchanged': assets,
    'motionCapturePairs': capture_pairs,
    'productSha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                      for p in ['assets/css/enrollment.css', 'case-studies/enrollment.html']},
    'issue01AndTickets03And05Unchanged': True, 'gitDiffCheck': 'passed',
    'scope': 'Integrated discovery board and three journey screens; final tickets 03/05 acceptance remains pending.'
}
(OUT / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({'discovery': discovery['summary'], 'journey': journey['summary'],
                  'historicalArtifactsUnchanged': len(historical),
                  'identicalMotionCapturePairs': sum(p['normalAndReducedIdentical'] for p in capture_pairs),
                  'totalMotionCapturePairs': len(capture_pairs)}))
