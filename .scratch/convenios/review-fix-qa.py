"""Focused network review regression, adapted from integration-smoke.py and 03-library-qa.py.

Approved seam: rendered case page. Own worktree server must run on port 8134.
No navigation/contact/full-case acceptance matrix; those remain parent-owned.
"""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / 'review-fix-evidence'
OUT.mkdir(exist_ok=True)
URL = 'http://127.0.0.1:8134/case-studies/convenios.html'
R = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
     'executed_at': datetime.now(timezone.utc).isoformat(), 'url': URL,
     'checks': [], 'views': [], 'diagnostics': []}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    R['browser'] = browser.version
    for width in (320, 375, 768, 1440):
        for motion in ('no-preference', 'reduce'):
            label = f'{width}-{motion}'
            ctx = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion=motion)
            pg = ctx.new_page()
            pg.on('pageerror', lambda e, label=label: R['diagnostics'].append({'view': label, 'error': str(e)}))
            pg.on('console', lambda m, label=label: m.type in ('error', 'warning') and R['diagnostics'].append({'view': label, 'console': m.text}))
            pg.on('requestfailed', lambda q, label=label: R['diagnostics'].append({'view': label, 'request': q.url, 'error': q.failure}))
            pg.on('response', lambda q, label=label: q.status >= 400 and R['diagnostics'].append({'view': label, 'request': q.url, 'status': q.status}))
            pg.goto(URL, wait_until='networkidle')
            pg.evaluate('document.fonts.ready')
            row = pg.get_by_role('article', name='Find care in the provider network.', exact=True)
            if motion == 'reduce':
                check(label + ': network immediately available', row.evaluate("e=>{const s=getComputedStyle(e.closest('section'));return s.opacity==='1'&&s.visibility==='visible'}"))

            # Actual wheel traversal starts at page top; no jumps or visibility overrides.
            pg.mouse.move(100, 450)
            samples = []
            copy_seen = image_seen = False
            for _ in range(100):
                sample = row.evaluate("""e=>{const c=e.querySelector('h3').parentElement.getBoundingClientRect(),
                    i=e.querySelector('img'),r=i.getBoundingClientRect(),s=getComputedStyle(e.closest('section'));
                    return {y:scrollY,copy:[c.top,c.bottom],image:[r.top,r.bottom],
                    opacity:+s.opacity,visible:s.visibility==='visible',loaded:i.complete&&i.naturalWidth>0}}""")
                samples.append(sample)
                shown = sample['opacity'] > .99 and sample['visible']
                copy_seen |= shown and sample['copy'][0] < 900 and sample['copy'][1] > 64
                image_seen |= shown and sample['loaded'] and sample['image'][0] < 900 and sample['image'][1] > 64
                if sample['image'][1] < 64:
                    break
                pg.mouse.wheel(0, 400)
                pg.wait_for_timeout(550)
            check(label + ': loaded network and explanation visible during ordinary wheel traversal', copy_seen and image_seen)
            row.get_by_role('img').evaluate('i=>i.decode()')
            geometry = row.evaluate("""e=>{const c=e.querySelector('h3').parentElement,i=e.querySelector('img'),
                a=c.getBoundingClientRect(),b=i.getBoundingClientRect(),f=i.parentElement.getBoundingClientRect();
                const rect=r=>({left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height});
                return {copy:rect(a),image:rect(b),figure:rect(f),
                copyFirst:!!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),
                natural:[i.naturalWidth,i.naturalHeight],loaded:i.complete&&i.naturalWidth>0,
                overflow:document.documentElement.scrollWidth>innerWidth,
                padding:getComputedStyle(i.parentElement).padding,
                font:getComputedStyle(c.querySelector('p')).fontSize}}""")
            c, i, f = geometry['copy'], geometry['image'], geometry['figure']
            check(label + ': explanation first in reading order', geometry['copyFirst'])
            check(label + ': mobile explanation first or desktop image left',
                  c['bottom'] <= f['top'] + 1 if width <= 768 else f['right'] <= c['left'] + 1, geometry)
            check(label + ': no overlap or horizontal overflow',
                  not geometry['overflow'] and min(c['left'], f['left']) >= 0 and max(c['right'], f['right']) <= width
                  and (c['bottom'] <= f['top'] + 1 or f['right'] <= c['left'] + 1), geometry)
            check(label + ': loaded proportional image and unchanged readable type',
                  geometry['loaded'] and geometry['natural'] == [430, 686]
                  and abs(i['width'] / i['height'] - 430 / 686) < .002 and float(geometry['font'][:-2]) >= 16, geometry)

            # Capture only the final network viewport and loaded image after wheel validation.
            row.evaluate("e=>scrollTo({top:scrollY+e.getBoundingClientRect().top-80,behavior:'instant'})")
            pg.wait_for_timeout(100)
            pg.screenshot(path=str(OUT / f'network-{label}.png'))
            row.get_by_role('img').screenshot(path=str(OUT / f'network-image-{label}.png'))
            R['views'].append({'view': label, 'geometry': geometry, 'wheel': samples})
            ctx.close()
    browser.close()

check('no page errors, console warnings/errors, failed requests or HTTP errors', not R['diagnostics'], R['diagnostics'])
R['summary'] = {'passed': sum(c['ok'] for c in R['checks']), 'failed': sum(not c['ok'] for c in R['checks'])}
(OUT / 'results.json').write_text(json.dumps(R, indent=2), encoding='utf-8')
print(R['summary'], flush=True)
raise SystemExit(bool(R['summary']['failed']))
