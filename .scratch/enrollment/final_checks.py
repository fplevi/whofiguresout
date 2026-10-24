import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[2]
page_html = (root / 'case-studies/enrollment.html').read_text(encoding='utf-8')
old_html = subprocess.check_output(['git', 'show', 'HEAD:case-studies/enrollment.html'], cwd=root, text=True, encoding='utf-8')
for pattern in [r'<div class="cs-compare"[\s\S]*?</section>', r'<div class="cs-next">[\s\S]*?</div>', r'<header>[\s\S]*?</header>']:
    assert re.search(pattern, page_html).group() == re.search(pattern, old_html).group()

results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for width in [375, 1025, 1280, 1440]:
        page = browser.new_page(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
        page.goto('http://localhost:8000/case-studies/enrollment.html', wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        if width in [375, 1440]:
            page.locator('.cs-header').screenshot(path=str(Path(__file__).parent / 'qa' / f'after-header-{width}.png'))
        cards = page.locator('.cs-stat__number').evaluate_all('(els) => els.map(el => ({width: el.clientWidth, content: el.scrollWidth}))')
        assert all(card['width'] >= card['content'] for card in cards), (width, cards)
        slider = page.get_by_role('slider', name='Comparison slider')
        slider.focus()
        slider.press('Home')
        slider.press('ArrowRight')
        assert slider.input_value() == '1'
        assert page.locator('.cs-compare__handle').evaluate("el => el.style.left") == '1%'
        results.append({'width': width, 'cardContentFits': True, 'reducedMotionKeyboardComparator': True})
        page.close()
    browser.close()
result = {'protectedMarkupMatchesHead': ['comparator', 'next-project', 'primary-navigation'], 'percentage': (1105-408)/408*100, 'browserChecks': results}
(Path(__file__).parent / 'qa' / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
