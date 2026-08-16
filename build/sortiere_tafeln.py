# -*- coding: utf-8 -*-
"""
Bringt die Mechanismus-Tafeln in 40_mech.html in numerische Reihenfolge.
Ein Block reicht von seinem Kommentarmarker bis zum naechsten Marker
bzw. bis zum abschliessenden .boxen-Kasten.
"""
import io
import re

P = "src/40_mech.html"
s = io.open(P, encoding="utf-8").read()

MARKER = re.compile(r"[ \t]*<!-- =+ (M-\d\d) -->\n")
stellen = [(m.start(), m.group(1)) for m in MARKER.finditer(s)]
if not stellen:
    raise SystemExit("keine Tafelmarker gefunden")

# Ende des letzten Blocks: der abschliessende Kasten
ende = s.index('<div class="boxen">', stellen[-1][0])

kopf = s[:stellen[0][0]]
fuss = s[ende:]

bloecke = []
for i, (pos, name) in enumerate(stellen):
    schluss = stellen[i + 1][0] if i + 1 < len(stellen) else ende
    bloecke.append((name, s[pos:schluss]))

vorher = [n for n, _ in bloecke]
bloecke.sort(key=lambda b: int(b[0][2:]))
nachher = [n for n, _ in bloecke]

io.open(P, "w", encoding="utf-8").write(kopf + "".join(b for _, b in bloecke) + fuss)

print("vorher: %s" % " ".join(vorher))
print("nachher: %s" % " ".join(nachher))
print("Tafeln: %d" % len(bloecke))
