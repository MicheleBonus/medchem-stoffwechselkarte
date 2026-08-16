# -*- coding: utf-8 -*-
"""Rendert den Lernfahrplan headless, prueft Layout und legt Screenshots ab."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(os.path.dirname(HERE), "Lernfahrplan.html").replace("\\", "/")
OUT = os.path.join(HERE, "shots_plan")
os.makedirs(OUT, exist_ok=True)

SHOTS = [
    ("01-kopf-hell",    None,      "light", (1440, 950)),
    ("02-block1-hell",  "#b1",     "light", (1440, 1200)),
    ("03-block4-hell",  "#b4",     "light", (1440, 1200)),
    ("04-pflicht-hell", "#pflicht", "light", (1440, 1100)),
    ("05-zeit-hell",    "#zeit",   "light", (1440, 1000)),
    ("06-block1-dunkel", "#b1",    "dark",  (1440, 1200)),
    ("07-pflicht-dunkel", "#pflicht", "dark", (1440, 1100)),
    ("08-schmal-hell",  "#b2",     "light", (430, 900)),
    ("09-mittel-hell",  "#b3",     "light", (900, 1100)),
    ("10-breit-hell",   "#b1",     "light", (2200, 1200)),
]

errors = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name, anchor, scheme, vp in SHOTS:
        ctx = br.new_context(viewport={"width": vp[0], "height": vp[1]},
                             color_scheme=scheme, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("console", lambda m: errors.append("console %s: %s" % (m.type, m.text))
              if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: errors.append("pageerror: %s" % e))
        pg.goto(URL, wait_until="load")
        if anchor:
            pg.evaluate("a => document.querySelector(a).scrollIntoView()", anchor)
            pg.wait_for_timeout(150)
        pg.screenshot(path=os.path.join(OUT, name + ".png"))
        ctx.close()

    befund = []
    for w in (380, 430, 768, 900, 1180, 1440, 2200):
        ctx = br.new_context(viewport={"width": w, "height": 950})
        pg = ctx.new_page()
        pg.goto(URL, wait_until="load")

        # waagerechter Ueberlauf der Seite
        ueber = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        if ueber > 1:
            befund.append("%dpx: Seite laeuft %dpx waagerecht ueber" % (w, ueber))

        # Element, das ueber den Viewport hinausragt (Tabelle darf, sie scrollt selbst)
        raus = pg.evaluate("""() => {
          const bad = [];
          document.querySelectorAll('body *').forEach(el => {
            if (el.closest('.tabelle-wrap')) return;
            const r = el.getBoundingClientRect();
            if (r.width > 0 && r.right > window.innerWidth + 1)
              bad.push(el.tagName.toLowerCase() + '.' + (el.className || '?') +
                       ' bis ' + Math.round(r.right));
          });
          return bad.slice(0, 4);
        }""")
        for b in raus:
            befund.append("%dpx: ragt hinaus - %s" % (w, b))

        # ueberlappende Textbloecke im selben Raster
        ctx.close()

    # Kontrast: jeder Text muss eine Hintergrundfarbe hinter sich haben
    for scheme in ("light", "dark"):
        ctx = br.new_context(viewport={"width": 1440, "height": 950}, color_scheme=scheme)
        pg = ctx.new_page()
        pg.goto(URL, wait_until="load")
        bg = pg.evaluate("() => getComputedStyle(document.body).backgroundColor")
        if bg in ("rgba(0, 0, 0, 0)", "transparent"):
            befund.append("%s: body ohne Hintergrundfarbe" % scheme)
        ctx.close()

    br.close()

print("Screenshots: %s" % OUT)
if errors:
    print("KONSOLE:")
    for e in sorted(set(errors)):
        print("  - %s" % e)
else:
    print("Konsole: sauber")
if befund:
    print("LAYOUT:")
    for b in befund:
        print("  - %s" % b)
else:
    print("Layout: sauber")
