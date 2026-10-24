import pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parents[2]
out = root / ".scratch/enrollment/qa/compare-grip"
url = "http://127.0.0.1:8765/case-studies/enrollment.html"
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 375):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
        pg.goto(url); pg.wait_for_load_state("networkidle")
        c = pg.query_selector(".cs-compare")
        c.scroll_into_view_if_needed()
        pg.evaluate("document.querySelectorAll('.cs-compare img').forEach(i=>i.loading='eager')")
        pg.wait_for_timeout(800)
        box = c.bounding_box()
        def grip(name):
            g = pg.query_selector(".cs-compare__grip").bounding_box()
            pg.screenshot(path=str(out / f"{w}-{name}.png"), clip={"x": g["x"]-60, "y": g["y"]-50, "width": g["width"]+120, "height": g["height"]+100})
        pg.mouse.move(0, 0); grip("rest")
        c.screenshot(path=str(out / f"{w}-frame.png"))
        pg.mouse.move(box["x"]+box["width"]/2, box["y"]+box["height"]/2); grip("hover")
        pg.mouse.move(0, 0)
        pg.focus(".cs-compare__slider"); pg.keyboard.press("ArrowLeft"); grip("focus")
        for k in range(28): pg.keyboard.press("ArrowLeft")
        grip("at-20"); c.screenshot(path=str(out / f"{w}-frame-at-20.png"))
        g = pg.query_selector(".cs-compare__grip").bounding_box()
        print(w, "grip", g, "glyph text:", pg.evaluate("getComputedStyle(document.querySelector('.cs-compare__handle'),'::after').content"))
        pg.close()
    b.close()
