# -*- coding: utf-8 -*-
"""Rendert eine einzelne Tafel aus tafeln.json zur Sichtpruefung."""
import io
import json
import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
TID = sys.argv[1] if len(sys.argv) > 1 else "m05"

svg = json.load(io.open(os.path.join(HERE, "tafeln.json"), encoding="utf-8"))[TID]
kopf = io.open(os.path.join(HERE, "src", "00_head.html"), encoding="utf-8").read()
css = kopf[kopf.index("<style>"):kopf.index("</style>") + 8]

seite = os.path.join(HERE, "vorschau_%s.html" % TID)
io.open(seite, "w", encoding="utf-8").write(
    css + '<body style="padding:30px"><figure class="tafel" style="margin:0">'
    + svg + "</figure></body>")

url = "file:///" + seite.replace("\\", "/")
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for scheme in ("light", "dark"):
        ctx = br.new_context(viewport={"width": 1120, "height": 1200},
                             color_scheme=scheme, device_scale_factor=2)
        pg = ctx.new_page()
        meld = []
        pg.on("console", lambda m: meld.append("%s: %s" % (m.type, m.text))
              if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: meld.append("pageerror: %s" % e))
        pg.goto(url, wait_until="load")

        # Text ausserhalb des viewBox?
        raus = pg.evaluate("""() => {
          const svg = document.querySelector('svg');
          const vb = svg.viewBox.baseVal, bad = [];
          svg.querySelectorAll('text').forEach(el => {
            const b = el.getBBox(), m = el.getCTM();
            const x0 = b.x * m.a + b.y * m.c + m.e, y0 = b.x * m.b + b.y * m.d + m.f;
            const x1 = x0 + b.width * m.a, y1 = y0 + b.height * m.d;
            // 12px Rand: Text, der die Kante streift, wirkt abgeschnitten
            if (x0 < 12 || y0 < 12 || x1 > vb.width - 12 || y1 > vb.height - 8)
              bad.push(el.textContent.slice(0, 30) + ' @' + Math.round(x0) + ',' + Math.round(y0));
          });
          return bad.slice(0, 8);
        }""")

        # Text ueber Text?
        stoss = pg.evaluate("""() => {
          const svg = document.querySelector('svg'), ts = [];
          svg.querySelectorAll('text').forEach(el => {
            if (el.closest('defs')) return;
            const b = el.getBBox(), m = el.getCTM();
            ts.push({t: el.textContent.trim(),
                     x0: b.x * m.a + b.y * m.c + m.e, y0: b.x * m.b + b.y * m.d + m.f,
                     w: b.width * m.a, h: b.height * m.d});
          });
          const bad = [];
          for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
            const a = ts[i], c = ts[j];
            if (!a.t || !c.t) continue;
            const ox = Math.min(a.x0 + a.w, c.x0 + c.w) - Math.max(a.x0, c.x0);
            const oy = Math.min(a.y0 + a.h, c.y0 + c.h) - Math.max(a.y0, c.y0);
            if (ox > 2.5 && oy > 2.5) bad.push(a.t.slice(0, 18) + ' / ' + c.t.slice(0, 18));
          }
          return bad.slice(0, 10);
        }""")

        # Linie oder Pfeil quer durch eine Beschriftung?
        kreuzt = pg.evaluate("""() => {
          const svg = document.querySelector('svg');
          const texte = [];
          svg.querySelectorAll('text').forEach(el => {
            if (el.closest('defs')) return;
            const b = el.getBBox(), m = el.getCTM();
            // Die Em-Box reicht deutlich ueber die sichtbaren Glyphen hinaus.
            // Ohne diesen Einzug meldet die Pruefung jeden Pfeil, der oberhalb
            // der Versalhoehe vorbeilaeuft, als Treffer.
            const h = b.height * m.d;
            texte.push({s: el.textContent.trim(),
                        x0: b.x * m.a + b.y * m.c + m.e + 1.5,
                        y0: b.x * m.b + b.y * m.d + m.f + h * 0.26,
                        x1: b.x * m.a + b.y * m.c + m.e + b.width * m.a - 1.5,
                        y1: b.x * m.b + b.y * m.d + m.f + h * 0.90});
          });
          const hits = [];
          svg.querySelectorAll('path, line').forEach(g => {
            if (g.closest('defs')) return;
            let len; try { len = g.getTotalLength(); } catch (e) { return; }
            if (!len) return;
            const m = g.getCTM(), n = Math.min(90, Math.ceil(len / 2));
            for (let i = 0; i <= n; i++) {
              let q; try { q = g.getPointAtLength(len * i / n); } catch (e) { return; }
              const x = q.x * m.a + q.y * m.c + m.e, y = q.x * m.b + q.y * m.d + m.f;
              for (const t of texte)
                if (x > t.x0 && x < t.x1 && y > t.y0 && y < t.y1) {
                  hits.push(g.tagName + ' kreuzt "' + t.s.slice(0, 30) + '"');
                  return;
                }
            }
          });
          return [...new Set(hits)];
        }""")

        print("--- %s" % scheme)
        print("   Konsole:", meld or "sauber")
        print("   ausserhalb viewBox:", raus or "keiner")
        print("   Textkollisionen:", stoss or "keine")
        print("   Linien durch Text:", kreuzt or "keine")
        pg.screenshot(path=os.path.join(HERE, "shots_plan",
                                        "tafel-%s-%s.png" % (TID, scheme)),
                      full_page=True)
        ctx.close()
    br.close()
print("Screenshots in shots_plan/tafel-%s-*.png" % TID)
