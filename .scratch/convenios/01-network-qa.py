"""Ticket 01: rendered-page seam, adapted from Billing visual-narrative QA.

python .scratch/convenios/01-network-qa.py red|green [evidence-root]
Only observes the served page. No mocks, private implementation assertions or live app tests.
"""
import json
import io
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf8')
PHASE = sys.argv[1]
ROOT = Path(sys.argv[2] if len(sys.argv) > 2 else '.scratch/convenios/01-evidence')
ROOT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8111'
URL = BASE + '/case-studies/convenios.html'
R = {'phase': PHASE, 'url': URL, 'checks': [], 'diagnostics': [], 'matrix': []}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def save():
    R['summary'] = {'passed': sum(c['ok'] for c in R['checks']),
                    'failed': sum(not c['ok'] for c in R['checks'])}
    (ROOT / f'01-{PHASE}-results.json').write_text(json.dumps(R, indent=2, ensure_ascii=False), encoding='utf8')


with sync_playwright() as p:
    browser = p.chromium.launch()
    R['browser'] = browser.version
    for width in [320, 375, 768, 1440]:
        for motion in ['no-preference', 'reduce']:
            label = f'{width}-{motion}'
            ctx = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion=motion)
            pg = ctx.new_page()
            pg.on('pageerror', lambda e, label=label: R['diagnostics'].append({'view': label, 'pageerror': str(e)}))
            pg.on('requestfailed', lambda q, label=label: R['diagnostics'].append({'view': label, 'request': q.url, 'failure': q.failure}))
            pg.on('response', lambda q, label=label: q.status >= 400 and R['diagnostics'].append({'view': label, 'status': q.status, 'request': q.url}))
            pg.goto(URL, wait_until='networkidle')
            check(label + ': home remains in hero', pg.get_by_role('img', name='CASSI Convênios home screen with digital card information, key services and notifications').count() == 1)
            network = pg.get_by_role('article').filter(has=pg.get_by_role('heading', name='Find care in the provider network.', exact=True))
            check(label + ': network has its own explanation', network.count() == 1)
            card = pg.get_by_role('article').filter(has=pg.get_by_role('heading', name='Keep the essentials close.', exact=True))
            check(label + ': card keeps view/copy/share without unsupported biometrics',
                  'view, copy and share' in card.inner_text() and 'biometric' not in card.inner_text().lower())
            initial = pg.locator('main section').evaluate_all("es=>es.map(e=>({heading:e.querySelector('h2,h1')?.textContent,opacity:getComputedStyle(e).opacity}))")
            if motion == 'reduce':
                check(label + ': sections immediately visible', all(float(s['opacity']) == 1 for s in initial), initial)
            # Real wheel traversal is the reveal test. No scrollIntoView or scrollTo here.
            visits = []
            while True:
                visits += pg.locator('main section, article').evaluate_all("es=>es.filter(e=>{const r=e.getBoundingClientRect();return r.bottom>64&&r.top<innerHeight&&Number(getComputedStyle(e).opacity)===1&&Number(getComputedStyle(e.parentElement.closest('section')||e).opacity)===1}).map(e=>e.querySelector('h1,h2,h3')?.textContent)")
                before = pg.evaluate('scrollY')
                pg.mouse.wheel(0, 300)
                pg.wait_for_timeout(550 if motion == 'no-preference' else 80)
                if pg.evaluate('scrollY') == before:
                    break
            pg.wait_for_timeout(650)
            visibility = pg.locator('main section').evaluate_all("es=>es.map(e=>({heading:e.querySelector('h1,h2')?.textContent,opacity:getComputedStyle(e).opacity,height:e.getBoundingClientRect().height}))")
            check(label + ': every section appears during ordinary wheel traversal',
                  all(s['heading'] in visits and float(s['opacity']) == 1 for s in visibility), visibility)
            pg.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
            imgs = pg.locator('main img').evaluate_all("es=>es.map(i=>({src:i.getAttribute('src'),alt:i.alt,nw:i.naturalWidth,nh:i.naturalHeight,w:i.getBoundingClientRect().width,h:i.getBoundingClientRect().height,fit:getComputedStyle(i).objectFit,loading:i.loading,decoding:i.decoding}))")
            check(label + ': all page images loaded', all(i['nw'] and i['nh'] for i in imgs), imgs)
            # Hero uses object-fit containment; body evidence must itself have natural aspect ratio.
            check(label + ': body images proportional', all(i['fit'] == 'contain' or abs(i['w']/i['h']-i['nw']/i['nh']) < .02 for i in imgs[1:]))
            check(label + ': no horizontal overflow', pg.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            if network.count():
                check(label + ': network between card and accounts', pg.get_by_role('article').evaluate_all("es=>{const names=es.map(e=>e.querySelector('h3')?.textContent);return names[0]==='Keep the essentials close.'&&names[1]==='Find care in the provider network.'&&names[2]==='Make room for more than one account.'}"))
                copy = network.locator('p').inner_text()
                check(label + ': available map/list copy is factual', all(s in copy.lower() for s in ['available', 'map', 'list']) and not any(s in copy.lower() for s in ['geolocation', 'distance', 'initial launch', 'pending']))
                check(label + ': one static image, no disclosure or raw link', network.get_by_role('img').count() == 1 and network.locator('a,button,details,summary').count() == 0)
                geometry = network.evaluate("e=>{const p=e.querySelector('p'),i=e.querySelector('img'),a=p.getBoundingClientRect(),b=i.getBoundingClientRect();return {dom:!!(p.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),above:a.bottom<=b.top+1,separate:a.bottom<=b.top+1||a.right<=b.left+1||b.right<=a.left+1,inside:b.left>=0&&b.right<=innerWidth,font:getComputedStyle(p).fontSize,color:getComputedStyle(p).color}}")
                check(label + ': explanation precedes image without overlap', geometry['dom'] and geometry['separate'] and geometry['inside'] and (width > 768 or geometry['above']), geometry)
                ni = network.get_by_role('img')
                check(label + ': meaningful alt and deferred body image', bool(ni.get_attribute('alt')) and ni.get_attribute('loading') == 'lazy' and ni.get_attribute('decoding') == 'async')
                # All images are loaded and all sections have been reached by wheel already.
                # Capture from the top to keep the fixed nav out of evidence-row crops.
                pg.evaluate('scrollTo(0,0)')
                pg.wait_for_timeout(100)
                box = network.bounding_box()
                raw = pg.screenshot(path=str(ROOT / f'01-loaded-page-{label}.png'), full_page=True, animations='disabled')
                Image.open(io.BytesIO(raw)).crop((round(box['x']), round(box['y']), round(box['x']+box['width']), round(box['y']+box['height']))).save(ROOT / f'01-network-{label}.png')
                ni.screenshot(path=str(ROOT / f'01-network-image-{label}.png'), animations='disabled')
            if PHASE == 'red' and width == 320 and motion == 'no-preference':
                pg.locator('section').filter(has=pg.get_by_role('heading', name='Designed around everyday needs.', exact=True)).screenshot(path=str(ROOT / '01-red-features-320.png'))
            R['matrix'].append({'view': label, 'images': imgs, 'visibility': visibility, 'visited': sorted(set(v for v in visits if v))})
            ctx.close()
            save()

    if PHASE != 'red':
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
        pg = ctx.new_page()
        pg.goto(BASE, wait_until='networkidle')
        homecard = pg.get_by_role('link', name='CASSI Convênios case study: Product Leadership', exact=True)
        check('home card preserved', 'Launched' in homecard.inner_text() and 'on iOS and Android' in homecard.inner_text())
        homecard.click()
        pg.wait_for_url(URL)
        check('home card navigates to case', pg.get_by_role('heading', level=1, name='CASSI Convênios').is_visible())
        nav = pg.get_by_role('navigation', name='Main navigation').get_by_role('link').evaluate_all("es=>es.map(a=>a.getAttribute('href'))")
        check('navigation destinations preserved', nav == ['../', '../#work', '../#contact', '../#about'], nav)
        pg.get_by_role('link', name='← Back to work').click()
        pg.wait_for_url(BASE + '/#work')
        check('return to Work works', pg.get_by_role('link', name='CASSI Convênios case study: Product Leadership', exact=True).is_visible())
        pg.goto(BASE + '/case-studies/enrollment.html', wait_until='networkidle')
        pg.get_by_role('link', name='CASSI Convênios →').click()
        pg.wait_for_url(URL)
        pg.get_by_role('link', name='Harmony →').click()
        pg.wait_for_url(BASE + '/case-studies/harmony.html')
        check('adjacent case path Enrollment → Convênios → Harmony works', pg.get_by_role('heading', level=1, name='Harmony').is_visible())
        pg.goto(URL, wait_until='networkidle')
        check('store destinations preserved', pg.get_by_role('link', name='Google Play ↗').get_attribute('href') == 'https://play.google.com/store/apps/details?id=br.com.cassi.app.reciprocidade&pcampaignid=web_share' and pg.get_by_role('link', name='App Store ↗').get_attribute('href') == 'https://apps.apple.com/br/app/cassi-conv%C3%AAnios/id6705117118')
        check('contact form present, never submitted', pg.locator('form').get_attribute('action') == 'https://formspree.io/f/mbdqyywl' and pg.get_by_role('button', name='Copy email address').count() == 1)
        focus = []
        for _ in range(25):
            pg.keyboard.press('Tab')
            focus.append(pg.evaluate("()=>{const e=document.activeElement,s=getComputedStyle(e);return {text:e.getAttribute('aria-label')||e.textContent.trim()||e.getAttribute('placeholder'),tag:e.tagName,visible:e.getBoundingClientRect().width>0,outline:s.outlineStyle,width:s.outlineWidth}}"))
            if focus[-1]['text'] in ['Google Play ↗', 'Copy email address']:
                name = 'store' if focus[-1]['text'] == 'Google Play ↗' else 'contact'
                pg.screenshot(path=str(ROOT / f'01-keyboard-{name}-1440.png'))
        targets = ['Work', '← Back to work', 'Google Play ↗', 'App Store ↗', 'Harmony →', 'Copy email address', 'Your name', 'Your email', 'Your message']
        check('relevant links and contact fields keyboard reachable with visible focus', all(any(f['text'] == t and f['visible'] and f['outline'] != 'none' and float(f['width'].replace('px','')) >= 2 for f in focus) for t in targets), focus)
        check('metadata and analytics present', pg.title() == 'CASSI Convênios | Felipe Levi' and pg.locator('meta[property="og:url"]').get_attribute('content') == 'https://felipelevi.site/case-studies/convenios.html' and pg.locator('script[src*="googletagmanager.com"]').count() == 1 and 'wo2llblzgf' in pg.content())
        ctx.close()
    browser.close()
save()
print(R['summary'])
sys.exit(1 if R['summary']['failed'] else 0)
