"""Ticket 03 browser QA, adapted from Billing visual-narrative-qa.py.

Run: python .scratch/convenios/03-library-qa.py <red|green|final>
The approved seam is the rendered page and externally visible browser behavior.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PHASE = sys.argv[1]
BASE = "http://127.0.0.1:8113"
ROOT = Path(__file__).resolve().parent
EVID = ROOT / f"03-evidence-{PHASE}"
EVID.mkdir(exist_ok=True)
R = {"phase": PHASE, "url": BASE, "executed_at": datetime.now(timezone.utc).isoformat(),
     "checks": [], "console": [], "failed_requests": [], "page_errors": []}


def check(name, ok, detail=None):
    R["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch()
    R["browser"] = b.version
    ctx = b.new_context(viewport={"width": 320, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(BASE + "/case-studies/convenios.html", wait_until="networkidle")
    library = pg.get_by_role("article", name="Build a foundation for the next release.")
    library.scroll_into_view_if_needed()
    img = library.get_by_role("img")
    img.evaluate("i=>i.decode()")
    dimensions = img.evaluate("""i=>{const r=i.getBoundingClientRect();return {
        naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,width:r.width,height:r.height,
        drawnWidth:Math.min(r.width,r.height*i.naturalWidth/i.naturalHeight)}}""")
    # A focused source must survive the smallest viewport at near-native scale;
    # visual inspection of the capture remains necessary for states/touch areas.
    check("320: button documentation retains readable source scale in page",
          dimensions["drawnWidth"] / dimensions["naturalWidth"] >= 0.85, dimensions)
    library.screenshot(path=str(EVID / "03-library-320.png"))
    if PHASE not in ("red", "green"):
        copy = library.inner_text()
        outcome = pg.get_by_role("region", name="A new app. A shared foundation.") if PHASE == "red-copy" else pg.get_by_role("region", name="A dedicated app. Its own foundation.")
        check("library story is complete in page and distinguishes its own foundation",
              library.get_by_role("link").count() == 0
              and "predates Harmony" in copy and "own component library and visual language" in copy
              and "states and touch areas" in copy
              and "reduced rework" not in outcome.inner_text(),
              {"library": copy, "outcome": outcome.inner_text(), "links": library.get_by_role("link").count()})
    ctx.close()
    if PHASE.startswith("final") or PHASE == "red-motion":
        for width in (320, 375, 768, 1440):
            for motion in ("no-preference", "reduce"):
                label = f"{width}-{motion}"
                ctx = b.new_context(viewport={"width": width, "height": 900}, reduced_motion=motion)
                pg = ctx.new_page()
                pg.on("console", lambda m, label=label: m.type in ("error", "warning") and R["console"].append(f"{label}: {m.type}: {m.text}"))
                pg.on("pageerror", lambda e, label=label: R["page_errors"].append(f"{label}: {e}"))
                pg.on("requestfailed", lambda r, label=label: R["failed_requests"].append(f"{label}: {r.url}: {r.failure}"))
                pg.on("response", lambda r, label=label: r.status >= 400 and R["failed_requests"].append(f"{label}: {r.status}: {r.url}"))
                pg.goto(BASE + "/case-studies/convenios.html", wait_until="networkidle")
                sections = pg.locator("main section[aria-labelledby]")
                if motion == "reduce":
                    available = sections.evaluate_all("es=>es.every(e=>getComputedStyle(e).opacity==='1'&&getComputedStyle(e).visibility==='visible')")
                    check(f"{label}: sections immediately available", available)
                # Ordinary wheel traversal from the top, with no element jumps.
                visited = set()
                wheel_samples = []
                for step in range(100):
                    sample = sections.evaluate_all("""es=>es.map(e=>{const r=e.getBoundingClientRect();return {
                        name:e.getAttribute('aria-labelledby'),height:r.height,top:r.top,bottom:r.bottom,
                        opacity:getComputedStyle(e).opacity,visibility:getComputedStyle(e).visibility}})""")
                    for s in sample:
                        if s["top"] < 900 and s["bottom"] > 64 and s["opacity"] == "1" and s["visibility"] == "visible":
                            visited.add(s["name"])
                    wheel_samples.append({"y": pg.evaluate("scrollY"), "sections": sample})
                    at_bottom = pg.evaluate("scrollY+innerHeight>=document.documentElement.scrollHeight-2")
                    if at_bottom and step < 99:
                        # Include the settled final viewport, not a mid-fade contact snapshot.
                        pg.wait_for_timeout(600)
                        settled = sections.evaluate_all("""es=>es.filter(e=>{const r=e.getBoundingClientRect();return r.top<900&&r.bottom>64&&getComputedStyle(e).opacity==='1'}).map(e=>e.getAttribute('aria-labelledby'))""")
                        visited.update(settled)
                        break
                    pg.mouse.wheel(0, 250)
                    pg.wait_for_timeout(200)
                pg.wait_for_timeout(600)
                after = sections.evaluate_all("es=>es.map(e=>({name:e.getAttribute('aria-labelledby'),opacity:getComputedStyle(e).opacity}))")
                check(f"{label}: every section visible during ordinary wheel traversal",
                      all(s["name"] in visited for s in after), {"visited": sorted(visited), "final": after})
                (EVID / f"03-wheel-{label}.json").write_text(json.dumps(wheel_samples, indent=2), encoding="utf-8")
                pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)", timeout=30000)
                images = pg.locator("main img").evaluate_all("""es=>es.map(i=>{const r=i.getBoundingClientRect();return {
                    source:i.getAttribute('src'),nw:i.naturalWidth,nh:i.naturalHeight,width:r.width,height:r.height,
                    alt:i.alt,fit:getComputedStyle(i).objectFit,loading:i.loading,decoding:i.decoding,declaredWidth:i.getAttribute('width'),declaredHeight:i.getAttribute('height')}})""")
                check(f"{label}: all images loaded with meaningful alternatives and intrinsic dimensions",
                      all(i["nw"] > 0 and len(i["alt"]) > 20 and int(i["declaredWidth"]) == i["nw"] and int(i["declaredHeight"]) == i["nh"] for i in images), images)
                check(f"{label}: all rendered images proportional",
                      all(i["fit"] == "contain" or abs(i["width"] / i["height"] - i["nw"] / i["nh"]) < 0.02 for i in images),
                      "Includes contained images: their letterboxed element can differ from the undistorted painted image.")
                check(f"{label}: body evidence lazy and asynchronous", all(i["loading"] == "lazy" and i["decoding"] == "async" for i in images[1:]))
                check(f"{label}: no horizontal overflow", pg.evaluate("document.documentElement.scrollWidth<=innerWidth"))
                rows = pg.get_by_role("article").evaluate_all("""es=>es.map(e=>{const i=e.querySelector('img'),c=e.querySelector('h3').parentElement,
                    r=i.getBoundingClientRect(),t=c.getBoundingClientRect();return {
                    title:e.querySelector('h3').textContent,images:e.querySelectorAll('img').length,
                    copyFirst:!!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),
                    above:t.bottom<=r.top+1,overlap:!(t.bottom<=r.top+1||r.bottom<=t.top+1||t.right<=r.left+1||r.right<=t.left+1)}})""")
                check(f"{label}: one image per row, copy first, no overlap", all(r["images"] == 1 and r["copyFirst"] and not r["overlap"] for r in rows), rows)
                if width <= 768:
                    check(f"{label}: every explanation above its image", all(r["above"] for r in rows))
                check(f"{label}: library remains last evidence", rows[-1]["title"] == "Build a foundation for the next release.")
                library = pg.get_by_role("article", name="Build a foundation for the next release.")
                geometry = library.evaluate("""e=>{const i=e.querySelector('img'),r=i.getBoundingClientRect(),c=e.querySelector('h3').parentElement.getBoundingClientRect();
                    return {above:c.bottom<=r.top,scale:r.width/i.naturalWidth,width:r.width,bodyWidth:e.getBoundingClientRect().width}}""")
                check(f"{label}: library is wide, legible and below its explanation", geometry["above"] and geometry["scale"] >= 0.85, geometry)
                check(f"{label}: no raw-image link or disclosure hides library", library.locator("a,details,dialog,button").count() == 0)
                copy_style = library.locator("p").evaluate("e=>({font:getComputedStyle(e).fontSize,color:getComputedStyle(e).color,background:getComputedStyle(document.body).backgroundColor})")
                check(f"{label}: explanation retains 16px readable type", float(copy_style["font"].replace("px", "")) >= 16, copy_style)
                # A tall element screenshot can include the fixed nav over its heading.
                # Capture a real viewport with the explanation below the nav, then the loaded crop.
                library.evaluate("e=>e.scrollIntoView({block:'start'})")
                pg.evaluate("scrollBy(0,-80)")
                pg.wait_for_timeout(100)
                pg.screenshot(path=str(EVID / f"03-library-{label}.png"))
                library.get_by_role("img").screenshot(path=str(EVID / f"03-loaded-crop-{label}.png"))
                pg.get_by_role("region", name="A dedicated app. Its own foundation.").screenshot(path=str(EVID / f"03-outcome-{label}.png"))
                if width in (375, 1440):
                    pg.locator("main img").first.screenshot(path=str(EVID / f"03-preserved-hero-{label}.png"))
                    for row in pg.get_by_role("article").all():
                        name = row.get_attribute("aria-labelledby")
                        row.evaluate("e=>e.scrollIntoView({block:'start'})")
                        pg.evaluate("scrollBy(0,-80)")
                        pg.wait_for_timeout(100)
                        pg.screenshot(path=str(EVID / f"03-evidence-{name}-{label}.png"))
                ctx.close()

        # Preserved portfolio visit: keyboard and local navigation, no store/service or form submission.
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(BASE + "/", wait_until="networkidle")
        card = pg.get_by_role("link", name="CASSI Convênios case study: Product Leadership")
        check("home: existing card remains", "Launched" in card.inner_text() and "on iOS and Android" in card.inner_text())
        # Reach links with real Tab input so :focus-visible is exercised.
        def tab_to(locator):
            for _ in range(80):
                pg.keyboard.press("Tab")
                if locator.evaluate("e=>e===document.activeElement"):
                    return locator.evaluate("e=>{const s=getComputedStyle(e);return e.matches(':focus-visible')&&s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>=2}")
            return False

        check("home: case card reachable with visible keyboard focus", tab_to(card))
        pg.screenshot(path=str(EVID / "03-home-keyboard.png"))
        pg.keyboard.press("Enter")
        pg.wait_for_url("**/case-studies/convenios.html")
        check("home: keyboard opens case", pg.get_by_role("heading", name="CASSI Convênios", exact=True).is_visible())
        nav = pg.get_by_role("navigation", name="Main navigation").get_by_role("link").evaluate_all("es=>es.map(e=>e.getAttribute('href'))")
        check("case: navigation destinations preserved", nav == ["../", "../#work", "../#contact", "../#about"], nav)
        for name, href in (("Google Play ↗", "https://play.google.com/store/apps/details?id=br.com.cassi.app.reciprocidade&pcampaignid=web_share"),
                           ("App Store ↗", "https://apps.apple.com/br/app/cassi-conv%C3%AAnios/id6705117118")):
            link = pg.get_by_role("link", name=name, exact=True)
            check(f"case: {name} destination and visible keyboard focus", link.get_attribute("href") == href and tab_to(link))
        contact = pg.get_by_role("region", name="Let's work together.")
        check("case: contact retained without submission", contact.locator("form").get_attribute("action") == "https://formspree.io/f/mbdqyywl" and contact.get_by_role("textbox").count() == 3)
        check("case: email copy button reachable with visible keyboard focus", tab_to(contact.get_by_role("button", name="Copy email address")))
        check("case: contact field keyboard focus visible", tab_to(contact.get_by_role("textbox", name="Your name")))
        pg.screenshot(path=str(EVID / "03-contact-keyboard.png"))
        pg.get_by_role("link", name="← Back to work").click()
        pg.wait_for_url(BASE + "/#work")
        check("case: return to Work works", pg.get_by_role("link", name="CASSI Convênios case study: Product Leadership").is_visible())
        pg.goto(BASE + "/case-studies/enrollment.html", wait_until="networkidle")
        pg.get_by_role("link", name="CASSI Convênios →").click()
        pg.wait_for_url("**/case-studies/convenios.html")
        pg.get_by_role("link", name="Harmony →").click()
        pg.wait_for_url("**/case-studies/harmony.html")
        check("adjacent cases: Enrollment to Convênios to Harmony works", pg.get_by_role("heading", name="Harmony", exact=True).is_visible())
        ctx.close()
        check("browser: no page JavaScript errors", not R["page_errors"], R["page_errors"])
    b.close()

R["summary"] = {"passed": sum(c["ok"] for c in R["checks"]),
                "failed": sum(not c["ok"] for c in R["checks"])}
(ROOT / f"03-results-{PHASE}.json").write_text(json.dumps(R, indent=2), encoding="utf-8")
print(R["summary"])
sys.exit(bool(R["summary"]["failed"]))
