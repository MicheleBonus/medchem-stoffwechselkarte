# -*- coding: utf-8 -*-
"""
M-02 · Thiaminpyrophosphat, gebaut mit mech.py.

Der Thiazoliumring war bisher ein handgesetztes Fuenfeck mit angehaengten
Textstuecken. Jetzt sind alle vier Stufen - Thiazolium, Ylid, 2-Lactyl-TPP und
Enamin - echte Strukturen, und die Umpolung ist mit Pfeilen ausgefuehrt.
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

THIAZ = "Cc1c(*)sc[n+]1*"
YLID = "Cc1c(*)s[c-][n+]1*"
LACTYL = "Cc1c(*)sc(C(C)(O)C(=O)[O-])[n+]1*"
ENAMIN = "CC1=C(*)SC(=C(C)O)N1*"
# atomLabel geht direkt in das SVG - HTML-Entitaeten werden dort nicht
# dekodiert, es muss echter Unicode sein.
RESTE = {3: "OPP", 7: "Pyrimidin"}
RESTE_L = {3: "OPP", 13: "Pyrimidin"}
RESTE_E = {3: "OPP", 10: "Pyrimidin"}

t = mech.Tafel(1000, 1200)

# ===================================================== ZONE A · das Ylid
t.zone(24, "A · EIN UNGEWÖHNLICH SAURES WASSERSTOFFATOM")
t.text(20, 54, "Das Wasserstoffatom am C2 des Thiazoliumrings hat einen pK<tspan "
               "baseline-shift='sub' font-size='9'>a</tspan> um 18 — für ein "
               "Kohlenstoff-Wasserstoff-Atom ungewöhnlich niedrig. Eine gewöhnliche", size=12.5)
t.text(20, 73, "Base des Enzyms genügt, um es abzuziehen.", size=12.5)

thia = mech.Molekuel(THIAZ, 160, 216, labels=RESTE, wasserstoff=[5],
                     zeige={5: "oben"}, name="Thiazolium")
t.mole.append(thia)
ht = thia.h_index[5]
t.atomnummer(thia, 5, "C2", winkel=200, abstand=40, size=10.5, farbe=W, gewicht=700)
base = t.paar(160, 132, 270, "Base des Enzyms")
t.text(160, 116, "B&#8315;", size=12.5, anchor="middle", gewicht=700, farbe=E)
t.text(160, 100, "eine Base des Enzyms", size=10, anchor="middle", farbe=G)
t.pfeil(base, (thia, 5, ht), bogen=0.26, seite=1, farbe=W)
t.pfeil((thia, 5, ht), thia.abseits(5, ht), bogen=0.45, seite=-1, farbe=W)
t.unterschrift(thia, "Thiazolium — das C2 sitzt zwischen", "Schwefel und Ammonium", abstand=32)

t.reaktionspfeil(276, 216, 350)
t.text(313, 242, "&#8722; H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ylid = mech.Molekuel(YLID, 460, 216, labels=RESTE, zeige={5: "oben"}, name="Ylid")
t.mole.append(ylid)
t.elektronenpaar(ylid, 5, 270)
t.unterschrift(ylid, "das Ylid — Carbanion und Ammonium", "im selben Molekül", abstand=32)

t.kasten(600, 108, 380, 152, fill="var(--cofaktor-bg)", stroke=C)
t.text(618, 130, "WARUM DAS FUNKTIONIERT", size=11, gewicht=700, farbe=C)
t.text(618, 152, "Ein Carbanion ist für sich genommen nicht haltbar.", size=12.5)
t.text(618, 171, "Hier sitzt es direkt neben einem quartären, positiv", size=12.5)
t.text(618, 190, "geladenen Stickstoff; beide Ladungen gleichen sich", size=12.5)
t.text(618, 209, "aus. Das Ergebnis ist ein Ylid.", size=12.5)
t.text(618, 232, "Derselbe Kunstgriff wie beim PLP (Tafel M-01): ein", size=12.5)
t.text(618, 251, "positiv geladener Ringstickstoff nimmt Ladung auf.", size=12.5)

# ===================================================== ZONE B · die Umpolung
t.zone(320, "B · DIE UMPOLUNG — AUS EINEM ELEKTROPHIL WIRD EIN NUCLEOPHIL")
t.text(20, 350, "Das Ylid greift den Ketokohlenstoff des Pyruvats an. Nach Abgang von "
                "Kohlendioxid trägt derselbe Kohlenstoff plötzlich negative Ladungsdichte.",
       size=12.5)

ylid2 = mech.Molekuel(YLID, 140, 464, labels=RESTE, zeige={5: "rechts"}, name="Ylid")
t.mole.append(ylid2)
lp_y = t.elektronenpaar(ylid2, 5, 0)

pyr = mech.Molekuel("CC(=O)C(=O)[O-]", 372, 442, zeige={1: "links"}, name="Pyruvat")
t.mole.append(pyr)
t.pfeil(lp_y, (pyr, 1), bogen=0.24, seite=-1, farbe=W)
t.pfeil((pyr, 1, 2), (pyr, 2), bogen=0.45, seite=1, farbe=W)
# Die Marke "Keto-C" liess sich nirgends kollisionsfrei setzen und ist neben
# der Unterschrift ohnehin redundant.
t.unterschrift(ylid2, "das Ylid greift an", abstand=30)
t.unterschrift(pyr, "Pyruvat — der Ketokohlenstoff", "ist hier noch elektrophil", abstand=30)

t.reaktionspfeil(494, 464, 560)

lac = mech.Molekuel(LACTYL, 700, 464, labels=RESTE_L, zeige={5: "links"},
                    name="2-Lactyl-TPP")
t.mole.append(lac)
t.unterschrift(lac, "2-Lactyl-TPP — das Addukt", abstand=30)

# --- zweite Reihe: Decarboxylierung
# Fuer die Decarboxylierung so drehen, dass das Carboxylat nach oben in
# freien Raum zeigt - am quartaeren C6 ist sonst kein Platz fuer die Pfeile.
lac2 = mech.Molekuel(LACTYL, 180, 740, labels=RESTE_L,
                     zeige={9: "oben", 5: "unten"}, name="2-Lactyl-TPP")
t.mole.append(lac2)
# Nur ein Pfeil: C6 ist quartaer, fuer einen zweiten ist dort kein Platz.
# Wohin die Elektronen weiterwandern, sagt die Unterschrift.
t.pfeil((lac2, 6, 9), lac2.aussen(6, abstand=40), bogen=0.36, seite=-1, farbe=W)
t.unterschrift(lac2, "die C&#8722;C-Bindung bricht, die Elektronen bleiben am Kohlenstoff",
               "und bilden mit dem Ring die Doppelbindung des Enamins", abstand=32)

t.reaktionspfeil(330, 720, 404)
t.text(367, 710, "&#8722; CO&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ena = mech.Molekuel(ENAMIN, 540, 720, labels=RESTE_E, zeige={5: "links"}, name="Enamin")
t.mole.append(ena)
t.unterschrift(ena, "Enamin — der „aktivierte Aldehyd“", abstand=32, farbe=W, gewicht=700)

t.kasten(680, 632, 300, 176, fill="var(--surface-2)")
t.text(698, 654, "DERSELBE KOHLENSTOFF, VIER WEGE", size=11, gewicht=700, farbe=G)
t.text(698, 676, "Im Pyruvat war er elektrophil, jetzt ist er", size=12)
t.text(698, 695, "nucleophil. Was mit ihm geschieht, entscheidet", size=12)
t.text(698, 714, "allein das Enzym:", size=12)
t.text(698, 738, "+ H&#8314; → Acetaldehyd (Pyruvat-Decarboxylase)", size=12, farbe=E)
t.text(698, 757, "+ Liponamid → Acetyl-CoA (PDH)", size=12, farbe=E)
t.text(698, 776, "+ Aldose → C&#8322;-Übertragung (Transketolase)", size=12, farbe=E)
t.text(698, 795, "+ α-Ketosäure → Acyloin (α-KGDH)", size=12, farbe=E)

# ===================================================== ZONE C · Thiaminmangel
t.zone(866, "C · WAS BEI THIAMINMANGEL AUSFÄLLT")
t.text(20, 896, "Drei Enzyme gleichzeitig — und alle drei sitzen an Engstellen des "
                "Energiestoffwechsels.", size=12.5)

MANGEL = [
    (20, "Pyruvat-Dehydrogenase", "Pyruvat staut sich vor dem Citratzyklus und wird zu",
     "Laktat reduziert. Klinisch: Laktatazidose."),
    (350, "α-Ketoglutarat-Dehydrogenase", "Der Citratzyklus stockt an seiner zweiten",
     "Decarboxylierung. Die ATP-Ausbeute bricht ein."),
    (680, "Transketolase", "Der nicht-oxidative Teil des Pentosephosphatwegs",
     "fällt aus — deshalb der Aktivitätstest im Erythrozyten."),
]
for x, enzym, z1, z2 in MANGEL:
    t.text(x, 934, enzym, size=12.5, gewicht=700, farbe=E)
    t.text(x, 956, z1, size=12)
    t.text(x, 975, z2, size=12)

t.kasten(20, 1000, 960, 76, fill="var(--warn-bg)", stroke=W)
t.text(38, 1022, "DIE REIHENFOLGE ENTSCHEIDET", size=11, gewicht=700, farbe=W)
t.text(38, 1044, "Weil das Gehirn seinen Energiebedarf fast ausschließlich aus Glucose deckt, "
                 "trifft es der Ausfall zuerst. Deshalb wird Thiamin vor einer", size=12.5)
t.text(38, 1063, "Glucoseinfusion gegeben — sonst verbraucht die einsetzende Glykolyse den "
                 "letzten Rest des Cofaktors und löst die Wernicke-Enzephalopathie aus.",
       size=12.5)

t.text(20, 1120, "Der Vergleich mit Tafel M-01 lohnt sich: Beide Cofaktoren stabilisieren ein "
                 "Carbanion mit einem positiv geladenen Ringstickstoff. PLP tut das an einer "
                 "Aminosäure,", size=12.5, farbe=G)
t.text(20, 1140, "TPP an einer α-Ketosäure — zwei ganz verschiedene Reaktionsklassen aus "
                 "demselben elektronischen Prinzip.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Thiaminpyrophosphat in drei Zonen. Zone A zeigt, wie eine Base des Enzyms mit einem "
    "Elektronenpaarpfeil das Wasserstoffatom vom Kohlenstoff zwei des Thiazoliumrings abzieht; "
    "das entstehende Carbanion wird vom benachbarten positiv geladenen Stickstoff als Ylid "
    "stabilisiert. Zone B zeigt die Umpolung: Das Ylid greift den Ketokohlenstoff des Pyruvats "
    "an, es entsteht 2-Lactyl-Thiaminpyrophosphat. In der zweiten Reihe bricht die "
    "Kohlenstoff-Kohlenstoff-Bindung zur Carboxylatgruppe, Kohlendioxid geht ab, und die "
    "Elektronen bilden die Doppelbindung zum Ring: das Enamin, der sogenannte aktivierte "
    "Aldehyd. Derselbe Kohlenstoff, der im Pyruvat elektrophil war, ist jetzt nucleophil. Zone C "
    "nennt die drei Enzyme, die bei Thiaminmangel gleichzeitig ausfallen."
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

mech.speichern("m02", t.svg(ARIA), t)
