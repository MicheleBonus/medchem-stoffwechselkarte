# -*- coding: utf-8 -*-
"""
Prueft die gebaute Website in docs/ Seite fuer Seite.

    python shot_site.py            alle Seiten
    python shot_site.py teil3 m01  nur diese

Geprueft wird je Seite und in beiden Farbschemata:
  - Konsolen- und Seitenfehler
  - waagerechter Ueberlauf, SVGs ohne Hoehe
  - SVG-Text ueber den viewBox hinaus
  - einander ueberlappende Beschriftungen
  - Linien und Boegen, die durch eine Beschriftung laufen
  - jeder Verweis auf eine andere Seite: Datei da, Anker da
"""
import io
import os
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
OUT = os.path.join(HERE, "shots")
os.makedirs(OUT, exist_ok=True)

SEITEN = sorted(p[:-5] for p in os.listdir(DOCS) if p.endswith(".html"))
if len(sys.argv) > 1:
    SEITEN = [s for s in SEITEN if s in sys.argv[1:]]

SCHUSS = {"index", "teil0", "teil2", "m01", "fahrplan", "mechanismen"}

JS_SPILL = """() => {
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
}"""

JS_COLLIDE = """() => {
  const hits = [];
  document.querySelectorAll('figure.tafel svg, figure.karte svg').forEach((svg, si) => {
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
        ts.push({ b: box(b, mu), s: t.textContent.trim() });
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
  return [...new Set(hits)];
}"""

JS_KREUZT = """() => {
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
      return { x0: Math.min(...xs)+2, x1: Math.max(...xs)-2,
               y0: Math.min(...ys) + (Math.max(...ys)-Math.min(...ys))*0.26,
               y1: Math.min(...ys) + (Math.max(...ys)-Math.min(...ys))*0.90,
               s: t.textContent.trim() };
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
}"""

JS_DIAG = """() => {
  const de = document.documentElement;
  const over = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > de.clientWidth + 2)
      over.push(el.tagName + '.' + (el.className || '').toString().slice(0,40)
                + ' right=' + Math.round(r.right));
  });
  const svgs = [...document.querySelectorAll('svg')];
  return {
    ueberlauf: document.body.scrollWidth > de.clientWidth + 2,
    taeter: over.slice(0, 6),
    svgs: svgs.length,
    svgOhneHoehe: svgs.filter(s => s.getBoundingClientRect().height < 2).length,
    links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))
  };
}"""


def anker_der_seiten():
    karte = {}
    for p in os.listdir(DOCS):
        if not p.endswith(".html"):
            continue
        t = io.open(os.path.join(DOCS, p), encoding="utf-8").read()
        karte[p[:-5]] = set(re.findall(r'\sid="([^"]+)"', t))
    return karte


ANKER = anker_der_seiten()
befund = []
schuesse = 0

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for slug in SEITEN:
        url = "file:///" + os.path.join(DOCS, slug + ".html").replace("\\", "/")
        for schema in ("light", "dark"):
            for breite in ((1440, 950), (430, 900)) if schema == "light" else ((1440, 950),):
                fehl = []
                ctx = br.new_context(viewport={"width": breite[0], "height": breite[1]},
                                     color_scheme=schema, device_scale_factor=1)
                pg = ctx.new_page()
                pg.on("console", lambda m: fehl.append("console %s: %s" % (m.type, m.text))
                      if m.type in ("error", "warning") else None)
                pg.on("pageerror", lambda e: fehl.append("pageerror: %s" % e))
                pg.goto(url, wait_until="load")
                diag = pg.evaluate(JS_DIAG)
                if diag["ueberlauf"]:
                    fehl.append("waagerechter Ueberlauf bei %dpx: %s"
                                % (breite[0], "; ".join(diag["taeter"])))
                if diag["svgOhneHoehe"]:
                    fehl.append("%d SVG ohne Hoehe" % diag["svgOhneHoehe"])
                if breite[0] == 1440 and schema == "light":
                    for name, js in (("Text ueber viewBox", JS_SPILL),
                                     ("Textueberlappung", JS_COLLIDE),
                                     ("Linie durch Beschriftung", JS_KREUZT)):
                        for x in pg.evaluate(js):
                            fehl.append("%s: %s" % (name, x))
                    for href in dict.fromkeys(diag["links"]):
                        if href.startswith(("http", "mailto:")):
                            continue
                        datei, _, ank = href.partition("#")
                        ziel = datei[:-5] if datei.endswith(".html") else slug
                        if ziel not in ANKER:
                            fehl.append("Verweis auf fehlende Seite: %s" % href)
                        elif ank and ank not in ANKER[ziel]:
                            fehl.append("Verweis auf fehlenden Anker: %s" % href)
                    if slug in SCHUSS:
                        pg.screenshot(path=os.path.join(OUT, slug + "-hell.png"),
                                      full_page=False)
                        schuesse += 1
                if schema == "dark" and slug in SCHUSS:
                    pg.screenshot(path=os.path.join(OUT, slug + "-dunkel.png"))
                    schuesse += 1
                ctx.close()
                for f in dict.fromkeys(fehl):
                    befund.append("%-12s %-5s %4dpx  %s" % (slug, schema, breite[0], f))
        print(".", end="", flush=True)
    br.close()

print("\n%d Seiten geprueft, %d Screenshots in %s" % (len(SEITEN), schuesse, OUT))
if befund:
    print("BEFUND (%d):" % len(befund))
    for b in befund[:80]:
        print("  " + b)
    if len(befund) > 80:
        print("  ... und %d weitere" % (len(befund) - 80))
    sys.exit(1)
print("BEFUND: sauber")
