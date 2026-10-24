"""Ticket 05 rendered-page seam; adapted from Enrollment qa.py and Billing QA.

Uses the existing temporary Playwright install. Serve this worktree on port 8125.
"""
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / 'qa' / 'ticket-05'
OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8125/case-studies/enrollment.html'
TITLE = 'Submitted for analysis, with a reference for what comes next'


def story(page):
    figure = page.get_by_role('figure', name=TITLE, exact=True)
    assert figure.count() == 1, 'Reader cannot find the submission evidence beside the third decision'
    decision = page.get_by_role('heading', name='Structured status visibility throughout').locator('..').locator('..')
    assert decision.get_by_role('figure', name=TITLE, exact=True).count() == 1
    figure.scroll_into_view_if_needed()
    page.wait_for_timeout(650)
    assert figure.is_visible()
    copy = figure.inner_text()
    for meaning in ['submitted for analysis', 'protocol number', 'placeholder', 'not approval',
                    'does not verify email delivery', 'unmeasured objective']:
        assert meaning in copy, f'Missing evidence limit: {meaning}'
    image = figure.get_by_role('img')
    assert image.count() == 1
    assert len(image.get_attribute('alt')) > 70
    image.evaluate('i=>i.decode()')
    assert image.evaluate('i=>i.naturalWidth>0 && i.naturalHeight>0')
    assert image.evaluate('i=>+i.getAttribute("width")===i.naturalWidth && +i.getAttribute("height")===i.naturalHeight'), 'Intrinsic dimensions must match the presentation image'
    assert figure.evaluate('''f=>{
      const c=f.querySelector('figcaption'),i=f.querySelector('img');
      return !!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING)
        && !f.querySelector('a,button,input,details');
    }'''), 'The explanation must precede one static screenshot without additional controls'


if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width':375,'height':700}, reduced_motion='reduce')
        page.goto(URL, wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        try:
            story(page)
            result = {'story':'submission next steps','passed':True}
        except AssertionError as error:
            result = {'story':'submission next steps','passed':False,'error':str(error)}
        (OUT / f'{sys.argv[1]}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result))
        browser.close()
        assert result['passed'], result
