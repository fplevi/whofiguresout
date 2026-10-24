"""Full current-page browser checks, adapted from Enrollment/Billing QA.

Run the server on 8104, then: python .scratch/enrollment/matrix-ticket-04.py
"""
import importlib.util
import json
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.dont_write_bytecode = True

spec = importlib.util.spec_from_file_location('ticket', Path(__file__).with_name('qa-ticket-04.py'))
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
from playwright.sync_api import sync_playwright

OUT, URL = qa.OUT, qa.URL
R = {'environment': {}, 'checks': [], 'errors': [], 'requests': [], 'matrix': []}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail)


def scroll_from_top(page, motion):
    """User wheel events only, before any element jumps or screenshots."""
    page.mouse.move(100, 350)
    seen = set()
    start = page.evaluate('scrollY')
    count = 0
    while count < 150:
        observed = page.evaluate('''() => [...document.querySelectorAll('main section, main h3, main figure')]
          .filter(e=> {const r=e.getBoundingClientRect();
            let visible=true; for(let n=e;n;n=n.parentElement) {
              const s=getComputedStyle(n); if(+s.opacity<0.99||s.visibility==='hidden') visible=false;
            }
            return visible&&r.top<innerHeight&&r.bottom>80;
          }).map(e=>e.getAttribute('aria-labelledby')||e.id||e.textContent.trim().slice(0,70))''')
        seen.update(observed)
        if page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'):
            break
        page.mouse.wheel(0, 250)
        # Let the existing 500ms entrance finish while this viewport is in view.
        page.wait_for_timeout(600 if motion == 'no-preference' else 100)
        count += 1
    page.wait_for_timeout(600)
    expected = page.evaluate('''() => [...document.querySelectorAll('main section, main h3, main figure')]
      .map(e=>e.getAttribute('aria-labelledby')||e.id||e.textContent.trim().slice(0,70))''')
    hidden = page.locator('main section').evaluate_all('els=>els.filter(e=>+getComputedStyle(e).opacity<.99).map(e=>e.outerHTML.slice(0,100))')
    return {'startY': start, 'wheelEvents': count, 'seen': sorted(seen),
            'missing': [s for s in expected if s not in seen], 'hiddenAfterScroll': hidden}


def comparison(page, context, label):
    slider = page.get_by_role('slider')
    check(label+' one comparison', slider.count() == 1)
    # Enter and leave through Tab, starting from the back link immediately before it.
    page.locator('.cs-header__back').focus()
    page.keyboard.press('Tab')
    check(label+' Tab enters comparison', slider.evaluate('e=>e===document.activeElement'))
    for key, value in [('Home', '0'), ('ArrowRight', '1'), ('End', '100'), ('ArrowLeft', '99')]:
        page.keyboard.press(key)
        page.wait_for_timeout(100)
        reveal = page.locator('.cs-compare__before').evaluate('e=>getComputedStyle(e).clipPath')
        handle = page.locator('.cs-compare__handle').evaluate('e=>getComputedStyle(e).left')
        check(label+' comparison '+key, slider.input_value() == value, {'value': slider.input_value(), 'clip': reveal, 'handlePx': handle})
        check(label+' reveal corresponds '+key, reveal == f'inset(0px {100-int(value)}% 0px 0px)')
    page.keyboard.press('Tab')
    check(label+' Tab leaves comparison', page.locator('.cs-next__link').evaluate('e=>e===document.activeElement'))
    slider.evaluate("e=>e.scrollIntoView({block:'start',behavior:'instant'})")
    page.evaluate('scrollBy(0,-100)')
    page.wait_for_timeout(600)
    box = slider.bounding_box()
    y = max(150, box['y']+min(160,box['height']/2))
    check(label+' interaction point visible', 80 < y < page.viewport_size['height'])
    page.mouse.click(box['x']+box['width']*.25,y)
    check(label+' pointer changes reveal', 15 < int(slider.input_value()) < 35)
    page.touchscreen.tap(box['x']+box['width']*.75,y)
    check(label+' touch changes reveal', 65 < int(slider.input_value()) < 85)


