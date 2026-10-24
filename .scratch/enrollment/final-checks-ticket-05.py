"""Ticket 05 integrity and preservation, adapted from Enrollment final_checks.py.

Browser QA lives at the approved rendered page seam; file checks preserve originals.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageChops

sys.dont_write_bytecode = True
spec=importlib.util.spec_from_file_location('ticket05',Path(__file__).with_name('qa-ticket-05.py'))
qa=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
BASE='f8f9034'


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


R={'baseline':BASE,'originals':[],'sharedFilesUnchanged':[], 'protectedCaptures':[]}
paths=git('ls-tree','-r','--name-only',BASE,'--','assets/images/enrollment').decode().splitlines()
for rel in paths:
    old=git('show',f'{BASE}:{rel}')
    current=(ROOT/rel).read_bytes()
    assert current==old,rel
    R['originals'].append({'path':rel,'sha256':sha(current),'unchanged':True})

for rel in ['assets/css/case-study.css','assets/js/scroll-animations.js',
            'assets/js/contact-form.js','.scratch/enrollment/issues/01-metric-definition.md']:
    assert not git('diff',BASE,'--',rel).strip(),rel
    R['sharedFilesUnchanged'].append({'path':rel,'worktreeSHA256':sha((ROOT/rel).read_bytes())})
issue=ROOT/'.scratch/enrollment/issues/01-metric-definition.md'
original_issue=git('show',f'{BASE}:.scratch/enrollment/issues/01-metric-definition.md')
# Windows checkout uses CRLF. Verify exact expected checkout bytes, not rewritten text.
assert issue.read_bytes()==original_issue.replace(b'\n',b'\r\n')
assert b'Status: needs-info' in issue.read_bytes()
R['issue01']={'status':'needs-info','byteIdenticalToBaselineCRLFCheckout':True,
              'sha256':sha(issue.read_bytes())}

manifest=json.loads((ROOT/'.scratch/enrollment/presentation-assets-05.json').read_text(encoding='utf-8'))
source=ROOT/manifest['source']
presentation=ROOT/manifest['presentation']
assert sha(source.read_bytes())==manifest['sourceSHA256']
original=Image.open(source).convert('RGBA')
derived=Image.open(presentation).convert('RGBA')
assert list(original.size)==manifest['sourceDimensions']
assert list(derived.size)==manifest['presentationDimensions']
assert original.crop(tuple(manifest['cropBoundsXYXY'])).tobytes()==derived.tobytes()
R['presentation']={'manifest':'.scratch/enrollment/presentation-assets-05.json',
                   'losslessCropPixelIdentity':True,'sha256':sha(presentation.read_bytes())}

baseline=git('show',f'{BASE}:case-studies/enrollment.html').decode('utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch()
    for width in [375,1440]:
        for name,html in [('baseline',baseline),('current',None)]:
            page=browser.new_page(viewport={'width':width,'height':900 if width==1440 else 700},reduced_motion='reduce')
            if html:
                page.route(qa.URL,lambda route:route.fulfill(status=200,content_type='text/html',body=baseline))
            page.goto(qa.URL,wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            for label,selector in [('header','.cs-header'),('outcome','[aria-labelledby="enrollment-outcome"]')]:
                path=f'{name}-{label}-{width}.png'
                page.locator(selector).screenshot(path=str(qa.OUT/path),style='.nav{visibility:hidden!important}')
                R['protectedCaptures'].append(path)
            page.close()
    browser.close()

matrix=json.loads((qa.OUT/'matrix.json').read_text(encoding='utf-8'))
assert matrix['summary']['failed']==0
assert len(matrix['matrix'])==8
expected={'Desk%20Research.png','parentesco.png','dados-parente.png','portabilidade-2.png',
          'submission-analysis.webp','old-enrollment-journey-simulator.jpg','new-enrollment-journey-simulator.jpg'}
for run in matrix['matrix']:
    selected=[i['src'].rsplit('/',1)[-1] for i in run['images']]
    assert len(selected)==7 and set(selected)==expected,selected
    static=[f for f in run['figures'] if f['images']==1]
    assert len(static)==4
R['renderedSelection']={'processImages':1,'interfaceScreens':4,'comparisons':1,
                        'exactSelectionAllEightRuns':True,'omittedScreensAbsent':True}
R['matrixSummary']=matrix['summary']
R['minimumMeasuredOrientationContrast']=min(c['ratio'] for m in matrix['matrix'] for c in m['contrast'])
R['comparatorRelocationIntegrated']=all(m['comparison']['relocated'] for m in matrix['matrix'])
R['integrationTip']=git('rev-parse','integration/enrollment-visual-narrative').decode().strip()
R['testedHead']=git('rev-parse','HEAD').decode().strip()
subprocess.run(['git','merge-base','--is-ancestor',R['integrationTip'],'HEAD'],cwd=ROOT,check=True)
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
R['latestIntegrationIsAncestor']=True
(qa.OUT/'final-checks.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps({'originalsUnchanged':len(R['originals']),'issue01ByteUnchanged':True,
                  'cropPixelIdentity':True,'matrix':R['matrixSummary'],
                  'minimumContrast':R['minimumMeasuredOrientationContrast'],
                  'integrationTip':R['integrationTip']}))
