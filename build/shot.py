# -*- coding: utf-8 -*-
"""Rendert die Metabolitkarte headless und legt Screenshots + Konsolenfehler ab."""
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(os.path.dirname(HERE), "Metabolitkarte.html").replace("\\", "/")
OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)

# (name, anker, scheme, viewport)
SHOTS = [
    ("01-kopf-hell",      None,     "light", (1440, 950)),
    ("02-metakarte-hell", "#teil0",  "light", (1440, 950)),
    ("03-kaskade-hell",   "#a2-2",   "light", (1440, 950)),
    ("04-tafel-plp-hell", "#m01",    "light", (1440, 1100)),
    ("05-tafel-fad-hell", "#m06",    "light", (1440, 950)),
    ("06-metakarte-dunkel", "#teil0", "dark", (1440, 950)),
    ("07-kaskade-dunkel", "#a2-3",   "dark",  (1440, 950)),
    ("08-tafel-plp-dunkel", "#m01",  "dark",  (1440, 1100)),
    ("09-schmal-hell",    "#a1-4",   "light", (430, 900)),
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
            pg.wait_for_timeout(180)
        pg.screenshot(path=os.path.join(OUT, name + ".png"))
        ctx.close()

    # Layout-Diagnose
    ctx = br.new_context(viewport={"width": 1440, "height": 950})
    pg = ctx.new_page()
    pg.goto(URL, wait_until="load")

    # SVG-Text laeuft ueber den viewBox hinaus? (SVG-Text bricht nicht um)
    spill = pg.evaluate("""() => {
      const bad = [];
      document.querySelectorAll('figure.tafel svg, figure.karte svg').forEach((svg, si) => {
        const vb = svg.viewBox.baseVal;
        svg.querySelectorAll('text').forEach(t => {
          let b; try { b = t.getBBox(); } catch (e) { return; }
          const overR = b.x + b.width  - (vb.x + vb.width);
          const overB = b.y + b.height - (vb.y + vb.height);
          if (overR > 1 || overB > 1)
            bad.push('svg#' + si + ' +' + Math.round(Math.max(overR, overB)) + 'px  "'
                     + t.textContent.trim().slice(0, 58) + '"');
        });
      });
      return bad;
    }""")

    # Ueberlappen sich Textzeilen innerhalb einer Tafel?
    collide = pg.evaluate("""() => {
      const hits = [];
      document.querySelectorAll('figure.tafel svg, figure.karte svg').forEach((svg, si) => {
        // Text in <defs> wird nie an Ort und Stelle gezeichnet -> ausschliessen,
        // sonst melden alle <use>-Vorlagen ihre identischen lokalen Boxen als Kollision.
        // getBBox() liefert LOKALE Koordinaten - ohne CTM melden alle gleich
        // positionierten Elemente translatierter Gruppen falsche Kollisionen.
        const box = (b, m) => {
          const xs = [], ys = [];
          for (const [px, py] of [[b.x, b.y], [b.x + b.width, b.y],
                                  [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]) {
            xs.push(m.a * px + m.c * py + m.e);
            ys.push(m.b * px + m.d * py + m.f);
          }
          const x0 = Math.min(...xs), y0 = Math.min(...ys);
          return { x: x0, y: y0, width: Math.max(...xs) - x0, height: Math.max(...ys) - y0 };
        };
        const ts = [...svg.querySelectorAll('text')].filter(t => !t.closest('defs')).map(t => {
          let b, m;
          try { b = t.getBBox(); m = t.getCTM(); } catch (e) { return null; }
          if (!m) return null;
          return { b: box(b, m), s: t.textContent.trim() };
        }).filter(Boolean);

        // <use>-Instanzen: deren Textinhalt steckt im Shadow-Tree und ist fuer
        // querySelectorAll unsichtbar. Ohne diese Ergaenzung ist die Pruefung
        // fuer jede Tafel mit wiederverwendeten Bausteinen blind.
        svg.querySelectorAll('use').forEach(u => {
          const id = (u.getAttribute('href') || u.getAttribute('xlink:href') || '').replace('#', '');
          const tpl = id && svg.querySelector('#' + CSS.escape(id));
          if (!tpl) return;
          let m; try { m = u.getCTM(); } catch (e) { return; }
          if (!m) return;
          const ux = parseFloat(u.getAttribute('x') || 0), uy = parseFloat(u.getAttribute('y') || 0);
          const mu = m.translate(ux, uy);
          tpl.querySelectorAll('text').forEach(t => {
            let b; try { b = t.getBBox(); } catch (e) { return; }
            // getBBox im Template ist bereits relativ zum Template-Ursprung
            ts.push({ b: box(b, mu), s: t.textContent.trim(), ausUse: true });
          });
        });
        for (let i = 0; i < ts.length; i++)
          for (let j = i + 1; j < ts.length; j++) {
            const a = ts[i].b, c = ts[j].b;
            const ox = Math.min(a.x+a.width, c.x+c.width) - Math.max(a.x, c.x);
            const oy = Math.min(a.y+a.height, c.y+c.height) - Math.max(a.y, c.y);
            if (ox > 3 && oy > 3)
              hits.push('svg#' + si + '  "' + ts[i].s.slice(0,32) + '" x "' + ts[j].s.slice(0,32) + '"');
          }
      });
      return hits;
    }""")

    # Laeuft eine Linie oder ein Bogen durch eine Beschriftung?
    # (Die Text-gegen-Text-Pruefung oben findet das nicht.)
    kreuzt = pg.evaluate("""() => {
      const hits = [];
      const toRoot = (el, p) => {
        const m = el.getCTM(); if (!m) return null;
        return { x: m.a*p.x + m.c*p.y + m.e, y: m.b*p.x + m.d*p.y + m.f };
      };
      document.querySelectorAll('figure.tafel svg, figure.karte svg').forEach((svg, si) => {
        const texte = [...svg.querySelectorAll('text')].filter(t => !t.closest('defs')).map(t => {
          let b, m; try { b = t.getBBox(); m = t.getCTM(); } catch (e) { return null; }
          if (!m) return null;
          const xs = [], ys = [];
          for (const [px, py] of [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]]) {
            xs.push(m.a*px + m.c*py + m.e); ys.push(m.b*px + m.d*py + m.f);
          }
          // 2px Innenrand: ein Strich, der die Box nur streift, zaehlt nicht
          return { x0: Math.min(...xs)+2, x1: Math.max(...xs)-2,
                   y0: Math.min(...ys) + (Math.max(...ys)-Math.min(...ys))*0.26,
                   y1: Math.min(...ys) + (Math.max(...ys)-Math.min(...ys))*0.90,
                   s: t.textContent.trim() };   // sichtbare Glyphenhoehe, nicht Em-Box
        }).filter(Boolean);

        svg.querySelectorAll('path, line, polyline, circle').forEach(g => {
          if (g.closest('defs') || g.closest('marker')) return;
          if (g.getAttribute('stroke') === 'none') return;
          let len; try { len = g.getTotalLength(); } catch (e) { return; }
          if (!len) return;
          const n = Math.min(400, Math.max(20, Math.round(len / 3)));
          for (let i = 0; i <= n; i++) {
            let p; try { p = toRoot(g, g.getPointAtLength(len * i / n)); } catch (e) { return; }
            if (!p) return;
            for (const t of texte) {
              if (p.x > t.x0 && p.x < t.x1 && p.y > t.y0 && p.y < t.y1) {
                hits.push('svg#' + si + '  ' + g.tagName + ' kreuzt "' + t.s.slice(0, 46) + '"');
                return;
              }
            }
          }
        });
      });
      return [...new Set(hits)];
    }""")

    diag = pg.evaluate("""() => {
      const de = document.documentElement;
      const over = [];
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && r.right > de.clientWidth + 2)
          over.push(el.tagName + '.' + (el.className || '').toString().slice(0,40)
                    + ' right=' + Math.round(r.right));
      });
      const svgs = [...document.querySelectorAll('svg')];
      const zero = svgs.filter(s => s.getBoundingClientRect().height < 2).length;
      return {
        bodyScrollW: document.body.scrollWidth,
        clientW: de.clientWidth,
        horizontalOverflow: document.body.scrollWidth > de.clientWidth + 2,
        offenders: over.slice(0, 12),
        svgTotal: svgs.length,
        svgZeroHeight: zero,
        docHeight: document.body.scrollHeight
      };
    }""")
    br.close()

print("Screenshots:", len(SHOTS), "->", OUT)
for k, v in diag.items():
    print("  %-20s %s" % (k, v))

print("\nSVG-Text ueber viewBox hinaus: %d" % len(spill))
for x in spill[:15]:
    print("   ", x)
print("SVG-Textueberlappungen: %d" % len(collide))
for x in collide[:15]:
    print("   ", x)
print("Linien durch Beschriftungen: %d" % len(kreuzt))
for x in kreuzt[:15]:
    print("   ", x)
if errors:
    print("\nKonsole/Seitenfehler:")
    for e in dict.fromkeys(errors):
        print("  ", e)
else:
    print("\nkeine Konsolenfehler")
