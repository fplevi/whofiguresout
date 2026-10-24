"""CSS-refactor comparison at the approved rendered-browser seam.

Adapts visual-narrative-qa.py's named regions, 700px viewport, real wheel
traversal, reduced-motion/no-JS contexts and loaded captures. Both origins serve
the same unchanged page/assets; the before server serves Git's pre-fix CSS.
No internal class names or exact nesting are browser acceptance contracts.
"""
import functools
import hashlib
import http.server
import json
from pathlib import Path
import platform
import subprocess
import sys
import threading
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
BASE = '3a466dbb17c20b7522a62128503281fdc0f48a7f'
OUT = ROOT / '.scratch/harmony/qa/code-review-css'
OUT.mkdir(parents=True, exist_ok=True)
EVIDENCE = [('primitives', 'Primitive color scales'),
            ('semantics', 'Semantic roles by use'),
            ('responsive', 'Responsive variables'),
            ('buttons', 'Button variants, sizes, and states'),
            ('component-navigation', 'Navigation across contexts'),
            ('templates', 'Composing page templates'),
            ('storybook', 'Button properties in Storybook')]
CSS = subprocess.check_output(['git', 'show', f'{BASE}:assets/css/harmony.css'], cwd=ROOT)
R = {'baseline': BASE, 'checks': [], 'comparisons': [], 'pageErrors': [], 'localErrors': []}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)
    (OUT / 'results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.server.before and urlsplit(self.path).path == '/assets/css/harmony.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', str(len(CSS)))
            self.end_headers()
            self.wfile.write(CSS)
        else:
            super().do_GET()


def serve(before):
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
    server.before = before
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def signature(region):
    # Semantic elements and document-space geometry, not internal structure.
    return region.evaluate("""r=>{
      const props=['display','position','box-sizing','width','height','max-width',
        'margin-top','margin-right','margin-bottom','margin-left',
        'padding-top','padding-right','padding-bottom','padding-left',
        'border-top-width','border-right-width','border-bottom-width','border-left-width',
        'border-radius','border-color','font-family','font-size','font-weight',
        'font-style','line-height','letter-spacing','text-align','color','background-color',
        'object-fit','opacity','visibility','transform','grid-template-columns','gap','align-items'];
      const metric=e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);
        return {text:e.tagName==='IMG'?e.alt:e.innerText,
          rect:{x:b.x,y:b.y+scrollY,width:b.width,height:b.height},
          style:Object.fromEntries(props.map(p=>[p,s.getPropertyValue(p)])),
          clipped:e.scrollWidth>e.clientWidth+1};};
      const i=r.querySelector('img'),p=r.querySelector('p'),f=r.querySelector('figure'),
        c=r.querySelector('figcaption'),ib=i.getBoundingClientRect(),pb=p.getBoundingClientRect();
      return {heading:metric(r.querySelector('h2,h3')),paragraphs:[...r.querySelectorAll('p')].map(metric),
        figure:metric(f),image:metric(i),caption:metric(c),row:metric(r),
        media:{source:new URL(i.currentSrc).pathname,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,
          loaded:i.complete&&i.naturalWidth>0,ratio:ib.width/ib.height},
        reading:{domFirst:!!(p.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),
          above:pb.bottom<=ib.top,disjoint:pb.bottom<=ib.top||ib.right<=pb.left||pb.right<=ib.left,
          imageLeft:ib.right<=pb.left,imageRight:pb.right<=ib.left,
          associated:f.getAttribute('aria-describedby')===p.id},
        controls:r.querySelectorAll('a,button,details,summary').length};}""")


before_server, after_server = serve(True), serve(False)
origins = [('before', f'http://127.0.0.1:{before_server.server_port}'),
           ('after', f'http://127.0.0.1:{after_server.server_port}')]
try:
    check('comparison HTML is unchanged from pre-fix Git tip',
          (ROOT / 'case-studies/harmony.html').read_bytes().replace(b'\r\n', b'\n') ==
          subprocess.check_output(['git', 'show', f'{BASE}:case-studies/harmony.html'], cwd=ROOT).replace(b'\r\n', b'\n'))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        R['environment'] = {'browser': browser.version, 'python': platform.python_version(),
                            'platform': platform.platform(), 'height': 700, 'origins': dict(origins),
                            'baselineCssSha256': hashlib.sha256(CSS).hexdigest(),
                            'afterCssSha256': hashlib.sha256((ROOT / 'assets/css/harmony.css').read_bytes()).hexdigest()}
        for width in [320, 375, 768, 1440]:
            for mode in ['normal', 'reduced', 'no-js']:
                snapshots = []
                for label, origin in origins:
                    context = browser.new_context(viewport={'width': width, 'height': 700},
                                                  reduced_motion='reduce' if mode == 'reduced' else 'no-preference',
                                                  java_script_enabled=mode != 'no-js')
                    page = context.new_page()
                    prefix = f'{width}/{mode}/{label}'
                    page.on('pageerror', lambda error: R['pageErrors'].append(str(error)))
                    page.on('response', lambda response: response.url.startswith(origin) and response.status >= 400 and R['localErrors'].append({'url': response.url, 'status': response.status}))
                    page.on('requestfailed', lambda request: request.url.startswith(origin) and R['localErrors'].append({'url': request.url, 'failure': request.failure}))
                    page.goto(origin + '/case-studies/harmony.html', wait_until='load')
                    page.evaluate('document.fonts.ready')
                    page.wait_for_timeout(700)
                    # Ordinary input reaches the evidence before any element jumps.
                    start = page.evaluate('scrollY')
                    reached, concealed = set(), []
                    for step in range(160):
                        for key, title in EVIDENCE:
                            region = page.get_by_role('region', name=title, exact=True)
                            observed = region.locator('h2,h3,p,img,figcaption').evaluate_all("""es=>es.flatMap(e=>{
                              const b=e.getBoundingClientRect();if(b.bottom<88||b.top>650)return [];
                              let visible=true;for(let a=e;a;a=a.parentElement){const s=getComputedStyle(a);
                                if(+s.opacity<.99||s.visibility==='hidden'||s.display==='none')visible=false;}
                              return [{tag:e.tagName,visible}];})""")
                            for item in observed:
                                reached.add(key + '/' + item['tag'])
                                if not item['visible']:
                                    concealed.append({'key': key, **item})
                        if page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'):
                            break
                        page.mouse.wheel(0, 300 if mode == 'normal' else 400)
                        page.wait_for_timeout(600 if mode == 'normal' else 50)
                    check(prefix + ': wheel reads every image and caption from top to bottom without gating',
                          start == 0 and page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2') and
                          all(key + '/' + tag in reached for key, _ in EVIDENCE for tag in ['IMG', 'FIGCAPTION']) and not concealed,
                          {'startY': start, 'endY': page.evaluate('scrollY'), 'steps': step, 'seen': sorted(reached), 'concealed': concealed})
                    page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
                    page.locator('main img').evaluate_all('is=>Promise.all(is.map(i=>i.decode()))')
                    check(prefix + ': seven evidence figures and no horizontal overflow',
                          page.locator('main figure').count() == 7 and page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                    rows = {}
                    for key, title in EVIDENCE:
                        region = page.get_by_role('region', name=title, exact=True)
                        data = signature(region)
                        rows[key] = data
                        metrics = [data['heading'], *data['paragraphs'], data['image'], data['caption']]
                        reading = data['reading']
                        check(prefix + '/' + key + ': loaded proportional image, readable associated copy and caption',
                              data['media']['loaded'] and abs(data['media']['ratio'] - data['media']['naturalWidth']/data['media']['naturalHeight']) < .01 and
                              reading['domFirst'] and reading['associated'] and reading['disjoint'] and
                              (reading['above'] if width <= 1024 or key not in ['buttons', 'component-navigation'] else
                               reading['imageRight'] if key == 'buttons' else reading['imageLeft']) and
                              all(not m['clipped'] and m['rect']['width'] > 0 and m['style']['opacity'] == '1' and m['style']['visibility'] == 'visible' for m in metrics) and
                              float(data['caption']['style']['font-size'][:-2]) >= 15 and data['controls'] == 0)
                        if mode == 'normal':
                            # Loaded full reading rows show both explanation and caption,
                            # including the lower edge of tall images. Not pixel assertions.
                            region.screenshot(path=str(OUT / f'{label}-{key}-{width}.png'))
                    snapshots.append(rows)
                    context.close()
                differences = [key for key, _ in EVIDENCE if snapshots[0][key] != snapshots[1][key]]
                check(f'{width}/{mode}: before/after layout, typography, geometry, style, sources and copy unchanged', not differences, differences)
                R['comparisons'].append({'width': width, 'mode': mode, 'before': snapshots[0], 'after': snapshots[1]})
        browser.close()
    check('no page exceptions or local failed requests/HTTP errors', not R['pageErrors'] and not R['localErrors'],
          {'pageErrors': R['pageErrors'], 'localErrors': R['localErrors']})
finally:
    before_server.shutdown()
    after_server.shutdown()
R['summary'] = {'passed': sum(c['ok'] for c in R['checks']), 'failed': sum(not c['ok'] for c in R['checks'])}
(OUT / 'results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps(R['summary']), flush=True)
raise SystemExit(bool(R['summary']['failed']))
