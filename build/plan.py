# -*- coding: utf-8 -*-
"""
Baut Lernfahrplan.html aus src_plan/*.html.

Der Platzhalter KARTE in href-Attributen wird durch die URL der grossen
Stoffwechselkarte ersetzt, damit die Paragraphen- und Tafelverweise im
veroeffentlichten Artefakt funktionieren.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_plan")
OUT = os.path.join(os.path.dirname(HERE), "Lernfahrplan.html")

KARTE = "https://claude.ai/code/artifact/53e45c5f-230e-4352-823c-d7d48ce2d19f"

parts = sorted(p for p in os.listdir(SRC) if p.endswith(".html"))
doc = "\n".join(io.open(os.path.join(SRC, p), encoding="utf-8").read() for p in parts)

doc = doc.replace('href="KARTE#', 'href="%s#' % KARTE)
doc = doc.replace('href="KARTE"', 'href="%s"' % KARTE)

fehler = []

# --- Platzhalter vollstaendig ersetzt?
rest = re.findall(r"KARTE", doc)
if rest:
    fehler.append("KARTE-Platzhalter uebrig: %d" % len(rest))

# --- doppelte IDs
ids = re.findall(r'\sid="([^"]+)"', doc)
dopp = sorted({i for i in ids if ids.count(i) > 1})
if dopp:
    fehler.append("doppelte IDs: %s" % ", ".join(dopp))

# --- tote interne Anker
intern = set(re.findall(r'href="#([^"]+)"', doc))
tot = sorted(intern - set(ids))
if tot:
    fehler.append("tote Anker: %s" % ", ".join(tot))

# --- Tag-Bilanz der Blockelemente
for tag in ("section", "article", "div", "table", "dl", "ol", "ul", "aside",
            "header", "footer", "main", "figure"):
    auf = len(re.findall(r"<%s[\s>]" % tag, doc))
    zu = len(re.findall(r"</%s>" % tag, doc))
    if auf != zu:
        fehler.append("%s: %d offen, %d geschlossen" % (tag, auf, zu))

# --- Karte-Anker gegen die gebaute Karte pruefen
karte = os.path.join(os.path.dirname(HERE), "Metabolitkarte.html")
if os.path.exists(karte):
    khtml = io.open(karte, encoding="utf-8").read()
    kids = set(re.findall(r'\sid="([^"]+)"', khtml))
    verwiesen = set(re.findall(re.escape(KARTE) + r"#([a-z0-9\-]+)", doc))
    fehlend = sorted(verwiesen - kids)
    if fehlend:
        fehler.append("Verweise ins Leere der Karte: %s" % ", ".join(fehlend))
else:
    fehler.append("Metabolitkarte.html nicht gefunden - Querverweise ungeprueft")

# --- AI-Tropes, die der Nutzer beanstandet hat
TROPES = [
    (r"nicht nur[^.]{0,60}, sondern auch", "nicht nur/sondern auch"),
    (r"\bDas ist (der|die|das) [A-Z]", "Das ist ..."),
    (r"\bes geht (nicht )?darum\b", "es geht darum"),
    (r"\b(spektakul|bemerkenswert|faszinier|erstaunlich)", "Superlativ"),
    (r"\bStellen Sie sich vor\b", "Leseransprache"),
]
for muster, name in TROPES:
    tr = re.findall(muster, doc, re.IGNORECASE)
    if tr:
        fehler.append("Formulierung '%s': %dx" % (name, len(tr)))

if fehler:
    print("PRUEFUNG:")
    for f in fehler:
        print("  - %s" % f)
else:
    print("PRUEFUNG: sauber")

io.open(OUT, "w", encoding="utf-8").write(doc)
print("geschrieben: %s (%d KB, %d Teile)"
      % (OUT, len(doc.encode("utf-8")) // 1024, len(parts)))

if fehler:
    sys.exit(1)
