# -*- coding: utf-8 -*-
"""
M-13 · 5-Lipoxygenase, gebaut mit mech.py.

Dasselbe Muster wie M-12: Abstraktion an einer doppelt allylischen Methylen-
gruppe, Sauerstoff von der Gegenseite. Nur zuendet hier ein Eisen statt eines
Tyrosinrests. Das Eisen traegt keinen Makrocyclus, also ebene=False.

Alle drei Kettenfragmente halten beide Enden ueber zeige= fest (C4 links, C11
rechts), damit dasselbe Atom von Bild zu Bild an derselben Stelle steht.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1260)

# ===================================================== ZONE A · erster Durchgang
t.zone(24, "A · ERSTER DURCHGANG: AUS DER FETTSÄURE WIRD EIN HYDROPEROXID")
t.text(20, 54, "Gezeigt ist der Ausschnitt C4 bis C11 der Arachidonsäure, beide Doppelbindungen in "
               "ihrer wirklichen <tspan font-style='italic'>cis</tspan>-Form. Das C7 zwischen "
               "ihnen ist doppelt", size=12.5)
t.text(20, 73, "allylisch, dort sitzt das schwächste Wasserstoffatom.", size=12.5)

zfe = t.zentrum(96, 200, "Fe(III)", axial=["OH"], unten="", ebene=False, schritt=46,
                name="Nicht-Häm-Eisen")
t.text(96, 256, "Fe(III)&#8722;OH", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(96, 272, "nur diese Form ist aktiv", size=10.5, anchor="middle", farbe=G)

# Beide Doppelbindungen des Ausschnitts sind cis (5Z, 8Z). Ohne die Richtungsangaben
# zeichnete RDKit sie all-trans, und der Satz von der cis-Geometrie stuende dann im
# Widerspruch zum eigenen Bild.
frag = mech.Molekuel(r"*/C=C\C/C=C\C*", 300, 176, labels={0: "C4", 7: "C11"},
                     wasserstoff=[3], zeige={0: "links", 7: "rechts"},
                     name="Arachidonsäure")
t.mole.append(frag)
hf = frag.h_index[3]
# Der Weg zum Eisen fuehrt oberhalb der Kette entlang. Unten liegt das C4-Ende im
# Weg, und ein Pfeil, der quer durch die C5=C6-Doppelbindung laeuft, waere nicht
# zu lesen.
t.pfeil((frag, 3, hf), zfe.ax(0, winkel=20, abstand=24), bogen=0.24, seite=1,
        typ="fischhaken", farbe=R)
t.pfeil((frag, 3, hf), frag.abseits(3, hf, 22), bogen=0.45, seite=1, typ="fischhaken",
        farbe=R)
t.atomnummer(frag, 3, "C7", winkel=260, abstand=28, size=10, farbe=R, gewicht=700)
t.unterschrift(frag, "das Radikal delokalisiert anschließend über C5 bis C9",
               abstand=32)

t.reaktionspfeil(420, 176, 494)
t.text(457, 164, "+ O&#8322; an C5", size=10.5, anchor="middle", gewicht=700, farbe=E)
t.text(457, 198, "von der Gegenseite", size=10, anchor="middle", farbe=G)

# 5-HPETE ist 5S-Hydroperoxy-6E,8Z. Der Keil am C5 traegt die 5S-Konfiguration,
# Delta-6 ist E, Delta-8 bleibt Z wie im Substrat.
hpete = mech.Molekuel(r"*[C@H](OO)/C=C/C=C\C*", 640, 176, labels={0: "C4", 9: "C11"},
                      zeige={0: "links", 9: "rechts"}, name="5-HPETE")
t.mole.append(hpete)
t.atomnummer(hpete, 1, "C5", winkel=45, abstand=30, size=10, farbe=W, gewicht=700)
t.unterschrift(hpete, "5-HPETE: das Hydroperoxid steht 5<tspan font-style='italic'>S</tspan>, "
                      "die Δ5-Doppelbindung ist",
               "nach Δ6 gewandert und dabei von <tspan font-style='italic'>Z</tspan> nach "
               "<tspan font-style='italic'>E</tspan> umgeschlagen", abstand=32)

t.kasten(20, 320, 470, 116, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 342, "DAS EISEN PENDELT ZWISCHEN ZWEI STUFEN", size=11, gewicht=700, farbe=C)
t.text(38, 364, "Fe(III)&#8722;OH nimmt das Wasserstoffatom auf und wird zu "
                "Fe(II)&#8722;OH&#8322;. Am Ende gibt es das", size=12.5)
t.text(38, 383, "Elektron an das Peroxylradikal ab und liegt wieder als Fe(III)", size=12.5)
t.text(38, 402, "vor. Nur diese Form ist katalytisch aktiv.", size=12.5)

t.kasten(510, 320, 470, 116, fill="var(--surface-2)")
t.text(528, 342, "DER VERGLEICH MIT DER CYCLOOXYGENASE", size=11, gewicht=700, farbe=G)
t.text(528, 364, "Beide Enzyme starten gleich: Abstraktion an einer doppelt", size=12.5)
t.text(528, 383, "allylischen Methylengruppe, Sauerstoff von der Gegenseite. Nur", size=12.5)
t.text(528, 402, "zündet die COX mit einem Tyrosylradikal (Tafel M-12).", size=12.5)

# ===================================================== ZONE B · zweiter Durchgang
t.zone(472, "B · ZWEITER DURCHGANG: DASSELBE ENZYM MACHT EIN EPOXID DARAUS")
t.text(20, 502, "Die 5-LOX lässt das Hydroperoxid nicht los. Sie abstrahiert nun ein "
                "Wasserstoffatom vom C10 und spaltet Wasser ab; zwischen C5 und C6 schließt "
                "sich ein Epoxid.", size=12.5)

hpete2 = mech.Molekuel(r"*[C@H](OO)/C=C/C=C\C*", 200, 596, labels={0: "C4", 9: "C11"},
                       zeige={0: "links", 9: "rechts"}, name="5-HPETE")
t.mole.append(hpete2)
t.unterschrift(hpete2, "5-HPETE", abstand=30, farbe=G)

t.reaktionspfeil(320, 596, 394)
t.text(357, 584, "&#8722; H&#8322;O", size=10.5, anchor="middle", gewicht=700, farbe=G)
t.text(357, 618, "LTA&#8324;-Synthase-", size=10, anchor="middle", farbe=G)
t.text(357, 632, "Teilaktivität", size=10, anchor="middle", farbe=G)

# LTA4 ist das 5S,6S-trans-Epoxid mit 7E,9E. Die dritte Doppelbindung des Triens
# liegt bei Delta-11 und damit hinter dem Ausschnitt C4 bis C11; die Unterschrift
# sagt das ausdruecklich, damit das Bild nicht mehr verspricht, als es zeigt.
lta = mech.Molekuel(r"*[C@@H]1O[C@H]1/C=C/C=C/*", 560, 596, labels={0: "C4", 8: "C11"},
                    zeige={0: "links", 8: "rechts"}, name="LTA4")
t.mole.append(lta)
t.unterschrift(lta, "LTA&#8324;: das 5,6-Epoxid, Weiche zu LTB&#8324; oder den Cysteinyl-Leukotrienen.",
               "Zwei der drei konjugierten Doppelbindungen liegen im Ausschnitt,",
               "die dritte (Δ11) folgt dahinter.", abstand=32)

t.kasten(20, 700, 960, 76, fill="var(--enzym-bg)", stroke=E)
t.text(38, 722, "OHNE FLAP GESCHIEHT NICHTS", size=11, gewicht=700, farbe=E)
t.text(38, 744, "FLAP ist kein Enzym, sondern ein Membranprotein, das der 5-LOX die "
                "Arachidonsäure überhaupt erst übergibt. Ohne FLAP findet keine Umsetzung",
       size=12.5)
t.text(38, 763, "statt. Deshalb ist auch FLAP ein Angriffspunkt, und deshalb arbeitet die "
                "5-LOX nur an der Kernmembran, nicht frei im Cytosol.", size=12.5)

# ===================================================== ZONE C · Zileuton
t.zone(818, "C · WARUM ZILEUTON EIN N-HYDROXYHARNSTOFF IST")
t.text(20, 848, "Der Hemmstoff greift nicht den Substratkanal an, sondern das Metall: Er "
                "reduziert das Fe(III) zu Fe(II) und nimmt dem Enzym damit die "
                "Oxidationskraft.", size=12.5)

zil = mech.Molekuel("CC(c1cc2ccccc2s1)N(O)C(N)=O", 220, 960, name="Zileuton")
t.mole.append(zil)
t.unterschrift(zil, "Zileuton: die N-Hydroxyharnstoff-Gruppe rechts",
               "chelatiert das Eisen und reduziert es", abstand=30, farbe=R)

t.kasten(520, 892, 460, 138, fill="var(--drug-bg)", stroke=R)
t.text(538, 914, "WARUM DAS PRINZIP AN SEINE GRENZEN STÖSST", size=11, gewicht=700, farbe=R)
t.text(538, 936, "Nicht-Häm-Eisen tragen viele Enzyme. Ein Hemmstoff, der", size=12.5)
t.text(538, 955, "auf das Metall zielt statt auf die Bindetasche, ist deshalb", size=12.5)
t.text(538, 974, "schwer selektiv zu machen.", size=12.5)
t.text(538, 997, "Die Hepatotoxizität hat Zileuton weitgehend aus der", size=12.5)
t.text(538, 1016, "Therapie verdrängt.", size=12.5)

t.kasten(20, 1074, 960, 96, fill="var(--surface-2)")
t.text(38, 1096, "DIE KLINISCH GENUTZTE ALTERNATIVE SETZT WEITER UNTEN AN", size=11,
       gewicht=700, farbe=G)
t.text(38, 1118, "Montelukast und Zafirlukast blockieren nicht das Enzym, sondern den "
                 "CysLT&#8321;-Rezeptor. Damit umgehen sie das Selektivitätsproblem. Der", size=12.5)
t.text(38, 1137, "Preis ist, dass LTB&#8324; weiter gebildet wird und seine chemotaktische "
                 "Wirkung behält.", size=12.5)

t.text(20, 1210, "Beide Äste der Kaskade, Cyclooxygenase und Lipoxygenase, gehen vom selben "
                 "Substrat aus. Wer den einen blockiert, verschiebt Substrat in den "
                 "anderen.", size=12.5, farbe=G)
t.text(20, 1230, "Daraus erklärt sich das Analgetika-Asthma unter NSAR.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "5-Lipoxygenase in drei Zonen. Zone A zeigt den ersten Durchgang an gezeichneten "
    "Strukturen: Ein Nicht-Haem-Eisen als Fe(III)-Hydroxid abstrahiert mit Fischhakenpfeilen "
    "das doppelt allylische Wasserstoffatom am C7 der Arachidonsaeure, gezeigt am Ausschnitt "
    "C4 bis C11 mit beiden Doppelbindungen in cis-Form; das Radikal "
    "delokalisiert ueber C5 bis C9, Sauerstoff addiert an C5 von der Gegenseite, und es "
    "entsteht 5-S-HPETE mit einer Delta-6-Doppelbindung in E-Form. Zone B zeigt den zweiten "
    "Durchgang desselben Enzyms: Nach Abstraktion "
    "am C10 und Wasserabspaltung schliesst sich zwischen C5 und C6 ein trans-Epoxid, es "
    "entsteht Leukotrien A4; zwei der drei konjugierten Doppelbindungen liegen im gezeigten "
    "Ausschnitt, die dritte dahinter. Zone C zeigt Zileuton, dessen "
    "N-Hydroxyharnstoff-Gruppe das Eisen chelatiert und zu Fe(II) reduziert."
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

mech.speichern("m13", t.svg(ARIA), t)
