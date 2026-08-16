# -*- coding: utf-8 -*-
"""
Baut die Website nach docs/ - eine Seite je Teil, eine je Mechanismus-Tafel.

    python site.py

Quellen
    src/          Teil 0 bis 9 und die Mechanismus-Tafeln als Fragmente
    src_plan/     der Lernfahrplan als Fragmente
    geruest/      karte.css, rail.html, kopf.html, start.html

Ausgabe
    docs/index.html, docs/fahrplan.html, docs/teil0.html ... docs/m17.html
    docs/assets/karte.css

Jede Datei traegt ein vollstaendiges HTML-Geruest. Interne Verweise stehen in
den Quellen weiter als "#anker"; welche Seite den Anker traegt, ermittelt der
Builder und schreibt den Verweis um. Ein Anker ohne Seite ist ein Abbruch.
"""
import io
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
SRC_PLAN = os.path.join(HERE, "src_plan")
GERUEST = os.path.join(HERE, "geruest")
DOCS = os.path.join(os.path.dirname(HERE), "docs")

BASIS = "Stoffwechselkarte der Signalmoleküle"


def lies(pfad):
    with io.open(pfad, encoding="utf-8") as f:
        return f.read()


def schreibe(pfad, text):
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ------------------------------------------------------------------ Bausteine
STRUCT = json.loads(lies(os.path.join(HERE, "structures.json")))
TAFELN = json.loads(lies(os.path.join(HERE, "tafeln.json")))

fehlt_struktur, fehlt_tafel = set(), set()


def einsetzen(doc):
    def s(m):
        k = m.group(1)
        if k not in STRUCT:
            fehlt_struktur.add(k)
            return "<span class='fehlt'>[Struktur fehlt: %s]</span>" % k
        return STRUCT[k]

    def t(m):
        k = m.group(1)
        if k not in TAFELN:
            fehlt_tafel.add(k)
            return "<span class='fehlt'>[Tafel fehlt: %s]</span>" % k
        return TAFELN[k]

    doc = re.sub(r"\{\{S:([a-z0-9_]+)\}\}", s, doc)
    doc = re.sub(r"\{\{T:([a-z0-9_]+)\}\}", t, doc)
    return doc


# ------------------------------------------------------- Mechanismusteil teilen
def teile_mechanismen():
    """40_mech.html -> (kopfteil, [(id, titel, sub, rumpf)], schlussteil)"""
    txt = lies(os.path.join(SRC, "40_mech.html"))
    marken = list(re.finditer(r"[ \t]*<!--\s*=+\s*M-(\d\d)\s*-->\n", txt))
    if len(marken) != 17:
        raise SystemExit("ABBRUCH: %d Tafelmarken in 40_mech.html, erwartet 17"
                         % len(marken))
    kopf = txt[:marken[0].start()]
    tafeln = []
    for i, m in enumerate(marken):
        anfang = m.end()
        ende = marken[i + 1].start() if i + 1 < len(marken) else len(txt)
        rumpf = txt[anfang:ende]
        tid = "m" + m.group(1)
        titel = re.search(r"<h3>(.*?)</h3>", rumpf, re.S).group(1)
        sub = re.search(r'<p class="tafel-sub">(.*?)</p>', rumpf, re.S)
        tafeln.append((tid, re.sub(r"\s+", " ", titel).strip(),
                       re.sub(r"\s+", " ", sub.group(1)).strip() if sub else "",
                       rumpf))
    # Der Schlussteil (Merkkasten + </section>) haengt an der letzten Tafel.
    letzte = tafeln[-1][3]
    schnitt = letzte.rindex("</figure>") + len("</figure>")
    schluss = letzte[schnitt:]
    tafeln[-1] = tafeln[-1][:3] + (letzte[:schnitt],)
    return kopf, tafeln, schluss


def entkleide(rumpf):
    """Ein Tafelrumpf steht im Quelltext innerhalb von <section>; als eigene
    Seite braucht er seine eigene Sektion."""
    return rumpf.rstrip().rstrip("\n")


