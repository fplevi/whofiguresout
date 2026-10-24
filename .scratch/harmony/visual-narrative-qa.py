"""Harmony composed-case browser seam; adapted from Billing visual-narrative-qa.py.

python .scratch/harmony/visual-narrative-qa.py --slice primitives --label red-primitives
Each slice is added before its implementation. --slice all exercises the matrix.
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser()
parser.add_argument('--slice', choices=['primitives', 'semantics', 'responsive', 'buttons', 'component-navigation', 'storybook', 'all', 'matrix', 'navigation', 'captures'], required=True)
parser.add_argument('--label', required=True)
parser.add_argument('--url', default='http://localhost:8011/case-studies/harmony.html')
args = parser.parse_args()
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'qa' / args.label
OUT.mkdir(parents=True, exist_ok=True)
URL = args.url
R = {'checks': [], 'console': [], 'failed_requests': []}
EVIDENCE = [('primitives', 'Primitive color scales'),
            ('semantics', 'Semantic roles by use'),
            ('responsive', 'Responsive variables'),
            ('buttons', 'Button variants, sizes, and states'),
            ('component-navigation', 'Navigation across contexts'),
            ('templates', 'Composing page templates'),
            ('storybook', 'Button properties in Storybook')]


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    (OUT / 'results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False), encoding='utf-8')
    print(('PASS ' if ok else 'FAIL ') + name)


def heading_words_intact(region):
    return region.get_by_role('heading').evaluate(r"""e=>{
      const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let node;
      while(node=walker.nextNode())for(const match of node.textContent.matchAll(/\S+/g)){
        const range=document.createRange();range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);
        if(new Set([...range.getClientRects()].map(r=>Math.round(r.top))).size>1)return false;
      }return true;}""")


def settle_focus(page):
    # Browser focus can initiate smooth scrolling. Observe the focus cue after
    # it enters the usable viewport, rather than capturing an intermediate frame.
    page.wait_for_timeout(700)
    page.wait_for_function("""()=>{const e=document.activeElement,r=e.getBoundingClientRect();
      return r.bottom>(e.closest('nav')?0:64)&&r.top<innerHeight-24;}""")


with sync_playwright() as p:
    browser = p.chromium.launch()
    R['environment'] = {'browser': browser.version, 'url': URL, 'viewportHeight': 700}
    ctx = browser.new_context(viewport={'width': 375, 'height': 700}, reduced_motion='reduce')
    page = ctx.new_page()
    page.goto(URL, wait_until='load')
    if args.slice in ['primitives', 'semantics', 'responsive', 'buttons', 'component-navigation', 'storybook']:
        key, title = next(e for e in EVIDENCE if e[0] == args.slice)
        region = page.get_by_role('region', name=title, exact=True)
        check(f'{key}: named evidence and explanatory heading exist', region.count() == 1)
        if region.count():
            image = region.get_by_role('img')
            image.scroll_into_view_if_needed()
            image.evaluate('(i)=>i.decode()')
            check(f'{key}: one loaded evidence with alternative', image.count() == 1 and bool(image.get_attribute('alt')) and image.evaluate('(i)=>i.complete&&i.naturalWidth>0'))
            check(f'{key}: explanation precedes image', region.evaluate("r=>{const p=r.querySelector('p'),i=r.querySelector('img');return !!p&&!!(p.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING)&&p.getBoundingClientRect().bottom<=i.getBoundingClientRect().top}"))
            region.screenshot(path=str(OUT / f'{key}-375.png'))
        else:
            page.screenshot(path=str(OUT / 'missing-evidence-375.png'))
        if args.slice == 'component-navigation':
            application = page.get_by_role('region', name='Applying the shared patterns.', exact=True)
            copy = application.inner_text().lower()
            check('accessibility and content remain ongoing requirements within component application',
                  all(term in copy for term in ['contrast', 'semantics', 'error messages', 'ongoing']) and
                  page.get_by_role('heading', name='Accessibility and content in component design', exact=True).count() == 0)
    ctx.close()
    if args.slice in ['all', 'matrix']:
        for width in [320, 375, 768, 1440]:
            for motion in ['no-preference', 'reduce']:
                context = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion=motion)
                page = context.new_page()
                page.on('pageerror', lambda error: R['console'].append(str(error)))
                page.on('requestfailed', lambda request: R['failed_requests'].append({'url': request.url, 'failure': request.failure}))
                page.on('response', lambda response: response.status >= 400 and R['failed_requests'].append({'url': response.url, 'status': response.status}))
                page.goto(URL, wait_until='load')
                page.wait_for_timeout(600)
                prefix = f'{width}/{motion}'
                # Start at the top. Check rendered content as a real wheel reaches
                # it, rather than letting a later jump conceal a reveal failure.
                seen, concealed, arrivals = set(), [], []
                start_y = page.evaluate('scrollY')
                for step in range(150):
                    # Preserve arrival viewports from the real wheel traversal,
                    # before the separate element-capture jumps below.
                    headings = page.locator('main h2, main h3').evaluate_all("""es=>es.filter(e=>{const r=e.getBoundingClientRect();return r.top>=88&&r.top<620;}).map(e=>({id:e.id,text:e.textContent}))""")
                    for heading in headings:
                        if heading['id'] not in [h['id'] for h in arrivals]:
                            filename = f'wheel-{width}-{motion}-{heading["id"]}.png'
                            page.screenshot(path=str(OUT / filename))
                            arrivals.append({**heading, 'scrollY': page.evaluate('scrollY'), 'capture': filename})
                    observations = page.evaluate("""()=>[...document.querySelectorAll('main h1, main h2, main h3, main p, main li, main figure, main form')].flatMap((e,index)=>{
                      const r=e.getBoundingClientRect(); if(r.bottom<100||r.top>620)return [];
                      let visible=true;for(let a=e;a;a=a.parentElement){const s=getComputedStyle(a);if(+s.opacity<0.99||s.visibility==='hidden'||s.display==='none')visible=false;}
                      return [{index,text:(e.innerText||e.getAttribute('aria-label')||e.tagName).slice(0,100),visible}];})""")
                    for observation in observations:
                        seen.add(observation['index'])
                        if not observation['visible']:
                            concealed.append(observation)
                    # Stop only at the actual bottom, without jumping.
                    if page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'):
                        break
                    page.mouse.wheel(0, 300)
                    page.wait_for_timeout(600)
                check(f'{prefix}: content visible when reached by wheel', not concealed, {'observedElements': len(seen), 'concealed': concealed})
                check(f'{prefix}: wheel traverses from top to document bottom', start_y == 0 and page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'), {'startY': start_y, 'endY': page.evaluate('scrollY'), 'steps': step, 'arrivals': arrivals})
                page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
                check(f'{prefix}: no horizontal overflow', page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                # Public headings and region associations, no class/nesting contract.
                titles = page.locator('main h2, main h3').all_text_contents(); titles = [t for t in titles if t in [e[1] for e in EVIDENCE]]
                check(f'{prefix}: foundations in approved reading order', titles[:3] == [e[1] for e in EVIDENCE[:3]], titles)
                check(f'{prefix}: component application follows foundations in approved order', titles[3:5] == [e[1] for e in EVIDENCE[3:5]], titles)
                images = page.locator('main figure img')
                check(f'{prefix}: precisely seven static evidences in approved order', images.count() == 7 and titles == [e[1] for e in EVIDENCE], titles)
                for key, title in EVIDENCE:
                    region = page.get_by_role('region', name=title, exact=True)
                    details = region.evaluate("""r=>{const i=r.querySelector('img'),p=r.querySelector('p'),f=r.querySelector('figure');
                      const ir=i.getBoundingClientRect(),pr=p.getBoundingClientRect();
                      return {loaded:i.complete&&i.naturalWidth>0,alt:i.alt,ratio:ir.width/ir.height,sourceRatio:i.naturalWidth/i.naturalHeight,
                        width:ir.width,naturalWidth:i.naturalWidth,images:r.querySelectorAll('img').length,domFirst:!!(p.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),
                        above:pr.bottom<=ir.top,disjoint:pr.bottom<=ir.top||ir.right<=pr.left||pr.right<=ir.left,
                        imageLeft:ir.right<=pr.left,imageRight:pr.right<=ir.left,
                        associated:f.getAttribute('aria-describedby')===p.id,
                        links:r.querySelectorAll('a,button,details,summary').length,source:i.currentSrc,
                        font:getComputedStyle(p).fontSize,color:getComputedStyle(p).color,
                        clipped:[...r.querySelectorAll('h2,h3,p,figcaption')].some(e=>e.scrollWidth>e.clientWidth+1)};}""")
                    check(f'{prefix}/{key}: heading words stay intact', heading_words_intact(region))
                    check(f'{prefix}/{key}: loaded, proportionate, one image', details['loaded'] and details['images'] == 1 and abs(details['ratio'] - details['sourceRatio']) < .01, details)
                    # Foundation assertions remain unchanged; component copy may
                    # sit beside the focal image only on a wide viewport.
                    above = details['disjoint'] if key in ['buttons', 'component-navigation'] and width > 1024 else details['above']
                    check(f'{prefix}/{key}: visible associated copy before evidence', details['domFirst'] and above and details['associated'] and not details['clipped'])
                    if width == 1440 and key in ['buttons', 'component-navigation']:
                        check(f'{prefix}/{key}: focal evidence alternates laterally', details['imageRight'] if key == 'buttons' else details['imageLeft'])
                    check(f'{prefix}/{key}: alternative and no image/disclosure controls', bool(details['alt']) and details['links'] == 0)
                    available = width - (48 if width <= 1024 else 160)
                    check(f'{prefix}/{key}: useful reading width without raster enlargement', abs(details['width'] - min(details['naturalWidth'], available)) <= 1)
                    # Readable prose is verified separately from raster detail.
                    check(f'{prefix}/{key}: prose retains 16px typography', float(details['font'][:-2]) >= 16)
                    region.evaluate("e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-88)")
                    page.wait_for_timeout(150)
                    page.screenshot(path=str(OUT / f'{key}-{width}-{motion}.png'))
                    if motion == 'reduce':
                        # Plate-only evidence after confirmed lazy-image load.
                        region.get_by_role('img').screenshot(path=str(OUT / f'{key}-plate-{width}.png'))
                context.close()
        # The static narrative is also an explicitly approved browser boundary.
        for width in [320, 375, 768, 1440]:
            context = browser.new_context(viewport={'width': width, 'height': 700}, java_script_enabled=False)
            page = context.new_page()
            page.goto(URL, wait_until='load')
            for step in range(150):
                page.mouse.wheel(0, 400)
                page.wait_for_timeout(30)
                if page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'):
                    break
            check(f'no-JS {width}: all seven images load', page.evaluate('[...document.querySelectorAll("main figure img")].length===7&&[...document.images].every(i=>i.complete&&i.naturalWidth>0)'))
            check(f'no-JS {width}: static copy and all sections visible', page.evaluate("""[...document.querySelectorAll('main section,main figure,main h3,main p')].every(e=>getComputedStyle(e).opacity==='1'&&getComputedStyle(e).visibility==='visible')"""))
            check(f'no-JS {width}: no horizontal overflow', page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            page.get_by_role('region', name='Responsive variables', exact=True).evaluate("e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-88)")
            page.screenshot(path=str(OUT / f'no-js-{width}.png'))
            for key, title in EVIDENCE[3:]:
                region = page.get_by_role('region', name=title, exact=True)
                region.evaluate("e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-88)")
                page.screenshot(path=str(OUT / f'no-js-{key}-{width}.png'))
            context.close()

    if args.slice == 'captures':
        for width in [320, 375, 768, 1440]:
            context = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion='reduce')
            page = context.new_page()
            page.goto(URL, wait_until='load')
            for key, title in EVIDENCE:
                region = page.get_by_role('region', name=title, exact=True)
                image = region.get_by_role('img')
                image.scroll_into_view_if_needed()
                image.evaluate('(i)=>i.decode()')
                dimensions = image.bounding_box()
                for part, offset in enumerate(range(0, round(dimensions['height']), 500)):
                    image.evaluate('(i,offset)=>window.scrollTo(0,i.getBoundingClientRect().top+scrollY-88+offset)', offset)
                    page.wait_for_timeout(100)
                    page.screenshot(path=str(OUT / f'{key}-detail-{width}-{part+1}.png'))
                check(f'{width}/{key}: loaded evidence captured in overlapping reading viewports', image.evaluate('(i)=>i.complete&&i.naturalWidth>0'))
            context.close()

    if args.slice in ['all', 'navigation']:
        for width in [320, 375, 768, 1440]:
            context = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion='reduce')
            page = context.new_page()
            page.goto(URL, wait_until='load')
            levels = page.get_by_role('heading').evaluate_all('es=>es.map(e=>+e.tagName.slice(1))')
            check(f'{width}: one h1 and no skipped heading level', levels.count(1) == 1 and all(b <= a + 1 for a, b in zip(levels, levels[1:])), levels)
            # Follow the actual tab sequence; Enter only on navigation links.
            focus = []
            while len(focus) < 15:
                page.keyboard.press('Tab')
                settle_focus(page)
                active = page.evaluate("""()=>{const e=document.activeElement,s=getComputedStyle(e),r=e.getBoundingClientRect();return {tag:e.tagName,name:e.getAttribute('aria-label')||e.innerText||e.getAttribute('placeholder'),href:e.getAttribute('href'),outline:s.outlineStyle,width:s.outlineWidth,left:r.left,right:r.right,top:r.top,bottom:r.bottom};}""")
                focus.append(active)
                if active['href'] == '../#work' or active['href'] == 'billing.html' or active['name'] == 'Send message':
                    suffix = 'nav' if active['href'] == '../#work' else 'next' if active['href'] == 'billing.html' else 'contact'
                    page.screenshot(path=str(OUT / f'focus-{suffix}-{width}.png'))
                if active['name'] == 'Send message':
                    break
            check(f'{width}: navigation, next project and contact reachable by Tab', [e['href'] for e in focus[:6]] == ['../', '../#work', '../#contact', '../#about', '../', 'billing.html'], focus)
            check(f'{width}: visible focus on interactive elements', all(
                e['outline'] != 'none' and e['width'] != '0px' and
                e['left'] >= 0 and e['right'] <= width and e['bottom'] > 0 and e['top'] < 700
                for e in focus))
            check(f'{width}: contact present, never submitted', page.locator('form[action="https://formspree.io/f/mbdqyywl"]').count() == 1 and page.get_by_role('button', name='Send message', exact=True).count() == 1)
            contrasts = page.get_by_role('region', name='Building a shared foundation.', exact=True).or_(page.get_by_role('region', name='Applying the shared patterns.', exact=True)).or_(page.get_by_role('region', name='Composing page templates', exact=True)).or_(page.get_by_role('region', name='Button properties in Storybook', exact=True)).locator('p,figcaption').evaluate_all("""es=>{
              const rgb=s=>s.match(/[\\d.]+/g).map(Number),lin=x=>(x/=255)<=0.04045?x/12.92:((x+.055)/1.055)**2.4;
              return es.map(e=>{const fg=rgb(getComputedStyle(e).color);let layers=[];
                for(let a=e;a;a=a.parentElement){layers.push(rgb(getComputedStyle(a).backgroundColor));}
                let bg=[255,255,255];for(const c of layers.reverse()){const alpha=c[3]??1;bg=bg.map((v,i)=>c[i]*alpha+v*(1-alpha));}
                const alpha=fg[3]??1,paint=bg.map((v,i)=>fg[i]*alpha+v*(1-alpha));
                const lum=c=>c.map(lin).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0),l1=lum(paint),l2=lum(bg);
                return {text:e.textContent.slice(0,60),font:getComputedStyle(e).fontSize,color:getComputedStyle(e).color,background:bg,ratio:(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)};});}""")
            check(f'{width}: orientation and explanatory text calculated contrast >=4.5', all(c['ratio'] >= 4.5 for c in contrasts), contrasts)
            # Return to nav and activate each preserved local destination using
            # the keyboard. Read destination headings/anchors; no remote form IO.
            destinations = [('Work', '/#work', 'work'), ('About', '/#about', 'about'), ('Contact', '/#contact', 'contact'),
                            ('Felipe Levi', '/', 'work'), ('← Back to work', '/', 'work'),
                            ('Billing & Debt Recovery →', '/case-studies/billing.html', None)]
            for name, suffix, anchor in destinations:
                page.goto(URL, wait_until='load')
                link = page.get_by_role('link', name=name, exact=True)
                link.focus()
                settle_focus(page)
                cue = link.evaluate("e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0&&r.left>=0&&r.right<=innerWidth}")
                page.screenshot(path=str(OUT / f'focus-activate-{width}-{name.split()[0]}.png'))
                check(f'{width}: visible focus before activating {name}', cue)
                page.keyboard.press('Enter')
                page.wait_for_url('**' + suffix)
                check(f'{width}: keyboard destination {name}', page.url.endswith(suffix) and (page.locator('#' + anchor).count() == 1 if anchor else page.get_by_role('heading', level=1).count() == 1), page.url)
            context.close()
    browser.close()

R['summary'] = {'passed': sum(c['ok'] for c in R['checks']), 'failed': sum(not c['ok'] for c in R['checks'])}
(OUT / 'results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False), encoding='utf-8')
print(R['summary'])
raise SystemExit(bool(R['summary']['failed']))