with sync_playwright() as p:
    browser = p.chromium.launch()
    R['environment'] = {'browser': 'Chromium '+browser.version, 'platform': sys.platform,
                        'url': URL, 'deviceScaleFactor': 1, 'hasTouch': True}
    for width in [320, 375, 768, 1440]:
        for motion in ['no-preference', 'reduce']:
            height = 900 if width == 1440 else 700
            label = f'{width}x{height}/{motion}'
            context = browser.new_context(viewport={'width':width,'height':height}, reduced_motion=motion, has_touch=True)
            page = context.new_page()
            page.on('pageerror', lambda e, l=label: R['errors'].append({'matrix':l,'error':str(e)}))
            page.on('requestfailed', lambda r, l=label: R['requests'].append({'matrix':l,'url':r.url,'failure':r.failure}))
            page.on('response', lambda r, l=label: r.status>=400 and R['requests'].append({'matrix':l,'url':r.url,'status':r.status}))
            page.goto(URL, wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            if motion == 'reduce':
                check(label+' reduced content immediately visible', page.locator('main section').evaluate_all('els=>els.every(e=>+getComputedStyle(e).opacity===1)'))
            wheel = scroll_from_top(page,motion)
            check(label+' every narrative reached by wheel from top', wheel['startY']==0 and not wheel['missing'] and not wheel['hiddenAfterScroll'], wheel)
            page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
            for name in qa.STORIES:
                qa.story(page, name)
            image_data = page.locator('figure[aria-labelledby^="enrollment-"]').evaluate_all('''els=>els.map(f=>{
              const c=f.querySelector('figcaption'), i=f.querySelector('img'), cr=c.getBoundingClientRect(),ir=i.getBoundingClientRect();
              return {name:f.getAttribute('aria-labelledby'),images:f.querySelectorAll('img').length,
                copyFirst:!!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),copyAbove:cr.bottom<=ir.top,
                w:ir.width,h:ir.height,nw:i.naturalWidth,nh:i.naturalHeight,width:i.width,height:i.height,
                lazy:i.loading,decoding:i.decoding,paragraphSize:getComputedStyle(c.querySelector('p')).fontSize,
                fg:getComputedStyle(c.querySelector('p')).color,bg:getComputedStyle(document.body).backgroundColor};})''')
            check(label+' three distinct static journey figures', len(image_data)==3 and all(i['images']==1 for i in image_data))
            check(label+' explanations before images without overlap', all(i['copyFirst'] and i['copyAbove'] for i in image_data), image_data)
            check(label+' proportional lazy async images and full body type', all(abs(i['w']/i['h']-i['nw']/i['nh'])<.001 and i['lazy']=='lazy' and i['decoding']=='async' and i['paragraphSize']=='16px' for i in image_data))
            check(label+' no horizontal overflow', page.evaluate('document.documentElement.scrollWidth') == width)
            outside = page.evaluate('''() => [...document.querySelectorAll('main *')].filter(e=>{
              const r=e.getBoundingClientRect();return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)&&!e.closest('.sr-only');
            }).map(e=>e.tagName+'.'+e.className)''')
            check(label+' no content clipped at viewport edge', not outside, outside)
            for name, (title, _, _) in qa.STORIES.items():
                figure = page.get_by_role('figure',name=title,exact=True)
                figure.screenshot(path=str(OUT/f'{name}-{width}-{motion}.png'),style='.nav {visibility:hidden!important}')
            comparison(page,context,label)
            page.screenshot(path=str(OUT/f'page-{width}-{motion}.png'),full_page=True)
            R['matrix'].append({'width':width,'height':height,'motion':motion,'wheel':wheel,'images':image_data})
            context.close()
    browser.close()
check('no application errors', not R['errors'], R['errors'])
local_failures=[r for r in R['requests'] if '127.0.0.1:8104' in r['url']]
check('no local failed assets', not local_failures, local_failures)
R['summary']={'passed':sum(c['passed'] for c in R['checks']),'failed':sum(not c['passed'] for c in R['checks'])}
(OUT/'matrix.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R['summary']))
assert R['summary']['failed']==0
