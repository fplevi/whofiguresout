"""Browser QA using the existing temporary Playwright installation; no project dependencies."""
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

output = Path(__file__).parent / 'qa'
output.mkdir(exist_ok=True)
baseline = '--baseline' in sys.argv
results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for width in ([375, 1440] if baseline else [320, 375, 768, 1440]):
        page = browser.new_page(viewport={'width': width, 'height': 1000}, device_scale_factor=1)
        errors, responses = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: responses.append({'url': response.url, 'status': response.status}))
        page.goto('http://localhost:8000/case-studies/enrollment.html', wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        for name in ['problem', 'decisions', 'shipped', 'outcome']:
            section = page.locator(f'section[aria-labelledby="enrollment-{name}"]')
            section.scroll_into_view_if_needed()
            page.wait_for_timeout(600)
            if width in [375, 1440]:
                section.screenshot(path=str(output / f'{"before" if baseline else "after"}-{name}-{width}.png'), style='.nav { visibility: hidden !important; }')
        if not baseline:
            slider = page.get_by_role('slider', name='Comparison slider')
            slider.focus()
            slider.press('Home')
            assert slider.input_value() == '0'
            assert page.locator('.cs-compare__handle').evaluate("el => el.style.left") == '0%'
            slider.press('ArrowRight')
            assert slider.input_value() == '1'
            slider.press('End')
            assert slider.input_value() == '100'
            assert page.locator('.cs-compare__before').evaluate("el => el.style.clipPath") == 'inset(0px 0% 0px 0px)'
            slider.press('ArrowLeft')
            assert slider.input_value() == '99'
            slider.evaluate("el => el.scrollIntoView({block: 'start', behavior: 'instant'})")
            page.wait_for_timeout(600)
            slider_box = slider.bounding_box()
            page.mouse.click(slider_box['x'] + slider_box['width'] * .25, max(150, slider_box['y'] + 150))
            assert 15 < int(slider.input_value()) < 35
        checks = page.evaluate('''() => ({
          width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
          brokenImages: [...document.images].filter(img => !img.complete || !img.naturalWidth).map(img => img.src),
          bullets: document.querySelectorAll('.cs-problem__points li').length,
          notes: [...document.querySelectorAll('.cs-decision__note')].map(note => ({
            below: note.getBoundingClientRect().top >= note.previousElementSibling.getBoundingClientRect().bottom,
            mask: getComputedStyle(note.querySelector('.cs-decision__note-icon')).maskImage,
            decorative: note.querySelector('.cs-decision__note-icon').getAttribute('aria-hidden')
          })),
          oldTags: document.querySelectorAll('.cs-stakes, .cs-decision__tradeoff').length,
          next: document.querySelector('.cs-next__link').getAttribute('href'),
          fonts: document.fonts.status
        })''')
        if not baseline:
            assert checks['scrollWidth'] == width, checks
            assert not checks['brokenImages'], checks
            assert checks['bullets'] == 3 and len(checks['notes']) == 3
            assert all(note['below'] and note['mask'] != 'none' and note['decorative'] == 'true' for note in checks['notes'])
            assert checks['oldTags'] == 0 and checks['next'] == 'convenios.html'
            assert not errors, errors
            icons = [response for response in responses if '/icons/tabler/enrollment/' in response['url']]
            assert len(icons) == 3 and all(icon['status'] == 200 for icon in icons), icons
        results.append({**checks, 'javascriptErrors': errors, 'icons': [r for r in responses if '/icons/' in r['url']]})
        page.close()
    browser.close()
(output / f'{"baseline" if baseline else "validation"}.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
