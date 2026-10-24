import pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parents[2]
out = root / ".scratch/enrollment/qa"
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 375):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto("http://127.0.0.1:8765/case-studies/enrollment.html"); pg.wait_for_load_state("networkidle")
        el = pg.query_selector(".enrollment-live"); el.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
        pg.evaluate("document.querySelector('.nav') && (document.querySelector('.nav').style.visibility='hidden')")
        pg.query_selector("section[aria-labelledby=enrollment-outcome]").screenshot(path=str(out / f"live-link-{w}.png"))
        pg.focus(".enrollment-live a"); el.screenshot(path=str(out / f"live-link-{w}-focus.png"))
        print(w, pg.evaluate("[...document.querySelectorAll('.enrollment-live p')].map(p=>Math.round(p.getBoundingClientRect().width))"))
        pg.close()
    b.close()
