"""Baseline preservation, source integrity, and measured orientation contrast.

Adapted from Enrollment final_checks.py; baseline is fixed at f8f9034.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True

spec=importlib.util.spec_from_file_location('ticket',Path(__file__).with_name('qa-ticket-04.py'))
qa=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
BASE='f8f9034'
baseline=subprocess.check_output(['git','show',f'{BASE}:case-studies/enrollment.html'],cwd=ROOT).decode('utf-8')
SELECTORS=['header','.cs-header','.cs-hero-image','[aria-labelledby="enrollment-problem"]',
           '[aria-labelledby="enrollment-role"]','[aria-labelledby="enrollment-outcome"]','.cs-next','#contact']
R={'baseline':BASE,'protected':[],'sourceIntegrity':[],'contrast':[]}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def colors(value):
    return [float(n) for n in re.findall(r'[\d.]+',value)]


def luminance(rgb):
    channels=[c/255 for c in rgb]
    lin=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in channels]
    return sum(c*w for c,w in zip(lin,[.2126,.7152,.0722]))


with sync_playwright() as p:
    b=p.chromium.launch()
    for width in [320,375,768,1440]:
        snapshots=[]
        for name,html in [('baseline',baseline),('current',None)]:
            page=b.new_page(viewport={'width':width,'height':900 if width==1440 else 700},reduced_motion='reduce')
            if html:
                page.route('**/case-studies/enrollment.html',lambda route:route.fulfill(status=200,content_type='text/html',body=baseline))
            page.goto(qa.URL,wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            snapshot={s:page.locator(s).evaluate('e=>e.outerHTML') for s in SELECTORS}
            snapshot['analyticsAndScripts']=page.locator('script').evaluate_all('els=>els.map(e=>e.outerHTML)')
            snapshot['decisions']=page.locator('.cs-decision__left').evaluate_all('els=>els.map(e=>e.outerHTML)')
            snapshot['contactControls']=page.locator('#contact input,#contact textarea,#contact button').evaluate_all('els=>els.map(e=>({tag:e.tagName,name:e.getAttribute("name"),type:e.type,label:e.getAttribute("aria-label"),required:e.required}))')
            snapshots.append(snapshot)
            if width in [375,1440]:
                page.locator('.cs-header').screenshot(path=str(qa.OUT/f'{name}-header-{width}.png'))
                page.locator('[aria-labelledby="enrollment-outcome"]').screenshot(path=str(qa.OUT/f'{name}-outcome-{width}.png'),style='.nav{visibility:hidden!important}')
            if name=='current':
                assert page.locator('#contact input').count()==2
                page.locator('#name').focus()
                page.keyboard.press('Tab')
                assert page.locator('#email').evaluate('e=>e===document.activeElement')
                page.keyboard.press('Tab')
                assert page.locator('#message').evaluate('e=>e===document.activeElement')
                contrast=page.locator('.enrollment-journey-evidence p').evaluate_all('els=>els.map(e=>({fg:getComputedStyle(e).color,bg:getComputedStyle(document.body).backgroundColor,size:getComputedStyle(e).fontSize}))')
                for c in contrast:
                    fg,bg=colors(c['fg']),colors(c['bg'])
                    alpha=fg[3] if len(fg)==4 else 1
                    blended=[fg[i]*alpha+bg[i]*(1-alpha) for i in range(3)]
                    ratio=(luminance(blended)+.05)/(luminance(bg)+.05)
                    assert ratio>=4.5,ratio
                    R['contrast'].append({'width':width,**c,'compositedRGB':blended,'ratio':ratio})
            slider=page.get_by_role('slider')
            slider.focus()
            page.wait_for_timeout(100)
            snapshot['comparisonFocus']=slider.evaluate('''e=>({
              name:e.getAttribute('aria-label'),opacity:getComputedStyle(e).opacity,
              outline:getComputedStyle(e).outlineStyle,
              parentOutline:getComputedStyle(e.parentElement).outlineStyle,
              parentShadow:getComputedStyle(e.parentElement).boxShadow
            })''')
            page.close()
        matches={s:snapshots[0][s]==snapshots[1][s] for s in snapshots[0]}
        assert all(matches.values()),matches
        R['protected'].append({'width':width,'exactBrowserMarkupMatches':matches,'contactTabOrder':True,'realSubmission':False})
        R['protected'][-1]['comparisonFocus']=snapshots[1]['comparisonFocus']
    b.close()

for path in sorted((ROOT/'assets/images/enrollment').iterdir()):
    rel=path.relative_to(ROOT).as_posix()
    old=subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=ROOT)
    same=digest(old)==digest(path.read_bytes())
    R['sourceIntegrity'].append({'path':rel,'sha256':digest(old),'unchanged':same})
    assert same,rel
issue='.scratch/enrollment/issues/01-metric-definition.md'
assert subprocess.check_output(['git','show',f'{BASE}:{issue}'],cwd=ROOT).decode('utf-8').replace('\r\n','\n')==(ROOT/issue).read_text(encoding='utf-8')
R['issue01Unchanged']=True
R['contact']='Controls inspected and keyboard traversed; no submit action or request.'
(qa.OUT/'final-checks.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps({'preservedWidths':len(R['protected']),'unchangedOriginals':len(R['sourceIntegrity']),
                  'minimumContrast':min(c['ratio'] for c in R['contrast']),'issue01Unchanged':True}))