# ----------------------------------------------------------------- Seitenliste
TEILE = [
    ("teil0", "10_teil0.html"),
    ("teil1", "20_teil1.html"),
    ("teil2", "30_teil2.html"),
    ("teil3", "35_teil3.html"),
    ("teil4", "37_teil4.html"),
    ("teil5", "38_teil5.html"),
    ("teil6", "39_teil6.html"),
    ("teil7", "39b_teil7.html"),
    ("teil8", "39c_teil8.html"),
    ("teil9", "39d_teil9.html"),
]

mech_kopf, mech_tafeln, mech_schluss = teile_mechanismen()

seiten = []          # (slug, titel, kurzbeschreibung, rumpf-html)


def kurz(html, grenze=180):
    m = re.search(r'<p class="abstract">(.*?)</p>', html, re.S)
    if not m:
        m = re.search(r'<p class="tafel-sub">(.*?)</p>', html, re.S)
    if not m:
        m = re.search(r'<p class="lead">(.*?)</p>', html, re.S)
    if not m:
        return ""
    s = re.sub(r"<[^>]+>", "", m.group(1))
    s = re.sub(r"\s+", " ", s).strip()
    return (s[:grenze].rsplit(" ", 1)[0] + " …") if len(s) > grenze else s


# --- Start
seiten.append(("index", "Start", "", lies(os.path.join(GERUEST, "start.html"))))

# --- Fahrplan
plan_teile = sorted(p for p in os.listdir(SRC_PLAN) if p.endswith(".html"))
plan_html = "\n".join(lies(os.path.join(SRC_PLAN, p)) for p in plan_teile)
# Der Fahrplan brachte sein eigenes Geruest mit; Titel und Stil kommen jetzt
# von der Website. Nur der Rumpf zwischen <main> und </main> wird uebernommen.
plan_html = re.sub(r"<style>.*?</style>", "", plan_html, flags=re.S)
plan_html = re.sub(r"<title>.*?</title>\s*", "", plan_html, flags=re.S)
plan_html = re.sub(r"</?main[^>]*>", "", plan_html)
plan_html = plan_html.replace('<header class="kopf">',
                              '<header class="kopf" id="fahrplan">', 1)
plan_html = '<section class="teil band">\n' + plan_html.strip() + "\n</section>\n"
seiten.append(("fahrplan", "Lernfahrplan",
               "Vier Blöcke, 26 Pflichtpositionen, zwei Zeitpläne.", plan_html))

# --- Teile 0 bis 9
for slug, datei in TEILE:
    html = lies(os.path.join(SRC, datei))
    titel = re.search(r"<h2>(.*?)</h2>", html, re.S).group(1)
    seiten.append((slug, re.sub(r"\s+", " ", titel).strip(), kurz(html), html))

# --- Mechanismus-Uebersicht
karten = []
for tid, titel, sub, _ in mech_tafeln:
    karten.append(
        '    <a class="tafelkarte" href="#%s">\n'
        '      <span class="tk-id">%s</span>\n'
        '      <b>%s</b>\n'
        '      <span class="tk-was">%s</span>\n'
        '    </a>' % (tid, tid.upper().replace("M", "M-"), titel, sub))
uebersicht = (mech_kopf.rstrip()
              + '\n\n  <div class="tafelgitter">\n'
              + "\n".join(karten) + "\n  </div>\n"
              + mech_schluss)
seiten.append(("mechanismen", "Die wiederkehrenden Mechanismen",
               kurz(mech_kopf), uebersicht))

# --- die 17 Tafelseiten
for tid, titel, sub, rumpf in mech_tafeln:
    kopf = ('<section class="teil band" id="%s-seite">\n'
            '  <div class="teil-kopf schmal">\n'
            '    <div class="nr"><a href="#teilM">Mechanismus-Tafeln</a></div>\n'
            '  </div>\n' % tid)
    seiten.append((tid, titel, sub, kopf + entkleide(rumpf) + "\n</section>\n"))

# --- Abschluss ans Ende von Teil 9 haengen
fuss_text = lies(os.path.join(SRC, "99_foot.html"))
fuss_text = fuss_text.replace("</main>", "").replace("</div>", "", 1) \
    if fuss_text.rstrip().endswith("</div>") else fuss_text
