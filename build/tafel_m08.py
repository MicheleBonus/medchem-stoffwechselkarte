# -*- coding: utf-8 -*-
"""
M-08 · Der Cytochrom-P450-Zyklus, gebaut mit mech.py.

Der Zyklus selbst ist ein Zustandsdiagramm - dafuer ist der Kreis die richtige
Darstellung. Neu ist, dass die acht Zustaende als gezeichnete Eisenzentren aus
einem Bausatz kommen statt als Textzeilen, und dass die drei Schritte, an denen
wirklich Chemie passiert, mit Elektronenpfeilen ausgefuehrt sind:
die heterolytische O-O-Spaltung, die Wasserstoffabstraktion und der Rebound.
"""
import math
import os

import mech

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1330)

# ===================================================== ZONE A · der Zyklus
t.zone(24, "A · DER KATALYTISCHE ZYKLUS — ACHT ZUSTÄNDE, ZWEI ELEKTRONEN")
t.text(20, 54, "Alle acht Zustände unterscheiden sich nur in zwei Dingen: der Oxidationsstufe "
               "des Eisens und dem, was axial daran hängt.", size=12.5)

CX, CY, RG, RA, RL = 300.0, 402.0, 215.0, 132.0, 100.0


def ort(grad, r=RG):
    a = math.radians(grad - 90.0)
    return CX + math.cos(a) * r, CY + math.sin(a) * r


# (Grad, Nummer, Eisen, axiale Kette, Doppelbindung, Porphyrin-Radikal)
STATIONEN = [
    (0,   "&#9312;", "Fe(III)", ["OH&#8322;"], False, False),
    (45,  "&#9313;", "Fe(III)", [],            False, False),
    (90,  "&#9314;", "Fe(II)",  [],            False, False),
    (135, "&#9315;", "Fe(II)",  ["O", "O"],    False, False),
    (180, "&#9316;", "Fe(III)", ["O", "O&#8315;"], False, False),
    (225, "&#9317;", "Fe(III)", ["O", "OH"],   False, False),
    (270, "&#9318;", "Fe(IV)",  ["O"],         True,  True),
    (315, "&#9319;", "Fe(III)", ["OH"],        False, False),
]

