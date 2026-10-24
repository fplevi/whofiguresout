import json, pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parents[2]
out = root / ".scratch/billing/qa/fullwidth-columns"
url = (root / "case-studies/billing.html").as_uri()
report = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1920, 1440, 1024, 375):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto(url); pg.wait_for_load_state("networkidle")
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        pg.add_style_tag(content="*{transition:none!important;animation:none!important} .reveal,[data-reveal]{opacity:1!important;transform:none!important}")
        pg.wait_for_timeout(800)
        report[w] = pg.evaluate("""() => [...document.querySelectorAll('.billing-row')].map(r => {
          const sec = r.closest('section'); const s = sec.getBoundingClientRect(); const cs = getComputedStyle(sec);
          const c = r.querySelector('.billing-row__copy').getBoundingClientRect();
          const m = r.querySelector('.billing-shot').getBoundingClientRect();
          const f = r.querySelector('.billing-shot__frame').getBoundingClientRect();
          const rr = r.getBoundingClientRect();
          return {title: r.querySelector('h3').textContent.trim(), row:[Math.round(rr.left),Math.round(rr.right)],
            content:[Math.round(s.left+parseFloat(cs.paddingLeft)),Math.round(s.right-parseFloat(cs.paddingRight))],
            copy:[Math.round(c.left),Math.round(c.width)], media:[Math.round(m.left),Math.round(m.width)], frame:Math.round(f.width)};
        })""")
        for i, h in enumerate(pg.query_selector_all('.billing-row'), 1):
            h.scroll_into_view_if_needed(); h.screenshot(path=str(out / f"{w}-row-{i}.png"))
        pg.close()
    b.close()
(out / "layout.json").write_text(json.dumps(report, indent=1))
for w, rows in report.items():
    print(w)
    for r in rows: print("  ", r)
