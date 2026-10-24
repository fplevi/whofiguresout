"""Shoot the fully revealed grid (reduced motion) for several data-seed values."""
import sys, re
from playwright.sync_api import sync_playwright
case, out, seeds = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]
URL = f'http://127.0.0.1:8765/case-studies/{case}.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 1000), (375, 900)]:
        ctx = b.new_context(reduced_motion='reduce', viewport={'width': w, 'height': h})
        for seed in seeds:
            pg = ctx.new_page()
            # Override data-seed as soon as the header is parsed, before the module runs
            pg.add_init_script(f"""new MutationObserver((_, o) => {{
              const s = document.querySelector('.wsh'); if (s) {{ s.dataset.seed = '{seed}'; o.disconnect(); }}
            }}).observe(document, {{ childList: true, subtree: true }});""")
            pg.goto(URL); pg.wait_for_timeout(300)
            pg.locator('.wsh__grid').screenshot(path=f'{out}/{case}-seed{seed}-{w}.png'); pg.close()
        ctx.close()
    b.close()