zentren = {}
for grad, nr, fe, ax, dop, rad in STATIONEN:
    gx, gy = ort(grad)
    zentren[grad] = t.zentrum(gx, gy, fe, axial=ax, doppelt=dop, radikal=rad,
                              name="Zustand %d" % (grad // 45 + 1))
    t.text(gx - 38, gy + 5, nr, size=13, anchor="middle", gewicht=700, farbe=G)

# Uebergaenge: Bogenpfeile innen, Beschriftung noch weiter innen
UEBERGANG = [
    (0,   "+ RH", "&#8722; H&#8322;O"),
    (45,  "+ e&#8315;", "aus NADPH"),
    (90,  "+ O&#8322;", ""),
    (135, "+ e&#8315;", "aus NADPH"),
    (180, "+ H&#8314;", ""),
    (225, "+ H&#8314;", "&#8722; H&#8322;O"),
    (270, "&#8722; H&#8226;", "Abstraktion"),
    (315, "&#8722; ROH", "Rebound"),
]
for grad, oben, unten in UEBERGANG:
    t.ringpfeil(CX, CY, RA, grad + 11, grad + 34)
    lx, ly = ort(grad + 22.5, RL)
    t.text(lx, ly, oben, size=11, anchor="middle", gewicht=700, farbe=E)
    if unten:
        t.text(lx, ly + 14, unten, size=9.5, anchor="middle", farbe=G)

t.text(CX, CY - 8, "P450", size=13, anchor="middle", gewicht=700, farbe=G)
t.text(CX, CY + 10, "ein Zyklus,", size=10.5, anchor="middle", farbe=G)
t.text(CX, CY + 24, "über fünfzig Isoformen", size=10.5, anchor="middle", farbe=G)

# Entkopplung: zwei kurze Abzweige und eine gemeinsame Erklaerung darunter
t.linie(462, 606, 508, 648, farbe=W, breite=1.4, strich="4 3")
t.text(516, 656, "O&#8322;&#8226;&#8315;", size=11, farbe=W, gewicht=700)
t.linie(140, 606, 96, 648, farbe=W, breite=1.4, strich="4 3")
t.text(86, 656, "H&#8322;O&#8322;", size=11, anchor="end", farbe=W, gewicht=700)
t.text(20, 700, "Entkopplung: bricht der Zyklus vorzeitig ab, entweicht aus &#9315; Superoxid, "
                "aus &#9317; Wasserstoffperoxid.", size=11.5, farbe=G)

# Legende rechts
t.kasten(620, 78, 360, 300, fill="var(--surface-2)")
t.text(638, 100, "DIE ACHT ZUSTÄNDE", size=11, gewicht=700, farbe=G)
LEGENDE = [
    ("&#9312;", "Fe(III)&#183;H&#8322;O", "Ruhezustand, low spin"),
    ("&#9313;", "Fe(III)&#183;RH", "Wasser verdrängt, high spin"),
    ("&#9314;", "Fe(II)&#183;RH", "nach dem ersten Elektron"),
    ("&#9315;", "Fe(II)&#8722;O&#8322;", "Oxy-Komplex, noch harmlos"),
    ("&#9316;", "Fe(III)&#8722;O&#8722;O&#8315;", "Peroxo, nach dem zweiten Elektron"),
    ("&#9317;", "Fe(III)&#8722;OOH", "Hydroperoxo, Compound 0"),
    ("&#9318;", "Fe(IV)=O, Porphyrin&#8226;&#8314;", "Compound I — das Oxidans"),
    ("&#9319;", "Fe(III)&#8722;OH, R&#8226;", "Radikalpaar im Käfig"),
]
for i, (nr, form, was) in enumerate(LEGENDE):
    y = 128 + i * 31
    t.text(640, y, nr, size=12.5, gewicht=700, farbe=G)
    t.text(660, y, form, size=12.5, gewicht=700, farbe=W)
    t.text(660, y + 14, was, size=10.5, farbe=G)

t.kasten(620, 396, 360, 164, fill="var(--cofaktor-bg)", stroke=C)
t.text(638, 418, "WARUM DER FÜNFTE LIGAND ENTSCHEIDET", size=11, gewicht=700, farbe=C)
t.text(638, 440, "Am Eisen sitzt unten ein Cystein-Thiolat, beim", size=12.5)
t.text(638, 459, "Hämoglobin dagegen ein Histidin. Der Schwefel", size=12.5)
t.text(638, 478, "schiebt Elektronendichte auf das Eisen und", size=12.5)
t.text(638, 497, "erzwingt die heterolytische Spaltung der", size=12.5)
t.text(638, 516, "O&#8722;O-Bindung. Nur so entsteht ein Oxidans, das", size=12.5)
t.text(638, 535, "die C&#8722;H-Bindung eines Alkans angreifen kann.", size=12.5)

t.kasten(620, 578, 360, 122, fill="var(--drug-bg)", stroke=R)
t.text(638, 600, "DREI ARTEN VON INTERAKTION", size=11, gewicht=700, farbe=R)
t.text(638, 622, "Kompetitiv — zwei Substrate am selben Enzym.", size=12.5)
t.text(638, 645, "Koordinativ — Azole binden mit einem Ring-", size=12.5)
t.text(638, 664, "Stickstoff direkt ans Häm-Eisen.", size=12.5)
t.text(638, 687, "Mechanismusbasiert — Ritonavir, Clarithromycin.", size=12.5)

# ===================================================== ZONE B · O-O-Spaltung
t.zone(748, "B · &#9317; → &#9318;  DIE HETEROLYTISCHE SPALTUNG — HIER ENTSTEHT DAS OXIDANS")
t.text(20, 778, "Das distale Sauerstoffatom wird protoniert und geht als Wasser ab. Beide "
                "Elektronen der O&#8722;O-Bindung nehmen es mit.", size=12.5)

z0 = t.zentrum(150, 890, "Fe(III)", axial=["O", "OH&#8322;"],
               name="Compound 0, protoniert")

# Beide Pfeile enden dort, wo ein Chemiker sie enden liesse: der eine im Raum
# neben der Abgangsgruppe, der andere am Eisen, ausgehend vom Thiolat-Paar.
wasser = t.marke(232, 826, "abgehendes Wasser")
t.pfeil(z0.axb(0, 1), wasser, bogen=0.30, seite=1, farbe=W)
t.text(240, 822, "geht als H&#8322;O ab", size=10.5, farbe=W, gewicht=700)
t.text(240, 838, "mit beiden Bindungselektronen", size=10.5, farbe=G)

lp_s = t.paar(96, 912, 30, "Cystein-Thiolat")
t.pfeil(lp_s, z0.fe(), bogen=0.24, seite=-1, farbe=W)
t.text(20, 944, "Schub vom Thiolat", size=10.5, farbe=W, gewicht=700)
t.text(150, 968, "protonierter Hydroperoxo-Komplex", size=10.5, anchor="middle", farbe=G)

t.reaktionspfeil(370, 890, 440)
t.text(405, 880, "&#8722; H&#8322;O", size=11, anchor="middle", gewicht=700, farbe=E)

z1 = t.zentrum(506, 890, "Fe(IV)", axial=["O"], doppelt=True, radikal=True,
               name="Compound I")
t.text(506, 946, "Compound I", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(506, 960, "Fe(IV)=O plus Porphyrin-Radikalkation", size=10.5, anchor="middle", farbe=G)

t.kasten(578, 800, 402, 168, fill="var(--surface-2)")
t.text(596, 822, "WARUM NICHT HOMOLYTISCH", size=11, gewicht=700, farbe=G)
t.text(596, 844, "Bräche die O&#8722;O-Bindung homolytisch, entstünden zwei", size=12.5)
t.text(596, 863, "Radikale und das Enzym würde sich selbst zerstören.", size=12.5)
t.text(596, 886, "Das Thiolat verhindert das: Es stabilisiert die höhere", size=12.5)
t.text(596, 905, "Oxidationsstufe am Eisen so weit, dass der heterolytische", size=12.5)
t.text(596, 924, "Weg günstiger wird. Die zweite Oxidationsäquivalenz", size=12.5)
t.text(596, 943, "lagert das Porphyrin als Radikalkation zwischen.", size=12.5)

# ===================================================== ZONE C · Abstraktion und Rebound
t.zone(1006, "C · &#9318; → &#9319; → &#9312;  ABSTRAKTION UND REBOUND — BEIDE SCHRITTE RADIKALISCH")
t.text(20, 1036, "Compound I holt sich zuerst ein Wasserstoffatom, dann fällt die Hydroxylgruppe "
                 "auf das entstandene Kohlenstoffradikal zurück. Der Rebound ist so", size=12.5)
t.text(20, 1056, "schnell, dass sich das Radikal in aller Regel nicht umlagert — daran lässt sich "
                 "der Mechanismus experimentell prüfen.", size=12.5)

zc1 = t.zentrum(84, 1150, "Fe(IV)", axial=["O"], doppelt=True, radikal=True,
                name="Compound I")
ibu = mech.Molekuel("CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O", 268, 1146,
                    wasserstoff=[1], zeige={1: "links"}, name="Ibuprofen")
t.mole.append(ibu)
hidx = ibu.h_index[1]

t.pfeil((ibu, 1, hidx), zc1.ax(0), bogen=0.20, seite=-1, typ="fischhaken", farbe=R)
t.pfeil((ibu, 1, hidx), (ibu, 1), bogen=0.55, seite=1, typ="fischhaken", farbe=R,
        mindestbogen=20)
t.unterschrift(ibu, "Ibuprofen — angegriffen wird die schwächste C&#8722;H-Bindung,",
               "das tertiäre Kohlenstoffatom der Isobutylgruppe")
t.text(84, 1206, "Compound I", size=10.5, anchor="middle", gewicht=700, farbe=W)

t.reaktionspfeil(432, 1146, 496)
t.text(464, 1136, "H&#8226;", size=11, anchor="middle", gewicht=700, farbe=E)

zc2 = t.zentrum(566, 1150, "Fe(III)", axial=["OH"], name="Fe(III)-Hydroxo")
ibr = mech.Molekuel("CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O", 750, 1146,
                    zeige={1: "links"}, name="Ibuprofen-Radikal")
t.mole.append(ibr)

e1 = t.einzelelektron(ibr, 1, 180)
t.pfeil(e1, zc2.ax(0), bogen=0.20, seite=-1, typ="fischhaken", farbe=R)
t.pfeil(zc2.axb(-1, 0), zc2.ax(0), bogen=0.55, seite=1, typ="fischhaken", farbe=R,
        mindestbogen=20)
t.unterschrift(ibr, "Kohlenstoffradikal — die Hydroxylgruppe fällt zurück,",
               "es entsteht 2-Hydroxyibuprofen (CYP2C9)")
t.text(566, 1206, "Fe(III)&#8722;OH", size=10.5, anchor="middle", gewicht=700, farbe=W)

# ===================================================== ZONE D · Bilanz
t.zone(1250, "D · WAS SICH DARAUS ABLEITEN LÄSST")
t.text(20, 1280, "Die Bilanz lautet R&#8722;H + O&#8322; + NADPH + H&#8314; → R&#8722;OH + "
                 "H&#8322;O + NADP&#8314;. Von den beiden Sauerstoffatomen geht eines ins "
                 "Substrat, eines ins Wasser — daher der Name", size=12.5)
t.text(20, 1300, "Monooxygenase, und daher der NADPH-Verbrauch, der die Biotransformation an den "
                 "Pentosephosphatweg koppelt.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Der katalytische Zyklus des Cytochrom P450 in vier Zonen. Zone A zeigt acht Eisenzentren "
    "im Kreis, jedes mit dem Porphyrin als Balken, dem Cystein-Thiolat darunter und dem "
    "axialen Liganden darueber: wassergebundenes Eisen drei, dann Substratbindung, erste "
    "Reduktion zu Eisen zwei, Sauerstoffanlagerung, zweite Reduktion zum Peroxokomplex, "
    "Protonierung zum Hydroperoxo, Compound eins mit Eisen vier gleich Sauerstoff und "
    "Porphyrin-Radikalkation, schliesslich das Hydroxo-Eisen mit dem Substratradikal. "
    "Zone B zeigt mit Elektronenpaarpfeilen, wie die Sauerstoff-Sauerstoff-Bindung "
    "heterolytisch bricht, wobei das Thiolat Elektronendichte auf das Eisen schiebt und "
    "Wasser abgeht. Zone C zeigt mit Fischhakenpfeilen die Abstraktion eines Wasserstoffatoms "
    "vom tertiaeren Kohlenstoff des Ibuprofens und den anschliessenden Rebound der "
    "Hydroxylgruppe auf das Kohlenstoffradikal."
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

mech.speichern("m08", t.svg(ARIA), t)
