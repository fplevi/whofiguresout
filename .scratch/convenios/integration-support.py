"""Combined-case behavior, accessibility and supporting asset checks.

Usage: python integration-support.py ROOT URL OUTPUT_DIR AXE_JS
The full responsive matrix reuses 03-library-qa.py separately.
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
root, base, out, axe = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "axe": []}


def check(name, ok, detail=None):
    results["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name, flush=True)


with sync_playwright() as p:
    browser = p.chromium.launch()
    results["browser"] = browser.version
    for width in (320, 375, 768, 1440):
        context = browser.new_context(viewport={"width": width, "height": 700}, reduced_motion="reduce")
        page = context.new_page()
        page.goto(base + "/case-studies/convenios.html", wait_until="networkidle")
        articles = page.get_by_role("article")
        names = articles.get_by_role("heading").all_text_contents()
        check(f"{width}: card, network, accounts, library sequence", names == [
            "Keep the essentials close.", "Find care in the provider network.",
            "Make room for more than one account.", "Build a foundation for the next release."], names)
        network = page.get_by_role("article", name="Find care in the provider network.")
        accounts = page.get_by_role("article", name="Make room for more than one account.")
        library = page.get_by_role("article", name="Build a foundation for the next release.")
        ntext = network.inner_text().lower()
        atext = accounts.inner_text().lower()
        check(f"{width}: available network explains map/list", all(s in ntext for s in ("available", "map", "list")))
        check(f"{width}: account switch explicitly without logout", "without logging out" in atext and "stay signed in" in atext)
        check(f"{width}: account explanation excludes unrelated services", not re.search(r"notification|authorization|statement|contract|family", atext))
        check(f"{width}: evidence stays visible without disclosure or raw links", articles.locator("a,button,details,dialog,[hidden]").count() == 0)
        story = articles.inner_text() if articles.count() == 1 else " ".join(articles.all_text_contents())
        story += page.get_by_role("region", name="A dedicated app. Its own foundation.").inner_text()
        check(f"{width}: no unsupported launch/geolocation/efficiency/certification claim", not re.search(
            r"biometric|geolocation|nearest|distance|reduced rework|certif|migrat|built on Harmony|initial launch|pending", story, re.I))
        check(f"{width}: own product library predates Harmony", "predates Harmony" in library.inner_text())
        # Readiness and screenshot positioning occur after the independent ordinary-wheel matrix.
        for article in articles.all():
            article.evaluate("e=>scrollTo({top:scrollY+e.getBoundingClientRect().top-80,behavior:'instant'})")
            article.get_by_role("img").evaluate("i=>i.decode()")
            page.screenshot(path=str(out / f"reader-{article.get_attribute('aria-labelledby')}-{width}.png"))
        page.add_script_tag(path=str(axe))
        audit = page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return {violations:r.violations,incomplete:r.incomplete.map(i=>({id:i.id,impact:i.impact,description:i.description,nodes:i.nodes.map(n=>n.target)})),passes:r.passes.length}}")
        results["axe"].append({"width": width, **audit})
        check(f"{width}: automated WCAG audit has no violations", not audit["violations"], [v["id"] for v in audit["violations"]])
        context.close()
    browser.close()

# Supporting artifact checks supplement browser behavior; no new runtime seam.
def original(path):
    return subprocess.check_output(["git", "show", "f8f9034:" + path], cwd=root)


changed = subprocess.check_output(["git", "diff", "--name-only", "f8f9034...HEAD"], cwd=root, text=True).splitlines()
allowed = {"case-studies/convenios.html", "assets/css/convenios.css",
           "assets/images/convenios/convenios-provider-network-crop.webp",
           "assets/images/convenios/convenios-button-touch-03.webp"}
check("production change scope stays within Convenios", all(p in allowed or p.startswith(".scratch/convenios/") for p in changed), changed)
case = "case-studies/convenios.html"
before, after = original(case).decode("utf-8"), (root / case).read_text(encoding="utf-8")
check("metadata, analytics, hero and problem/role prefix preserved", before.split('<section class="cs-section" aria-labelledby="convenios-decisions">')[0] == after.split('<section class="cs-section" aria-labelledby="convenios-decisions">')[0])
check("stores, adjacent navigation, contact and scripts preserved", before.split('<div class="cs-app__stores"')[1] == after.split('<div class="cs-app__stores"')[1])
check("home card and home document unchanged", original("index.html").decode("utf-8").replace("\r\n", "\n") == (root / "index.html").read_text(encoding="utf-8"))
original_paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "f8f9034", "assets/images/convenios"], cwd=root, text=True).splitlines()
check("all original Convenios images unchanged", all(original(p) == (root / p).read_bytes() for p in original_paths))
for source, output, bounds in [
    ("convenios-provider-network.png", "convenios-provider-network-crop.webp", (330, 48, 760, 734)),
    ("convenios-components.png", "convenios-button-touch-03.webp", (35, 560, 208, 823)),
]:
    src = Image.open(root / "assets/images/convenios" / source).convert("RGBA")
    dest = Image.open(root / "assets/images/convenios" / output).convert("RGBA")
    check(output + ": exact source crop, dimensions and alpha preserved", dest.size == (bounds[2]-bounds[0], bounds[3]-bounds[1]) and dest.tobytes() == src.crop(bounds).tobytes())
    if "network" in output:
        check("network derivative retains transparency", dest.getextrema()[3][0] == 0)

results["summary"] = {"passed": sum(c["ok"] for c in results["checks"]), "failed": sum(not c["ok"] for c in results["checks"])}
(out / "support-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(results["summary"])
sys.exit(bool(results["summary"]["failed"]))
