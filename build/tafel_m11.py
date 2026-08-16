# -*- coding: utf-8 -*-
"""
M-11 · Kupfer-Monooxygenasen, gebaut mit mech.py.

Das Kupfer traegt keinen Makrocyclus - deshalb wird das Zentrum hier ohne
Ebenenbalken gezeichnet (ebene=False). Sonst suggerierte das Bild ein Porphyrin,
das es nicht gibt.
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

t = mech.Tafel(1000, 1240)

# ===================================================== ZONE A · die Luecke
t.zone(24, "A · ZWEI KUPFERZENTREN OHNE VERBINDUNG")
t.text(20, 54, "Das eine Kupfer nimmt die Elektronen auf, das andere macht die Chemie. Zwischen "
               "ihnen liegen etwa elf Ångström — ohne Aminosäurekette, die sie verbände.",
       size=12.5)

cuh = t.zentrum(230, 156, "Cu(I)", unten="3 His", ebene=False, name="CuH")
t.text(230, 106, "Cu<tspan baseline-shift='sub' font-size='9'>H</tspan>", size=14,
       anchor="middle", gewicht=700, farbe=C)
t.text(230, 212, "der Eingang für die Elektronen", size=11, anchor="middle", farbe=G)

cum = t.zentrum(640, 156, "Cu(I)", unten="2 His, 1 Met", ebene=False, name="CuM")
t.text(640, 106, "Cu<tspan baseline-shift='sub' font-size='9'>M</tspan>", size=14,
       anchor="middle", gewicht=700, farbe=E)
t.text(640, 212, "hier binden Sauerstoff und Substrat", size=11, anchor="middle", farbe=G)

t.linie(276, 156, 594, 156, farbe=W, breite=1.4, strich="6 5")
t.text(435, 144, "≈ 11 Å, keine Proteinbrücke", size=12, anchor="middle", gewicht=700, farbe=W)
t.text(435, 176, "wie das zweite Elektron hinüberkommt, ist bis heute umstritten", size=10.5,
       anchor="middle", farbe=G)

asc = mech.Molekuel("OC[C@H](O)[C@H]1OC(=O)C([O-])=C1O", 88, 322, name="Ascorbat")
t.mole.append(asc)
t.ueberschrift(asc, "Ascorbat", abstand=30, farbe=G, gewicht=None, size=11)
t.reaktionspfeil(158, 300, 212, 218)
t.text(240, 300, "Zwei Ascorbat reduzieren beide Kupferzentren von Cu(II) zu Cu(I). Das ist "
                 "die zweite große Funktion des Vitamin C —", size=12.5)
t.text(240, 319, "neben der Prolylhydroxylierung im Kollagen. Ascorbat wird hier verbraucht, "
                 "nicht katalytisch genutzt.", size=12.5)

# ===================================================== ZONE B · der Zyklus
t.zone(400, "B · DER ZYKLUS AM KATALYTISCHEN KUPFER")
t.text(20, 430, "Der Sauerstoff wird nicht bis zum Ferryl-Äquivalent aktiviert. Schon der "
                "Superoxo-Komplex reicht, um ein Wasserstoffatom abzuziehen.", size=12.5)

z1 = t.zentrum(110, 540, "Cu(I)", unten="", ebene=False, schritt=46, name="Cu(I)")
t.text(110, 596, "Cu(I)", size=11, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(160, 540, 226)
t.text(193, 528, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=C)

z2 = t.zentrum(300, 540, "Cu(II)", axial=["O", "O&#8226;"], unten="", ebene=False,
               schritt=46, name="Superoxo")
t.text(300, 596, "Superoxo-Komplex", size=11, anchor="middle", gewicht=700, farbe=W)

dop = mech.Molekuel("NCCc1ccc(O)c(O)c1", 500, 500, wasserstoff=[1], zeige={1: "links"},
                    name="Dopamin")
t.mole.append(dop)
hd = dop.h_index[1]
t.pfeil((dop, 1, hd), z2.ax(1, winkel=20, abstand=34), bogen=0.24, seite=-1,
        typ="fischhaken", farbe=R)
t.pfeil((dop, 1, hd), dop.abseits(1, hd), bogen=0.45, seite=1, typ="fischhaken", farbe=R)
t.unterschrift(dop, "Dopamin — abstrahiert wird das benzylische",
               "Wasserstoffatom, nicht ein beliebiges", abstand=30)

t.reaktionspfeil(660, 540, 726)
t.text(693, 528, "Rebound", size=10.5, anchor="middle", gewicht=700, farbe=G)

nor = mech.Molekuel("NC[C@H](O)c1ccc(O)c(O)c1", 850, 540, stereo=True, name="Noradrenalin")
t.mole.append(nor)
t.unterschrift(nor, "Noradrenalin — die Hydroxylgruppe steht",
               "immer (<tspan font-style='italic'>R</tspan>)-konfiguriert", abstand=30)

t.kasten(20, 660, 960, 76, fill="var(--surface-2)")
t.text(38, 682, "DERSELBE ABLAUF WIE BEIM P450 — MIT EINEM SCHWÄCHEREN OXIDANS", size=11,
       gewicht=700, farbe=G)
t.text(38, 704, "Wasserstoffabstraktion, dann Rebound: die beiden Schritte aus Tafel M-08. "
                "Nur ist das Oxidans hier kein Fe(IV)=O, sondern ein Cu(II)-Superoxo —", size=12.5)
t.text(38, 723, "und deshalb greift das Enzym nur schwache C&#8722;H-Bindungen an, etwa "
                "benzylische. Ein Alkan könnte es nicht hydroxylieren.", size=12.5)

# ===================================================== ZONE C · die zwei Enzyme
t.zone(784, "C · ZWEI ENZYME NACH DEMSELBEN BAUPLAN")

t.kasten(20, 816, 470, 138, fill="var(--enzym-bg)", stroke=E)
t.text(38, 838, "DOPAMIN-β-HYDROXYLASE", size=11, gewicht=700, farbe=E)
t.text(38, 860, "Hydroxyliert benzylisch und macht damit aus", size=12.5)
t.text(38, 879, "Dopamin Noradrenalin. Sitzt in den Vesikeln der", size=12.5)
t.text(38, 898, "sympathischen Neurone und des Nebennierenmarks.", size=12.5)
t.text(38, 921, "Disulfiram hemmt sie als Nebenwirkung — daher der", size=12.5)
t.text(38, 940, "Blutdruckabfall unter der Therapie.", size=12.5)

t.kasten(510, 816, 470, 138, fill="var(--surface-2)")
t.text(528, 838, "PEPTIDYLGLYCIN-α-AMIDIERENDE MONOOXYGENASE", size=11, gewicht=700, farbe=G)
t.text(528, 860, "Hydroxyliert den α-Kohlenstoff eines endständigen", size=12.5)
t.text(528, 879, "Glycins. Das entstehende Carbinolamid zerfällt, und", size=12.5)
t.text(528, 898, "das Peptid trägt am Ende ein Säureamid.", size=12.5)
t.text(528, 921, "Ohne diesen Schritt sind Oxytocin, Vasopressin,", size=12.5)
t.text(528, 940, "Gastrin und Calcitonin unwirksam.", size=12.5)

t.kasten(20, 994, 960, 96, fill="var(--drug-bg)", stroke=R)
t.text(38, 1016, "WAS DAS FÜR DIE PRÜFUNG BEDEUTET", size=11, gewicht=700, farbe=R)
t.text(38, 1038, "Vitamin C hat zwei Funktionen, die in verschiedenen Kapiteln stehen und doch "
                 "dasselbe Prinzip haben: Es reduziert ein Metall im aktiven Zentrum.", size=12.5)
t.text(38, 1057, "Beim Kollagen ist es das Eisen der Prolylhydroxylase, hier das Kupfer. Skorbut "
                 "erklärt sich aus dem einen, der Catecholaminmangel aus dem anderen.", size=12.5)

t.text(20, 1140, "Das benzylische Wasserstoffatom ist deshalb angreifbar, weil das entstehende "
                 "Radikal vom Aromaten stabilisiert wird — dieselbe Überlegung wie bei der "
                 "schwächsten", size=12.5, farbe=G)
t.text(20, 1160, "C&#8722;H-Bindung des Ibuprofens in Tafel M-08.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Kupfer-Monooxygenasen in drei Zonen. Zone A zeigt die beiden Kupferzentren, das "
    "Elektronentransfer-Zentrum mit drei Histidinen und das katalytische Zentrum mit zwei "
    "Histidinen und einem Methionin, getrennt durch etwa elf Angstroem ohne verbindende "
    "Proteinkette; daneben das gezeichnete Ascorbat, das beide reduziert. Zone B zeigt den "
    "Zyklus: Aus Kupfer eins und Sauerstoff entsteht ein Superoxo-Komplex, der mit "
    "Fischhakenpfeilen ein benzylisches Wasserstoffatom vom Dopamin abstrahiert; nach dem "
    "Rebound entsteht Noradrenalin mit R-konfigurierter Hydroxylgruppe. Zone C stellt die "
    "beiden Enzyme dieses Bauplans nebeneinander, die Dopamin-beta-Hydroxylase und die "
    "Peptidylglycin-alpha-amidierende Monooxygenase."
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

mech.speichern("m11", t.svg(ARIA), t)
