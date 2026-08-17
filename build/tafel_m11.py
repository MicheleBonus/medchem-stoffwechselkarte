# -*- coding: utf-8 -*-
"""
M-11 · Kupfer-Monooxygenasen, gebaut mit mech.py.

Das Kupfer traegt keinen Makrocyclus - deshalb wird das Zentrum hier ohne
Ebenenbalken gezeichnet (ebene=False). Sonst suggerierte das Bild ein Porphyrin,
das es nicht gibt.

Die beiden Catecholamine liegen auf einem gemeinsamen Leitgeruest: Dopamin und
Noradrenalin unterscheiden sich nur um die eine Hydroxylgruppe, und genau die
soll ins Auge fallen - nicht eine verdrehte Ringlage. Der Kern stellt den
Brenzcatechinring so, dass die Seitenkette nach links zeigt und die beiden
Hydroxylgruppen nach rechts und rechts unten. Damit steht das benzylische
Wasserstoffatom auf der dem Kupfer zugewandten Seite, und die beiden Fischhaken
finden zwischen Substrat und Superoxo-Sauerstoff einen kurzen Weg, ohne das
Geruest zu kreuzen.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech
import mech_kerne
from mech import Atom, Bindung

HERE = os.path.dirname(os.path.abspath(__file__))

# Brenzcatechin-Ring samt benzylischem Kohlenstoff. Ladungs- und
# aromatizitaetsagnostisch geschrieben, damit beide Stufen sicher getroffen werden.
CATECHOLAMIN = mech_kerne.eigener(
    "catecholamin", "NCCc1ccc(O)c(O)c1",
    muster="[#6]~[#6]1~[#6]~[#6]~[#6](~[#8])~[#6](~[#8])~[#6]~1",
    ring=[3, 4, 5, 6, 8, 10], leit=3, folge=4, winkel=180.0)

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1240)

# ===================================================== ZONE A · die Luecke
t.zone(24, "A · ZWEI KUPFERZENTREN OHNE VERBINDUNG")
t.text(20, 54, "Das eine Kupfer nimmt die Elektronen auf, das andere macht die Chemie. Zwischen "
               "ihnen liegen etwa elf Ångström ohne eine Aminosäurekette, die sie verbände.",
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

# Ascorbat ist an O3 deprotoniert, nicht an O2: nur dieses Anion ist ueber
# C3=C2-C1=O bis zum Lactoncarbonyl delokalisiert. Das ist der Grund fuer
# pKs1 = 4,2; die 2-OH-Gruppe bleibt mit pKs2 = 11,6 protoniert.
asc = mech.Molekuel("OC[C@H](O)[C@H]1OC(=O)C(O)=C1[O-]", 88, 322, name="Ascorbat")
t.mole.append(asc)
t.ueberschrift(asc, "Ascorbat", abstand=30, farbe=G, gewicht=None, size=11)
t.reaktionspfeil(158, 300, 212, 218)
t.text(240, 300, "Zwei Ascorbat reduzieren beide Kupferzentren von Cu(II) zu Cu(I). Das ist "
                 "die zweite große Funktion des Vitamin C,", size=12.5)
t.text(240, 319, "neben der Prolylhydroxylierung im Kollagen. Ascorbat wird hier verbraucht, "
                 "nicht katalytisch genutzt.", size=12.5)

# ===================================================== ZONE B · der Zyklus
t.zone(400, "B · DER ZYKLUS AM KATALYTISCHEN KUPFER")
t.text(20, 430, "Der Sauerstoff wird nicht bis zum Ferryl-Äquivalent aktiviert. Schon der "
                "Superoxo-Komplex reicht, um ein Wasserstoffatom abzuziehen.", size=12.5)

z1 = t.zentrum(110, 540, "Cu(I)", unten="", ebene=False, schritt=46, name="Cu(I)")
t.text(110, 596, "Cu(I)", size=11, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(160, 540, 320)
t.text(240, 528, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=C)

# Das Superoxo-Zentrum steht so weit rechts, dass die beiden Fischhaken zum
# Dopamin im Sehnenfenster der Buecher bleiben (1,5 bis 4 Bindungslaengen).
z2 = t.zentrum(358, 540, "Cu(II)", axial=["O", "O&#8226;"], unten="", ebene=False,
               schritt=46, name="Superoxo")
t.text(358, 596, "Superoxo-Komplex", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(358, 614, "nach der Abstraktion Cu(II)&#8722;OOH", size=10, anchor="middle", farbe=G)

# Atom 2 ist der benzylische Kohlenstoff (Nachbar des Rings); Atom 1 die CH2-Gruppe
# am Stickstoff. Nur an Atom 2 sitzt im Produkt die Hydroxylgruppe, also muss auch
# der Fischhaken dort ansetzen.
dop = t.mol("NCCc1ccc(O)c(O)c1", 475, 500, wasserstoff=[2], kern=CATECHOLAMIN,
            name="Dopamin")
hd = dop.h_index[2]
# Die Abstraktion, in Fischhaken: das ungepaarte Elektron des Superoxo-Sauerstoffs
# holt sich das Wasserstoffatom, ein Elektron der benzylischen C-H-Bindung geht mit
# - zusammen bilden die beiden die neue O-H-Bindung.
#
# Der dritte Haken - das zweite Elektron derselben Bindung bleibt am benzylischen
# Kohlenstoff zurueck - ist nicht gezeichnet. Er fuehrte aus der C-H-Bindung auf
# deren eigenes Kohlenstoffatom, und dafuer ist am Atom kein Platz: es traegt drei
# Bindungen und damit drei gleich weite Winkelluecken. Die Luecke neben der
# C-H-Bindung liegt nur ein Drittel der geforderten Sehnenlaenge vom Schwanz
# entfernt; die beiden anderen erreicht kein Bogen, ohne eine Nachbarbindung zu
# kreuzen. Der Solver lehnt alle 768 Kandidaten ab. Wie in M-08 an derselben
# Stelle steht die Aussage deshalb im Text - unten in Zone C, beim stabilisierten
# benzylischen Radikal - statt als verbogener Pfeil im Bild.
#
# Beide Haken haengen am selben Sauerstoff. Ohne Angabe setzt der Solver ihre
# Anker auf dieselbe Gerade vom Sauerstoff zum Substrat, und die beiden Boegen
# laufen dort fuenf Pixel nebeneinander her - unter dem geforderten Mindestabstand
# zweier Pfeile. Deshalb sind die beiden Ankerorte ausdruecklich getrennt: das
# ungepaarte Elektron rechts neben dem Symbol, wo der Haken zum Wasserstoff
# hinausgeht, und die ankommende Spitze schraeg darunter, dort also, wo die neue
# O-H-Bindung entsteht.
t.schub(z2.ax(1, winkel=8, abstand=15), Atom(dop, hd), elektronen=1)
t.schub(Bindung(dop, 2, hd), z2.ax(1, winkel=70, abstand=12), elektronen=1)
t.unterschrift(dop, "Dopamin: abstrahiert wird das benzylische",
               "Wasserstoffatom, nicht ein beliebiges", abstand=30)

t.reaktionspfeil(660, 540, 726)
t.text(693, 528, "Rebound", size=10.5, anchor="middle", gewicht=700, farbe=G)
t.text(693, 562, "+ e&#8722;, + H&#8314;", size=10, anchor="middle", farbe=G)
t.text(693, 576, "&#8722; H&#8322;O", size=10, anchor="middle", farbe=G)

nor = t.mol("NC[C@H](O)c1ccc(O)c(O)c1", 850, 540, stereo=True, kern=CATECHOLAMIN,
            name="Noradrenalin")
t.unterschrift(nor, "Noradrenalin: die Hydroxylgruppe steht",
               "immer (<tspan font-style='italic'>R</tspan>)-konfiguriert", abstand=30)

t.kasten(20, 660, 960, 76, fill="var(--surface-2)")
t.text(38, 682, "DERSELBE ABLAUF WIE BEIM P450, MIT EINEM SCHWÄCHEREN OXIDANS", size=11,
       gewicht=700, farbe=G)
t.text(38, 704, "Wasserstoffabstraktion, dann Rebound: die beiden Schritte aus Tafel M-08. "
                "Nur ist das Oxidans hier kein Fe(IV)=O, sondern ein Cu(II)-Superoxo.", size=12.5)
t.text(38, 723, "Deshalb greift das Enzym nur schwache C&#8722;H-Bindungen an, etwa "
                "benzylische. Ein Alkan könnte es nicht hydroxylieren.", size=12.5)

# ===================================================== ZONE C · die zwei Enzyme
t.zone(784, "C · ZWEI ENZYME NACH DEMSELBEN BAUPLAN")

t.kasten(20, 816, 470, 138, fill="var(--enzym-bg)", stroke=E)
t.text(38, 838, "DOPAMIN-β-HYDROXYLASE", size=11, gewicht=700, farbe=E)
t.text(38, 860, "Hydroxyliert benzylisch und macht damit aus", size=12.5)
t.text(38, 879, "Dopamin Noradrenalin. Sitzt in den Vesikeln der", size=12.5)
t.text(38, 898, "sympathischen Neurone und des Nebennierenmarks.", size=12.5)
t.text(38, 921, "Disulfiram hemmt sie als Nebenwirkung. Daher der", size=12.5)
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
                 "Radikal vom Aromaten stabilisiert wird. Die Bindung ist dadurch rund", size=12.5,
       farbe=G)
t.text(20, 1160, "50 kJ/mol schwächer als eine gewöhnliche aliphatische C&#8722;H-Bindung. "
                 "Bei den P450 entscheidet dagegen die Bindetasche, siehe Tafel M-08.",
       size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Kupfer-Monooxygenasen in drei Zonen. Zone A zeigt die beiden Kupferzentren, das "
    "Elektronentransfer-Zentrum mit drei Histidinen und das katalytische Zentrum mit zwei "
    "Histidinen und einem Methionin, getrennt durch etwa elf Angstroem ohne verbindende "
    "Proteinkette; daneben das gezeichnete Ascorbat, das beide reduziert. Zone B zeigt den "
    "Zyklus: Aus Kupfer eins und Sauerstoff entsteht ein Superoxo-Komplex, der mit zwei "
    "Fischhakenpfeilen das benzylische Wasserstoffatom vom Dopamin abstrahiert. Der eine Haken "
    "bringt das ungepaarte Elektron des Superoxo-Sauerstoffs an das Wasserstoffatom, der andere "
    "fuehrt ein Elektron der benzylischen Kohlenstoff-Wasserstoff-Bindung zum Sauerstoff; "
    "zusammen bilden die beiden die neue Sauerstoff-Wasserstoff-Bindung. Das zweite Elektron "
    "dieser Bindung bleibt als Radikal am benzylischen Kohlenstoff zurueck. "
    "Aus dem Superoxo wird dabei ein Hydroperoxo. Nach dem Rebound, der "
    "ein Elektron und ein Proton verbraucht und Wasser freisetzt, "
    "entsteht Noradrenalin mit R-konfigurierter Hydroxylgruppe. Zone C stellt die "
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
