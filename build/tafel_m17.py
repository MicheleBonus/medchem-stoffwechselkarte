# -*- coding: utf-8 -*-
"""
M-17 · Glutathionperoxidase, gebaut mit mech.py.

Kein Metall, sondern ein Selen. Der Zyklus laeuft ueber drei Oxidationsstufen
desselben Atoms - deshalb sind alle drei als Struktur gezeichnet.
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

t = mech.Tafel(1000, 1220)

# ===================================================== ZONE A · der Selenol-Zyklus
t.zone(24, "A · DER SELENOL-ZYKLUS — DREI STUFEN AN EINEM ATOM")
t.text(20, 54, "Das aktive Zentrum ist ein Selenocystein, die einundzwanzigste proteinogene "
               "Aminosäure. Sein Selen durchläuft bei jedem Umsatz drei Oxidationsstufen und "
               "kehrt", size=12.5)
t.text(20, 73, "am Ende unverändert zurück.", size=12.5)

sel1 = mech.Molekuel("*C[SeH]", 120, 208, labels={0: "Enzym"}, zeige={2: "rechts"},
                     name="Selenol")
t.mole.append(sel1)
lp_se = t.elektronenpaar(sel1, 2, 300)
t.unterschrift(sel1, "Selenocystein als Selenolat —", "das eigentliche Nucleophil", abstand=30)

h2o2 = mech.Molekuel("OO", 300, 152, name="Wasserstoffperoxid")
t.mole.append(h2o2)
t.pfeil(lp_se, (h2o2, 0), bogen=0.26, seite=-1, farbe=W)
t.pfeil((h2o2, 0, 1), (h2o2, 1), bogen=0.42, seite=1, farbe=W)
t.unterschrift(h2o2, "H&#8322;O&#8322;", abstand=26, farbe=G)

t.reaktionspfeil(370, 208, 436)
t.text(403, 196, "&#8722; H&#8322;O", size=10, anchor="middle", gewicht=700, farbe=G)

sel2 = mech.Molekuel("*C[Se]O", 520, 208, labels={0: "Enzym"}, zeige={2: "links"},
                     name="Selenensaeure")
t.mole.append(sel2)
t.unterschrift(sel2, "Selenensäure — das Selen ist oxidiert", abstand=30, farbe=W)

t.reaktionspfeil(600, 208, 666)
t.text(633, 196, "+ GSH", size=10, anchor="middle", gewicht=700, farbe=E)
t.text(633, 230, "&#8722; H&#8322;O", size=10, anchor="middle", farbe=G)

sel3 = mech.Molekuel("*C[Se]S*", 780, 208, labels={0: "Enzym", 4: "GS"},
                     zeige={2: "links"}, name="Selenenylsulfid")
t.mole.append(sel3)
t.unterschrift(sel3, "Selenenylsulfid — ein gemischtes", "Se&#8722;S-Zwischenprodukt", abstand=30)

t.text(20, 344, "Ein zweites Glutathion löst das Sulfid wieder ab: Dabei entsteht "
                "GSSG, und das Selenol steht unverändert wieder bereit — der Kreis "
                "schließt sich.", size=12.5)

t.kasten(20, 392, 470, 118, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 414, "WARUM SELEN UND NICHT SCHWEFEL", size=11, gewicht=700, farbe=C)
t.text(38, 436, "Das Selenol ist mit einem pK<tspan baseline-shift='sub' font-size='9'>a</tspan> "
                "um 5 bei physiologischem", size=12.5)
t.text(38, 455, "pH vollständig deprotoniert — das Thiol eines Cysteins", size=12.5)
t.text(38, 474, "mit einem pK<tspan baseline-shift='sub' font-size='9'>a</tspan> um 8 nur zu "
                "einem kleinen Teil.", size=12.5)
t.text(38, 495, "Das Selenolat ist damit das bessere Nucleophil.", size=12, farbe=G)

t.kasten(510, 392, 470, 118, fill="var(--surface-2)")
t.text(528, 414, "ZWEI GLUTATHION PRO PEROXID", size=11, gewicht=700, farbe=G)
t.text(528, 436, "Das erste bildet das Selenenylsulfid, das zweite löst es", size=12.5)
t.text(528, 455, "wieder ab. Dabei entsteht GSSG, das oxidierte Dimer.", size=12.5)
t.text(528, 478, "Die Glutathion-Reduktase holt es mit NADPH zurück —", size=12.5)
t.text(528, 497, "und genau dort hängt der Pentosephosphatweg dran.", size=12.5)

# ===================================================== ZONE B · die Familie
t.zone(562, "B · EINE FAMILIE MIT ARBEITSTEILUNG")
t.text(20, 592, "Der Mensch hat acht Glutathionperoxidasen. Drei davon sollte man "
                "auseinanderhalten können.", size=12.5)

FAMILIE = [
    (20, "GPx1 — cytosolisch", "Die häufigste Form, vor allem im Erythrozyten.",
     "Entgiftet H&#8322;O&#8322; im Zellinneren."),
    (350, "GPx3 — im Plasma", "Wird von der Niere sezerniert und arbeitet",
     "extrazellulär. Sinkt bei Niereninsuffizienz."),
    (680, "GPx4 — an der Membran", "Reduziert Lipidhydroperoxide direkt in der",
     "Membran. Ihr Ausfall löst Ferroptose aus."),
]
for x, name, z1, z2 in FAMILIE:
    t.text(x, 630, name, size=12.5, gewicht=700, farbe=E)
    t.text(x, 652, z1, size=12)
    t.text(x, 671, z2, size=12)

t.kasten(20, 698, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 720, "WARUM DER SELENMANGEL DAS HERZ TRIFFT", size=11, gewicht=700, farbe=W)
t.text(38, 742, "Ohne Selen kann der Körper kein Selenocystein einbauen, und alle acht Enzyme "
                "fallen zugleich aus. Historisch beschrieben ist das als", size=12.5)
t.text(38, 761, "Keshan-Krankheit — eine Kardiomyopathie in selenarmen Regionen Chinas. Das "
                "Myokard reagiert besonders empfindlich auf oxidativen Stress.", size=12.5)

# ===================================================== ZONE C · die Verkettung
t.zone(834, "C · DIE KETTE, DIE AM PENTOSEPHOSPHATWEG ENDET")
t.text(20, 864, "Jede Stufe dieser Kette ist ein möglicher Ausfallpunkt — und jeder von ihnen "
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
t.text(38, 1058, "die G6PDH, bricht die Kette am hinteren Ende — und", size=12.5)
t.text(38, 1077, "unter oxidativer Belastung kommt es zur Hämolyse.", size=12.5)

t.kasten(510, 976, 470, 118, fill="var(--surface-2)")
t.text(528, 998, "WAS DIE BELASTUNG AUSLÖST", size=11, gewicht=700, farbe=G)
t.text(528, 1020, "Primaquin und andere 8-Aminochinoline, Sulfonamide,", size=12.5)
t.text(528, 1039, "Nitrofurantoin, Rasburicase — und Favabohnen, daher", size=12.5)
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
    "und das Selenol ist zurueck. Ein Kasten erklaert, warum Selen und nicht Schwefel: Das "
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

daten = {}
if os.path.exists(ZIEL):
    daten = json.load(io.open(ZIEL, encoding="utf-8"))
daten["m17"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m17  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m17"]), len(t.mole), len(t.anker)))
