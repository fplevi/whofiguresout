"""PROTOTYPE QA: screenshot each variant before/after a hover sweep at 1440 and 375."""
import sys
from playwright.sync_api import sync_playwright
OUT = '.scratch/billing-hero'
URL = 'http://127.0.0.1:8765/case-studies/prototype-billing-hero.html?variant='
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 1000), (375, 900)]:
        for v in 'D':
            pg = b.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(URL + v); pg.wait_for_timeout(600)
            pg.screenshot(path=f'{OUT}/{v}-{w}-start.png')
            box = pg.locator('.wsh__grid').bounding_box()
            pg.locator('.wsh__grid').scroll_into_view_if_needed()
            box = pg.locator('.wsh__grid').bounding_box()
            # sweep the top 60% of the grid row by row
            rows = 12
            for i in range(int(rows * 0.6)):
                y = box['y'] + box['height'] * (i + 0.5) / rows
                pg.mouse.move(box['x'] + 2, y)
                pg.mouse.move(box['x'] + box['width'] - 2, y, steps=25)
            pg.wait_for_timeout(500)
            pg.screenshot(path=f'{OUT}/{v}-{w}-swept.png', full_page=False)
            print(v, w, pg.locator('.wsh__count').inner_text(), errs)
            pg.close()
    b.close()
