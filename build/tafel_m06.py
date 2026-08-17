# -*- coding: utf-8 -*-
"""
M-06 · Flavin und die MAO, gebaut mit mech.py.

Vorher war das Isoalloxazin ein handgesetztes <use>-Template aus Sechsecken,
Selegilin eine Zeichenkette. Jetzt kommen alle drei Flavinformen - oxidiert,
reduziert und das N5-Addukt - aus demselben Zeichner wie der Rest des Dokuments.

Die Tafel ist auf die neue Pfeilsprache umgestellt:

  - KERN legt alle drei Flavinformen auf dieselbe Referenzlage. Oxidiert und
    reduziert unterscheiden sich nur in den Bindungsordnungen, nicht im
    Atomgeruest; das Suchmuster ist deshalb bindungs- und aromatizitaets-
    agnostisch geschrieben (~ als Bindung, [#7] statt n). Der Isoalloxazinring
    steht damit in jedem Bild gleich: Benzolring links, Pyrimidindion rechts,
    N5 oben, N10 mit dem Ribityl unten.
  - schub(quelle, ziel) beschreibt nur, welche Elektronen wohin gehen.
    Bauchseite, Oeffnungswinkel und Ankerlage kommen aus mech_schub.py,
    geprueft wird gegen mech_regeln.py.
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

FLAVIN_OX = "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(*)c2cc1CS*"
FLAVIN_RED = "Cc1cc2c(cc1CS*)N(*)C3=C(N2)C(=O)NC(=O)N3"
ADDUKT = "Cc1cc2c(cc1CS*)N(*)C3=C(N2C=C=CN(C)*)C(=O)NC(=O)N3"

# Das Leitgeruest des Isoalloxazins. Die Referenz traegt statt der Reste
# Methylgruppen; gesucht wird der ganze Dreiring, damit die Lage nicht an einem
# einzelnen Sechsring haengt. Ring B (C5a-N5-C4a-C10a-N10-C9a) legt die Lage
# fest: N5 zeigt nach oben (winkel=90), das Folgeatom C4a nach oben rechts.
# Damit liegt der Benzolring links, das Pyrimidindion rechts, und das Substrat
# kann von oben an das N5 herankommen.
KERN = mech_kerne.eigener(
    "isoalloxazin", "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C)c2cc1C",
    muster=("[#6]1~[#6]~[#6]2~[#7]~[#6]3~[#6](~[#8])~[#7]~[#6](~[#8])~[#7]"
            "~[#6]~3~[#7]~[#6]~2~[#6]~[#6]~1"),
    ring=[3, 4, 5, 12, 13, 15], leit=4, folge=5, winkel=90.0)

t = mech.Tafel(1000, 1452)

# ===================================================== ZONE A · der Zyklus
t.zone(24, "A · DER NORMALE KATALYSEZYKLUS DER MONOAMINOXIDASE")
t.text(20, 54, "Das Flavin nimmt vom α-Kohlenstoff des Amins ein Hydrid auf. Zurück bleibt ein "
               "Iminium-Kation, das von selbst zum Aldehyd zerfällt.", size=12.5)
t.text(20, 73, "Der Hydridtransfer liefert zunächst das Flavin-Anion FADH&#8315;; die Pfeilkette im "
               "Ring trägt die Ladung ans N1. Erst ein Proton macht daraus FADH&#8322;.",
       size=12.5)
t.text(20, 92, "Anders als NAD&#8314; führt Flavin denselben Vorgang auch in zwei "
               "Ein-Elektronen-Schritten. Genau das nutzen die irreversiblen Hemmstoffe aus.",
       size=12.5)

fox = t.mol(FLAVIN_OX, 200, 250, labels={14: "Ribityl", 20: "Cys"},
            kern=KERN, name="FAD oxidiert")
# Die Marken stehen dicht genug am eigenen Atom, dass kein Nachbaratom naeher
# liegt, und weichen dabei den Pfeilen aus: der Hydridpfeil kommt von oben ans
# N5, die Ringkette endet links unter dem N1. Beide Flavinformen und das Addukt
# bekommen dieselben Winkel und Abstaende; nur dann lassen sich die Bilder
# nebeneinander lesen, ohne dass der Blick die Marken neu suchen muss.
t.atomnummer(fox, 4, "N5", winkel=250, abstand=34, size=10.5, farbe=R, gewicht=700)
t.atomnummer(fox, 11, "N1", winkel=60, abstand=26, size=10.5, farbe=R, gewicht=700)

# Die Lage des Amins ist nicht beliebig, und zwar wegen des ersten Pfeils. Er
# geht vom freien Paar des Stickstoffs in die C-N-Bindung, also zurueck an das
# eigene Atom; er muss deshalb um den Stickstoff herumgreifen. Auf welcher Seite
# der Bindung er landet, haengt daran, wohin das Paar gesetzt wird, und das haengt
# an der Schreibrichtung des Symbols: "NH2" reicht waagerecht weit, senkrecht
# kaum. Stand das R nach oben (zeige={0: "oben"}), so kam das Paar rechts neben
# den Stickstoff, die Spitze aber unter die Bindung - der Bogen kreuzte sie.
# Bei rotate=30 liegt das Paar ueber dem Symbol und die Spitze daneben, auf
# derselben Seite: kein Schnitt, Lot 0,22 L, Laengslage genau in der Mitte.
amin = t.mol("*CN", 272, 165, labels={0: "R"}, wasserstoff=[1],
             rotate=30, name="Amin")
ha = amin.h_index[1]

# Ein einziger Reaktionsschritt, deshalb eine Kette: Das freie Paar am Stickstoff
# schiebt die C=N-Doppelbindung auf, das Bindungspaar der C-H-Bindung geht als
# Hydrid an das N5, und das Paar der Doppelbindung N5=C4a weicht ueber den Ring bis
# zum N1 aus. Frueher stand der letzte Teil als ein gestrichelter Pfeil quer durch
# den Ring da; ausgeschrieben ist er das, was im Examen an der Tafel verlangt wird.
# Am N1 sitzt danach die negative Ladung des Flavin-Anions, und dort greift im
# Produkt das Proton aus dem Medium an - deshalb ist N1 in beiden Formen beschriftet.
t.schub(Paar(amin, 2), Bindung(amin, 1, 2), kette="A")
t.schub(Bindung(amin, 1, ha), Atom(fox, 4), kette="A")
t.schub(Bindung(fox, 4, 5), Bindung(fox, 5, 12), kette="A")
t.schub(Bindung(fox, 11, 12), Paar(fox, 11), kette="A")

t.ueberschrift(amin, "das Amin: sein α-H geht als Hydrid ans N5", abstand=26,
               size=12.5, farbe=G, gewicht=700)
t.unterschrift(fox, "FAD, oxidiert, kovalent über einen Thioether",
               "am Cystein des Motivs Ser-Gly-Gly-Cys-Tyr", abstand=44)

t.reaktionspfeil(320, 250, 640)
t.text(480, 238, "+ H&#8314;", size=10, anchor="middle", farbe=G)

fred = t.mol(FLAVIN_RED, 760, 250, labels={9: "Cys", 11: "Ribityl"},
             kern=KERN, name="FADH2")
t.atomnummer(fred, 14, "N5", winkel=250, abstand=34, size=10.5, farbe=R, gewicht=700)
t.atomnummer(fred, 20, "N1", winkel=60, abstand=26, size=10.5, farbe=R, gewicht=700)
t.unterschrift(fred, "FADH&#8322;: das N5 trägt das Hydrid,",
               "das N1 das Proton aus dem Medium", abstand=44)

# Substratseite
t.text(20, 384, "AUF DER SUBSTRATSEITE", size=11, gewicht=700, farbe=G)
amin2 = t.mol("*CN", 130, 446, labels={0: "R"}, zeige={2: "rechts"}, name="Amin")
t.unterschrift(amin2, "Amin", abstand=26, farbe=G)
t.reaktionspfeil(196, 446, 258)
t.text(227, 422, "ans Flavin", size=10, anchor="middle", farbe=G)
t.text(227, 436, "&#8722; H&#8315;", size=10, anchor="middle", farbe=G)

imin = t.mol("*C=[NH2+]", 322, 446, labels={0: "R"}, zeige={2: "rechts"},
             name="Iminium")
t.unterschrift(imin, "Iminium", abstand=26, farbe=G)
t.reaktionspfeil(388, 446, 450)
t.text(419, 422, "&#8722; NH&#8324;&#8314;", size=10, anchor="middle", farbe=G)
t.text(419, 436, "+ H&#8322;O", size=10, anchor="middle", farbe=G)

ald = t.mol("*C=O", 514, 446, labels={0: "R"}, zeige={2: "rechts"}, name="Aldehyd")
t.unterschrift(ald, "Aldehyd, dann ALDH", abstand=26, farbe=G)

t.kasten(620, 392, 360, 108, fill="var(--warn-bg)", stroke=W)
t.text(638, 414, "DIE REOXIDATION KOSTET ETWAS", size=11, gewicht=700, farbe=W)
t.text(638, 436, "FADH&#8322; + O&#8322; → FAD + H&#8322;O&#8322;. Jeder Umsatz der MAO", size=12.5)
t.text(638, 455, "erzeugt also ein Molekül Wasserstoffperoxid.", size=12.5)
t.text(638, 478, "Daher der Verdacht, dass hohe MAO-Aktivität zum", size=12.5)
t.text(638, 497, "oxidativen Stress dopaminerger Neurone beiträgt.", size=12.5)

# ===================================================== ZONE B · Suizidinhibition
t.zone(546, "B · SUIZIDINHIBITION DURCH DIE PROPARGYLGRUPPE")
t.text(20, 576, "Selegilin und Rasagilin sind zunächst gewöhnliche Substrate. Erst die Oxidation "
                "durch das Enzym macht aus ihnen einen Michael-Akzeptor,", size=12.5)
t.text(20, 595, "und den greift das nucleophile N5 des reduzierten Flavins an. Der Hemmstoff "
                "baut also sein eigenes Gift.", size=12.5)

# (R)-Konfiguration: RDKit-CIP fuer diesen SMILES ist R. Das Spiegelbild
# C#CCN(C)[C@@H](C)Cc1ccccc1 waere (S) und damit das schwaechere Enantiomer.
sel = t.mol("C#CCN(C)[C@H](C)Cc1ccccc1", 178, 730, zeige={0: "oben"},
            stereo=True, name="Selegilin")
flavin_marke = t.marke(268, 654, "Flavin N5")
t.text(268, 640, "Flavin", size=11, anchor="middle", gewicht=700, farbe=R)
# Ein einzelnes Elektron des freien Paars geht auf das Flavin ueber: halber Kopf.
t.schub(Paar(sel, 3), flavin_marke, elektronen=1)
t.unterschrift(sel, "(R)-Selegilin: die Propargylgruppe oben",
               "ist der ganze Unterschied zum Substrat", abstand=32)

t.reaktionspfeil(316, 730, 396)
t.text(356, 708, "ein Elektron,", size=10, anchor="middle", farbe=R, gewicht=700)
t.text(356, 722, "dann H ans Flavin", size=10, anchor="middle", farbe=R, gewicht=700)
t.text(356, 752, "Radikalpaar", size=10, anchor="middle", farbe=G)
t.text(356, 766, "im Käfig", size=10, anchor="middle", farbe=G)

add = t.mol(ADDUKT, 700, 730, labels={9: "Cys", 11: "Ribityl", 20: "R"},
            kern=KERN, name="N5-Addukt")
# Am Addukt traegt das N5 drei Bindungen; oben links, wo die Marke in Zone A
# steht, laeuft hier die Addukt-Kette. Die Marke rueckt deshalb als einzige in
# die Luecke zwischen Ring und Kette.
t.atomnummer(add, 14, "N5", winkel=207, abstand=34, size=10.5, farbe=R, gewicht=700)
t.unterschrift(add, "das N5-Addukt: der Cofaktor ist kovalent blockiert,",
               "das Enzym damit endgültig aus dem Verkehr", abstand=32, farbe=R, gewicht=700)

# ===================================================== ZONE C · Folgerungen
t.zone(942, "C · WAS SICH FÜR DIE THERAPIE DARAUS ERGIBT")

t.kasten(20, 974, 470, 158, fill="var(--drug-bg)", stroke=R)
t.text(38, 996, "DIE WIRKDAUER HAT NICHTS MIT DER HALBWERTSZEIT ZU TUN", size=11,
       gewicht=700, farbe=R)
t.text(38, 1018, "Selegilin hat eine Plasmahalbwertszeit von unter zwei", size=12.5)
t.text(38, 1037, "Stunden, wirkt aber über Tage. Der Grund steht in Zone B:", size=12.5)
t.text(38, 1056, "Das Enzym ist zerstört, nicht besetzt.", size=12.5)
t.text(38, 1079, "Die Aktivität kehrt erst mit der Neusynthese zurück.", size=12.5)
t.text(38, 1098, "Vor dem Wechsel auf ein serotonerges Antidepressivum", size=12.5)
t.text(38, 1117, "gilt deshalb eine Karenz von zwei Wochen.", size=12.5)

t.kasten(510, 974, 470, 158, fill="var(--surface-2)")
t.text(528, 996, "WARUM RASAGILIN DAS BESSERE MOLEKÜL IST", size=11, gewicht=700, farbe=G)
t.text(528, 1018, "Dieselbe Propargylgruppe, derselbe Mechanismus, aber sie sitzt", size=12.5)
t.text(528, 1037, "an einem Indangerüst statt an einem Amphetamin.", size=12.5)
t.text(528, 1060, "Selegilin wird zu Methamphetamin und Amphetamin", size=12.5)
t.text(528, 1079, "abgebaut; daher Schlafstörungen und Blutdruckanstieg.", size=12.5)
t.text(528, 1098, "Rasagilin liefert stattdessen Aminoindan, das selbst", size=12.5)
t.text(528, 1117, "keine stimulierende Wirkung hat.", size=12.5)

t.kasten(20, 1156, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1178, "DIE SELEKTIVITÄT IST EINE DOSISFRAGE", size=11, gewicht=700, farbe=W)
t.text(38, 1200, "In niedriger Dosis hemmt Selegilin nur die MAO-B, die im ZNS überwiegt und "
                 "vorwiegend Dopamin abbaut. Erst in höherer Dosis trifft es auch", size=12.5)
t.text(38, 1219, "die MAO-A und damit den Tyraminabbau in der Darmwand. Genau dort liegt die "
                 "Grenze zur Käse-Reaktion.", size=12.5)

t.kasten(20, 1276, 960, 96, fill="var(--surface-2)")
t.text(38, 1298, "DER UNTERSCHIED ZU MOCLOBEMID", size=11, gewicht=700, farbe=G)
t.text(38, 1320, "Moclobemid hemmt die MAO-A reversibel und kompetitiv: Steigt die "
                 "Tyraminkonzentration, verdrängt das Tyramin den Hemmstoff und wird", size=12.5)
t.text(38, 1339, "wieder abgebaut. Deshalb ist die Diät dort entbehrlich: der Mechanismus, nicht "
                 "die Selektivität, entscheidet über das Risiko.", size=12.5)

t.text(20, 1414, "Tranylcypromin schließlich hemmt beide Isoformen irreversibel und verlangt "
                 "deshalb dieselbe Vorsicht wie Selegilin in hoher Dosis.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Flavin und die Monoaminoxidase in drei Zonen. Zone A zeigt den normalen Zyklus mit "
    "gezeichneten Strukturen: Das oxidierte Flavin, kovalent ueber einen Thioether an ein "
    "Cystein gebunden, nimmt mit einem Elektronenpaarpfeil das Wasserstoffatom vom "
    "Alpha-Kohlenstoff des Amins als Hydrid auf; gleichzeitig bildet das "
    "Stickstoff-Elektronenpaar die Iminium-Doppelbindung. Zwei weitere Pfeile derselben "
    "Kette fuehren das Paar der Doppelbindung zwischen N5 und C4a in die Bindung zwischen "
    "C4a und C10a und von dort das Paar der Doppelbindung zwischen C10a und N1 als freies "
    "Paar auf das N1. Beide Flavinformen sind an N5 und "
    "N1 beschriftet: Das Hydrid landet am N5, die negative Ladung des Flavin-Anions ueber "
    "das Ringsystem am N1, und erst ein Proton aus dem Medium macht daraus FADH zwei. "
    "Deshalb steht am Reaktionspfeil ein Proton. Auf der Substratseite verliert das Amin ein "
    "Hydrid an das Flavin, und das Iminium zerfaellt mit Wasser zum Aldehyd und Ammonium. Die "
    "Reoxidation des Flavins durch Sauerstoff liefert Wasserstoffperoxid. Zone B zeigt die "
    "Suizidinhibition: Vom Stickstoff des R-konfigurierten Selegilins geht mit einem "
    "Fischhakenpfeil ein einzelnes Elektron auf das Flavin ueber; anschliessend geht auch das "
    "Wasserstoffatom des Propargylkohlenstoffs an das Flavin, und der Rest addiert kovalent "
    "an das N5. Es entsteht das gezeichnete N5-Addukt, das den Cofaktor endgueltig blockiert. "
    "Zone C zieht die therapeutischen Folgerungen."
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

mech.speichern("m06", t.svg(ARIA), t)