fuss_text = re.sub(r"</main>\s*</div>\s*$", "", fuss_text)
for i, (slug, titel, k, html) in enumerate(seiten):
    if slug == "teil9":
        seiten[i] = (slug, titel, k, html.rstrip() + "\n\n" + fuss_text)

# ------------------------------------------------------------ Anker einsammeln
seiten = [(s, t, k, einsetzen(h)) for s, t, k, h in seiten]

anker = {}          # id -> slug ; nur Anker ausserhalb der Grafiken
doppelt = []
for slug, _, _, html in seiten:
    # Marker-IDs innerhalb eines <svg> sind seitenlokal und nie Sprungziel.
    ohne = re.sub(r"<svg.*?</svg>", "", html, flags=re.S)
    gesehen = set()
    for i in re.findall(r'\sid="([^"]+)"', ohne):
        if i in gesehen:
            doppelt.append("%s doppelt auf %s" % (i, slug))
        gesehen.add(i)
        if i in anker:
            doppelt.append("%s (in %s und %s)" % (i, anker[i], slug))
        else:
            anker[i] = slug

# Die Rail und die Startseite verweisen auf Seitenanfaenge.
HAUPTANKER = {"index": "start", "fahrplan": "fahrplan", "mechanismen": "teilM"}
for slug, _, _, _ in seiten:
    if slug.startswith("teil"):
        HAUPTANKER[slug] = slug
    elif re.match(r"m\d\d$", slug):
        HAUPTANKER[slug] = slug

leer = set()


def ziel(a, von):
    """#anker -> Verweis von der Seite 'von' aus."""
    s = anker.get(a)
    if s is None:
        leer.add(a)
        return "#" + a
    if s == von:
        return "#" + a
    if HAUPTANKER.get(s) == a:
        return "index.html" if s == "index" else "%s.html" % s
    return "%s.html#%s" % (s, a)


# --------------------------------------------------------------------- Geruest
CSS = "\n\n".join(lies(os.path.join(GERUEST, n))
                  for n in ("karte.css", "site.css", "fahrplan.css"))
RAIL = lies(os.path.join(GERUEST, "rail.html"))

REIHE = [s for s, _, _, _ in seiten]

