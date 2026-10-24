"""Enrollment ticket 03: approved rendered-page seam; no project dependencies.

Adapted from Enrollment qa.py/final_checks.py and Billing visual-narrative-qa.py.
"""
import json
import os
import platform
import re
from pathlib import Path
from urllib.parse import urlsplit
import subprocess
import sys
import traceback

from PIL import Image, ImageChops, ImageStat

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('ENROLLMENT_QA_OUT', str(ROOT / '.scratch/enrollment/qa/ticket-03')))
OUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('ENROLLMENT_QA_URL', 'http://127.0.0.1:8123/case-studies/enrollment.html')
ORIGIN = '{0.scheme}://{0.netloc}'.format(urlsplit(URL))
NAME = 'Compare plan cards before and plan benefits after'


def protected(page):
    return page.evaluate('''() => {
      const selectors = ['head', 'header', '.cs-header', '.cs-hero-image',
        '[aria-labelledby="enrollment-problem"]', '[aria-labelledby="enrollment-role"]',
        '[aria-labelledby="enrollment-outcome"]', '.cs-next', '.contact'];
      return Object.fromEntries(selectors.map(s => {
        const e = document.querySelector(s).cloneNode(true);
        e.removeAttribute('style');
        if (s === 'head') e.querySelectorAll('script[src^="https://scripts.clarity.ms/"], script[src^="https://www.clarity.ms/tag/"]').forEach(n => n.remove());
        return [s, e.outerHTML];
      }));
    }''')


def placement(page):
    # Reader encounters the comparison between the first and second arguments.
    comparison = page.locator('.cs-compare')
    assert comparison.count() == 1, 'One purposeful comparison'
    first = page.get_by_role('heading', name='Remove mandatory pre-registration')
    second = page.get_by_role('heading', name="Reorganize steps around the user's mental model")
    assert first.evaluate('(e,c) => !!(e.compareDocumentPosition(document.querySelector(c)) & Node.DOCUMENT_POSITION_FOLLOWING)', '.cs-compare')
    assert second.evaluate('(e,c) => !!(e.compareDocumentPosition(document.querySelector(c)) & Node.DOCUMENT_POSITION_PRECEDING)', '.cs-compare'), 'Comparison must be beside exploration, before the next decision'
    assert page.get_by_text('What Shipped', exact=True).count() == 0
    guidance = page.get_by_text('The earlier screen presents plans as separate cards.', exact=False)
    assert guidance.count() == 1
    assert guidance.evaluate('(e,c) => !!(e.compareDocumentPosition(document.querySelector(c)) & Node.DOCUMENT_POSITION_FOLLOWING)', '.cs-compare')


