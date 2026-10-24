"""Responsive browser QA for the authorized Billing revision; no site dependencies."""
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.scratch/billing'
sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

before = (OUT / 'before.html').read_text(encoding='utf-8')
after = (ROOT / 'case-studies/billing.html').read_text(encoding='utf-8')
preserved = {}
for label, pattern in {
    'navigation': r'<header>[\s\S]*?</header>',
    'contact': r'<!-- Contact -->[\s\S]*?</section>',
    'images': r'<img\b[^>]*>',
    'stats': r'<div class="cs-stats"[\s\S]*?\n      </div>',
    'next_project': r'<div class="cs-next">[\s\S]*?</div>',
    'scripts': r'<script\b[^>]*>[\s\S]*?</script>',
    'anchor_ids': r'\bid="[^"]+"',
}.items():
    preserved[label] = re.findall(pattern, before) == re.findall(pattern, after)
assert all(preserved.values()), preserved

results = {'preserved': preserved, 'viewports': [], 'motion': [], 'clipboard': None}
with sync_playwright() as p:
    browser = p.chromium.launch()
    results['browser'] = browser.version
    for width in [320, 375, 768, 1440]:
        page = browser.new_page(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
        errors, icons, local_failures = [], [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        def response_handler(response):
            if '/assets/icons/' in response.url:
                icons.append({'url': response.url, 'status': response.status})
            if response.url.startswith('http://localhost:8000/') and response.status >= 400:
                local_failures.append({'url': response.url, 'status': response.status})
        page.on('response', response_handler)
        page.goto('http://localhost:8000/case-studies/billing.html', wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        data = page.evaluate('''() => {
          const rect = el => { const r = el.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom}; };
          const intro = document.querySelector('[aria-labelledby="billing-problem"] .cs-section__body');
          const list = document.querySelector('.cs-problem__points');
          return {
            viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth,
            overflow: [...document.querySelectorAll('body *')].filter(el => {
              const r = el.getBoundingClientRect();
              return r.width && (r.x < -1 || r.right > innerWidth + 1);
            }).map(el => el.className),
            points: list.children.length,
            pointsBelowIntro: rect(list).y >= rect(intro).bottom,
            markers: getComputedStyle(list).listStyleType,
            oldAsideOrPills: document.querySelectorAll('.cs-stakes,.cs-problem__layout,.cs-decision__tradeoff').length,
            notes: [...document.querySelectorAll('.cs-decision')].map(el => {
              const body = el.querySelector('.cs-decision__body');
              const note = el.querySelector('.cs-decision__note');
              const icon = note.querySelector('.cs-decision__note-icon');
              const css = getComputedStyle(note);
              return {text:note.innerText, belowBody:rect(note).y >= rect(body).bottom,
                columns:getComputedStyle(el).gridTemplateColumns, background:css.backgroundColor,
                icon:rect(icon), mask:getComputedStyle(icon).maskImage,
                decorative:icon.getAttribute('aria-hidden')};
            }),
            images: [...document.images].map(img => ({src:img.getAttribute('src'),loaded:img.complete && img.naturalWidth > 0})),
            target: document.querySelectorAll('.cs-decision__body')[2].innerText,
            historical: document.querySelector('[aria-labelledby="billing-outcome"] .cs-section__body').innerText,
            next: document.querySelector('.cs-next__link').getAttribute('href')
          };
        }''')
        assert data['scrollWidth'] == width and not data['overflow'], data
        assert data['points'] == 3 and data['pointsBelowIntro'] and data['markers'] == 'disc', data
        assert data['oldAsideOrPills'] == 0 and len(data['notes']) == 3, data
        for note in data['notes']:
            assert note['belowBody'] and note['icon']['width'] == 24 and note['icon']['height'] == 24, note
            assert note['decorative'] == 'true' and note['mask'] != 'none', note
            assert note['background'] == 'rgba(0, 0, 0, 0)', note
            assert len(note['columns'].split()) == 1, note
        assert all(img['loaded'] for img in data['images']), data
        assert len(icons) == 3 and all(item['status'] == 200 for item in icons), icons
        assert not errors and not local_failures, (errors, local_failures)
        assert 'design target' in data['target'] and 'Clarity' in data['target'], data
        assert data['next'] == 'enrollment.html', data
        if width in [375, 1440]:
            for section in ['problem', 'decisions', 'shipped', 'outcome']:
                page.locator(f'[aria-labelledby="billing-{section}"]').screenshot(path=str(OUT / f'{section}-{width}.png'), style='header { visibility: hidden !important; }')
            page.evaluate('window.scrollTo(0,0)')
            page.screenshot(path=str(OUT / f'header-{width}.png'))
        results['viewports'].append({'width':width, 'checks':data, 'icons':icons, 'pageErrors':errors, 'localFailures':local_failures})
        page.close()
    for width in [375, 1440]:
        context = browser.new_context(viewport={'width':width, 'height':1000}, permissions=['clipboard-read','clipboard-write'])
        page = context.new_page()
        page.goto('http://localhost:8000/case-studies/billing.html', wait_until='networkidle')
        for section in page.locator('.cs-section').all():
            section.scroll_into_view_if_needed()
            page.wait_for_timeout(600)
            assert float(section.evaluate('el => getComputedStyle(el).opacity')) == 1
        page.locator('.contact__copy').click()
        page.wait_for_function("document.querySelector('.contact__copy-feedback').textContent === 'Copied!'")
        assert page.evaluate('navigator.clipboard.readText()') == 'fplevi@gmail.com'
        results['motion'].append({'width':width,'allSectionsRevealed':True,'clipboard':True})
        context.close()
    results['clipboard'] = 'Copied! and expected email confirmed in both widths; no form submission.'
    browser.close()

hashes = json.loads((OUT/'protected-before.json').read_text())
results['protectedFileComparison'] = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == old for path, old in hashes.items()}
(OUT/'qa-results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'widths':[item['width'] for item in results['viewports']], 'preserved':preserved,
    'motion':results['motion'],'protectedFileComparison':results['protectedFileComparison']}, indent=2))
