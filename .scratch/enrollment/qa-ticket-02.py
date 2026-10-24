"""Ticket 02 rendered-page tests; adapted from Enrollment qa.py and final_checks.py.

Uses the existing temporary Playwright installation, without project dependencies.
"""
import json
import os
import hashlib
from pathlib import Path
import platform
import subprocess
import sys
import traceback

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / 'qa' / 'ticket-02'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8102/case-studies/enrollment.html'
ROOT = Path(__file__).resolve().parents[2]
BASELINE = 'f8f9034'
PROTECTED = ['header', '.cs-header', '.cs-hero-image',
             'section[aria-labelledby="enrollment-problem"]',
             'section[aria-labelledby="enrollment-role"]',
             'section[aria-labelledby="enrollment-outcome"]', '.cs-next', '#contact']


def preserved_surfaces(page):
    # Entrance animation writes runtime styles onto section roots. Compare authored
    # content independently of that motion state; visibility is tested on the wheel path.
    surfaces = {selector: page.locator(selector).evaluate('''e => {
      const copy=e.cloneNode(true); copy.removeAttribute('style'); return copy.outerHTML;
    }''') for selector in PROTECTED}
    surfaces['analytics-and-scripts'] = page.locator('script').evaluate_all(r'''els => els
      .filter(e => !e.src || e.src.includes(location.host) || /googletagmanager|clarity/.test(e.src))
      .map(e => e.outerHTML).join('\n')''')
    return surfaces


def wheel_entire_page(page):
    """Start at top, then use real wheel input only until the end of the page."""
    assert page.evaluate('scrollY') == 0
    trace = []
    seen = set()
    for _ in range(140):
        visible = page.locator('main > section, .cs-next').evaluate_all('''els => els.filter(e => {
          const r=e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 80;
        }).map(e => e.getAttribute('aria-labelledby') || e.className)''')
        seen.update(visible)
        trace.append(page.evaluate('scrollY'))
        if page.evaluate('scrollY + innerHeight >= document.documentElement.scrollHeight - 2'):
            break
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(100)
    page.wait_for_timeout(650)
    sections = page.locator('main > section, .cs-next').evaluate_all('''els => els.map(e => ({
      name:e.getAttribute('aria-labelledby') || e.className,
      opacity:getComputedStyle(e).opacity, visibility:getComputedStyle(e).visibility,
      height:e.getBoundingClientRect().height
    }))''')
    assert page.evaluate('scrollY + innerHeight >= document.documentElement.scrollHeight - 2'), 'Wheel path did not reach bottom'
    assert all(s['name'] in seen and s['opacity'] == '1' and s['visibility'] == 'visible' for s in sections), sections
    return {'input': 'mouse.wheel(0, 300)', 'scrollY': trace, 'sections': sections}


def contrast_samples(page):
    """Measure computed sRGB foreground composited over computed ancestor backgrounds."""
    return page.get_by_role('region', name='Organizing discovery.', exact=True).locator('h2, p').evaluate_all('''els => {
      const rgba = s => { const a=s.match(/[\\d.]+/g).map(Number); return [...a.slice(0,3), a[3] ?? 1]; };
      const over = (a,b) => a.slice(0,3).map((v,i) => v*a[3]+b[i]*(1-a[3]));
      const lum = c => c.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4)
        .reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
      return els.map(e=>{
        const chain=[]; for(let n=e;n;n=n.parentElement) chain.unshift(n);
        let bg=[255,255,255]; for(const n of chain) bg=over(rgba(getComputedStyle(n).backgroundColor),bg);
        const cs=getComputedStyle(e), fg=over(rgba(cs.color),bg), a=lum(fg), b=lum(bg);
        return {text:e.textContent.trim(), cssColor:cs.color, background:bg, compositedForeground:fg,
          ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05), fontSize:cs.fontSize, lineHeight:cs.lineHeight};
      });
    }''')


def comparison_still_works(page, context):
    slider = page.get_by_role('slider')
    assert slider.count() == 1
    # Tab entry and exit through the existing page's public focus order.
    page.get_by_role('link', name='Back to work').focus()
    page.keyboard.press('Tab')
    assert slider.evaluate('e => e === document.activeElement')
    for key, expected in [('Home', '0'), ('ArrowRight', '1'), ('End', '100'), ('ArrowLeft', '99')]:
        slider.press(key)
        page.wait_for_timeout(80)
        assert slider.input_value() == expected
        # Inspect the visible reveal boundary and clipping, not a private JS helper.
        reveal = slider.evaluate('''e => {
          const c=e.parentElement, before=c.querySelector('.cs-compare__before'), h=c.querySelector('.cs-compare__handle');
          return {clip:getComputedStyle(before).clipPath,left:parseFloat(getComputedStyle(h).left),width:c.clientWidth};
        }''')
        assert abs(reveal['left'] / reveal['width'] * 100 - int(expected)) < 1, (key, expected, reveal)
        assert f'{100 - int(expected)}%' in reveal['clip'] or (expected == '100' and reveal['clip'] == 'inset(0px 0% 0px 0px)')
    page.keyboard.press('Tab')
    assert page.get_by_role('link', name='CASSI Convênios').evaluate('e => e === document.activeElement')
    # Center a visible part of the image below the fixed nav before pointer/touch input.
    slider.evaluate('e => e.scrollIntoView({block:"start", behavior:"instant"})')
    page.evaluate('scrollBy(0,-100)')
    page.wait_for_timeout(600)
    box = slider.bounding_box()
    y = max(130, box['y'] + 40)
    assert y < page.viewport_size['height']
    page.mouse.click(box['x'] + box['width'] * .25, y)
    pointer = int(slider.input_value())
    assert 15 <= pointer <= 35, pointer
    page.touchscreen.tap(box['x'] + box['width'] * .75, y)
    touch = int(slider.input_value())
    assert 65 <= touch <= 85, touch
    return {'name': slider.get_attribute('aria-label'), 'keyboard': ['Tab', 'Home', 'ArrowRight', 'End', 'ArrowLeft', 'Tab'],
            'pointerValue': pointer, 'emulatedTouchValue': touch,
            'focusLimitation': 'Preserved baseline range is transparent; visible focus/name improvements belong to ticket 03.'}