KOPFVORLAGE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titel)s</title>
<meta name="description" content="%(kurz)s">
<link rel="stylesheet" href="assets/karte.css">
<link rel="icon" href="assets/marke.svg" type="image/svg+xml">
<script>
(function(){try{var t=localStorage.getItem("thema");
if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}})();
</script>
</head>
<body class="%(bodyklasse)s">
<a class="sprung" href="#inhalt">Zum Inhalt springen</a>
<div class="shell">
%(rail)s
<main id="inhalt">
"""

FUSSVORLAGE = """%(blaettern)s
</main>
</div>
<script src="assets/thema.js" defer></script>
</body>
</html>
"""


def rail_fuer(slug):
    r = RAIL
    r = re.sub(r'href="#([^"]+)"', lambda m: 'href="%s"' % ziel(m.group(1), slug), r)

    def markiere(m):
        href = m.group(1)
        seite = href.split("#")[0].replace(".html", "") or slug
        if href.startswith("#"):
            seite = slug
        if seite == slug and "#" not in href:
            return '<a href="%s" aria-current="page"' % href
        return m.group(0)

    r = re.sub(r'<a href="([^"]+)"', markiere, r)
    return r


def blaettern(i):
    vor = REIHE[i - 1] if i > 0 else None
    zur = REIHE[i + 1] if i + 1 < len(REIHE) else None
    namen = {s: t for s, t, _, _ in seiten}
    teile = ['<nav class="blaettern" aria-label="Seiten">']
    if vor:
        teile.append('  <a class="zurueck" href="%s.html"><span>Zurück</span>'
                     '<b>%s</b></a>' % (vor, namen[vor]))
    else:
        teile.append('  <span></span>')
    if zur:
        teile.append('  <a class="weiter" href="%s.html"><span>Weiter</span>'
                     '<b>%s</b></a>' % (zur, namen[zur]))
    teile.append("</nav>")
    return "\n".join(teile)


# ------------------------------------------------------------------- schreiben
if os.path.isdir(DOCS):
    shutil.rmtree(DOCS)
os.makedirs(os.path.join(DOCS, "assets"))

for i, (slug, titel, k, html) in enumerate(seiten):
    html = re.sub(r'href="KARTE#([^"]+)"',
                  lambda m: 'href="%s"' % ziel(m.group(1), slug), html)
    html = html.replace('href="KARTE"', 'href="index.html"')
    html = re.sub(r'href="#([^"]+)"',
                  lambda m: 'href="%s"' % ziel(m.group(1), slug), html)
    voll = BASIS if slug == "index" else "%s · %s" % (
        re.sub(r"<[^>]+>", "", titel), BASIS)
    doc = (KOPFVORLAGE % {"titel": voll, "kurz": k.replace('"', "'"),
                          "rail": rail_fuer(slug), "bodyklasse": "s-" + slug +
                          (" fahrplan" if slug == "fahrplan" else "")}
           + html.rstrip() + "\n"
           + FUSSVORLAGE % {"blaettern": blaettern(i)})
    schreibe(os.path.join(DOCS, slug + ".html"), doc)

schreibe(os.path.join(DOCS, "assets", "karte.css"), CSS)
shutil.copyfile(os.path.join(GERUEST, "thema.js"),
                os.path.join(DOCS, "assets", "thema.js"))
shutil.copyfile(os.path.join(GERUEST, "marke.svg"),
                os.path.join(DOCS, "assets", "marke.svg"))
schreibe(os.path.join(DOCS, ".nojekyll"), "")

# --------------------------------------------------------------------- Pruefen
fehler = []
if fehlt_struktur:
    fehler.append("fehlende Strukturen: %s" % ", ".join(sorted(fehlt_struktur)))
if fehlt_tafel:
    fehler.append("fehlende Tafeln: %s" % ", ".join(sorted(fehlt_tafel)))
if doppelt:
    fehler.append("doppelte IDs: %s" % ", ".join(doppelt))
if leer:
    fehler.append("Verweise ins Leere: %s" % ", ".join(sorted(leer)))

import check_svg  # noqa: E402
if check_svg.main([os.path.join(DOCS, s + ".html") for s, _, _, _ in seiten]):
    fehler.append("HTML-Tags in inline-SVG")

for tid, tsvg in sorted(TAFELN.items()):
    treffer = sorted(set(h.lower() for h in check_svg.RX_BAD.findall(tsvg)))
    if treffer:
        fehler.append("HTML-Tags im SVG der Tafel %s: %s" % (tid, ", ".join(treffer)))

# Tag-Bilanz je Seite
for slug, _, _, _ in seiten:
    doc = lies(os.path.join(DOCS, slug + ".html"))
    ohne_svg = re.sub(r"<svg.*?</svg>", "", doc, flags=re.S)
    for tag in ("section", "article", "div", "table", "dl", "ol", "ul", "aside",
                "header", "footer", "main", "figure", "nav"):
        auf = len(re.findall(r"<%s[\s>]" % tag, ohne_svg))
        zu = len(re.findall(r"</%s>" % tag, ohne_svg))
        if auf != zu:
            fehler.append("%s.html %s: %d offen, %d geschlossen"
                          % (slug, tag, auf, zu))
    if "{{" in doc:
        fehler.append("%s.html: Platzhalter uebrig" % slug)

gesamt = sum(os.path.getsize(os.path.join(DOCS, s + ".html"))
             for s, _, _, _ in seiten)
print("geschrieben: %s" % DOCS)
print("  Seiten: %d, zusammen %d KB, groesste %d KB"
      % (len(seiten), gesamt // 1024,
         max(os.path.getsize(os.path.join(DOCS, s + ".html"))
             for s, _, _, _ in seiten) // 1024))
print("  Anker: %d" % len(anker))
if fehler:
    print("PRUEFUNG:")
    for f in fehler:
        print("  - %s" % f)
    sys.exit(1)
print("PRUEFUNG: sauber")