def matrix(browser):
    report = {'browser': browser.version, 'environment': {'os': platform.platform(), 'python': platform.python_version(),
              'headless': True, 'deviceScaleFactor': 1, 'emulatedTouch': True},
              'testedCommit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'integrationTip': subprocess.check_output(['git', 'rev-parse', 'integration/enrollment-visual-narrative'], cwd=ROOT, text=True).strip(),
              'url': URL, 'scope': 'Final combined Enrollment page: one discovery board, four interface screens and one comparison, after all four implementation slices merged.',
              'preservationExclusions': 'Runtime section-root animation styles and asynchronously injected Clarity scripts; authored analytics/head source is checked separately against f8f9034.',
              'cases': [], 'errors': []}
    before = json.loads((OUT / 'protected-before.json').read_text(encoding='utf-8'))
    for snapshot in before.values():
        snapshot['head'] = re.sub(r'<script[^>]+src="https://(?:scripts\.clarity\.ms/|www\.clarity\.ms/tag/)[^"]*"[^>]*></script>', '', snapshot['head'])
    try:
        for motion in (['reduce'] if '--reduced-only' in sys.argv else ['no-preference', 'reduce']):
            for width in [320, 375, 768, 1440]:
                height = 900 if width == 1440 else 700
                context = browser.new_context(viewport={'width': width, 'height': height},
                    reduced_motion=motion, has_touch=True, device_scale_factor=1)
                page = context.new_page()
                case = {'width': width, 'height': height, 'motion': motion, 'checks': [],
                        'javascriptErrors': [], 'console': [], 'failedRequests': [], 'httpErrors': [], 'contactPosts': []}
                report['cases'].append(case)
                page.on('pageerror', lambda e: case['javascriptErrors'].append(str(e)))
                page.on('console', lambda m: case['console'].append({'type': m.type, 'text': m.text}) if m.type in ['error', 'warning'] else None)
                page.on('requestfailed', lambda r: case['failedRequests'].append({'url': r.url, 'failure': r.failure}))
                page.on('response', lambda r: case['httpErrors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
                page.on('request', lambda r: case['contactPosts'].append(r.url) if r.method == 'POST' and 'formspree' in r.url else None)
                prefix = f'{width}-{motion}'

                def check(name, ok, detail=None):
                    case['checks'].append({'name': name, 'passed': bool(ok), 'detail': detail})
                    assert ok, (prefix, name, detail)

                page.goto(URL, wait_until='domcontentloaded')
                page.evaluate('document.fonts.ready')
                page.wait_for_function("document.querySelector('.cs-compare__handle').style.left === '50%'")
                placement(page)
                check('one comparison follows exploration and precedes decision02', True)
                current = protected(page)
                check('preserved current surfaces match f8f9034 and current pre-change',
                      current == before['f8f9034'] == before['current-pre-change'],
                      {key: {'expected': before['f8f9034'][key], 'actual': current[key]} for key in current if current[key] != before['f8f9034'][key]})
                page.screenshot(path=str(OUT / f'{prefix}-header.png'))
                section_states = """() => [...document.querySelectorAll('main section')].map(e => ({
                    name: e.getAttribute('aria-labelledby') || e.className,
                    opacity: getComputedStyle(e).opacity, height: Math.round(e.getBoundingClientRect().height)
                }))"""
                case['initialSections'] = page.evaluate(section_states)
                if motion == 'reduce':
                    check('reduced motion sections immediately available', all(float(s['opacity']) == 1 for s in case['initialSections']))

                # Real wheel from top, without jumps, opacity overrides or reduced-motion substitution.
                check('scroll begins at top', page.evaluate('scrollY') == 0)
                seen = set()
                for step in range(150):
                    seen.update(page.evaluate("""() => [...document.querySelectorAll('main h2, main h3, main h4')].filter(e => {
                        const r = e.getBoundingClientRect();
                        const ancestors = []; for(let p=e;p;p=p.parentElement) ancestors.push(p);
                        return r.bottom > 90 && r.top < innerHeight && ancestors.every(p => Number(getComputedStyle(p).opacity) > .99);
                    }).map(e => e.textContent.trim())"""))
                    if page.evaluate('scrollY + innerHeight >= document.documentElement.scrollHeight - 2'):
                        break
                    page.mouse.wheel(0, 240)
                    # Let the existing 500 ms entrance finish before judging readable text.
                    page.wait_for_timeout(550 if motion == 'no-preference' else 100)
                page.wait_for_timeout(650)
                case['wheelSteps'] = step
                check('wheel traversal reaches bottom', page.evaluate('scrollY + innerHeight >= document.documentElement.scrollHeight - 2'))
                case['seenHeadingsDuringWheel'] = sorted(seen)
                case['finalSections'] = page.evaluate(section_states)
                check('all narrative sections become visible through wheel scrolling', all(float(s['opacity']) == 1 for s in case['finalSections']), case['finalSections'])
                headings = page.locator('main h2, main h3, main h4').all_text_contents()
                check('each narrative heading encountered while scrolling', set(h.strip() for h in headings) <= seen, sorted(set(h.strip() for h in headings) - seen))
                page.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0 && i.naturalHeight > 0)')
                images = page.locator('main img').evaluate_all('''es => es.map(e => ({src:e.getAttribute('src'),
                    natural:[e.naturalWidth,e.naturalHeight], intrinsic:[e.width,e.height],
                    declared:[e.getAttribute('width'),e.getAttribute('height')], alt:e.alt,
                    loading:e.loading, decoding:e.decoding, rect:[e.getBoundingClientRect().width,e.getBoundingClientRect().height]}))''')
                case['images'] = images
                check('all current images loaded and proportional', all(i['natural'][0] > 0 and abs(i['rect'][0] / i['rect'][1] - i['natural'][0] / i['natural'][1]) < .005 for i in images))
                check('all images have source dimensions, specific alternatives and lazy async loading', all(
                    i['natural'] == [int(v) for v in i['declared']] and len(i['alt']) > 50
                    and i['loading'] == 'lazy' and i['decoding'] == 'async' for i in images))
                # Recheck evidence already delivered by other slices on this merged page.
                evidence = page.locator('.enrollment-discovery, .enrollment-journey-evidence, .enrollment-submission-evidence').evaluate_all('''es => es.map(e => {
                    const image=e.querySelector('img'), copy=e.querySelector('figcaption') || e.querySelector('p:last-of-type'),
                        a=copy.getBoundingClientRect(), b=image.getBoundingClientRect();
                    return {name:e.getAttribute('aria-labelledby'), images:e.querySelectorAll('img').length,
                        copyFirst:!!(copy.compareDocumentPosition(image)&Node.DOCUMENT_POSITION_FOLLOWING),
                        copyAbove:a.bottom<=b.top, alt:image.alt,
                        font:getComputedStyle(copy.querySelector('p') || copy).fontSize,
                        outside:[...e.querySelectorAll('*')].some(n=>{const r=n.getBoundingClientRect();return r.left < -1 || r.right > innerWidth+1;})};
                })''')
                case['integratedEvidence'] = evidence
                check('discovery and four interface screens remain explained, ordered and fitted', len(evidence) == 5 and all(
                    e['images'] == 1 and e['copyFirst'] and e['copyAbove'] and len(e['alt']) > 60 and e['font'] == '16px' and not e['outside'] for e in evidence), evidence)
                selected = [i['src'].rsplit('/', 1)[-1] for i in images]
                check('exact final selection; omitted screens absent', len(selected) == 7 and set(selected) == {
                    'Desk%20Research.png', 'parentesco.png', 'dados-parente.png', 'portabilidade-2.png',
                    'submission-analysis.webp', 'old-enrollment-journey-simulator.jpg', 'new-enrollment-journey-simulator.jpg'}, selected)
                for item in evidence:
                    block = page.locator(f'[aria-labelledby="{item["name"]}"]')
                    block.screenshot(path=str(OUT / f'{prefix}-{item["name"]}.png'), style='.nav { visibility:hidden !important; }')
                compare_images = [i for i in images if 'simulator.jpg' in i['src']]
                check('original comparison dimensions, specific alternatives and lazy async loading', len(compare_images) == 2 and all(
                    i['natural'] == [1440,1485] and i['declared'] == ['1440','1485'] and len(i['alt']) > 50
                    and i['loading'] == 'lazy' and i['decoding'] == 'async' for i in compare_images))
                check('no horizontal overflow', page.evaluate('document.documentElement.scrollWidth') == width)
                check('explanations and metrics fit without text clipping', page.locator('figure figcaption h4, figure figcaption p, .enrollment-discovery__copy, .cs-stat__number').evaluate_all('es => es.every(e => e.scrollWidth <= e.clientWidth + 1)'))
                check('main content fits viewport edges', page.locator('main *').evaluate_all('''es => es.every(e => {
                    const r=e.getBoundingClientRect(); return !r.width || e.closest('.sr-only') || (r.left >= -.5 && r.right <= innerWidth + .5);
                })'''))
                check('all three problem points and decision notes remain', page.locator('.cs-problem__points li').count() == 3 and page.locator('.cs-decision__note').count() == 3)
                check('no raw-image links or disclosure controls added', page.locator('.enrollment-comparison a, .enrollment-comparison details, .enrollment-comparison button').count() == 0)
                geometry = page.evaluate('''() => {const c=document.querySelector('.enrollment-comparison figcaption'),
                    f=document.querySelector('.cs-compare'), a=c.getBoundingClientRect(), b=f.getBoundingClientRect();
                    return {copyBottom:a.bottom,imageTop:b.top,comparisonWidth:b.width,
                        fonts:[...c.querySelectorAll('p')].map(e=>getComputedStyle(e).fontSize)};}''')
                case['composition'] = geometry
                check('guidance precedes the wide comparison without overlap; body size preserved', geometry['copyBottom'] < geometry['imageTop'] and geometry['comparisonWidth'] >= width - (160 if width == 1440 else 48) - 1 and all(f == '16px' for f in geometry['fonts']))
                caption = page.locator('.enrollment-comparison figcaption')
                caption.evaluate("e => e.scrollIntoView({block:'start',behavior:'instant'})")
                page.evaluate('scrollBy(0,-95)')
                page.wait_for_timeout(150)
                page.screenshot(path=str(OUT / f'{prefix}-guidance.png'))
                # Isolated artifact only: hide the fixed nav so it cannot cover the element's title.
                # Viewport and interaction captures retain the real navigation.
                page.locator('.enrollment-comparison').screenshot(path=str(OUT / f'{prefix}-evidence.png'), style='.nav { visibility:hidden !important; }')

                # Keyboard entry from the preceding link, then native range keys and Tab exit.
                page.locator('.cs-header__back').focus()
                page.keyboard.press('Tab')
                slider = page.get_by_role('slider', name=NAME, exact=True)
                check('Tab enters named native comparison', slider.evaluate('e => e === document.activeElement'))
                check('visible focus frame', page.locator('.cs-compare').evaluate('e => getComputedStyle(e).outlineStyle === "solid" && parseFloat(getComputedStyle(e).outlineWidth) >= 2'))
                page.screenshot(path=str(OUT / f'{prefix}-focus.png'))
                key_results = []
                for key, value in [('Home',0), ('ArrowRight',1), ('End',100), ('ArrowLeft',99)]:
                    slider.press(key)
                    page.wait_for_function('v => document.querySelector("input[type=range]").value === String(v) && document.querySelector(".cs-compare__handle").style.left === v + "%"', arg=value)
                    page.wait_for_timeout(40)
                    position = page.locator('.cs-compare').evaluate('''e => {const r=e.getBoundingClientRect(),
                        h=e.querySelector('.cs-compare__handle').getBoundingClientRect();return {
                        dividerPercent:100*(h.x+h.width/2-r.x)/r.width,
                        clip:getComputedStyle(e.querySelector('.cs-compare__before')).clipPath};}''')
                    key_results.append({'key':key,'value':slider.input_value(),**position})
                    check(f'{key} updates value and visible reveal', int(slider.input_value()) == value and abs(position['dividerPercent'] - value) < .1 and abs(float(position['clip'].split()[1].rstrip('%')) - (100-value)) < .1, position)
                case['keys'] = key_results
                # Compare rendered endpoint pixels to independent original raster sources.
                for key, source in [('Home','new'), ('End','old')]:
                    slider.press(key)
                    page.wait_for_timeout(50)
                    shot = OUT / f'{prefix}-{source}.png'
                    page.locator('.cs-compare').screenshot(path=str(shot))
                    actual = Image.open(shot).convert('RGB')
                    expected = Image.open(ROOT / f'assets/images/enrollment/{source}-enrollment-journey-simulator.jpg').convert('RGB').resize(actual.size, Image.Resampling.LANCZOS)
                    crop = (int(actual.width*.12),int(actual.height*.2),int(actual.width*.88),int(actual.height*.7))
                    mean = sum(ImageStat.Stat(ImageChops.difference(actual.crop(crop), expected.crop(crop))).mean) / 3
                    check(f'{key} visibly shows {source} original raster', mean < 8, {'meanChannelDifference':mean})
                page.keyboard.press('Tab')
                check('Tab exits to next project', page.locator('.cs-next__link').evaluate('e => e === document.activeElement'))
                page.keyboard.press('Shift+Tab')
                check('Shift+Tab re-enters comparison', slider.evaluate('e => e === document.activeElement'))

                # Put actual interaction point below fixed navigation; never click behind it.
                slider.evaluate("e => e.scrollIntoView({block:'start',behavior:'instant'})")
                page.evaluate('scrollBy(0,-110)')
                page.wait_for_timeout(150)
                rect = slider.bounding_box()
                y = min(height - 40, rect['y'] + min(rect['height']*.5, 220))
                x25, x75 = rect['x']+rect['width']*.25, rect['x']+rect['width']*.75
                check('pointer/touch target is visible below navigation', page.evaluate('''p => {
                    const nav = document.querySelector('.nav').getBoundingClientRect();
                    return p.y > nav.bottom && document.elementFromPoint(p.x,p.y).type === 'range';}''', {'x':x25,'y':y}), {'x25':x25,'x75':x75,'y':y})
                page.mouse.click(x25,y)
                case['pointerValue'] = int(slider.input_value())
                check('pointer changes comparison at visible point', 18 <= case['pointerValue'] <= 32)
                page.wait_for_function('v => document.querySelector(".cs-compare__handle").style.left === v + "%" && document.querySelector(".cs-compare__before").style.clipPath === `inset(0px ${100-v}% 0px 0px)`', arg=case['pointerValue'])
                check('pointer value corresponds to visible reveal', True)
                session = context.new_cdp_session(page)
                session.send('Input.dispatchTouchEvent', {'type':'touchStart','touchPoints':[{'x':x25,'y':y}]})
                for fraction in [.4,.55,.75]:
                    session.send('Input.dispatchTouchEvent', {'type':'touchMove','touchPoints':[{'x':rect['x']+rect['width']*fraction,'y':y}]})
                session.send('Input.dispatchTouchEvent', {'type':'touchEnd','touchPoints':[]})
                case['touchValue'] = int(slider.input_value())
                check('emulated touch drag changes comparison', 68 <= case['touchValue'] <= 82)
                page.wait_for_function('v => document.querySelector(".cs-compare__handle").style.left === v + "%" && document.querySelector(".cs-compare__before").style.clipPath === `inset(0px ${100-v}% 0px 0px)`', arg=case['touchValue'])
                check('touch value corresponds to visible reveal', True)
                session.detach()
                check('navigation, back and next destinations are served', all(page.request.get(h).ok for h in [
                    ORIGIN + '/', ORIGIN + '/case-studies/convenios.html']))
                page.locator('#contact').scroll_into_view_if_needed()
                check('contact fields and copy control available without submission', page.get_by_role('textbox',name='Your name').is_visible() and page.get_by_role('textbox',name='Your email').is_visible() and page.get_by_role('textbox',name='Your message').is_visible() and page.get_by_role('button',name='Copy email address').is_visible())
                page.locator('#name').focus()
                page.keyboard.press('Tab')
                check('contact Tab from name to email', page.locator('#email').evaluate('e => e === document.activeElement'))
                page.keyboard.press('Tab')
                check('contact Tab from email to message', page.locator('#message').evaluate('e => e === document.activeElement'))
                check('no actual contact POST', not case['contactPosts'])
                check('no application errors or local failed assets', not case['javascriptErrors'] and not [r for r in case['failedRequests'] + case['httpErrors'] if r['url'].startswith(ORIGIN + '/')])
                print(f'PASS {prefix}: {len(case["checks"])} browser checks')
                context.close()
    except Exception:
        report['errors'].append(traceback.format_exc())
        raise
    finally:
        report['summary'] = {'passed': sum(c['passed'] for case in report['cases'] for c in case['checks']),
                             'failed': sum(not c['passed'] for case in report['cases'] for c in case['checks'])}
        (OUT / 'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 700}, reduced_motion='reduce')
    if '--baseline' in sys.argv:
        snapshots = {}
        for ref in ['f8f9034', 'fa56b5c']:
            html = subprocess.check_output(['git', 'show', f'{ref}:case-studies/enrollment.html'], cwd=ROOT)
            page.route(URL, lambda route, request, html=html: route.fulfill(body=html, content_type='text/html'))
            page.goto(URL, wait_until='domcontentloaded')
            page.evaluate('document.fonts.ready')
            snapshots[ref] = protected(page)
            page.unroute(URL)
        page.goto(URL, wait_until='domcontentloaded')
        snapshots['current-pre-change'] = protected(page)
        assert snapshots['f8f9034'] == snapshots['current-pre-change']
        (OUT / 'protected-before.json').write_text(json.dumps(snapshots, indent=2), encoding='utf-8')
        print('PASS protected current pre-change surfaces match f8f9034')
    else:
        page.goto(URL, wait_until='domcontentloaded')
        placement(page)
        print('PASS comparison belongs to exploration with preceding guidance')
        if '--control' in sys.argv:
            slider = page.get_by_role('slider', name=NAME, exact=True)
            assert slider.count() == 1, 'Comparison control explains its purpose'
            for _ in range(15):
                page.keyboard.press('Tab')
                if slider.evaluate('e => e === document.activeElement'):
                    break
            assert slider.evaluate('e => e === document.activeElement'), 'Tab enters comparison'
            assert page.locator('.cs-compare').evaluate('e => getComputedStyle(e).outlineStyle !== "none" && parseFloat(getComputedStyle(e).outlineWidth) >= 2'), 'Visible focus surrounds the comparison'
            page.keyboard.press('Tab')
            assert not slider.evaluate('e => e === document.activeElement'), 'Tab leaves comparison'
            print('PASS named control, Tab entry/exit and visible focus')
        if '--matrix' in sys.argv:
            page.close()
            matrix(browser)
    browser.close()
