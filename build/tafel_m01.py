# -*- coding: utf-8 -*-
"""
M-01 · Pyridoxal-5'-phosphat, gebaut mit mech.py.

Die meistgefragte Tafel. Der Kern ist eine raeumliche Aussage - die Dunathan-Regel -,
und die laesst sich in einer Strichzeichnung nur zeigen, wenn die Ebene selbst
gezeichnet wird. Zone B tut das mit drei Schraegansichten des Cα.
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech

HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HERE, "tafeln.json")

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1500)

PLP = "Cc1[nH+]cc(COP(=O)([O-])[O-])c(%s)c1[O-]"

# ===================================================== ZONE A · Transaldiminierung
t.zone(24, "A · TRANSALDIMINIERUNG — DER COFAKTOR WECHSELT DEN PARTNER")
t.text(20, 54, "Im Ruhezustand hängt PLP als Schiffsche Base an einem Lysin des Enzyms. Das "
               "Substrat verdrängt das Lysin, ohne dass der Cofaktor je frei wird.", size=12.5)

intern = mech.Molekuel(PLP % "/C=N/*", 176, 190, labels={14: "Lys"},
                       zeige={2: "unten", 13: "oben"}, name="internes Aldimin")
t.mole.append(intern)
t.unterschrift(intern, "internes Aldimin — Ruhezustand des Enzyms")

t.reaktionspfeil(330, 190, 402)
t.text(366, 178, "+ Substrat", size=10.5, anchor="middle", gewicht=700, farbe=E)
t.text(366, 208, "&#8722; Lysin", size=10.5, anchor="middle", farbe=G)

extern = mech.Molekuel(PLP % "/C=N/[C@@H](*)C(=O)[O-]", 570, 190, labels={15: "R"},
                       zeige={2: "unten", 13: "oben"}, name="externes Aldimin")
t.mole.append(extern)
t.atomnummer(extern, 14, "C&#945;", winkel=250, abstand=28, size=10.5, farbe=W, gewicht=700)
t.unterschrift(extern, "externes Aldimin — drei Bindungen am C&#945; stehen zur Wahl")

t.kasten(760, 96, 220, 166, fill="var(--cofaktor-bg)", stroke=C)
t.text(778, 118, "DAS PRINZIP", size=11, gewicht=700, farbe=C)
t.text(778, 140, "Jede Spaltung am C&#945; erzeugt", size=12)
t.text(778, 159, "ein Carbanion. Allein wäre es", size=12)
t.text(778, 178, "nicht haltbar; das konjugierte", size=12)
t.text(778, 197, "System schiebt die Ladung bis", size=12)
t.text(778, 216, "zum protonierten Ring-Stick-", size=12)
t.text(778, 235, "stoff, der sie aufnimmt.", size=12)
t.text(778, 256, "Ohne das ⊕ am Ring-N geht nichts.", size=10.5, farbe=C)

# ===================================================== ZONE B · Dunathan
t.zone(322, "B · DIE DUNATHAN-REGEL — DAS ENZYM WÄHLT DIE BINDUNG")
t.text(20, 352, "Gebrochen wird die Bindung, die das Enzym senkrecht zur π-Ebene des Aldimins "
                "stellt: nur sie überlappt mit dem konjugierten System. Die drei "
                "Ansichten unten", size=12.5)
t.text(20, 371, "zeigen dasselbe C&#945; aus derselben Richtung — gedreht wird nur die "
                "Konformation, die das jeweilige Apoenzym erzwingt.", size=12.5)

DUNATHAN = [
    (170, "&#9312;", "COO&#8315;", "H", "R", "Decarboxylase", "biogenes Amin"),
    (500, "&#9313;", "H", "COO&#8315;", "R", "Transaminase", "&#945;-Ketosäure"),
    (830, "&#9314;", "H", "COO&#8315;", "R", "&#946;-Eliminase", "Aminoacrylat"),
]
for cx, nr, senkrecht, links, rechts, enzym, produkt in DUNATHAN:
    cy = 470.0
    t.text(cx, 404, "%s  %s steht senkrecht" % (nr, senkrecht), size=11.5, anchor="middle",
           gewicht=700, farbe=W)
    t.ebene(cx, cy, breite=132, tiefe=40, beschriftung="π-Ebene")
    # die beiden Bindungen in der Ebene
    t.linie(cx, cy, cx - 46, cy + 15, breite=1.6)
    t.text(cx - 52, cy + 26, links, size=10.5, anchor="end")
    t.linie(cx, cy, cx + 42, cy - 14, breite=1.6)
    t.text(cx + 48, cy - 16, rechts, size=10.5)
    # die dritte Bindung steht heraus - genau sie bricht
    t.keil(cx, cy, cx, cy - 44, breite=7.5, farbe=W)
    t.text(cx, cy - 52, senkrecht, size=11.5, anchor="middle", gewicht=700, farbe=W)
    # nach unten die Bindung zum Stickstoff des Aldimins
    t.strichkeil(cx, cy, cx - 6, cy + 42, breite=6.5)
    t.text(cx - 8, cy + 56, "N=C4&#8242;", size=10, anchor="middle", farbe=G)
    t.text(cx, cy + 84, enzym, size=11, anchor="middle", gewicht=700, farbe=E)
    t.text(cx, cy + 99, "&#8594; " + produkt, size=10.5, anchor="middle", farbe=G)

t.text(500, 596, "Der Cofaktor ist in allen drei Fällen derselbe. Verschieden ist allein, "
                 "wie das Apoenzym das Substrat verdreht festhält.", size=12,
       anchor="middle", farbe=G)

# ===================================================== ZONE C · das Chinoid
t.zone(636, "C · DAS CHINOID — ALLE DREI WEGE LAUFEN ÜBER DIESELBE ZWISCHENSTUFE")
t.text(20, 666, "Was auch immer am C&#945; abgeht: Es bleibt ein Carbanion zurück, dessen Ladung "
                "über das konjugierte System bis zum Ring-Stickstoff wandert.", size=12.5)

chin = mech.Molekuel(PLP % "/C=N/[CH-]*", 210, 800, labels={15: "R"},
                     zeige={2: "unten", 13: "oben"}, name="Chinoid")
t.mole.append(chin)
# Beide Pfeile laufen aussen am Geruest entlang. Der erste zeigt den Schritt,
# der zweite fasst die Weiterleitung ueber den Ring gestrichelt zusammen.
lp = t.elektronenpaar(chin, 14, 25)
t.pfeil(lp, chin.aussen(13, 14, abstand=26), bogen=0.40, seite=1, farbe=W)
t.pfeil(chin.aussen(12, abstand=28), chin.aussen(2, abstand=30),
        bogen=0.55, seite=-1, farbe=W, strich="5 3")
# Die Pfeile laufen rechts aussen vorbei; die Beschriftung geht nach links.
t.atomnummer(chin, 14, "C&#945;", winkel=265, abstand=32, size=10.5, farbe=W, gewicht=700)
t.text(300, 758, "&#9312; das Paar bildet", size=10.5, farbe=W, gewicht=700)
t.text(300, 773, "die C&#945;=N-Bindung", size=10.5, farbe=W)
t.text(300, 806, "&#9313; weiter über C4&#8242;", size=10.5, farbe=W, gewicht=700)
t.text(300, 821, "und den Ring bis N1", size=10.5, farbe=W)
t.unterschrift(chin, "Chinoid — hier als Carbanion-Grenzstruktur gezeichnet;",
               "der gestrichelte Pfeil fasst die Delokalisierung über den Ring zusammen")

WEGE = [
    (742, "&#9312; Decarboxylierung", W,
     ["Nach Abgang von CO&#8322; nimmt das C&#945; ein Proton auf.",
      "Produkt: das biogene Amin, PLP wird frei."],
     "AADC · GAD · HDC · ODC",
     "Carbidopa und Benserazid (AADC) · Eflornithin (ODC)"),
    (872, "&#9313; Transaminierung", W,
     ["Das Proton geht ans C4&#8242;, es entsteht das Ketimin.",
      "Die Aminogruppe bleibt als PMP am Cofaktor."],
     "AST (GOT) · ALT (GPT) · GABA-Transaminase",
     "Vigabatrin — Suizidsubstrat der GABA-Transaminase"),
    (1002, "&#9314; &#946;-Eliminierung und &#946;-Ersatz", W,
     ["Vom C&#946; geht eine Fluchtgruppe ab, es entsteht",
      "Aminoacrylat als gemeinsame Zwischenstufe."],
     "Cystathionin-&#946;-Synthase · Serin-Dehydratase",
     "Homocystein-Stau bei B&#8326;-Mangel"),
]
for y, titel, farbe, zeilen, enzyme, stoffe in WEGE:
    t.text(470, y, titel, size=12.5, gewicht=700, farbe=farbe)
    for i, z in enumerate(zeilen):
        t.text(470, y + 21 + i * 18, z, size=12)
    t.text(470, y + 21 + len(zeilen) * 18, enzyme, size=11, gewicht=700, farbe=E)
    t.text(470, y + 38 + len(zeilen) * 18, stoffe, size=11, farbe=R)

# ===================================================== ZONE D · Hemmstoffe
t.zone(1120, "D · WIE ARZNEISTOFFE HIER ANGREIFEN")
t.text(20, 1152, "Zwei ganz verschiedene Prinzipien, beide am selben Cofaktor.", size=12.5)

t.kasten(20, 1180, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(38, 1202, "DEN COFAKTOR ABFANGEN", size=11, gewicht=700, farbe=R)
t.text(38, 1224, "Carbidopa und Benserazid tragen eine Hydrazino-", size=12.5)
t.text(38, 1243, "Gruppe. Sie bilden mit dem Aldehyd des PLP ein", size=12.5)
t.text(38, 1262, "stabiles Hydrazon und verhindern damit schon die", size=12.5)
t.text(38, 1281, "Bildung des internen Aldimins.", size=12.5)
t.text(38, 1304, "Isoniazid tut chemisch dasselbe, aber im ganzen", size=12.5)
t.text(38, 1323, "Körper — daher die Polyneuropathie.", size=12.5)

t.kasten(510, 1180, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(528, 1202, "DEN MECHANISMUS MISSBRAUCHEN", size=11, gewicht=700, farbe=R)
t.text(528, 1224, "Vigabatrin ist ein echtes Suizidsubstrat: Es durch-", size=12.5)
t.text(528, 1243, "läuft den Mechanismus bis zum Chinoid und alkyliert", size=12.5)
t.text(528, 1262, "erst dann das Enzym kovalent.", size=12.5)
t.text(528, 1285, "Prüfungsfalle: Vigabatrin hemmt die GABA-Trans-", size=12.5)
t.text(528, 1304, "aminase, also den Abbau — nicht die Decarboxylase,", size=12.5)
t.text(528, 1323, "also nicht den Aufbau.", size=12.5)

t.kasten(20, 1354, 960, 76, fill="var(--surface-2)")
t.text(38, 1376, "WARUM PLP IN SO VIELEN KAPITELN AUFTAUCHT", size=11, gewicht=700, farbe=G)
t.text(38, 1398, "Vierzehn Enzyme dieser Unterlage arbeiten mit PLP: die Decarboxylasen aller "
                 "biogenen Amine, die Transaminasen, die GABA-Transaminase, die", size=12.5)
t.text(38, 1417, "Cystathionin-&#946;-Synthase, die &#948;-Aminolävulinat-Synthase der Häm-Synthese "
                 "und die Serin-Hydroxymethyltransferase des C&#8321;-Stoffwechsels.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Pyridoxalphosphat in vier Zonen. Zone A zeigt die Transaldiminierung: Das interne Aldimin "
    "mit einem Lysin des Enzyms wird durch das Substrat zum externen Aldimin. Zone B zeigt die "
    "Dunathan-Regel in drei Schraegansichten: Die pi-Ebene des Aldimins ist als Parallelogramm "
    "gezeichnet, das Alpha-Kohlenstoffatom liegt darin, und jeweils eine seiner drei Bindungen "
    "steht als Keil senkrecht auf der Ebene - bei der Decarboxylase die Carboxylatgruppe, bei "
    "der Transaminase und der Beta-Eliminase das Wasserstoffatom. Nur die senkrechte Bindung "
    "bricht. Zone C zeigt das Chinoid als Carbanion-Grenzstruktur mit Elektronenpfeilen, die "
    "die Ladung ueber die Kohlenstoff-Stickstoff-Doppelbindung bis zum protonierten "
    "Ring-Stickstoff schieben, und daneben die drei Reaktionswege mit Enzymen und Arzneistoffen. "
    "Zone D nennt die beiden Hemmprinzipien: Hydrazine fangen den Cofaktor ab, Vigabatrin "
    "missbraucht den Mechanismus als Suizidsubstrat."
)

fehler, bericht = t.pruefe()
print("Pfeilanker:")
for z in bericht:
    print(z)
if fehler:
    print("FEHLER:")
    for f in fehler:
        print("  - %s" % f)
    raise SystemExit(1)

for m in t.mole:
    x0, y0, x1, y1 = m.rand()
    if x0 < 10 or y0 < 10 or x1 > t.b - 10 or y1 > t.h - 10:
        print("WARNUNG: %s reicht bis (%.0f,%.0f)-(%.0f,%.0f)" % (m.name, x0, y0, x1, y1))

daten = {}
if os.path.exists(ZIEL):
    daten = json.load(io.open(ZIEL, encoding="utf-8"))
daten["m01"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m01  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m01"]), len(t.mole), len(t.anker)))
