#!/usr/bin/env python3
"""Loads every page in a headless browser and reports broken images,
JS errors, horizontal overflow, and dead internal links.

Usage:  python3 -m http.server 8080 &   then   python3 tools/check_pages.py
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"
PAGES = ["/index.html", "/news.html", "/projects.html", "/experience.html", "/skills.html",
         "/education.html", "/activities.html",
         "/projects/hvac.html", "/projects/travel-agent.html", "/projects/agentpay.html",
         "/projects/infodistill.html", "/projects/nei-slam.html",
         "/projects/godot-mcp.html", "/projects/defillama.html", "/projects/warp-tote.html",
         "/projects/dp-adult.html", "/talks/mlm-membership-inference.html"]
WIDTHS = [320, 390, 768, 1024, 1440]

fail = 0
with sync_playwright() as p:
    br = p.chromium.launch(headless=True)
    pg = br.new_page(viewport={"width": 1440, "height": 1000})
    for path in PAGES:
        errs = []
        pg.on("pageerror", lambda e: errs.append(f"JS: {e}"))
        pg.goto(BASE + path); pg.wait_for_load_state("networkidle")
        broken = pg.eval_on_selector_all(
            "img", "els=>els.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'))")
        # internal links that 404
        hrefs = pg.eval_on_selector_all(
            "a[href]", "els=>els.map(a=>a.getAttribute('href')).filter(h=>h&&!/^(https?:|mailto:|#)/.test(h))")
        dead = []
        for h in set(hrefs):
            r = pg.request.get(BASE + "/" + h.lstrip("./").replace("../", ""))
            if r.status >= 400:
                dead.append(h)
        msgs = []
        # logos and the portrait are user-supplied; missing ones degrade gracefully
        optional = [b for b in broken if "/logos/" in b or "profile.jpg" in b]
        hard = [b for b in broken if b not in optional]
        if optional: print(f"note {path}\n      awaiting user assets: {sorted(set(optional))}")
        if hard: msgs.append(f"broken images: {hard}")
        if dead:   msgs.append(f"dead links: {dead}")
        if errs:   msgs.append(f"errors: {errs}")
        if msgs:
            fail = 1
            print(f"FAIL {path}")
            for m in msgs: print("      " + m)
        else:
            print(f"ok   {path}")
    # responsive overflow
    over = []
    for w in WIDTHS:
        pg.set_viewport_size({"width": w, "height": 900})
        for path in PAGES:
            pg.goto(BASE + path); pg.wait_for_load_state("networkidle")
            d = pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
            if d > 1: over.append((w, path, d))
    print("overflow:", over if over else "none")
    if over: fail = 1
    br.close()
sys.exit(fail)
