"""Rendered protected-surface comparison with the original pre-narrative case.

Uses the existing Playwright installation. An ephemeral local baseline serves
Git's original pages with byte-preserved shared assets; never submits contact.
"""
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

BASE = 'f8f9034fb32de4b7839ac0a003db2bb791af883e'
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.scratch/harmony/qa/final-preserved-surfaces-verified'
OUT.mkdir(parents=True, exist_ok=True)
CURRENT = 'http://localhost:8044'
R = {'baseline': BASE, 'checks': [], 'comparisons': []}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    (OUT / 'results.json').write_text(json.dumps(R, indent=2) + '\n', encoding='utf-8')
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def signature(page):
    # Public text, navigation destinations, media/form configuration and names.
    return {
        'title': page.title(),
        'header': page.get_by_role('banner').inner_text(),
        'nav': page.get_by_role('navigation').get_by_role('link').evaluate_all(
            "es=>es.map(e=>({name:e.textContent,href:e.getAttribute('href')}))"),
        'protectedCopy': [page.get_by_role('region', name=title, exact=True).inner_text()
            for title in ['Separate libraries. Repeated decisions.',
                          'Leading design, working with development.',
                          'Adopted in new projects. Evolving with the team.',
                          'Prototyping with AI, exploring the path to React.']],
        'hero': page.locator('video').evaluate("e=>Object.fromEntries([...e.attributes].map(a=>[a.name,a.value]))"),
        'form': page.get_by_role('button', name='Send message', exact=True).evaluate(
            "e=>({action:e.form.getAttribute('action'),method:e.form.method,fields:[...e.form.elements].map(f=>({tag:f.tagName,type:f.type,name:f.name,placeholder:f.placeholder,label:f.labels?.[0]?.textContent,required:f.required}))})"),
        'contact': page.locator('#contact').get_by_role('link').evaluate_all(
            "es=>es.map(e=>({name:e.textContent,href:e.getAttribute('href')}))"),
        'next': page.get_by_role('link', name='Billing & Debt Recovery →', exact=True).get_attribute('href')}


with tempfile.TemporaryDirectory(prefix='harmony-original-') as folder:
    baseline = Path(folder)
    # Shared assets are unchanged against BASE, independently checked by the
    # integrity helper. Hardlinks avoid unnecessary copies of media binaries.
    shutil.copytree(ROOT / 'assets', baseline / 'assets', copy_function=os.link)
    for relative in ['index.html', 'case-studies/harmony.html', 'case-studies/billing.html']:
        path = baseline / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=folder))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    original_origin = f'http://127.0.0.1:{server.server_port}'
    with sync_playwright() as p:
        browser = p.chromium.launch()
        R['environment'] = {'browser': browser.version, 'currentOrigin': CURRENT,
                            'baselineOrigin': original_origin, 'height': 700,
                            'baseline': 'temporary Git HTML + unchanged shared assets'}
        for width in [320, 375, 768, 1440]:
            snapshots = []
            for label, origin in [('original', original_origin), ('current', CURRENT)]:
                context = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion='reduce')
                page = context.new_page()
                url = origin + '/case-studies/harmony.html'
                page.goto(url, wait_until='load')
                snapshots.append(signature(page))
                page.screenshot(path=str(OUT / f'{label}-top-{width}.png'))
                poster = page.locator('video').evaluate("""async e=>{
                  const i=new Image();i.src=e.poster;await i.decode();
                  const r=e.getBoundingClientRect();return {loaded:i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight,renderWidth:r.width,renderHeight:r.height,videoWidth:e.videoWidth,readyState:e.readyState};}""")
                check(f'{width}/{label}: hero poster loads and media has positive geometry',
                      poster['loaded'] and poster['renderWidth'] > 0 and poster['renderHeight'] > 0, poster)
                page.locator('video').scroll_into_view_if_needed()
                page.screenshot(path=str(OUT / f'{label}-hero-{width}.png'))
                for name, suffix, anchor in [
                    ('Felipe Levi', '/', 'work'), ('← Back to work', '/', 'work'),
                    ('Work', '/#work', 'work'), ('About', '/#about', 'about'),
                    ('Contact', '/#contact', 'contact'),
                    ('Billing & Debt Recovery →', '/case-studies/billing.html', None)]:
                    page.goto(url, wait_until='load')
                    link = page.get_by_role('link', name=name, exact=True)
                    link.focus()
                    page.keyboard.press('Enter')
                    page.wait_for_url(origin + suffix)
                    check(f'{width}/{label}: keyboard activates {name}',
                          page.url == origin + suffix and
                          (page.locator('#' + anchor).count() == 1 if anchor else page.get_by_role('heading', level=1).count() == 1))
                page.goto(url, wait_until='load')
                page.get_by_role('textbox', name='Your name', exact=True).focus()
                page.wait_for_function("""()=>{const r=document.activeElement.getBoundingClientRect();return r.top>=64&&r.bottom<=innerHeight;}""")
                page.screenshot(path=str(OUT / f'{label}-contact-{width}.png'))
                check(f'{width}/{label}: contact available without submission',
                      page.get_by_role('textbox', name='Your email', exact=True).count() == 1 and
                      page.get_by_role('textbox', name='Your message', exact=True).count() == 1)
                context.close()
            check(f'{width}: protected rendered text, names, destinations, media and form configuration match original', snapshots[0] == snapshots[1])
            R['comparisons'].append({'width': width, 'original': snapshots[0], 'current': snapshots[1]})
        browser.close()
    server.shutdown()
R['summary'] = {'passed': sum(c['ok'] for c in R['checks']), 'failed': sum(not c['ok'] for c in R['checks'])}
(OUT / 'results.json').write_text(json.dumps(R, indent=2) + '\n', encoding='utf-8')
print(R['summary'])
raise SystemExit(bool(R['summary']['failed']))
