"""Billing visual-narrative QA (ticket 04). Usage: python qa.py <evidence_dir> <results_json>"""
import json, sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/case-studies/billing.html"
EVID, OUT = sys.argv[1], sys.argv[2]
R = {"checks": [], "console": [], "failed_requests": []}


def check(name, ok, detail=""):
    R["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def load_all(pg):
    h = pg.evaluate("document.body.scrollHeight")
    for y in range(0, h + 900, 400):
        pg.evaluate(f"window.scrollTo(0,{y})")
        pg.wait_for_timeout(40)
    pg.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)", timeout=30000)


STEPS = ["Access", "Contract identification", "View outstanding debts", "Start negotiation",
         "Choose payment method", "Confirm negotiation", "Pay invoice(s)", "Debts cleared"]

with sync_playwright() as p:
    b = p.chromium.launch()

    # Layout per width (reduced motion so sections are visible immediately).
    for w in [320, 375, 768, 1440]:
        ctx = b.new_context(viewport={"width": w, "height": 900}, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.on("console", lambda m, w=w: m.type in ("error", "warning") and R["console"].append(f"{w}: {m.type}: {m.text}"))
        pg.on("requestfailed", lambda r, w=w: R["failed_requests"].append(f"{w}: {r.url} {r.failure}"))
        pg.on("response", lambda r, w=w: r.status >= 400 and R["failed_requests"].append(f"{w}: {r.status} {r.url}"))
        pg.goto(URL, wait_until="networkidle")
        load_all(pg)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        check(f"{w}: no horizontal overflow", sw <= w, f"scrollWidth={sw}")
        wide = pg.evaluate("""w=>[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();
            return r.width>0 && (r.right>w+1||r.left<-1) && !e.closest('.sr-only') && !e.matches('.sr-only')}).map(e=>e.className||e.tagName).slice(0,5)""", w)
        check(f"{w}: no element outside viewport", not wide, str(wide))
        imgs = pg.evaluate("""()=>[...document.querySelectorAll('.billing-shot__img')].map(i=>({src:i.getAttribute('src').split('/').pop(),
            nw:i.naturalWidth,nh:i.naturalHeight,w:i.getBoundingClientRect().width,h:i.getBoundingClientRect().height,lazy:i.loading}))""")
        check(f"{w}: 8 screenshots loaded", len(imgs) == 8 and all(i["nw"] > 0 for i in imgs), ", ".join(i["src"] for i in imgs))
        check(f"{w}: screenshots keep intrinsic ratio",
              all(abs(i["w"] / i["h"] - i["nw"] / i["nh"]) < 0.02 for i in imgs))
        check(f"{w}: screenshots lazy-loaded", all(i["lazy"] == "lazy" for i in imgs))
        rows = pg.evaluate("""()=>[...document.querySelectorAll('.billing-row')].map(r=>{const c=r.querySelector('.billing-row__copy'),f=r.querySelector('.billing-shot');
            const cr=c.getBoundingClientRect(),fr=f.getBoundingClientRect();
            return {cls:r.className, imgs:r.querySelectorAll('img').length, domCopyFirst:!!(c.compareDocumentPosition(f)&Node.DOCUMENT_POSITION_FOLLOWING),
            copyAbove:cr.bottom<=fr.top+1, mediaLeft:fr.right<=cr.left+1, mediaRight:fr.left>=cr.right-1,
            capFirst: !f.querySelector('figcaption') || f.firstElementChild.tagName==='FIGCAPTION',
            overlap: !(cr.bottom<=fr.top+1||fr.bottom<=cr.top+1||cr.right<=fr.left+1||fr.right<=cr.left+1)}})""")
        check(f"{w}: one screenshot per row", all(r["imgs"] == 1 for r in rows), f"{len(rows)} rows")
        check(f"{w}: copy precedes screenshot in DOM", all(r["domCopyFirst"] and r["capFirst"] for r in rows))
        check(f"{w}: copy and screenshot do not overlap", not any(r["overlap"] for r in rows))
        if w <= 1024:
            check(f"{w}: copy above screenshot on screen", all(r["copyAbove"] for r in rows))
        else:
            ok = all((r["mediaLeft"] if "media-left" in r["cls"] else r["mediaRight"] if "media-right" in r["cls"] else r["copyAbove"]) for r in rows)
            kinds = [("left" if "media-left" in r["cls"] else "right" if "media-right" in r["cls"] else "wide") for r in rows]
            check(f"{w}: desktop alternation matches spec", ok and kinds == ["left", "right", "left", "right", "left", "wide", "left", "wide"], str(kinds))
        # Flow layout: visual order follows numbering (row-major).
        pos = pg.evaluate("()=>[...document.querySelectorAll('.billing-flow__step')].map(l=>{const r=l.getBoundingClientRect();return [Math.round(r.top),Math.round(r.left)]})")
        cols = {1440: 4, 768: 2}.get(w, 1)
        rowtops = [pos[i][0] for i in range(0, 8, cols)]
        ordered = all(pos[i][1] < pos[i + 1][1] for i in range(7) if (i + 1) % cols) and rowtops == sorted(rowtops)
        check(f"{w}: flow renders {cols} column(s) in numbered order", ordered, str(pos))
        conn = pg.evaluate("()=>[...document.querySelectorAll('.billing-flow__step')].map(l=>getComputedStyle(l,'::after').content!=='none')")
        expect = [((i + 1) % cols != 0) if cols > 1 else (i < 7) for i in range(8)]
        check(f"{w}: connectors only toward next step (none at row ends)", conn == expect, str(conn))
        # Evidence (viewport captures, after scrolling each block into view).
        for name, sel in [("flow", ".billing-decision--flow"), ("access", ".billing-row:nth-of-type(2)"),
                          ("payments", ".billing-rows .billing-row:nth-child(2)"), ("installments", ".billing-rows .billing-row:nth-child(3)"),
                          ("review", ".billing-rows .billing-row:nth-child(4)"), ("documents", ".billing-rows .billing-row:nth-child(5)"),
                          ("dashboard", ".billing-rows .billing-row:nth-child(6)")]:
            if w not in (375, 1440):
                if name != "flow":
                    continue
            el = pg.locator(sel).first
            el.evaluate("e=>e.scrollIntoView({block:'start'})")
            pg.evaluate("window.scrollBy(0,-80)")
            pg.wait_for_timeout(250)
            pg.screenshot(path=f"{EVID}/narrative-{name}-{w}.png")
        ctx.close()

    # Flow: static cards, all content visible, endpoints highlighted, nothing interactive.
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle")
    st = pg.evaluate("""()=>[...document.querySelectorAll('.billing-flow__step')].map(l=>{const t=l.querySelector('.billing-flow__text');const cs=getComputedStyle(l);
        return {t:l.querySelector('.billing-flow__title').textContent,n:l.querySelector('.billing-flow__number').textContent,
        visible:t.getBoundingClientRect().height>0&&getComputedStyle(t).visibility==='visible',endpoint:l.classList.contains('billing-flow__step--endpoint'),
        shadow:cs.boxShadow!=='none'}})""")
    check("flow: 8 steps in documented order", [s["t"] for s in st] == STEPS, str([s["t"] for s in st]))
    check("flow: numbering 01–08", [s["n"] for s in st] == [f"0{i}" for i in range(1, 9)])
    check("flow: every explanation visible by default", all(s["visible"] for s in st))
    check("flow: only steps 01 and 08 highlighted", [s["endpoint"] and s["shadow"] for s in st] == [True] + [False] * 6 + [True])
    check("flow: list is an ordered list", pg.evaluate("document.querySelector('.billing-flow__steps').tagName") == "OL")
    inter = pg.evaluate("document.querySelectorAll('.billing-flow details, .billing-flow summary, .billing-flow a, .billing-flow button, .billing-flow [tabindex]').length")
    check("flow: no interactive elements", inter == 0, str(inter))
    acc = pg.evaluate("document.querySelector('.billing-flow__steps').getAttribute('aria-label')")
    check("flow: list has accessible name", bool(acc), acc)
    arrow = pg.evaluate("getComputedStyle(document.querySelector('.billing-flow__step'),'::after').backgroundColor")
    check("flow: arrows use accent fill", arrow == "rgb(244, 168, 124)", arrow)
    ctx.close()

    # No JavaScript.
    ctx = b.new_context(viewport={"width": 375, "height": 900}, java_script_enabled=False)
    pg = ctx.new_page()
    pg.goto(URL, wait_until="load")
    n = pg.locator(".billing-flow__step").count()
    op = pg.evaluate("[...document.querySelectorAll('.billing-flow__text')].every(t=>t.getBoundingClientRect().height>0)")
    vis = pg.evaluate("()=>[...document.querySelectorAll('.cs-section')].every(s=>getComputedStyle(s).opacity==='1')")
    check("no-JS: 8 steps and explanations visible, sections visible", n == 8 and op and vis, f"steps={n} texts={op} visible={vis}")
    ctx.close()

    # Normal motion: sections appear on scroll, including after expanding all steps.
    for w in [375, 1440]:
        ctx = b.new_context(viewport={"width": w, "height": 700})
        pg = ctx.new_page()
        pg.goto(URL, wait_until="networkidle")
        hid = pg.evaluate("()=>[...document.querySelectorAll('.cs-section')].filter(s=>s.style.opacity==='0').length")
        y = 0
        while y < pg.evaluate("document.body.scrollHeight") + 700:
            pg.mouse.wheel(0, 300); y += 300
            pg.wait_for_timeout(80)
        pg.wait_for_timeout(800)
        res = pg.evaluate("()=>[...document.querySelectorAll('.cs-section')].map(s=>({id:s.getAttribute('aria-labelledby'),o:getComputedStyle(s).opacity,h:Math.round(s.getBoundingClientRect().height)}))")
        check(f"motion {w}: all sections visible after scroll (initially hidden: {hid})",
              all(r["o"] == "1" for r in res), str(res))
        ratio = max(r["h"] for r in res) * 0.08
        check(f"motion {w}: tallest section reachable at 0.08 threshold", ratio < 700, f"8% of tallest = {ratio:.0f}px vs viewport 700px")
        ctx.close()

    # Preserved surfaces and copy precision.
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle")
    nav = pg.evaluate("()=>[...document.querySelectorAll('.nav a')].map(a=>a.getAttribute('href'))")
    check("nav links preserved", nav == ["../", "../#work", "../#contact", "../#about"], str(nav))
    nxt = pg.evaluate("document.querySelector('.cs-next__link').getAttribute('href')")
    check("next project preserved", nxt == "enrollment.html")
    stats = pg.evaluate("()=>[...document.querySelectorAll('.cs-stat')].map(s=>s.innerText.replace(/\\n+/g,' '))")
    check("metrics preserved", stats == ["BRL 4.5M already paid through self-service", "BRL 54.1M in installment negotiations",
                                         "3,000+ contracts reactivated with benefits", "10,000+ negotiations completed autonomously"], str(stats))
    form = pg.evaluate("()=>{const f=document.getElementById('contact-form');return f&&f.action+'|'+f.querySelectorAll('input,textarea').length}")
    check("contact form present (not submitted)", form == "https://formspree.io/f/mbdqyywl|3", form)
    pg.locator(".contact__copy").scroll_into_view_if_needed()
    check("contact copy button present", pg.locator(".contact__copy").is_visible())
    hero = pg.evaluate("document.querySelector('.cs-header__hook').textContent")
    check("hero hook preserved", hero.startswith("Debt negotiation moved from phone calls"))
    html = pg.content()
    for bad in ["in real time", "participant-facing", "tela.png", "billing-digital-platform-flow", "cs-image-grid"]:
        check(f"copy/markup: '{bad}' absent", bad not in html)
    for good in ["5 minutes", "five minutes"]:
        pass
    check("copy: five minutes still framed as design target", "The design target was to let participants complete negotiations in under five minutes" in html)
    contrast = pg.evaluate("()=>[...document.querySelectorAll('.billing-shot__caption,.billing-row__body,.billing-flow__text')].map(e=>getComputedStyle(e).color)")
    check("orientation text uses strong secondary color", all(c == "rgba(242, 242, 245, 0.65)" for c in contrast), contrast[0])
    links = pg.evaluate("document.querySelectorAll('.billing-shot a, .billing-row a').length")
    check("no full-size links in screen rows", links == 0, str(links))
    ctx.close()
    b.close()

R["summary"] = {"passed": sum(c["ok"] for c in R["checks"]), "failed": sum(not c["ok"] for c in R["checks"])}
json.dump(R, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(R["summary"], "console:", R["console"], "failed:", R["failed_requests"])
