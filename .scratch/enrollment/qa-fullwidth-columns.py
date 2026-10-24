import json, pathlib, sys
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parents[2]
out = root / ".scratch/enrollment/qa/fullwidth-columns"
url = (root / "case-studies/enrollment.html").as_uri()
report = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 1920, 1024, 375):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto(url); pg.wait_for_load_state("networkidle")
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        pg.wait_for_timeout(800)
        rows = pg.evaluate("""() => [...document.querySelectorAll('.enrollment-evidence-row')].map(r => {
          const sec = r.closest('section').getBoundingClientRect();
          const cs = getComputedStyle(r.closest('section'));
          const c = r.querySelector(':scope > figcaption, :scope > .enrollment-evidence-row__copy').getBoundingClientRect();
          const m = r.querySelector(':scope > img, :scope > .cs-compare').getBoundingClientRect();
          const rr = r.getBoundingClientRect();
          return {row:[Math.round(rr.left),Math.round(rr.right)], content:[Math.round(sec.left+parseFloat(cs.paddingLeft)),Math.round(sec.right-parseFloat(cs.paddingRight))],
                  copy:[Math.round(c.left),Math.round(c.width)], media:[Math.round(m.left),Math.round(m.width)]};
        })""")
        report[w] = rows
        for i, h in enumerate(pg.query_selector_all('.enrollment-evidence-row'), 1):
            h.scroll_into_view_if_needed(); h.screenshot(path=str(out / f"{w}-row-{i}.png"))
        pg.close()
    b.close()
(out / "layout.json").write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))