def matrix(browser):
    old_html = subprocess.check_output(['git', 'show', f'{BASELINE}:case-studies/enrollment.html'], cwd=ROOT).decode('utf-8')
    baseline_page = browser.new_page(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    baseline_url = URL.replace('enrollment.html', 'enrollment-baseline.html')
    baseline_page.route(baseline_url, lambda route: route.fulfill(status=200, content_type='text/html', body=old_html))
    baseline_page.goto(baseline_url, wait_until='networkidle')
    protected = preserved_surfaces(baseline_page)
    baseline_page.close()
    result = {'environment': {'os': platform.platform(), 'python': platform.python_version(), 'browser': browser.version,
              'engine': 'Playwright Chromium, headless, device scale 1; emulated touch, no real device'},
              'url': URL, 'baseline': BASELINE, 'runs': [], 'pageErrors': [], 'failedRequests': [],
              'consoleWarningsAndErrors': [], 'formSubmissions': []}
    try:
        for width in [320, 375, 768, 1440]:
            for motion in ['no-preference', 'reduce']:
                height = 900 if width == 1440 else 700
                ctx = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=motion,
                                          device_scale_factor=1, has_touch=True)
                page = ctx.new_page()
                run = {'width': width, 'height': height, 'motion': motion}
                result['runs'].append(run)
                page.on('pageerror', lambda error: result['pageErrors'].append(str(error)))
                page.on('console', lambda m: m.type in ['warning', 'error'] and result['consoleWarningsAndErrors'].append(m.text))
                page.on('requestfailed', lambda r: result['failedRequests'].append({'url': r.url, 'failure': r.failure}))
                page.on('response', lambda r: r.status >= 400 and result['failedRequests'].append({'url': r.url, 'status': r.status}))
                page.on('request', lambda r: r.method == 'POST' and 'formspree' in r.url and result['formSubmissions'].append(r.url))
                try:
                    page.goto(URL, wait_until='networkidle')
                    page.evaluate('document.fonts.ready')
                    current = preserved_surfaces(page)
                    run['protectedMatchesBaseline'] = {key: current[key] == value for key, value in protected.items()}
                    assert all(run['protectedMatchesBaseline'].values()), run['protectedMatchesBaseline']
                    run['protectedSha256'] = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in current.items()}
                    if motion == 'reduce':
                        assert page.locator('main > section').evaluate_all('els=>els.every(e=>getComputedStyle(e).opacity==="1")')
                        run['reducedMotionImmediatelyVisible'] = True
                    run['wheelTraversal'] = wheel_entire_page(page)
                    page.wait_for_function('[...document.images].every(i => i.complete && i.naturalWidth > 0)')
                    run['allImages'] = page.locator('img').evaluate_all('''els=>els.map(i=>({src:i.getAttribute('src'),
                      natural:[i.naturalWidth,i.naturalHeight],rendered:[i.width,i.height],alt:i.alt}))''')
                    discovery_is_explained_before_decisions(page)
                    board = page.get_by_role('region', name='Organizing discovery.', exact=True)
                    img = board.get_by_role('img')
                    data = img.evaluate('''i => ({natural:[i.naturalWidth,i.naturalHeight],
                      intrinsic:[i.getAttribute('width'),i.getAttribute('height')],
                      rendered:[i.getBoundingClientRect().width,i.getBoundingClientRect().height],
                      alt:i.alt,loading:i.loading,decoding:i.decoding})''')
                    run['boardImage'] = data
                    assert data['natural'] == [1672, 661] and data['intrinsic'] == ['1672', '661']
                    assert data['loading'] == 'lazy' and data['decoding'] == 'async'
                    assert abs(data['rendered'][0] / data['rendered'][1] - 1672 / 661) < .01
                    assert board.locator('a,button,input,details,summary,[tabindex]').count() == 0
                    assert page.evaluate('document.documentElement.scrollWidth') == width
                    run['textFits'] = board.locator('h2,p').evaluate_all('''els=>els.every(e=>{
                      const r=e.getBoundingClientRect(); return e.scrollWidth<=e.clientWidth+1 && r.left>=0 && r.right<=innerWidth;
                    })''')
                    assert run['textFits']
                    run['contrast'] = contrast_samples(page)
                    assert all(s['ratio'] >= 4.5 for s in run['contrast'])
                    assert all(float(s['fontSize'][:-2]) >= 16 for s in run['contrast'])
                    run['statContentFits'] = page.locator('.cs-stat__number').evaluate_all('els=>els.every(e=>e.scrollWidth<=e.clientWidth)')
                    assert run['statContentFits']
                    run['headingLevels'] = page.locator('main h1,main h2,main h3').evaluate_all('els=>els.map(e=>({level:e.tagName,text:e.innerText}))')
                    label = f'{width}-{motion}'
                    # After the real wheel traversal, return to top only for captures.
                    # Crop the full-page render at document coordinates so fixed nav
                    # does not overlay a heading in a tall element screenshot.
                    page.evaluate('scrollTo(0,0)')
                    page.wait_for_timeout(100)
                    page.screenshot(path=str(OUT / f'board-{label}.png'), full_page=True, clip=board.bounding_box())
                    page.screenshot(path=str(OUT / f'page-{label}.png'), full_page=True)
                    run['screenshots'] = [f'board-{label}.png', f'page-{label}.png']
                    run['comparison'] = comparison_still_works(page, ctx)
                    # Form fields and submit remain available, without sending a message.
                    assert page.get_by_role('textbox', name='Your name').count() == 1
                    assert page.get_by_role('textbox', name='Your email').count() == 1
                    assert page.get_by_role('textbox', name='Your message').count() == 1
                    assert page.get_by_role('button', name='Send message').count() == 1
                    run['status'] = 'passed'
                    print(f'PASS {width}x{height} {motion}', flush=True)
                except Exception as error:
                    run['status'] = 'failed'
                    run['failure'] = traceback.format_exc()
                    print(f'FAIL {width}x{height} {motion}: {run["failure"]}', flush=True)
                finally:
                    ctx.close()
    finally:
        result['localFailedRequests'] = [r for r in result['failedRequests'] if r['url'].startswith('http://127.0.0.1:8102/')]
        result['summary'] = {'passed': sum(r.get('status') == 'passed' for r in result['runs']),
                             'failed': sum(r.get('status') != 'passed' for r in result['runs'])}
        (OUT / 'matrix.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    assert result['summary'] == {'passed': 8, 'failed': 0}, result['summary']
    assert not result['pageErrors'], result['pageErrors']
    assert not result['localFailedRequests'], result['localFailedRequests']
    assert not result['formSubmissions']
    print(json.dumps(result['summary']))


def discovery_is_explained_before_decisions(page):
    """A reader can understand the single board between role and decisions."""
    board = page.get_by_role('region', name='Organizing discovery.', exact=True)
    assert board.count() == 1, 'Expected one dedicated discovery-synthesis region'
    board.scroll_into_view_if_needed()
    text = board.inner_text()
    for artifact in ['CSD matrix', 'brainstorming', 'user/customer journey', 'empathy map']:
        assert artifact in text, f'The HTML explanation must identify {artifact}'
    assert 'Desk Research' in text and 'sources or methods' in text
    image = board.get_by_role('img')
    assert image.count() == 1
    assert page.get_by_role('img', name=image.get_attribute('alt'), exact=True).count() == 1
    assert board.evaluate('''el => {
      const img = el.querySelector('img');
      const explanation = [...el.querySelectorAll('p')].at(-1);
      const role = document.getElementById('enrollment-role').closest('section');
      const decisions = document.getElementById('enrollment-decisions').closest('section');
      return !!(role.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)
        && !!(el.compareDocumentPosition(decisions) & Node.DOCUMENT_POSITION_FOLLOWING)
        && !!(explanation.compareDocumentPosition(img) & Node.DOCUMENT_POSITION_FOLLOWING)
        && explanation.getBoundingClientRect().bottom <= img.getBoundingClientRect().top;
    }'''), 'Role, explanation, board and decisions must follow the intended reading order'


if __name__ == '__main__':
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        if '--matrix' in sys.argv:
            try:
                matrix(browser)
            finally:
                browser.close()
            sys.exit(0)
        page = browser.new_page(viewport={'width': 375, 'height': 700}, reduced_motion='reduce')
        page.goto(URL, wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        try:
            discovery_is_explained_before_decisions(page)
        except AssertionError as error:
            (OUT / 'discovery-test-failure.json').write_text(json.dumps({'failure': str(error), 'url': URL,
                'viewport': [375, 700], 'motion': 'reduce'}, indent=2), encoding='utf-8')
            raise
        finally:
            browser.close()
    (OUT / 'green.json').write_text(json.dumps({'stage': 'green', 'behavior': 'Discovery explanation and one board between role and decisions',
        'viewport': [375, 700], 'motion': 'reduce', 'status': 'passed'}, indent=2), encoding='utf-8')
    print('PASS: discovery is explained between role and decisions')
