# -*- coding: utf-8 -*-
"""
M-13 · 5-Lipoxygenase, gebaut mit mech.py.

Dasselbe Muster wie M-12: Abstraktion an einer doppelt allylischen Methylen-
gruppe, Sauerstoff von der Gegenseite. Nur zuendet hier ein Eisen statt eines
Tyrosinrests. Das Eisen traegt keinen Makrocyclus, also ebene=False.

Alle vier Stufen der Fettsaeurekette haengen an einem gemeinsamen Leitgeruest
(KERN unten): der Weg C4 bis C11, an beiden Enden von einem Rest abgeschlossen.
Frueher hielt zeige= nur die beiden Enden fest; das dreht, aber es spiegelt
nicht, und deshalb stand der Zickzack von Bild zu Bild einmal so und einmal
anders. Das Leitgeruest haelt Drehung und Haendigkeit fest, laesst aber die
Doppelbindungen ihre eigene Geometrie behalten - nachgemessen bleibt jede
Bindung so cis oder trans, wie das SMILES sie nennt. Genau darauf kommt es in
dieser Tafel an: Delta-5 ist Z, Delta-6 im Produkt E.

Die Abstraktion braucht zwei Fischhaken aus derselben Bindung C7-H: der eine
geht mit dem Wasserstoffatom an das Hydroxid, der andere bleibt am C7. Eine
Kette sind sie nicht - Kopf an Schwanz haengt nur, was nacheinander geschieht,
und diese beiden laufen gleichzeitig auseinander.

Gezeichnet ist nur der erste. Fuer den zweiten gibt es unter dem heutigen
Regelkatalog keinen zulaessigen Bogen; die Rechnung dazu steht unten an Ort und
Stelle. Wie in Tafel M-01 steht die Aussage deshalb im Text.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech
import mech_kerne
from mech import Atom, Bindung   # noqa: F401  (Atom: siehe die Notiz bei Zone A)

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1260)

# Der gemeinsame Kern aller vier Stufen: die Kette C4-C5-...-C11, an beiden Enden
# ein Rest. Das Muster ist bindungsordnungs-agnostisch (~) und nennt die Enden
# ausdruecklich als Platzhalteratome ([#0]); ohne beides traefe es die Stufe mit
# dem Epoxid nicht, in der C5 und C6 einfach gebunden sind. In allen vier Stufen
# trifft es genau einmal und in derselben Richtung - nachgerechnet, nicht geraten.
# 'ring' meint hier die Kette selbst; die Lage haengt an ihr, leit=0 stellt das
# C4-Ende nach links (winkel=180), folge=1 legt den Umlaufsinn fest. Damit laeuft
# die Reaktion mit der Leserichtung von links nach rechts.
KERN = mech_kerne.eigener(
    "fettsaeure-c4-c11", r"*/C=C\C/C=C\C*",
    muster="[#0]~[#6]~[#6]~[#6]~[#6]~[#6]~[#6]~[#0]",
    ring=[0, 1, 2, 3, 4, 5, 6, 7], leit=0, folge=1, winkel=180.0)

# ===================================================== ZONE A · erster Durchgang
t.zone(24, "A · ERSTER DURCHGANG: AUS DER FETTSÄURE WIRD EIN HYDROPEROXID")
t.text(20, 54, "Gezeigt ist der Ausschnitt C4 bis C11 der Arachidonsäure, beide Doppelbindungen in "
               "ihrer wirklichen <tspan font-style='italic'>cis</tspan>-Form. Das C7 zwischen "
               "ihnen ist doppelt", size=12.5)
t.text(20, 73, "allylisch, dort sitzt das schwächste Wasserstoffatom.", size=12.5)

zfe = t.zentrum(150, 196, "Fe(III)", axial=["OH"], unten="", ebene=False, schritt=46,
                name="Nicht-Häm-Eisen")
t.text(150, 252, "Fe(III)&#8722;OH", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(150, 268, "nur diese Form ist aktiv", size=10.5, anchor="middle", farbe=G)

# Beide Doppelbindungen des Ausschnitts sind cis (5Z, 8Z). Ohne die Richtungsangaben
# zeichnete RDKit sie all-trans, und der Satz von der cis-Geometrie stuende dann im
# Widerspruch zum eigenen Bild.
frag = t.mol(r"*/C=C\C/C=C\C*", 300, 176, labels={0: "C4", 7: "C11"},
             wasserstoff=[3], kern=KERN, name="Arachidonsäure")
hf = frag.h_index[3]
# Der erste Fischhaken: das Wasserstoffatom geht mit einem Elektron der Bindung
# C7-H an das Hydroxid des Eisens. Wo der Bogen langlaeuft, sucht der Solver
# selbst; er setzt den Schwanz neben die Bindung C7-H und fuehrt ihn unter dem
# C4-Ende hindurch nach links.
t.schub(Bindung(frag, 3, hf), zfe.ax(0), elektronen=1)
# Der zweite Fischhaken - das Elektron, das am C7 zurueckbleibt - ist nicht
# gezeichnet, sondern steht als Zeile ueber der Struktur. Er waere
#     t.schub(Bindung(frag, 3, hf), Atom(frag, 3), elektronen=1)
# und dafuer gibt es unter dem heutigen Katalog keinen zulaessigen Bogen: liegt
# die Spitze in derselben Winkelluecke wie der Schwanz, wird die Sehne 0,31-0,40 L
# lang und faellt unter die 0,60 L, die F4 fuer 'intra' fordert; liegt sie in der
# Luecke auf der anderen Seite, kreuzt der Bauch die eigene Quellbindung. Das ist
# keine Frage dieser Tafel: ein einzeln stehendes Propan mit einem sichtbaren
# Wasserstoff scheitert an derselben Stelle. Wie in Tafel M-01, wo der letzte
# Schritt der Chinoid-Kaskade aus demselben Grund fehlt, steht die Aussage
# deshalb im Text statt als verbogener Pfeil.
t.ueberschrift(frag, "das zweite Elektron der Bindung C7&#8722;H bleibt am C7 zurück",
               abstand=34, size=10.5, farbe=W, gewicht=700)
# Die Nummer sitzt dicht ueber dem C7, in der Winkelluecke zwischen den beiden
# Bindungen. Weiter hinaus geschoben waere sie naeher am Nachbarn C8 als am
# gemeinten C7 - bei einer Zickzackkette liegt jeder Punkt weit ueber einem Tal
# schon dichter an einem der beiden Gipfel.
t.atomnummer(frag, 3, "C7", winkel=290, abstand=16, size=10, farbe=R, gewicht=700)
t.unterschrift(frag, "das Radikal delokalisiert anschließend über C5 bis C9",
               abstand=32)

t.reaktionspfeil(420, 176, 494)
t.text(457, 164, "+ O&#8322; an C5", size=10.5, anchor="middle", gewicht=700, farbe=E)
t.text(457, 198, "von der Gegenseite", size=10, anchor="middle", farbe=G)

# 5-HPETE ist 5S-Hydroperoxy-6E,8Z. Der Keil am C5 traegt die 5S-Konfiguration,
# Delta-6 ist E, Delta-8 bleibt Z wie im Substrat.
hpete = t.mol(r"*[C@H](OO)/C=C/C=C\C*", 640, 176, labels={0: "C4", 9: "C11"},
              kern=KERN, name="5-HPETE")
# Die Nummer gehoert ueber das C5: unten steht schon die Marke C4, und zwei
# Beschriftungen nebeneinander liest niemand als zwei verschiedene Atome. Sie
# steht dicht am Atom, aus demselben Grund wie das C7 der ersten Stufe.
t.atomnummer(hpete, 1, "C5", winkel=289, abstand=15, size=10, farbe=W, gewicht=700)
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

hpete2 = t.mol(r"*[C@H](OO)/C=C/C=C\C*", 200, 596, labels={0: "C4", 9: "C11"},
               kern=KERN, name="5-HPETE")
t.unterschrift(hpete2, "5-HPETE", abstand=30, farbe=G)

t.reaktionspfeil(320, 596, 394)
t.text(357, 584, "&#8722; H&#8322;O", size=10.5, anchor="middle", gewicht=700, farbe=G)
t.text(357, 618, "LTA&#8324;-Synthase-", size=10, anchor="middle", farbe=G)
t.text(357, 632, "Teilaktivität", size=10, anchor="middle", farbe=G)

# LTA4 ist das 5S,6S-trans-Epoxid mit 7E,9E. Die dritte Doppelbindung des Triens
# liegt bei Delta-11 und damit hinter dem Ausschnitt C4 bis C11; die Unterschrift
# sagt das ausdruecklich, damit das Bild nicht mehr verspricht, als es zeigt.
lta = t.mol(r"*[C@@H]1O[C@H]1/C=C/C=C/*", 560, 596, labels={0: "C4", 8: "C11"},
            kern=KERN, name="LTA4")
t.unterschrift(lta, "LTA&#8324;: das 5,6-Epoxid, Weiche zu LTB&#8324; oder den Cysteinyl-Leukotrienen.",
               "Zwei der drei konjugierten Doppelbindungen liegen im Ausschnitt,",
               "die dritte (Δ11) folgt dahinter.", abstand=32)

# Der Kasten steht zwoelf Pixel tiefer als frueher: die Unterschrift des LTA4
# hat seit dem Leitgeruest drei Zeilen und reichte sonst bis an die Kante.
t.kasten(20, 712, 960, 76, fill="var(--enzym-bg)", stroke=E)
t.text(38, 734, "OHNE FLAP GESCHIEHT NICHTS", size=11, gewicht=700, farbe=E)
t.text(38, 756, "FLAP ist kein Enzym, sondern ein Membranprotein, das der 5-LOX die "
                "Arachidonsäure überhaupt erst übergibt. Ohne FLAP findet keine Umsetzung",
       size=12.5)
t.text(38, 775, "statt. Deshalb ist auch FLAP ein Angriffspunkt, und deshalb arbeitet die "
                "5-LOX nur an der Kernmembran, nicht frei im Cytosol.", size=12.5)

# ===================================================== ZONE C · Zileuton
t.zone(818, "C · WARUM ZILEUTON EIN N-HYDROXYHARNSTOFF IST")
t.text(20, 848, "Der Hemmstoff greift nicht den Substratkanal an, sondern das Metall: Er "
                "reduziert das Fe(III) zu Fe(II) und nimmt dem Enzym damit die "
                "Oxidationskraft.", size=12.5)

zil = t.mol("CC(c1cc2ccccc2s1)N(O)C(N)=O", 220, 960, name="Zileuton")
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
    "Strukturen: Ein Nicht-Haem-Eisen als Fe(III)-Hydroxid abstrahiert das doppelt "
    "allylische Wasserstoffatom am C7 der Arachidonsaeure, gezeigt am Ausschnitt "
    "C4 bis C11 mit beiden Doppelbindungen in cis-Form. Ein Fischhakenpfeil fuehrt von der "
    "Bindung zwischen C7 und diesem Wasserstoffatom zum Hydroxid am Eisen; dass das zweite "
    "Elektron dieser Bindung am C7 zurueckbleibt, steht als Zeile ueber der Struktur. "
    "Das Radikal "
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
