"""Ticket 02 rendered-page QA; adapted from Billing's visual-narrative QA.

Run: python .scratch/convenios/02-accounts-qa.py <evidence_dir> <results_json> [--copy-only]
Server must belong to this checkout on port 8112. No production app interaction.
"""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8112"
URL = BASE + "/case-studies/convenios.html"
EVID, OUT = Path(sys.argv[1]), Path(sys.argv[2])
EVID.mkdir(parents=True, exist_ok=True)
R = {"url": URL, "checks": [], "console": [], "failed_requests": []}


def check(name, ok, detail=None):
    R["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name, detail if detail is not None else "")


def accounts(pg):
    return pg.get_by_role("article").filter(
        has=pg.get_by_role("heading", name="Make room for more than one account."))


def wheel_through(pg):
    """Use real wheel input from the top; never jump to trigger visibility."""
    seen = set()
    samples = []
    pg.mouse.move(100, 350)
    for _ in range(120):
        state = pg.evaluate("""() => ({y:scrollY, h:document.documentElement.scrollHeight,
          sections:[...document.querySelectorAll('main section')].map(s=>({
            name:s.getAttribute('aria-labelledby'), opacity:getComputedStyle(s).opacity,
            top:s.getBoundingClientRect().top,bottom:s.getBoundingClientRect().bottom}))})""")
        for s in state["sections"]:
            if s["top"] < 700 and s["bottom"] > 64 and float(s["opacity"]) > .99:
                seen.add(s["name"])
        samples.append(state)
        if state["y"] + 700 >= state["h"] - 2:
            break
        pg.mouse.wheel(0, 350)
        # Allow the existing 500ms entrances to settle at each ordinary reading stop.
        pg.wait_for_timeout(650)
    pg.wait_for_timeout(650)
    return seen, samples


def matrix(b):
    for motion in ["no-preference", "reduce"]:
        for w in [320, 375, 768, 1440]:
            label = f"{w}-{motion}"
            ctx = b.new_context(viewport={"width": w, "height": 700}, reduced_motion=motion)
            pg = ctx.new_page()
            pg.on("pageerror", lambda e, label=label: R["console"].append(f"{label}: {e}"))
            pg.on("requestfailed", lambda r, label=label: R["failed_requests"].append(
                {"run": label, "url": r.url, "failure": r.failure}))
            pg.on("response", lambda r, label=label: r.status >= 400 and R["failed_requests"].append(
                {"run": label, "url": r.url, "status": r.status}))
            pg.goto(URL, wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            if motion == "reduce":
                immediate = pg.locator("main section").evaluate_all(
                    "ss=>ss.every(s=>getComputedStyle(s).opacity==='1' && getComputedStyle(s).transform==='none')")
                check(f"{label}: content immediately available", immediate)
            seen, samples = wheel_through(pg)
            expected = pg.locator("main section").evaluate_all("ss=>ss.map(s=>s.getAttribute('aria-labelledby'))")
            check(f"{label}: every section visible during ordinary wheel traversal",
                  set(expected) <= seen, {"seen": sorted(seen), "expected": expected})
            R.setdefault("wheel", {})[label] = samples
            pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
            imgs = pg.locator("main img").evaluate_all("""imgs=>imgs.map(i=>({
                src:i.getAttribute('src'),nw:i.naturalWidth,nh:i.naturalHeight,
                w:i.getBoundingClientRect().width,h:i.getBoundingClientRect().height,
                fit:getComputedStyle(i).objectFit,alt:i.alt,loading:i.loading,decoding:i.decoding}))""")
            check(f"{label}: every image loaded with meaningful alternative", all(i["nw"] and i["alt"] for i in imgs), imgs)
            check(f"{label}: images preserve proportions", all(
                i["fit"] in ("contain", "cover") or abs(i["w"] / i["h"] - i["nw"] / i["nh"]) < .02 for i in imgs))
            check(f"{label}: no horizontal overflow", pg.evaluate("document.documentElement.scrollWidth<=innerWidth"))
            row = accounts(pg)
            g = row.evaluate("""r=>{let p=r.querySelector('p'),i=r.querySelector('img');
              let a=p.getBoundingClientRect(),b=i.getBoundingClientRect(),s=getComputedStyle(p);
              return {copyFirst:!!(p.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),
                above:a.bottom<=b.top+1,overlap:!(a.bottom<=b.top+1||b.bottom<=a.top+1||a.right<=b.left+1||b.right<=a.left+1),
                font:parseFloat(s.fontSize),fg:s.color,bg:getComputedStyle(document.body).backgroundColor,
                imageCount:r.querySelectorAll('img').length,interactionCount:r.querySelectorAll('a,button,details').length}}""")
            check(f"{label}: accounts copy before one image, no overlap or disclosure",
                  g["copyFirst"] and not g["overlap"] and g["imageCount"] == 1 and g["interactionCount"] == 0
                  and (w > 768 or g["above"]), g)
            check(f"{label}: account body type remains at least 16px", g["font"] >= 16)
            # Composite rendered alpha text over the actual body background, then WCAG luminance.
            fg = [float(v) for v in re.findall(r"[\d.]+", g["fg"])]
            bg = [float(v) for v in re.findall(r"[\d.]+", g["bg"])][:3]
            alpha = fg[3] if len(fg) == 4 else 1
            color = [fg[i] * alpha + bg[i] * (1-alpha) for i in range(3)]
            def luminance(rgb):
                linear = [v / 255 / 12.92 if v / 255 <= .04045 else ((v / 255 + .055) / 1.055) ** 2.4 for v in rgb]
                return sum(v*k for v,k in zip(linear, [.2126,.7152,.0722]))
            contrast = (luminance(color)+.05)/(luminance(bg)+.05)
            check(f"{label}: account explanation contrast >= 4.5:1", contrast >= 4.5, round(contrast, 2))
            check(f"{label}: accounts image stays lazy/asynchronous",
                  row.locator("img").get_attribute("loading") == "lazy" and row.locator("img").get_attribute("decoding") == "async")
            # Captures occur only after real traversal and successful image readiness.
            row.screenshot(path=str(EVID / f"02-accounts-{label}.png"))
            row.locator("img").screenshot(path=str(EVID / f"02-loaded-image-{label}.png"))
            row.scroll_into_view_if_needed()
            pg.screenshot(path=str(EVID / f"02-viewport-{label}.png"))
            pg.screenshot(path=str(EVID / f"02-page-{label}.png"), full_page=True)
            ctx.close()


def navigation(b):
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(BASE, wait_until="networkidle")
    card = pg.get_by_role("link", name="CASSI Convênios case study: Product Leadership")
    check("home card preserves launch message", "Launched" in card.inner_text() and "on iOS and Android" in card.inner_text())
    card.click()
    check("home card opens case", pg.url == URL)
    check("hero retains home image", pg.locator("main img").first.get_attribute("src").endswith("convenios-home.webp"))
    check("nav destinations preserved", pg.locator("nav a").evaluate_all("aa=>aa.map(a=>a.getAttribute('href'))") == ["../", "../#work", "../#contact", "../#about"])
    check("store destinations preserved", pg.get_by_role("group", name="Get CASSI Convênios").locator("a").evaluate_all("aa=>aa.map(a=>a.getAttribute('href'))") == [
        "https://play.google.com/store/apps/details?id=br.com.cassi.app.reciprocidade&pcampaignid=web_share",
        "https://apps.apple.com/br/app/cassi-conv%C3%AAnios/id6705117118"])
    for text in ["Back to work", "Google Play", "App Store", "Harmony", "fplevi@gmail.com", "Copy email address"]:
        loc = pg.get_by_role("button" if text == "Copy email address" else "link", name=re.compile(re.escape(text))).first
        loc.focus()
        # Advance a real keyboard event from the preceding element to test keyboard focus styling.
        pg.keyboard.press("Shift+Tab")
        pg.keyboard.press("Tab")
        focus = loc.evaluate("""e=>{let s=getComputedStyle(e);return {active:document.activeElement===e,
            visible:e.matches(':focus-visible'),outline:s.outlineStyle,width:s.outlineWidth,shadow:s.boxShadow}}""")
        check(f"keyboard: {text} reachable with visible focus", focus["active"] and focus["visible"] and
              (focus["outline"] != "none" and focus["width"] != "0px" or focus["shadow"] != "none"), focus)
        if text in ["Google Play", "Back to work"]:
            pg.screenshot(path=str(EVID / f"02-focus-{'store' if text == 'Google Play' else 'back'}.png"))
    check("contact present without submission", pg.locator("#contact-form").get_attribute("action") == "https://formspree.io/f/mbdqyywl" and pg.locator("#contact-form input,#contact-form textarea").count() == 3)
    pg.get_by_role("link", name="Harmony →", exact=True).click()
    check("next case opens Harmony", pg.url.endswith("/case-studies/harmony.html"))
    pg.goto(BASE + "/case-studies/enrollment.html", wait_until="networkidle")
    pg.get_by_role("link", name="CASSI Convênios →", exact=True).click()
    check("preceding case opens Convenios", pg.url == URL)
    pg.get_by_role("link", name="← Back to work", exact=True).click()
    check("return to Work", pg.url == BASE + "/#work" and pg.locator("#work").is_visible())
    ctx.close()


def recapture(b):
    """Supplemental visual review; wheel evidence remains in the matrix result.

    Element/full-page captures hide the fixed nav to avoid a stitched-image
    overlay artifact. Viewport captures retain the real nav and an 80px offset.
    """
    for motion in ["no-preference", "reduce"]:
        for w in [320, 375, 768, 1440]:
            label = f"{w}-{motion}"
            ctx = b.new_context(viewport={"width": w, "height": 700}, reduced_motion=motion)
            pg = ctx.new_page()
            pg.goto(URL, wait_until="networkidle")
            wheel_through(pg)
            pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
            check(f"{label}: recapture uses loaded images", True)
            row = accounts(pg)
            row.screenshot(path=str(EVID / f"02-accounts-{label}.png"), style=".nav {visibility:hidden !important}")
            row.locator("img").screenshot(path=str(EVID / f"02-loaded-image-{label}.png"))
            row.evaluate("e=>e.scrollIntoView({block:'start'})")
            pg.evaluate("scrollBy(0,-80)")
            pg.screenshot(path=str(EVID / f"02-viewport-{label}.png"))
            pg.screenshot(path=str(EVID / f"02-page-{label}.png"), full_page=True,
                          style=".nav {visibility:hidden !important}")
            ctx.close()


with sync_playwright() as p:
    b = p.chromium.launch()
    R["browser"] = b.version
    ctx = b.new_context(viewport={"width": 375, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle")
    row = accounts(pg)
    text = row.inner_text()
    check("accounts: switching without logout is explicit", bool(re.search(
        r"switch[^.]*without (?:logging|signing) out", text, re.I)), text)
    check("accounts: unrelated services are not attributed to this evidence",
          not re.search(r"notification|authorization|statement", text, re.I), text)
    row.scroll_into_view_if_needed()
    row.locator("img").evaluate("i=>i.decode()")
    row.screenshot(path=str(EVID / "02-copy.png"))
    ctx.close()
    if "--recapture" in sys.argv:
        recapture(b)
    elif "--copy-only" not in sys.argv:
        matrix(b)
        navigation(b)
    b.close()

R["summary"] = {"passed": sum(c["ok"] for c in R["checks"]),
                "failed": sum(not c["ok"] for c in R["checks"])}
OUT.write_text(json.dumps(R, indent=2, ensure_ascii=False), encoding="utf-8")
print(R["summary"])
sys.exit(1 if R["summary"]["failed"] else 0)
