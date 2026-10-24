"""Ticket 04 browser seam, adapted from Enrollment qa.py and Billing narrative QA.

Uses the existing temporary Playwright install; no project dependencies.
"""
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / 'qa' / 'ticket-04'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8104/case-studies/enrollment.html'
STORIES = {
    'eligibility': ('Eligibility within the journey', 'parentesco.png', 'seven-step'),
    'personal': ('Personal details and document preparation', 'dados-parente.png', 'partly outside'),
    'portability': ('Portability as a specific situation', 'portabilidade-2.png', 'categories remain closed'),
}


def story(page, name):
    title, source, meaning = STORIES[name]
    figure = page.get_by_role('figure', name=title, exact=True)
    assert figure.count() == 1, f'Reader cannot find the {name} evidence: {title}'
    figure.scroll_into_view_if_needed()
    page.wait_for_timeout(650)
    assert figure.is_visible()
    assert meaning in figure.inner_text(), f'{name}: missing orientation'
    image = figure.get_by_role('img')
    assert image.count() == 1 and image.get_attribute('src').endswith('/' + source)
    assert image.get_attribute('alt') and len(image.get_attribute('alt')) > 60
    image.evaluate('(i) => i.decode()')
    assert image.evaluate('(i) => i.naturalWidth === 1920 && i.naturalHeight === 1200')
    assert figure.evaluate('''f => {
      const c=f.querySelector('figcaption'), i=f.querySelector('img');
      return !!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING)
        && !f.querySelector('a,button,input,details');
    }'''), f'{name}: explanation must precede static evidence'


if __name__ == '__main__':
    name = sys.argv[1]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 700}, reduced_motion='reduce')
        page.goto(URL, wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        try:
            story(page, name)
            result = {'story': name, 'passed': True}
        except AssertionError as error:
            result = {'story': name, 'passed': False, 'error': str(error)}
        (OUT / f'{name}-{sys.argv[2]}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        browser.close()
        print(json.dumps(result))
        assert result['passed'], result
