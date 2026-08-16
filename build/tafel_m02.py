# -*- coding: utf-8 -*-
"""
M-02 · Thiaminpyrophosphat, gebaut mit mech.py.

Der Thiazoliumring war bisher ein handgesetztes Fuenfeck mit angehaengten
Textstuecken. Jetzt sind alle vier Stufen (Thiazolium, Ylid, 2-Lactyl-TPP und
Enamin) echte Strukturen, und die Umpolung ist mit Pfeilen ausgefuehrt.
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

# Die beiden Bruecken sind mitgezeichnet: C5 traegt -CH2-CH2-OPP, N3 traegt
# -CH2-Pyrimidin. Haengt man "OPP" und "Pyrimidin" direkt an den Ring, liest
# sich das C5-OPP als Enolphosphat und der Pyrimidinring als N-Aryl.
THIAZ = "Cc1c(CC*)sc[n+]1C*"
YLID = "Cc1c(CC*)s[c-][n+]1C*"
LACTYL = "Cc1c(CC*)sc(C(C)(O)C(=O)[O-])[n+]1C*"
ENAMIN = "CC1=C(CC*)SC(=C(C)O)N1C*"
# atomLabel geht direkt in das SVG; HTML-Entitaeten werden dort nicht
# dekodiert, es muss echter Unicode sein.
RESTE = {5: "OPP", 10: "Pyrimidin"}
RESTE_L = {5: "OPP", 16: "Pyrimidin"}
RESTE_E = {5: "OPP", 13: "Pyrimidin"}

t = mech.Tafel(1000, 1290)

# ===================================================== ZONE A · das Ylid
t.zone(24, "A · EIN UNGEWÖHNLICH SAURES WASSERSTOFFATOM")
t.text(20, 54, "Das Wasserstoffatom am C2 des Thiazoliumrings hat einen pK<tspan "
               "baseline-shift='sub' font-size='9'>a</tspan> um 18. Für eine "
               "Kohlenstoff-Wasserstoff-Bindung ist das ungewöhnlich sauer;", size=12.5)
t.text(20, 73, "für eine Base des Enzyms bleibt es trotzdem unerreichbar. Abgezogen wird es "
               "dennoch, und zwar vom Cofaktor selbst.", size=12.5)

t.text(170, 134, "der Iminostickstoff des Aminopyrimidins", size=10, anchor="middle", farbe=G)
t.text(170, 150, "Imino-N", size=12.5, anchor="middle", gewicht=700, farbe=C)
base = t.paar(170, 166, 270, "Iminostickstoff des Aminopyrimidins")

thia = mech.Molekuel(THIAZ, 170, 252, labels=RESTE, wasserstoff=[7],
                     zeige={7: "oben"}, name="Thiazolium")
t.mole.append(thia)
ht = thia.h_index[7]
t.atomnummer(thia, 7, "C2", winkel=200, abstand=40, size=10.5, farbe=W, gewicht=700)
# Eine Base greift den Wasserstoffkern an, nicht die Mitte der C-H-Bindung:
# der Pfeil endet am Wasserstoffatom.
t.pfeil(base, (thia, ht), bogen=0.16, seite=1, farbe=W, gap=2.5, mindestbogen=7.0)
# Das Elektronenpaar der C-H-Bindung bleibt am C2 und wird dort zum freien Paar
# des Ylids. Ein Punkt "neben dem C2, vom Wasserstoff weg" laege mitten im Ring,
# und der Pfeilkopf zeigte dann auf den Stickstoff. Bezugspunkt ist deshalb das
# Ringstickstoffatom: der Pfeil endet auf der davon abgewandten Seite des C2.
t.pfeil((thia, 7, ht), thia.abseits(7, 8, abstand=20), bogen=0.45, seite=-1, farbe=W)
t.unterschrift(thia, "Thiazolium: das C2 sitzt zwischen", "Schwefel und Ammonium", abstand=32)

t.reaktionspfeil(300, 252, 376)
t.text(338, 278, "&#8722; H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ylid = mech.Molekuel(YLID, 470, 252, labels=RESTE, zeige={7: "oben"}, name="Ylid")
t.mole.append(ylid)
t.elektronenpaar(ylid, 7, 270)
t.unterschrift(ylid, "das Ylid: Carbanion und Ammonium", "im selben Molekül", abstand=32)

t.kasten(600, 100, 380, 258, fill="var(--cofaktor-bg)", stroke=C)
t.text(618, 122, "WARUM DAS TROTZDEM GELINGT", size=11, gewicht=700, farbe=C)
t.text(618, 144, "Ein Glutamat oder Histidin des Enzyms liegt elf bis", size=12)
t.text(618, 163, "vierzehn Größenordnungen darunter; thermodynamisch", size=12)
t.text(618, 182, "kann keines dieses Proton abziehen.", size=12)
t.text(618, 205, "Der Akzeptor ist der Cofaktor selbst. Ein Glutamat", size=12)
t.text(618, 224, "protoniert den Aminopyrimidinring, der dadurch ins", size=12)
t.text(618, 243, "Iminotautomer übergeht. Die V-förmige Konformation", size=12)
t.text(618, 262, "legt dessen Iminostickstoff neben das C2: Base und", size=12)
t.text(618, 281, "Proton sind schon Nachbarn, das Ylid entsteht als", size=12)
t.text(618, 300, "Zwitterion.", size=12)
t.text(618, 323, "Sein Anteil bleibt winzig, stellt sich aber in", size=12, farbe=G)
t.text(618, 342, "Millisekunden ein. Kinetisch genügt das.", size=12, farbe=G)

# ===================================================== ZONE B · die Umpolung
t.zone(384, "B · DIE UMPOLUNG: AUS EINEM ELEKTROPHIL WIRD EIN NUCLEOPHIL")
t.text(20, 414, "Das Ylid greift den Ketokohlenstoff des Pyruvats an. Nach Abgang von "
                "Kohlendioxid trägt derselbe Kohlenstoff plötzlich negative Ladungsdichte.",
       size=12.5)

ylid2 = mech.Molekuel(YLID, 170, 545, labels=RESTE, zeige={7: "rechts"}, name="Ylid")
t.mole.append(ylid2)
lp_y = t.elektronenpaar(ylid2, 7, 0)

pyr = mech.Molekuel("CC(=O)C(=O)[O-]", 390, 522, zeige={1: "links"}, name="Pyruvat")
t.mole.append(pyr)
t.pfeil(lp_y, (pyr, 1), bogen=0.24, seite=-1, farbe=W)
t.pfeil((pyr, 1, 2), pyr.abseits(2, 1, abstand=18), bogen=0.40, seite=1, farbe=W)
# Die Marke "Keto-C" liess sich nirgends kollisionsfrei setzen und ist neben
# der Unterschrift ohnehin redundant.
t.unterschrift(ylid2, "das Ylid greift an", abstand=30)
t.unterschrift(pyr, "Pyruvat: der Ketokohlenstoff", "ist hier noch elektrophil", abstand=30)

t.reaktionspfeil(512, 545, 588)
# Der Angriff liefert zunaechst das Alkoholat; die gezeichnete OH-Gruppe
# entsteht erst durch Protonierung, sonst fehlt der Bilanz ein H+.
t.text(550, 533, "+ H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

lac = mech.Molekuel(LACTYL, 744, 545, labels=RESTE_L, zeige={7: "links"},
                    name="2-Lactyl-TPP")
t.mole.append(lac)
t.unterschrift(lac, "2-Lactyl-TPP, das Addukt", abstand=30)

# --- zweite Reihe: Decarboxylierung
# Fuer die Decarboxylierung so drehen, dass das Carboxylat nach oben in
# freien Raum zeigt; am quartaeren Kohlenstoff ist sonst kein Platz fuer die
# Pfeile.
lac2 = mech.Molekuel(LACTYL, 190, 800, labels=RESTE_L,
                     zeige={11: "oben", 7: "unten"}, name="2-Lactyl-TPP")
t.mole.append(lac2)
# Zwei Pfeile: die brechende C-C-Bindung bildet die Doppelbindung zum Ring,
# und das Pi-Paar der C=N+-Bindung weicht auf den Stickstoff aus. Nur so ist
# erklaert, warum der Ringstickstoff im naechsten Bild neutral ist.
t.pfeil((lac2, 8, 11), (lac2, 7, 8), bogen=0.40, seite=-1, farbe=W)
t.pfeil((lac2, 7, 14), lac2.abseits(14, 7, abstand=20), bogen=0.34, seite=1, farbe=W)
t.unterschrift(lac2, "die C&#8722;C-Bindung bricht, die Elektronen bilden die",
               "Doppelbindung zum Ring, und das π-Paar der",
               "C=N&#8314;-Bindung geht auf den Stickstoff", abstand=32)

t.reaktionspfeil(340, 780, 414)
t.text(377, 770, "&#8722; CO&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ena = mech.Molekuel(ENAMIN, 560, 790, labels=RESTE_E, zeige={7: "links"}, name="Enamin")
t.mole.append(ena)
t.unterschrift(ena, "Enamin: der „aktivierte Aldehyd“", abstand=32, farbe=W, gewicht=700)

t.kasten(680, 722, 300, 198, fill="var(--surface-2)")
t.text(698, 744, "DERSELBE KOHLENSTOFF, VIER ENZYME", size=11, gewicht=700, farbe=G)
t.text(698, 766, "Im Pyruvat war er elektrophil, jetzt ist er", size=12)
t.text(698, 785, "nucleophil. Was aus ihm wird, entscheidet", size=12)
t.text(698, 804, "allein das Enzym:", size=12)
t.text(698, 828, "+ H&#8314; → Acetaldehyd (Pyruvat-Decarboxylase)", size=12, farbe=E)
t.text(698, 847, "+ Liponamid → Acetyl-CoA (PDH)", size=12, farbe=E)
t.text(698, 866, "+ Liponamid → Succinyl-CoA (α-KGDH)", size=12, farbe=E)
t.text(698, 885, "+ Aldose → C&#8322;-Übertragung (Transketolase)", size=12, farbe=E)
t.text(698, 906, "(die α-KGDH mit α-Ketoglutarat statt Pyruvat)", size=11, farbe=G)

# ===================================================== ZONE C · Thiaminmangel
t.zone(956, "C · WAS BEI THIAMINMANGEL AUSFÄLLT")
t.text(20, 986, "Drei Enzyme fallen gleichzeitig aus, und alle drei sitzen an Engstellen des "
                "Energiestoffwechsels.", size=12.5)

MANGEL = [
    (20, "Pyruvat-Dehydrogenase", "Pyruvat staut sich vor dem Citratzyklus und wird zu",
     "Laktat reduziert. Klinisch: Laktatazidose."),
    (350, "α-Ketoglutarat-Dehydrogenase", "Der Citratzyklus stockt an seiner zweiten",
     "Decarboxylierung. Die ATP-Ausbeute bricht ein."),
    (680, "Transketolase", "Der nicht-oxidative Teil des Pentosephosphatwegs",
     "fällt aus. Daher der Aktivitätstest im Erythrozyten."),
]
for x, enzym, z1, z2 in MANGEL:
    t.text(x, 1024, enzym, size=12.5, gewicht=700, farbe=E)
    t.text(x, 1046, z1, size=12)
    t.text(x, 1065, z2, size=12)

t.kasten(20, 1090, 960, 76, fill="var(--warn-bg)", stroke=W)
t.text(38, 1112, "DIE REIHENFOLGE ENTSCHEIDET", size=11, gewicht=700, farbe=W)
t.text(38, 1134, "Weil das Gehirn seinen Energiebedarf fast ausschließlich aus Glucose deckt, "
                 "trifft es der Ausfall zuerst. Deshalb wird Thiamin vor einer", size=12.5)
t.text(38, 1153, "Glucoseinfusion gegeben. Sonst verbraucht die einsetzende Glykolyse den "
                 "letzten Rest des Cofaktors und löst die Wernicke-Enzephalopathie aus.",
       size=12.5)

t.text(20, 1210, "Der Vergleich mit Tafel M-01 lohnt sich: Beide Cofaktoren stabilisieren ein "
                 "Carbanion mit einem positiv geladenen Ringstickstoff. PLP tut das an einer "
                 "Aminosäure,", size=12.5, farbe=G)
t.text(20, 1230, "TPP an einer α-Ketosäure. Daraus werden zwei ganz verschiedene "
                 "Reaktionsklassen aus demselben elektronischen Prinzip.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Thiaminpyrophosphat in drei Zonen. Zone A zeigt, wie das C2-Wasserstoffatom des "
    "Thiazoliumrings abgezogen wird. Der Protonenakzeptor ist kein Enzymrest, sondern der "
    "Cofaktor selbst: der Iminostickstoff des Aminopyrimidinrings, den die V-foermige "
    "Konformation unmittelbar neben das C2 legt. Ein Elektronenpaarpfeil geht von diesem "
    "Stickstoff auf das Wasserstoffatom, ein zweiter aus der Kohlenstoff-Wasserstoff-Bindung "
    "zurueck auf das C2. Das entstehende Carbanion wird vom benachbarten positiv geladenen "
    "Stickstoff als Ylid stabilisiert. Der Ylidanteil bleibt winzig, stellt sich aber in "
    "Millisekunden ein. Zone B zeigt die Umpolung: Das Ylid greift den Ketokohlenstoff des "
    "Pyruvats an, nach Protonierung entsteht 2-Lactyl-Thiaminpyrophosphat. In der zweiten Reihe "
    "bricht die Kohlenstoff-Kohlenstoff-Bindung zur Carboxylatgruppe, Kohlendioxid geht ab, die "
    "Elektronen bilden die Doppelbindung zum Ring, und das Pi-Paar der "
    "Kohlenstoff-Stickstoff-Doppelbindung weicht auf den Stickstoff aus. Es entsteht das Enamin, "
    "der sogenannte aktivierte Aldehyd. Derselbe Kohlenstoff, der im Pyruvat elektrophil war, ist "
    "jetzt nucleophil. Zone C nennt die drei Enzyme, die bei Thiaminmangel gleichzeitig ausfallen."
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
