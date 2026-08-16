# -*- coding: utf-8 -*-
"""
Sucht HTML-Tags innerhalb von inline-SVG.

Hintergrund: Der HTML-Parser verlaesst den SVG-Fremdkontext, sobald eines
bestimmter HTML-Tags auftaucht (i, b, sub, span, p, br ...). Das SVG wird dann
mitten im Baum geschlossen und der Resttext landet als Fliesstext auf der Seite.
Innerhalb von <svg> darf nur <tspan> zur Textauszeichnung verwendet werden.
"""
import glob
import io
import re
import sys

BREAKOUT = (r"i|b|em|strong|sub|sup|small|span|p|div|br|u|s|code|var|font|big|"
            r"nobr|tt|center|li|ul|ol|dl|dd|dt|h[1-6]|hr|img|pre|table|ruby|"
            r"listing|menu|embed|meta|head|body|blockquote")

RX_SVG = re.compile(r"<svg\b.*?</svg>", re.S)
RX_BAD = re.compile(r"</?(" + BREAKOUT + r")(?:\s[^>]*?)?/?>", re.I)


def main(paths):
    total = 0
    for f in sorted(paths):
        s = io.open(f, encoding="utf-8").read()
        for m in RX_SVG.finditer(s):
            blk = m.group(0)
            hits = RX_BAD.findall(blk)
            if not hits:
                continue
            zeile = s[:m.start()].count("\n") + 1
            tags = sorted(set(h.lower() for h in hits))
            print("%-20s SVG ab Zeile %-5d  Tags: %s  (%d Treffer)"
                  % (f.replace("\\", "/").split("/")[-1], zeile, ", ".join(tags), len(hits)))
            for bm in RX_BAD.finditer(blk):
                a = max(0, bm.start() - 60)
                schnipsel = " ".join(blk[a:bm.end() + 40].split())
                print("      ...%s..." % schnipsel)
            total += len(hits)
    print("\nGesamt: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or glob.glob("src/*.html")))
