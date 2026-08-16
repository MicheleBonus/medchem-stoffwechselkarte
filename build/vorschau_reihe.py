# -*- coding: utf-8 -*-
"""
Zeigt eine Gruppe von Strukturformeln nebeneinander, so wie sie im Dokument
stehen wuerden, und legt ein Bild in shots/ ab.

    python vorschau_reihe.py ipp dmapp gpp fpp
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import gen_structures as g

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)

ids = sys.argv[1:]
if not ids:
    raise SystemExit("Aufruf: python vorschau_reihe.py <id> <id> ...")

CSS = io.open(os.path.join(HERE, "geruest", "karte.css"), encoding="utf-8").read()
ZUSATZ = io.open(os.path.join(HERE, "geruest", "site.css"), encoding="utf-8").read()

kacheln = []
for i in ids:
    if i not in g.MOLS:
        raise SystemExit("unbekannte id: %s" % i)
    smi, lbl = g.MOLS[i]
    svg = g.render(smi, lbl, **g.SCHMUCK.get(i, {}))
    kacheln.append("<figure class='mol'>%s<figcaption>%s</figcaption></figure>" % (svg, i))

doc = ("<!doctype html><html lang='de'><head><meta charset='utf-8'>"
       "<title>Reihe</title><style>%s\n%s\n"
       ".probe{display:flex;flex-wrap:wrap;gap:18px;padding:26px;align-items:flex-start}"
       ".probe figure.mol{margin:0;padding:12px;border:1px solid var(--rule);"
       "border-radius:8px;background:var(--surface);max-width:300px}"
       ".probe figure.mol svg{width:100%%;height:auto;display:block}"
       ".probe figcaption{font:600 12px var(--f-mono);color:var(--ink-3);"
       "text-align:center;margin-top:6px}"
       "</style></head><body><div class='probe'>%s</div></body></html>"
       % (CSS, ZUSATZ, "\n".join(kacheln)))

pfad = os.path.join(OUT, "reihe-" + "-".join(ids)[:60] + ".html")
io.open(pfad, "w", encoding="utf-8", newline="\n").write(doc)

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for schema in ("light", "dark"):
        ctx = br.new_context(viewport={"width": 1340, "height": 700},
                             color_scheme=schema, device_scale_factor=2)
        pg = ctx.new_page()
        pg.goto("file:///" + pfad.replace("\\", "/"), wait_until="load")
        bild = pfad.replace(".html", "-%s.png" % schema)
        pg.locator(".probe").screenshot(path=bild)
        print("geschrieben:", bild)
        ctx.close()
    br.close()
