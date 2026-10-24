"""Supplement tall element captures with loaded reading viewports.

Adapted from the existing Harmony captures workflow. Fixed navigation stays in
its real position; reading text is positioned below it, captions near the bottom.
"""
import functools
import http.server
import json
from pathlib import Path
import subprocess
import threading
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
BASE = '3a466dbb17c20b7522a62128503281fdc0f48a7f'
OUT = ROOT / '.scratch/harmony/qa/code-review-css-reading'
OUT.mkdir(parents=True, exist_ok=True)
CSS = subprocess.check_output(['git', 'show', f'{BASE}:assets/css/harmony.css'], cwd=ROOT)
EVIDENCE = [('primitives', 'Primitive color scales'), ('semantics', 'Semantic roles by use'),
            ('responsive', 'Responsive variables'), ('buttons', 'Button variants, sizes, and states'),
            ('component-navigation', 'Navigation across contexts'), ('templates', 'Composing page templates'),
            ('storybook', 'Button properties in Storybook')]


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.server.before and urlsplit(self.path).path == '/assets/css/harmony.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', str(len(CSS)))
            self.end_headers()
            self.wfile.write(CSS)
        else:
            super().do_GET()


servers = []
records = []
try:
    for before in [True, False]:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
        server.before = before
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in [320, 375, 768, 1440]:
            for label, server in zip(['before', 'after'], servers):
                context = browser.new_context(viewport={'width': width, 'height': 700}, reduced_motion='reduce')
                page = context.new_page()
                page.goto(f'http://127.0.0.1:{server.server_port}/case-studies/harmony.html', wait_until='load')
                page.evaluate('document.fonts.ready')
                for key, title in EVIDENCE:
                    region = page.get_by_role('region', name=title, exact=True)
                    image = region.get_by_role('img')
                    image.scroll_into_view_if_needed()
                    image.evaluate('i=>i.decode()')
                    assert image.evaluate('i=>i.complete&&i.naturalWidth>0')
                    for part in ['explanation', 'caption']:
                        if part == 'explanation':
                            region.evaluate("r=>scrollTo({top:r.getBoundingClientRect().top+scrollY-88,behavior:'instant'})")
                        else:
                            region.locator('figcaption').evaluate("c=>scrollTo({top:c.getBoundingClientRect().bottom+scrollY-innerHeight+24,behavior:'instant'})")
                        page.wait_for_timeout(100)
                        filename = f'{label}-{key}-{width}-{part}.png'
                        page.screenshot(path=str(OUT / filename))
                        records.append({'label': label, 'width': width, 'row': key, 'part': part, 'capture': filename})
                context.close()
        browser.close()
    result = {'baseline': BASE, 'mode': 'reduce', 'height': 700, 'loadedRows': 56, 'captures': records}
    (OUT / 'captures.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Captured {len(records)} loaded reading viewports across 56 before/after rows.')
finally:
    for server in servers:
        server.shutdown()
