"""QA for the word-search hero on the real Billing page."""
from playwright.sync_api import sync_playwright
OUT = '.scratch/billing-hero'
URL = 'http://127.0.0.1:8765/case-studies/billing.html'

def sweep(pg, frac=0.6, rows=12):
    g = pg.locator('.wsh__grid'); g.scroll_into_view_if_needed(); box = g.bounding_box()
    for i in range(int(rows * frac)):
        y = box['y'] + box['height'] * (i + 0.5) / rows
        pg.mouse.move(box['x'] + 2, y); pg.mouse.move(box['x'] + box['width'] - 2, y, steps=25)

with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 1000), (375, 900)]:
        pg = b.new_page(viewport={'width': w, 'height': h}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{OUT}/real-{w}-start.png')
        sweep(pg); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/real-{w}-swept.png')
        print(w, 'after sweep:', pg.locator('.wsh__count').inner_text(),
              'overflowX:', pg.evaluate('document.documentElement.scrollWidth > innerWidth'), errs)
        pg.click('.wsh__reveal'); pg.wait_for_timeout(3000)
        print(w, 'after reveal all:', pg.locator('.wsh__count').inner_text(),
              'reveal hidden:', pg.locator('.wsh__reveal').is_hidden())
        pg.keyboard.press('Tab')  # focus walk to a chip
        pg.locator('.wsh__chip').nth(2).focus(); pg.wait_for_timeout(400)
        print(w, 'balloon on chip focus:', pg.locator('.wsh__balloon.is-visible').inner_text().replace('\n', ' | '))
        pg.screenshot(path=f'{OUT}/real-{w}-chipfocus.png')
        pg.close()
    # breakpoint change keeps found words
    pg = b.new_page(viewport={'width': 1440, 'height': 1000}); pg.goto(URL); pg.wait_for_timeout(300)
    sweep(pg, 0.4); before = pg.locator('.wsh__count').inner_text()
    pg.set_viewport_size({'width': 375, 'height': 900}); pg.wait_for_timeout(400)
    print('resize:', before, '->', pg.locator('.wsh__count').inner_text(), 'cols', pg.evaluate("getComputedStyle(document.querySelector('.wsh__grid')).getPropertyValue('--cols')"))
    pg.close()
    # reduced motion
    ctx = b.new_context(reduced_motion='reduce', viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    pg.goto(URL); pg.wait_for_timeout(300); print('reduced motion:', pg.locator('.wsh__count').inner_text()); ctx.close()
    # no JS
    ctx = b.new_context(java_script_enabled=False, viewport={'width': 1440, 'height': 1000}); pg = ctx.new_page()
    pg.goto(URL); pg.screenshot(path=f'{OUT}/real-1440-nojs.png')
    print('no-js chips:', pg.locator('.wsh__chip').all_inner_texts(), 'grid visible:', pg.locator('.wsh__grid').is_visible()); ctx.close()
    b.close()
