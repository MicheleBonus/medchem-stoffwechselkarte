# -*- coding: utf-8 -*-
"""
Ersetzt das handgesetzte SVG einer Mechanismus-Tafel durch den Platzhalter
{{T:id}}, sodass build.py die mit mech.py gebaute Fassung einsetzt.

    python einsetzen.py m08
"""
import io
import re
import sys

P = "src/40_mech.html"
TID = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
if not re.match(r"^m\d\d$", TID):
    raise SystemExit("Aufruf: python einsetzen.py m08")

NR = "M-%s" % TID[1:]
NACH = "M-%02d" % (int(TID[1:]) + 1)

s = io.open(P, encoding="utf-8").read()
marke = "<!-- =============================================================== %s -->"
start = s.index(marke % NR)
try:
    ende = s.index(marke % NACH)
except ValueError:                       # letzte Tafel: bis zum Abschlusskasten
    ende = s.index('<div class="boxen">', start)
block = s[start:ende]

if "{{T:%s}}" % TID in block:
    raise SystemExit("%s ist bereits ersetzt" % NR)

svg0 = block.index("<svg ")
svg1 = block.index("</svg>") + len("</svg>")
alt = block[svg0:svg1]
neu = block[:svg0] + "{{T:%s}}" % TID + block[svg1:]

io.open(P, "w", encoding="utf-8").write(s[:start] + neu + s[ende:])
print("%s: %d Zeichen handgesetztes SVG durch {{T:%s}} ersetzt" % (NR, len(alt), TID))
