"""Supporting source/asset inventory for ticket 02, separate from browser QA.

Run after merging integration: python .scratch/convenios/02-preservation.py
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image

BASE = "integration/convenios-visual-narrative"


def original(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"])


def text(raw):
    return raw.decode("utf-8").replace("\r\n", "\n")


def without_accounts(html):
    return re.sub(r'<article[^>]*aria-labelledby="convenios-accounts"[\s\S]*?</article>', "", html)


def without_accounts_style(css):
    return re.sub(r'/\* Trim only transparent[\s\S]+?object-position: 45% 50%;\n}\n\n', "", css)


checks = {}
html = "case-studies/convenios.html"
css = "assets/css/convenios.css"
checks["HTML outside the accounts row unchanged"] = without_accounts(text(original(html))) == without_accounts(text(Path(html).read_bytes()))
checks["CSS outside accounts-only presentation unchanged"] = without_accounts_style(text(original(css))) == without_accounts_style(text(Path(css).read_bytes()))
for path in ["index.html", "assets/css/case-study.css", "assets/js/scroll-animations.js",
             "assets/css/contact.css", "assets/js/contact-form.js", "assets/css/nav.css"]:
    checks[f"{path} unchanged"] = text(original(path)) == text(Path(path).read_bytes())
hashes = {}
for path in Path("assets/images/convenios").iterdir():
    if path.is_file():
        key = path.as_posix()
        checks[f"{key} unchanged"] = original(key) == path.read_bytes()
        hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
png = Image.open("assets/images/convenios/convenios-accounts.png").convert("RGBA")
webp = Image.open("assets/images/convenios/convenios-accounts.webp").convert("RGBA")
checks["accounts PNG/WebP equivalent decoded pixels"] = png.size == webp.size and png.tobytes() == webp.tobytes()
checks["CSS visible source bounds retain all nontransparent pixels"] = (186 >= 156.96 and 711 <= 832.16
    and webp.getchannel("A").getbbox() == (186, 102, 711, 759))
report = {"integration_tip": subprocess.check_output(["git", "rev-parse", BASE], text=True).strip(),
          "checks": checks, "image_sha256": hashes,
          "summary": {"passed": sum(checks.values()), "failed": sum(not v for v in checks.values())}}
Path(".scratch/convenios/02-preservation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["summary"])
raise SystemExit(0 if all(checks.values()) else 1)
