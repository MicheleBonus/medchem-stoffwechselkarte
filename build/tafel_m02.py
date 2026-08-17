# -*- coding: utf-8 -*-
"""
M-02 · Thiaminpyrophosphat, gebaut mit mech.py.

Der Thiazoliumring war bisher ein handgesetztes Fuenfeck mit angehaengten
Textstuecken. Jetzt sind alle vier Stufen (Thiazolium, Ylid, 2-Lactyl-TPP und
Enamin) echte Strukturen, und die Umpolung ist mit Pfeilen ausgefuehrt.

Umgestellt auf die neue Pfeilsprache:

  - KERN legt alle vier Stufen auf dieselbe Referenzlage (mech_kerne.eigener).
    Der Thiazoliumring steht dadurch in jedem Bild gleich: C2 oben, Schwefel
    rechts, Ringstickstoff links mit dem Aminopyrimidin, C5 unten rechts mit dem
    Diphosphat. Das ist die Lehrbuchlage von TPP - Pyrimidin links, Thiazolium
    rechts - und sie haelt die Reaktionszentren nach oben in den freien Raum.
  - schub(quelle, ziel) sagt nur, welche Elektronen wohin gehen. Bauchseite,
    Oeffnungswinkel, Ankerlage und der Winkel jedes freien Elektronenpaars kommen
    aus dem Solver in mech_schub.py; geprueft wird gegen mech_regeln.py.

Von den sechs frueheren Pfeilen sind vier geblieben. Die beiden anderen gehoeren
zum selben Muster: ein Bindungspaar bleibt am eigenen Atom zurueck, und dieses
Atom traegt drei Bindungen, von denen eine auf der Winkelhalbierenden der beiden
uebrigen steht (das C2-H des Thiazoliums, das N-CH2 des Ringstickstoffs). Beide
sind mit der Pfeilart "zurueck" noch einmal angemeldet und wieder abgelehnt
worden; die Zaehler stehen an Ort und Stelle. Kurz: die freien Keile sind 108
und zweimal 126 Grad breit, ihre Mitten liegen 54 bis 63 Grad neben der
Quellbindung. Schwanz und Spitze auf derselben Seite dieser Bindung geben
hoechstens 0,44 L Sehne - das harte Fenster beginnt bei 0,50 L -, und jeder
Bogen, der das Fenster erreicht, hat Schwanz und Spitze auf verschiedenen Seiten
und muss die Quellbindung, eine Nachbarbindung oder das N+-Symbol durchqueren.
Zeichenbar wuerden beide erst, wenn die Spitze 0,74 bis 0,80 L vom Atom entfernt
stehen duerfte statt der zugelassenen 0,45 L; das ist der weit ausholende Haken,
den der Katalog unter Z3 verworfen hat. Alles daran ist massstabsfrei, bei
bindung=26 und bindung=31 nachgerechnet. Was die Elektronen tun, steht deshalb
in den Unterschriften.
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

# Das Leitgeruest: der Thiazoliumring ohne die beiden Bruecken. Das Muster ist
# ladungs- und aromatizitaetsagnostisch (~ als Bindung, [#7] statt n), sonst
# faende es das neutrale Enamin nicht. Es trifft alle vier Stufen.
# leit=1 ist das C4, folge=7 der im Ring darauf folgende Stickstoff; damit liegt
# neben der Drehung auch die Haendigkeit fest. -126 Grad stellen das C2 nach oben.
KERN = mech_kerne.eigener("thiazolium", "Cc1c(CC)sc[n+]1C",
                          muster="[#6]~[#6]1~[#6]~[#16]~[#6]~[#7]~1~[#6]",
                          ring=[1, 2, 5, 6, 7], leit=1, folge=7, winkel=-126.0)

t = mech.Tafel(1000, 1290)

# ===================================================== ZONE A · das Ylid
t.zone(24, "A · EIN UNGEWÖHNLICH SAURES WASSERSTOFFATOM")
t.text(20, 54, "Das Wasserstoffatom am C2 des Thiazoliumrings hat einen pK<tspan "
               "baseline-shift='sub' font-size='9'>a</tspan> um 18. Für eine "
               "Kohlenstoff-Wasserstoff-Bindung ist das ungewöhnlich sauer;", size=12.5)
t.text(20, 73, "für eine Base des Enzyms bleibt es trotzdem unerreichbar. Abgezogen wird es "
               "dennoch, und zwar vom Cofaktor selbst.", size=12.5)

t.text(180, 134, "der Iminostickstoff des Aminopyrimidins", size=10, anchor="middle", farbe=G)
t.text(180, 150, "Imino-N", size=12.5, anchor="middle", gewicht=700, farbe=C)
base = t.paar(180, 166, 270, "Iminostickstoff des Aminopyrimidins")

thia = t.mol(THIAZ, 180, 258, labels=RESTE, wasserstoff=[7], kern=KERN,
             name="Thiazolium")
ht = thia.h_index[7]
t.atomnummer(thia, 7, "C2", winkel=352, abstand=30, size=10.5, farbe=W, gewicht=700)
# Die Base greift den Wasserstoffkern an, nicht die Mitte der C-H-Bindung: der
# Pfeil endet am Wasserstoffatom.
t.schub(base, Atom(thia, ht))
# Der zweite Pfeil dieses Schrittes - das Bindungspaar der C-H-Bindung bleibt am
# C2 zurueck - ist nicht gezeichnet. Er ist als Rueckhaken angemeldet worden und
# an der Geometrie gescheitert, nachgemessen mit der jetzigen Pfeilsprache:
#   Am C2 stehen drei Bindungen (S bei 36, N bei 144, H bei 270 Grad), und das H
#   liegt genau auf der Winkelhalbierenden. Die freien Keile sind darum 108 und
#   zweimal 126 Grad breit; ihre Mitten liegen 63 Grad neben der C-H-Bindung.
#   Von den 108 Ankerpaaren liegen 68 im harten Sehnenfenster 0,50-1,05 L, und
#   alle 816 Boegen daraus kreuzen: 622 die eigene C-H-Bindung, der Rest die
#   C-S- oder die C-N-Bindung. Kreuzungsfrei bleiben nur die Boegen mit Schwanz
#   und Spitze auf derselben Seite der C-H-Bindung; deren laengste Sehne ist
#   0,447 L, und ihr Freiraum zu fremder Tinte betraegt 0,22 L (gefordert sind
#   0,25 L). Der Pfeil scheitert also zweifach.
#   Zeichenbar wuerde er erst, wenn die Spitze 0,80 L statt hoechstens 0,45 L vom
#   C2 entfernt stehen duerfte - das ist Levys weit um das Atom schwingender
#   Haken, den der Katalog unter Z3 ausdruecklich verworfen hat.
#   Alles daran ist massstabsfrei: bei bindung=26 und bindung=31 kommt derselbe
#   Befund heraus.
# Wo die Elektronen bleiben, sagt das freie Paar am C2 des Ylids nebenan.
t.unterschrift(thia, "Thiazolium: das C2 sitzt zwischen Schwefel und Ammonium;",
               "das Paar der C&#8722;H-Bindung bleibt an ihm zurück und wird",
               "zum freien Paar des Ylids", abstand=28)

t.reaktionspfeil(300, 258, 384)
t.text(342, 284, "&#8722; H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ylid = t.mol(YLID, 500, 258, labels=RESTE, kern=KERN, name="Ylid")
# Das Carbanion des Produkts. Der Kern setzt das C2 an die Ringspitze, also
# zeigt sein freies Paar nach oben.
t.elektronenpaar(ylid, 7, 270)
t.unterschrift(ylid, "das Ylid: Carbanion und Ammonium", "im selben Molekül", abstand=32)

t.kasten(620, 100, 360, 258, fill="var(--cofaktor-bg)", stroke=C)
t.text(638, 122, "WARUM DAS TROTZDEM GELINGT", size=11, gewicht=700, farbe=C)
t.text(638, 144, "Ein Glutamat oder Histidin des Enzyms liegt elf bis", size=12)
t.text(638, 163, "vierzehn Größenordnungen darunter; thermodynamisch", size=12)
t.text(638, 182, "kann keines dieses Proton abziehen.", size=12)
t.text(638, 205, "Der Akzeptor ist der Cofaktor selbst. Ein Glutamat", size=12)
t.text(638, 224, "protoniert den Aminopyrimidinring, der dadurch ins", size=12)
t.text(638, 243, "Iminotautomer übergeht. Die V-förmige Konformation", size=12)
t.text(638, 262, "legt dessen Iminostickstoff neben das C2: Base und", size=12)
t.text(638, 281, "Proton sind schon Nachbarn, das Ylid entsteht als", size=12)
t.text(638, 300, "Zwitterion.", size=12)
t.text(638, 323, "Sein Anteil bleibt winzig, stellt sich aber in", size=12, farbe=G)
t.text(638, 342, "Millisekunden ein. Kinetisch genügt das.", size=12, farbe=G)

# ===================================================== ZONE B · die Umpolung
t.zone(384, "B · DIE UMPOLUNG: AUS EINEM ELEKTROPHIL WIRD EIN NUCLEOPHIL")
t.text(20, 414, "Das Ylid greift den Ketokohlenstoff des Pyruvats an. Nach Abgang von "
                "Kohlendioxid trägt derselbe Kohlenstoff plötzlich negative Ladungsdichte.",
       size=12.5)

ylid2 = t.mol(YLID, 190, 585, labels=RESTE, kern=KERN, name="Ylid")

# Das Pyruvat steht schraeg darueber: das freie Paar des Ylids zeigt vom C2 an
# der Ringspitze nach oben, und dorthin greift es an. Die Unterschrift des
# Pyruvats steht ausnahmsweise darueber, weil unter ihm der Pfeil laeuft.
# Der Drehwinkel ist nicht beliebig, sondern am zweiten Pfeil gemessen: bei der
# frueheren Lage ("zeige") blieb dem Pfeil vom Pi-Paar der Carbonylbindung nur
# eine Sehne von 0,50 L, und seine Spitze zeigte 56 Grad am Sauerstoff vorbei.
# Bei 110 Grad wird die Sehne 0,56 L - im Buchfenster fuer den Rueckhaken -,
# die Spitze weicht nur noch 42 Grad ab, und der Freiraum steigt von 0,30 auf
# 0,51 L. Der Angriffspfeil wird dabei zugleich besser (Kopfabweichung 4 statt
# 14 Grad).
pyr = t.mol("CC(=O)C(=O)[O-]", 275, 505, rotate=110, name="Pyruvat")
# Ein Schritt: das freie Paar des Ylids bildet die neue C-C-Bindung, das
# Pi-Paar der Carbonylbindung weicht auf den Sauerstoff aus.
# Die beiden Pfeile treffen sich am Ketokohlenstoff selbst - der eine endet
# davor, der andere beginnt an dessen Carbonylbindung. Ihre Anker liegen deshalb
# konstruktionsbedingt knapp eine Bindungslaenge auseinander (0,91 L); das ist
# der Fall, fuer den mech_regeln.py das weitere Fenster "kette_atom" fuehrt.
t.schub(Paar(ylid2, 7), Atom(pyr, 1), kette="b")
t.schub(Bindung(pyr, 1, 2), Paar(pyr, 2), kette="b")
# Die Marke "Keto-C" liess sich nirgends kollisionsfrei setzen und ist neben
# der Unterschrift ohnehin redundant.
t.unterschrift(ylid2, "das Ylid greift an", abstand=30)
t.text(275, 452, "Pyruvat: der Ketokohlenstoff", size=10.5, anchor="middle", farbe=G)
t.text(275, 467, "ist hier noch elektrophil", size=10.5, anchor="middle", farbe=G)

t.reaktionspfeil(420, 570, 560)
# Der Angriff liefert zunaechst das Alkoholat; die gezeichnete OH-Gruppe
# entsteht erst durch Protonierung, sonst fehlt der Bilanz ein H+.
t.text(490, 558, "+ H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

lac = t.mol(LACTYL, 740, 570, labels=RESTE_L, kern=KERN, name="2-Lactyl-TPP")
t.unterschrift(lac, "2-Lactyl-TPP, das Addukt", abstand=30)

# --- zweite Reihe: Decarboxylierung
lac2 = t.mol(LACTYL, 200, 795, labels=RESTE_L, kern=KERN, name="2-Lactyl-TPP")
# Gezeichnet ist der Bindungsbruch: die brechende C-C-Bindung bildet die
# Doppelbindung zum Ring.
# art="ring" ist hier kein Ringpfeil im topologischen Sinn, sondern die
# Sehnenklasse: der Pfeil greift um ein einziges gemeinsames Atom herum, und dafuer
# gilt das kurze Fenster 0,60-0,90 L. Ohne die Angabe zielt der Solver auf die
# Mitte des Fensters fuer innermolekulare Pfeile (0,98 L), findet die passende
# Sehne nur auf der falschen Seite der brechenden Bindung und laesst den Bauch
# dann quer ueber genau die Bindung laufen, aus der die Elektronen kommen.
t.schub(Bindung(lac2, 8, 11), Bindung(lac2, 7, 8), art="ring")
# Der zweite Pfeil desselben Schrittes - das Pi-Paar der C=N+-Bindung weicht auf
# den Ringstickstoff aus - ist nicht gezeichnet, aus derselben Ursache wie in
# Zone A und ebenso nachgemessen:
#   Am N3 stehen drei Bindungen (C4 bei 72, das CH2-Pyrimidin bei 198, C2 bei
#   324 Grad); das CH2 liegt auf der Winkelhalbierenden, die Keilmitten liegen
#   wieder 63 bzw. 54 Grad neben der C=N+-Bindung. 68 der 108 Ankerpaare liegen
#   im harten Fenster 0,50-1,05 L, und alle 816 Boegen daraus kreuzen: 406 das
#   Glyphenrechteck des N+, 245 die eigene C=N+-Bindung, 98 die N-CH2- und 96
#   die N-C4-Bindung. Kreuzungsfrei bleibt nur, was auf derselben Seite der
#   C=N+-Bindung ansetzt und endet; dessen laengste Sehne ist 0,437 L.
#   Zeichenbar wuerde er ab einem Spitzenabstand von 0,74 L vom N3 (Sehne dann
#   0,50 L, Freiraum 0,47 L); erlaubt sind hoechstens 0,45 L. Auch das ist
#   massstabsfrei - bindung=26 und bindung=31 aendern nichts.
# Die Unterschrift sagt, wohin das Paar geht.
t.unterschrift(lac2, "die C&#8722;C-Bindung bricht, die Elektronen bilden die",
               "Doppelbindung zum Ring, und das π-Paar der",
               "C=N&#8314;-Bindung geht auf den Stickstoff", abstand=32)

t.reaktionspfeil(320, 783, 420)
t.text(370, 773, "&#8722; CO&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=W)

ena = t.mol(ENAMIN, 520, 800, labels=RESTE_E, kern=KERN, name="Enamin")
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
    "Stickstoff auf das Wasserstoffatom; das Bindungspaar der Kohlenstoff-Wasserstoff-Bindung "
    "bleibt am C2 zurueck und ist als freies Paar am Ylid daneben gezeichnet. "
    "Das entstehende Carbanion wird vom benachbarten positiv geladenen "
    "Stickstoff als Ylid stabilisiert. Der Ylidanteil bleibt winzig, stellt sich aber in "
    "Millisekunden ein. Zone B zeigt die Umpolung: Das Ylid greift den Ketokohlenstoff des "
    "Pyruvats an, nach Protonierung entsteht 2-Lactyl-Thiaminpyrophosphat. In der zweiten Reihe "
    "bricht die Kohlenstoff-Kohlenstoff-Bindung zur Carboxylatgruppe, Kohlendioxid geht ab, die "
    "Elektronen bilden die Doppelbindung zum Ring, und das Pi-Paar der "
    "Kohlenstoff-Stickstoff-Doppelbindung weicht auf den Stickstoff aus. Es entsteht das Enamin, "
    "der sogenannte aktivierte Aldehyd. Derselbe Kohlenstoff, der im Pyruvat elektrophil war, ist "
    "jetzt nucleophil. Der Thiazoliumring steht in allen vier Stufen in derselben Lage, damit der "
    "Unterschied zwischen den Stufen ins Auge faellt und nicht die Ausrichtung. "
    "Zone C nennt die drei Enzyme, die bei Thiaminmangel gleichzeitig ausfallen."
)

fehler, bericht = t.pruefe()
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
