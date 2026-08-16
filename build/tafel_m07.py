# -*- coding: utf-8 -*-
"""
M-07 · Nicotinamid-Coenzyme, gebaut mit mech.py.

Die letzte der elf neu gezeichneten Tafeln. Zone B nutzt dieselben raeumlichen
Mittel wie M-01: Die beiden Wasserstoffatome am sp3-C4 werden als Keil und
Strichkeil gezeichnet - anders laesst sich pro-R gegen pro-S nicht zeigen.
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

NADOX = "NC(=O)c1ccc[n+](*)c1"
NADRED = "NC(=O)C1=CN(*)C=CC1"

t = mech.Tafel(1000, 1320)

# ===================================================== ZONE A · Hydridtransfer
t.zone(24, "A · DAS HYDRID GEHT AN C4")
t.text(20, 54, "Gezeigt ist die Lactat-Dehydrogenase. Das Substrat gibt ein Hydrid ab, der "
               "Pyridiniumring nimmt es auf — beides in einem einzigen Schritt, ohne "
               "Zwischenstufe.", size=12.5)

lac = mech.Molekuel("CC(O)C(=O)[O-]", 132, 208, wasserstoff=[1], zeige={2: "oben"},
                    name="Lactat")
t.mole.append(lac)
hl = lac.h_index[1]
lp_o = t.elektronenpaar(lac, 2, 300)
t.pfeil(lp_o, lac.aussen(1, 2, abstand=24), bogen=0.40, seite=1, farbe=W)
t.unterschrift(lac, "L-Lactat — das Proton der OH-Gruppe", "nimmt ein Histidin des Enzyms auf",
               abstand=30)

nad = mech.Molekuel(NADOX, 400, 208, labels={8: "Ribose-ADP"}, zeige={4: "links"},
                    name="NAD+")
t.mole.append(nad)
t.pfeil((lac, 1, hl), (nad, 4), bogen=0.24, seite=-1, farbe=W)
t.atomnummer(nad, 4, "C4", winkel=180, abstand=46, size=10.5, farbe=W, gewicht=700)
t.unterschrift(nad, "NAD&#8314; — aromatisch und elektronenarm,", "deshalb nimmt C4 das Hydrid auf",
               abstand=30)

t.reaktionspfeil(516, 208, 584)
t.text(550, 196, "ein Schritt", size=10, anchor="middle", farbe=G)

pyr = mech.Molekuel("CC(=O)C(=O)[O-]", 656, 208, zeige={1: "links"}, name="Pyruvat")
t.mole.append(pyr)
t.unterschrift(pyr, "Pyruvat", abstand=28, farbe=G)

nadh = mech.Molekuel(NADRED, 866, 208, labels={6: "Ribose-ADP"}, zeige={9: "links"},
                     name="NADH")
t.mole.append(nadh)
t.unterschrift(nadh, "NADH — C4 ist jetzt sp&#179;,", "die Ladung ist neutralisiert", abstand=30)

t.kasten(20, 300, 960, 76, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 322, "DER UNTERSCHIED ZUM FLAVIN", size=11, gewicht=700, farbe=C)
t.text(38, 344, "Das Nicotinamid bewegt zwei Elektronen auf einmal; eine stabile Zwischenstufe mit "
                "einem ungepaarten Elektron gibt es nicht. Deshalb kann NADH nicht", size=12.5)
t.text(38, 363, "mit Sauerstoff reagieren — das Flavin dagegen schon (Tafel M-06). Aus demselben "
                "Grund erzeugen NAD-abhängige Dehydrogenasen keinen oxidativen Stress.", size=12.5)

# ===================================================== ZONE B · Stereospezifitaet
t.zone(414, "B · JEDES ENZYM WÄHLT EINE SEITE")
t.text(20, 444, "Am sp&#179;-hybridisierten C4 sitzen zwei Wasserstoffatome. Chemisch sind sie "
                "gleich, räumlich nicht: Das eine steht über, das andere unter der Ringebene.",
       size=12.5)
t.text(20, 463, "Jede Dehydrogenase überträgt stets dasselbe von beiden.", size=12.5)

nadh2 = mech.Molekuel(NADRED, 200, 590, labels={6: "Ribose-ADP"}, zeige={9: "oben"},
                      name="NADH")
t.mole.append(nadh2)
cx, cy = nadh2.atom(9)
t.keil(cx, cy, cx - 30, cy - 34, breite=7.5, farbe=E)
t.text(cx - 34, cy - 42, "H<tspan baseline-shift='sub' font-size='8'>A</tspan> · pro-<tspan "
       "font-style='italic'>R</tspan>", size=11, anchor="end", gewicht=700, farbe=E)
t.strichkeil(cx, cy, cx + 30, cy - 34, breite=7.0)
t.text(cx + 34, cy - 42, "H<tspan baseline-shift='sub' font-size='8'>B</tspan> · pro-<tspan "
       "font-style='italic'>S</tspan>", size=11, gewicht=700, farbe=R)
t.ebene(cx, cy + 30, breite=150, tiefe=34, farbe=G, beschriftung="Ringebene")
t.unterschrift(nadh2, "dasselbe C4, von der Seite gesehen", abstand=64)

t.text(430, 512, "A-Seite — das pro-<tspan font-style='italic'>R</tspan>-Wasserstoffatom",
       size=12.5, gewicht=700, farbe=E)
t.text(430, 534, "Alkohol-Dehydrogenase · Lactat-Dehydrogenase · Malat-Dehydrogenase", size=12)

t.text(430, 570, "B-Seite — das pro-<tspan font-style='italic'>S</tspan>-Wasserstoffatom",
       size=12.5, gewicht=700, farbe=R)
t.text(430, 592, "Glutamat-Dehydrogenase · GAPDH · Glucose-6-phosphat-Dehydrogenase", size=12)

t.kasten(430, 616, 550, 96, fill="var(--surface-2)")
t.text(448, 638, "WIE MAN DAS GEZEIGT HAT", size=11, gewicht=700, farbe=G)
t.text(448, 660, "Mit deuteriertem Substrat. Das eingebaute Deuterium erscheint bei jedem", size=12.5)
t.text(448, 679, "Enzym reproduzierbar an derselben Position — ein Beleg dafür, dass das", size=12.5)
t.text(448, 698, "Coenzym im aktiven Zentrum in fester Orientierung gebunden wird.", size=12.5)

# ===================================================== ZONE C · NAD gegen NADP
t.zone(766, "C · EINE PHOSPHATGRUPPE TRENNT ZWEI STOFFWECHSELWELTEN")
t.text(20, 796, "NADP&#8314; unterscheidet sich von NAD&#8314; an genau einer Stelle: einer "
                "Phosphatgruppe an der 2&#8242;-Position der Adenosin-Ribose.", size=12.5)

rib = mech.Molekuel("*OC[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O", 180, 918,
                    labels={0: "P", 6: "Adenin"}, zeige={8: "unten"}, name="NAD-Ribose")
t.mole.append(rib)
t.unterschrift(rib, "NAD&#8314; — hier steht eine freie OH-Gruppe", abstand=30, farbe=E)

ribp = mech.Molekuel("*OC[C@H]1O[C@@H](*)[C@H](OP(=O)([O-])[O-])[C@@H]1O", 560, 918,
                     labels={0: "P", 6: "Adenin"}, zeige={8: "unten"}, name="NADP-Ribose")
t.mole.append(ribp)
t.unterschrift(ribp, "NADP&#8314; — und hier ein Phosphat", abstand=30, farbe=R)

t.kasten(760, 852, 220, 132, fill="var(--surface-2)")
t.text(778, 874, "KEINE CHEMIE,", size=11, gewicht=700, farbe=G)
t.text(778, 890, "NUR EIN KENNZEICHEN", size=11, gewicht=700, farbe=G)
t.text(778, 914, "Die Phosphatgruppe greift", size=12)
t.text(778, 933, "nicht in die Reaktion ein.", size=12)
t.text(778, 956, "Sie sagt dem Enzym nur,", size=12)
t.text(778, 975, "welchen Pool es benutzt.", size=12)

# ===================================================== ZONE D · die zwei Pools
t.zone(1042, "D · WARUM DAS ZWEI GETRENNTE POOLS ERGIBT")

t.kasten(20, 1074, 470, 118, fill="var(--enzym-bg)", stroke=E)
t.text(38, 1096, "NAD&#8314; — DER ABBAU", size=11, gewicht=700, farbe=E)
t.text(38, 1118, "Liegt zu etwa 700 : 1 oxidiert vor. Ein so hoher", size=12.5)
t.text(38, 1137, "Überschuss an Oxidationsmittel zieht jede", size=12.5)
t.text(38, 1156, "Dehydrogenase in Richtung Oxidation: Glykolyse,", size=12.5)
t.text(38, 1175, "β-Oxidation, Citratzyklus.", size=12.5)

t.kasten(510, 1074, 470, 118, fill="var(--drug-bg)", stroke=R)
t.text(528, 1096, "NADPH — DER AUFBAU", size=11, gewicht=700, farbe=R)
t.text(528, 1118, "Liegt zu etwa 75 : 1 reduziert vor. Der Überschuss", size=12.5)
t.text(528, 1137, "an Reduktionsmittel treibt die Fettsäure- und", size=12.5)
t.text(528, 1156, "Steroidsynthese, die Glutathionreduktase und die", size=12.5)
t.text(528, 1175, "Monooxygenasen aus Tafel M-08.", size=12.5)

t.kasten(20, 1216, 960, 76, fill="var(--warn-bg)", stroke=W)
t.text(38, 1238, "DAS EIGENTLICH BEMERKENSWERTE", size=11, gewicht=700, farbe=W)
t.text(38, 1260, "Beide Pools liegen im selben Zellkompartiment nebeneinander, ohne sich zu "
                 "vermischen. Möglich ist das nur, weil jedes Enzym über die eine", size=12.5)
t.text(38, 1279, "Phosphatgruppe entscheidet, welches der beiden Coenzyme es bindet. Ein "
                 "Erkennungsmerkmal ersetzt hier eine Membran.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Nicotinamid-Coenzyme in vier Zonen. Zone A zeigt am Beispiel der Lactat-Dehydrogenase den "
    "Hydridtransfer: Das freie Elektronenpaar der Hydroxylgruppe bildet die Doppelbindung zum "
    "Sauerstoff, und gleichzeitig wandert das Wasserstoffatom als Hydrid an das Kohlenstoffatom "
    "vier des Pyridiniumrings. Es entstehen Pyruvat und NADH, dessen C4 nun sp3-hybridisiert "
    "ist. Zone B zeigt die Stereospezifitaet raeumlich: Die beiden Wasserstoffatome am C4 sind "
    "als Keil und als Strichkeil gezeichnet, das eine ueber, das andere unter der als Flaeche "
    "dargestellten Ringebene; jede Dehydrogenase uebertraegt stets dasselbe von beiden. Zone C "
    "zeigt den einzigen strukturellen Unterschied zwischen NAD und NADP: eine Phosphatgruppe an "
    "der 2-Strich-Position der Adenosin-Ribose. Zone D erklaert, warum daraus zwei getrennte "
    "Redoxpools entstehen."
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
daten["m07"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m07  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m07"]), len(t.mole), len(t.anker)))
