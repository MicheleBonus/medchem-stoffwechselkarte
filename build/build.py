# -*- coding: utf-8 -*-
"""
Setzt die Metabolitkarte aus src/*.html zusammen und ersetzt {{S:id}}
durch die in structures.json hinterlegten SVG-Strukturformeln.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(os.path.dirname(HERE), "Metabolitkarte.html")

with io.open(os.path.join(HERE, "structures.json"), encoding="utf-8") as f:
    STRUCT = json.load(f)

parts = sorted(os.listdir(SRC))
html = []
for p in parts:
    if not p.endswith(".html"):
        continue
    with io.open(os.path.join(SRC, p), encoding="utf-8") as f:
        html.append(f.read())
doc = "\n".join(html)

missing = set()


def sub(m):
    key = m.group(1).strip()
    if key not in STRUCT:
        missing.add(key)
        return ("<span class='fehlt'>[Struktur fehlt: %s]</span>" % key)
    return STRUCT[key]


doc = re.sub(r"\{\{S:([a-z0-9_]+)\}\}", sub, doc)

# Mechanismus-Tafeln, die mit mech.py gebaut wurden, liegen in tafeln.json.
TAFELN = {}
_tpfad = os.path.join(HERE, "tafeln.json")
if os.path.exists(_tpfad):
    with io.open(_tpfad, encoding="utf-8") as f:
        TAFELN = json.load(f)

fehlende_tafeln = set()


def sub_tafel(m):
    key = m.group(1).strip()
    if key not in TAFELN:
        fehlende_tafeln.add(key)
        return "<span class='fehlt'>[Tafel fehlt: %s]</span>" % key
    return TAFELN[key]


doc = re.sub(r"\{\{T:([a-z0-9_]+)\}\}", sub_tafel, doc)

# HTML-Tags in inline-SVG brechen den Fremdkontext des Parsers auf und
# schieben den Resttext als Fliesstext auf die Seite -> vor dem Schreiben pruefen.
import check_svg  # noqa: E402

if check_svg.main([os.path.join(SRC, p) for p in parts]):
    print("\nABBRUCH: HTML-Tags in inline-SVG gefunden (nur <tspan> ist zulaessig).")
    sys.exit(1)

# Die mit mech.py gebauten Tafeln stehen nicht mehr im Quelltext und wuerden
# der Pruefung oben entgehen.
for tid, tsvg in sorted(TAFELN.items()):
    treffer = sorted(set(h.lower() for h in check_svg.RX_BAD.findall(tsvg)))
    if treffer:
        print("\nABBRUCH: HTML-Tags im generierten SVG der Tafel %s: %s"
              % (tid, ", ".join(treffer)))
        sys.exit(1)

# Ein "folgt"-Badge, dessen Tafel inzwischen existiert, waere irrefuehrend.
vorhanden = set(re.findall(r'\sid="(m\d\d)"', doc))
veraltet = sorted({
    m for m in re.findall(r'class="mref pending"[^>]*>(M-\d\d)</span>', doc)
    if m.replace("-", "").lower() in vorhanden
})
if veraltet:
    print("\nABBRUCH: pending-Badges fuer bereits gebaute Tafeln: %s" % ", ".join(veraltet))
    sys.exit(1)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

used = len(re.findall(r"<svg xmlns", doc))
print("geschrieben: %s" % OUT)
print("  Groesse: %d KB" % (os.path.getsize(OUT) / 1024))
print("  Teile:   %s" % ", ".join(parts))
print("  SVGs:    %d" % used)
print("  Tafeln aus mech.py: %s" % (", ".join(sorted(TAFELN)) or "keine"))
if missing:
    print("  FEHLENDE STRUKTUREN (%d): %s" % (len(missing), ", ".join(sorted(missing))))
    sys.exit(1)
if fehlende_tafeln:
    print("  FEHLENDE TAFELN: %s" % ", ".join(sorted(fehlende_tafeln)))
    sys.exit(1)
