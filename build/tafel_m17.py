# -*- coding: utf-8 -*-
"""
M-17 · Glutathionperoxidase, gebaut mit mech.py.

Kein Metall, sondern ein Selen. Der Zyklus laeuft ueber drei Oxidationsstufen
desselben Atoms - deshalb sind alle drei als Struktur gezeichnet.

Die drei Stufen haengen an einem gemeinsamen Leitgeruest: Enzym-CH2-Se steht in
jedem der drei Bilder gleich, die Kette laeuft von links unten nach rechts oben.
Vorher richtete zeige= die erste Stufe nach rechts und die beiden anderen nach
links aus; der Leser musste jedes Bild neu einnorden, statt den Unterschied am
Selen zu sehen. Die Pfeile beschreiben nur noch die Chemie, die Geometrie kommt
aus dem Solver in mech_schub.py.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech
import mech_kerne
from mech import Atom, Bindung, Paar

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1220)

# Das Leitgeruest der drei Stufen: der Rest am Enzym, das CH2 und das Selen.
# Kein Ring, sondern eine Kette - die Referenzlage haengt deshalb am Schwerpunkt
# dieser drei Atome. Das Selen zeigt 30 Grad nach rechts oben, der Enzymrest
# damit nach links unten; das Reagens kommt in jeder Stufe von rechts oben
# herein, also mit der Leserichtung.
SEC = mech_kerne.eigener("selenocystein", "CC[SeH]",
                         muster="[!#1]~[#6]~[#34]",
                         ring=[0, 1, 2], leit=2, folge=1, winkel=30.0)

# ===================================================== ZONE A · der Selenol-Zyklus
t.zone(24, "A · DER SELENOL-ZYKLUS: DREI STUFEN AN EINEM ATOM")
t.text(20, 54, "Das aktive Zentrum ist ein Selenocystein, die einundzwanzigste proteinogene "
               "Aminosäure. Sein Selen durchläuft bei jedem Umsatz drei Oxidationsstufen und "
               "kehrt", size=12.5)
t.text(20, 73, "am Ende unverändert zurück.", size=12.5)

# Gezeichnet wird das Anion: bei pH 7 liegt das Selenocystein deprotoniert vor,
# und nur so bleibt die Ladungsbilanz des Angriffs auf H2O2 stimmig.
# Die y-Werte der drei Stufen sind nicht gleich, weil t.mol den Mittelpunkt des
# umschliessenden Rechtecks setzt und dieses Rechteck je nach Substituent am Selen
# anders liegt. Gleich stehen soll aber das Leitgeruest, nicht der Kasten darum:
# alle drei Werte sind deshalb so gewaehlt, dass das CH2 auf y=242,8 liegt und die
# Kette Enzym-CH2-Se in allen drei Bildern auf derselben Linie sitzt.
sel1 = t.mol("*C[Se-]", 120, 236.2, labels={0: "Enzym"}, kern=SEC,
             name="Selenolat")
t.unterschrift(sel1, "Selenocystein als Selenolat:", "das eigentliche Nucleophil", abstand=30)

h2o2 = t.mol("OO", 195, 166.2, rotate=-60, name="Wasserstoffperoxid")
# Angriff und Bindungsbruch sind ein Schritt: das Selenolat schiebt sein freies
# Paar auf den einen Sauerstoff, das Paar der O-O-Bindung geht auf den anderen,
# der als Hydroxid abgeht. Deshalb als Kette angemeldet - Kopf an Schwanz.
# Die O-O-Bindung steht steil, damit das Selen von unten links angreift und das
# abgehende Hydroxid nach rechts oben wegzeigt. Waagerecht gezeichnet muesste die
# Spitze des zweiten Pfeils in das H der rechten OH-Gruppe hinein, denn RDKit
# setzt den Wasserstoff genau dorthin, wo die Konvention die Spitze verlangt.
t.schub(Paar(sel1, 2), Atom(h2o2, 0), kette="A")
t.schub(Bindung(h2o2, 0, 1), Paar(h2o2, 1), kette="A")
t.ueberschrift(h2o2, "H&#8322;O&#8322;", abstand=22, size=10.5, farbe=G, gewicht=None)

t.reaktionspfeil(300, 232, 366)
t.text(333, 220, "&#8722; OH&#8315;", size=10, anchor="middle", gewicht=700, farbe=G)

sel2 = t.mol("*C[Se]O", 490, 228.9, labels={0: "Enzym"}, kern=SEC,
             name="Selenensaeure")
t.unterschrift(sel2, "Selenensäure: das Selen ist oxidiert", abstand=30, farbe=W)

t.reaktionspfeil(590, 232, 656)
t.text(623, 220, "+ GSH", size=10, anchor="middle", gewicht=700, farbe=E)
t.text(623, 254, "&#8722; H&#8322;O", size=10, anchor="middle", farbe=G)

sel3 = t.mol("*C[Se]S*", 780, 230.9, labels={0: "Enzym", 4: "GS"},
             kern=SEC, name="Selenenylsulfid")
t.unterschrift(sel3, "Selenenylsulfid: ein gemischtes", "Se&#8722;S-Zwischenprodukt", abstand=30)

t.text(20, 344, "Ein zweites Glutathion löst das Sulfid wieder ab: Dabei entsteht "
                "GSSG, und das Selenolat steht unverändert wieder bereit. Der Kreis "
                "schließt sich.", size=12.5)
t.text(20, 368, "Netto: H&#8322;O&#8322; + 2 GSH &#8594; GSSG + 2 H&#8322;O. Das Hydroxidion "
                "des ersten Schritts und das Proton des dritten ergeben zusammen das zweite Wasser.",
       size=12.5, gewicht=700)

t.kasten(20, 392, 470, 118, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 414, "WARUM SELEN UND NICHT SCHWEFEL", size=11, gewicht=700, farbe=C)
t.text(38, 436, "Das Selenol ist mit einem pK<tspan baseline-shift='sub' font-size='9'>a</tspan> "
                "um 5 bei physiologischem", size=12.5)
t.text(38, 455, "pH vollständig deprotoniert, das Thiol eines Cysteins", size=12.5)
t.text(38, 474, "mit einem pK<tspan baseline-shift='sub' font-size='9'>a</tspan> um 8 nur zu "
                "einem kleinen Teil.", size=12.5)
t.text(38, 495, "Das Selenolat ist damit das bessere Nucleophil.", size=12, farbe=G)

t.kasten(510, 392, 470, 118, fill="var(--surface-2)")
t.text(528, 414, "ZWEI GLUTATHION PRO PEROXID", size=11, gewicht=700, farbe=G)
t.text(528, 436, "Das erste bildet das Selenenylsulfid, das zweite löst es", size=12.5)
t.text(528, 455, "wieder ab. Dabei entsteht GSSG, das oxidierte Dimer.", size=12.5)
t.text(528, 478, "Die Glutathion-Reduktase holt es mit NADPH zurück.", size=12.5)
t.text(528, 497, "Genau dort hängt der Pentosephosphatweg dran.", size=12.5)

# ===================================================== ZONE B · die Familie
t.zone(562, "B · EINE FAMILIE MIT ARBEITSTEILUNG")
t.text(20, 592, "Der Mensch hat acht Glutathionperoxidasen. Drei davon sollte man "
                "auseinanderhalten können.", size=12.5)

FAMILIE = [
    (20, "GPx1 im Cytosol", "Die häufigste Form, vor allem im Erythrozyten.",
     "Entgiftet H&#8322;O&#8322; im Zellinneren."),
    (350, "GPx3 im Plasma", "Wird von der Niere sezerniert und arbeitet",
     "extrazellulär. Sinkt bei Niereninsuffizienz."),
    (680, "GPx4 an der Membran", "Reduziert Lipidhydroperoxide direkt in der",
     "Membran. Ihr Ausfall löst Ferroptose aus."),
]
for x, name, z1, z2 in FAMILIE:
    t.text(x, 630, name, size=12.5, gewicht=700, farbe=E)
    t.text(x, 652, z1, size=12)
    t.text(x, 671, z2, size=12)

t.kasten(20, 698, 960, 114, fill="var(--warn-bg)", stroke=W)
t.text(38, 720, "WARUM DER SELENMANGEL DAS HERZ TRIFFT", size=11, gewicht=700, farbe=W)
t.text(38, 742, "Ohne Selen kann der Körper kein Selenocystein einbauen. Fünf der acht Formen sind "
                "Selenoproteine: GPx1 bis GPx4 und GPx6.", size=12.5)
t.text(38, 761, "Sie fallen zugleich aus, während GPx5, GPx7 und GPx8 an dieser Stelle ein Cystein "
                "tragen und selenunabhängig bleiben.", size=12.5)
t.text(38, 780, "Historisch beschrieben ist der Mangel als Keshan-Krankheit, eine Kardiomyopathie in "
                "selenarmen Regionen Chinas mit empfindlichem Myokard.", size=12.5)

# ===================================================== ZONE C · die Verkettung
t.zone(834, "C · DIE KETTE, DIE AM PENTOSEPHOSPHATWEG ENDET")
t.text(20, 864, "Jede Stufe dieser Kette ist ein möglicher Ausfallpunkt, und jeder von ihnen "
                "führt zum selben klinischen Bild.", size=12.5)

KETTE = [
    (60, "H&#8322;O&#8322;", "das Substrat"),
    (250, "GPx", "braucht Selen"),
    (440, "GSSG", "entsteht dabei"),
    (630, "GR", "braucht NADPH"),
    (850, "G6PDH", "liefert NADPH"),
]
for x, name, note in KETTE:
    t.text(x, 926, name, size=13, anchor="middle", gewicht=700, farbe=W)
    t.text(x, 946, note, size=10.5, anchor="middle", farbe=G)
for x0, x1 in ((110, 200), (300, 390), (490, 580), (680, 800)):
    t.reaktionspfeil(x0, 920, x1)

t.kasten(20, 976, 470, 118, fill="var(--drug-bg)", stroke=R)
t.text(38, 998, "DER G6PDH-MANGEL", size=11, gewicht=700, farbe=R)
t.text(38, 1020, "Der Erythrozyt hat keinen Citratzyklus und bezieht sein", size=12.5)
t.text(38, 1039, "gesamtes NADPH aus dem Pentosephosphatweg. Fehlt", size=12.5)
t.text(38, 1058, "die G6PDH, bricht die Kette am hinteren Ende. Unter", size=12.5)
t.text(38, 1077, "oxidativer Belastung kommt es dann zur Hämolyse.", size=12.5)

t.kasten(510, 976, 470, 118, fill="var(--surface-2)")
t.text(528, 998, "WAS DIE BELASTUNG AUSLÖST", size=11, gewicht=700, farbe=G)
t.text(528, 1020, "Primaquin und andere 8-Aminochinoline, Sulfonamide,", size=12.5)
t.text(528, 1039, "Nitrofurantoin, Rasburicase und Favabohnen, daher", size=12.5)
t.text(528, 1058, "der Name Favismus. Alle erzeugen im Erythrozyten", size=12.5)
t.text(528, 1077, "mehr Peroxid, als die Kette abfangen kann.", size=12.5)

t.text(20, 1148, "Dieselbe Kette erklärt auch, warum N-Acetylcystein bei der Paracetamolvergiftung "
                 "hilft: Es liefert Cystein für die Glutathionsynthese und füllt damit den "
                 "Vorrat", size=12.5, farbe=G)
t.text(20, 1168, "wieder auf, den das NAPQI verbraucht hat.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Glutathionperoxidase in drei Zonen. Zone A zeigt den Selenol-Zyklus an gezeichneten "
    "Strukturen: Das Selenolat des Selenocysteins greift mit einem Elektronenpaarpfeil ein "
    "Sauerstoffatom des Wasserstoffperoxids an, die Sauerstoff-Sauerstoff-Bindung bricht, und "
    "es entsteht die Selenensaeure. Ein erstes Glutathion bildet daraus das gemischte "
    "Selenenylsulfid, ein zweites loest es wieder ab; dabei entsteht das oxidierte Dimer GSSG "
    "und das Selenolat ist zurueck. Netto setzt der Zyklus ein Wasserstoffperoxid und zwei "
    "Glutathion zu einem GSSG und zwei Wasser um. Alle drei Stufen stehen in derselben Lage: "
    "der Enzymrest links unten, das Selen rechts oben, damit der Unterschied am Selen ins Auge "
    "faellt und nicht die Ausrichtung. Ein Kasten erklaert, warum Selen und nicht "
    "Schwefel: Das "
    "Selenol ist bei physiologischem pH vollstaendig deprotoniert und damit das bessere "
    "Nucleophil. Zone B nennt drei Enzyme der Familie, Zone C die Kette von Wasserstoffperoxid "
    "ueber die Peroxidase, GSSG und die Glutathionreduktase bis zur "
    "Glucose-6-phosphat-Dehydrogenase."
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

mech.speichern("m17", t.svg(ARIA), t)
