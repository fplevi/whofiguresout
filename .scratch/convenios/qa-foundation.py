import http.server, threading, functools, json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent/'qa'/'foundation'
h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root)); h.log_message=lambda *a:None
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),h); threading.Thread(target=srv.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{srv.server_port}/case-studies/convenios.html'
res={}
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in (375,1024,1440,1920):
    pg=b.new_page(viewport={'width':w,'height':900}); pg.goto(url); pg.wait_for_load_state('networkidle')
    pg.add_style_tag(content='*{animation:none!important;transition:none!important} .reveal,[data-animate]{opacity:1!important;transform:none!important}')
    el=pg.locator('.cs-app__feature--library'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(400)
    res[w]=el.evaluate("""e=>{const r=x=>{const b=x.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};
      const s=e.closest('.cs-app__features');return {row:r(e),features:r(s),copy:r(e.querySelector('.cs-app__feature-copy')),fig:r(e.querySelector('.cs-app__figure')),img:r(e.querySelector('img')),loaded:e.querySelector('img').naturalWidth}}""")
    el.screenshot(path=str(out/f'{w}-library.png'))
  b.close()
(out/'layout.json').write_text(json.dumps(res,indent=1)); print(json.dumps(res))
