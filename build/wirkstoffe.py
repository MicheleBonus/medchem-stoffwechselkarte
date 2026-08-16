# -*- coding: utf-8 -*-
"""
Zieht alle im Dokument genannten Arzneistoffe aus den Auszeichnungen
(.d, .hemm, .mol figcaption) und listet sie mit dem Abschnitt, in dem
sie stehen. Grundlage fuer das Register in Teil 9.
"""
import io
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
DOC = "\n".join(io.open(os.path.join(DOCS, p), encoding="utf-8").read()
                for p in sorted(os.listdir(DOCS)) if p.endswith(".html"))

# Position jedes Abschnitts merken, um Fundstellen zuzuordnen
marken = [(m.start(), m.group(1))
          for m in re.finditer(r'<h3 class="ast" id="a(\d+-\d+)"', DOC)]
marken += [(m.start(), "M-" + m.group(1)[1:])
           for m in re.finditer(r'<div class="tafel-kopf" id="(m\d\d)"', DOC)]
marken.sort()


def abschnitt(pos):
    letzte = "0"
    for p, name in marken:
        if p > pos:
            break
        letzte = name
    return letzte.replace("-", ".") if "-" in letzte and letzte[0].isdigit() else letzte


treffer = defaultdict(set)
for muster in (r'<span class="d">([^<]+)</span>',
               r'<span class="hemm">([^<]*?)(?:<small>|</span>)'):
    for m in re.finditer(muster, DOC):
        roh = m.group(1)
        roh = re.sub(r"^[⊣\s]+", "", roh).strip(" ,;·")
        if not roh or len(roh) > 90:
            continue
        for name in re.split(r",\s*|\s+und\s+", roh):
            name = name.strip(" ,;·()")
            if len(name) < 4 or name[0].islower():
                continue
            treffer[name].add(abschnitt(m.start()))

print("Gefundene Wirkstoffnennungen: %d" % len(treffer))
for name in sorted(treffer):
    print("%-34s %s" % (name, " · ".join(sorted(treffer[name]))))
