# -*- coding: utf-8 -*-
"""
M-01 · Pyridoxal-5'-phosphat, gebaut mit mech.py.

Die meistgefragte Tafel. Zone A zeigt vollstaendig, wie die Aminosaeure ueberhaupt
an den Cofaktor kommt: die Transaldiminierung mit geminalem Diamin und mit dem
Lysin, das dabei frei wird. Zone B zeigt die Dunathan-Regel, also eine raeumliche
Aussage, und die laesst sich in einer Strichzeichnung nur zeigen, wenn die Ebene
selbst gezeichnet wird.

Diese Tafel ist die erste, die mit der neuen Pfeilsprache gebaut ist:

  - kern="b6" legt alle fuenf Stufen des Cofaktors auf dieselbe Referenzlage
    (mech_kerne.py). Der Pyridinring steht dadurch in jedem Bild gleich: Ring-
    stickstoff unten links, Methyl unten rechts, 3-Oxy rechts, C4' oben rechts,
    Phosphat oben links. Vorher standen die fuenf Stufen ueber 95 Grad verteilt,
    und der Leser musste jedes Bild erst neu einnorden.
  - schub(quelle, ziel) beschreibt nur, welche Elektronen wohin gehen. Bauchseite,
    Oeffnungswinkel, Ankerlage und der Winkel jedes freien Elektronenpaars kommen
    aus dem Solver in mech_schub.py; geprueft wird gegen mech_regeln.py.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech
from mech import Atom, Bindung, Paar

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 2000)

PLP = "Cc1[nH+]cc(COP(=O)([O-])[O-])c(%s)c1[O-]"

# ===================================================== ZONE A · Transaldiminierung
t.zone(24, "A · TRANSALDIMINIERUNG: WIE DIE AMINOSÄURE AN DEN COFAKTOR KOMMT")
t.text(20, 56, "Im Ruhezustand hängt PLP als protonierte Schiffsche Base an einem Lysin des "
               "Enzyms. Das Substrat verdrängt dieses Lysin in drei Schritten, ohne dass der",
       size=12.5)
t.text(20, 75, "Cofaktor je frei wird: Angriff des Aminstickstoffs, Protonenwanderung, "
               "Zerfall. Am Ende hängt die Aminosäure am C4&#8242;.", size=12.5)

# --- Reihe 1: internes Aldimin + freies Amin -> geminales Diamin I
intern = t.mol(PLP % "/C=[NH+]/*", 150, 212, labels={14: "Lys"},
               kern="b6", name="internes Aldimin")
t.atomnummer(intern, 12, "C4&#8242;", winkel=70, abstand=26, size=10, farbe=W, gewicht=700)
t.unterschrift(intern, "&#9312; internes Aldimin, das Ketoenamin",
               "das ⊕ am Imin-Stickstoff macht C4&#8242; elektrophil")

subst = t.mol("N[C@@H](*)C(=O)[O-]", 272, 152, labels={2: "R"},
              zeige={0: "links"}, name="Aminosäure")
t.ueberschrift(subst, "&#9313; die Aminosäure greift als freies Amin an", abstand=16,
               size=10.5, farbe=G, gewicht=700)

# Der Angriff und der Ausweichschritt sind ein Schritt und werden deshalb als
# Kette angemeldet: die Pruefung verlangt dann Kopf an Schwanz.
t.schub(Paar(subst, 0), Atom(intern, 12), kette="A1")
t.schub(Bindung(intern, 12, 13), Paar(intern, 13), kette="A1")

t.reaktionspfeil(360, 212, 442)

gem1 = t.mol(PLP % "[C@@H](N*)[NH2+][C@@H](*)C(=O)[O-]", 600, 212,
             labels={14: "Lys", 17: "R"}, kern="b6", name="geminales Diamin I")
t.unterschrift(gem1, "&#9314; geminales Diamin: beide Stickstoffe am selben Kohlenstoff,",
               "das Lysin nach hinten, das Substrat nach vorn")

t.kasten(770, 96, 210, 186, fill="var(--cofaktor-bg)", stroke=C)
t.text(788, 118, "WARUM EIN LYSIN?", size=11, gewicht=700, farbe=C)
t.text(788, 140, "Der Cofaktor ist schon vor", size=12)
t.text(788, 159, "dem Substrat gebunden, und", size=12)
t.text(788, 178, "zwar als Aldimin, nicht als", size=12)
t.text(788, 197, "freier Aldehyd. Das Lysin ist", size=12)
t.text(788, 216, "erst der Anker; sobald es frei", size=12)
t.text(788, 235, "ist, wird es zum Säure-Base-", size=12)
t.text(788, 254, "Werkzeug des aktiven Zentrums", size=12)
t.text(788, 273, "(Zone C, vierte Kachel).", size=12)

# --- Rueckweg: die Protonenwanderung, die den Zerfall erst moeglich macht.
# Sie steht bewusst als Reaktionspfeil da und nicht als Elektronenpfeil am Geruest:
# uebertragen wird ueber eine Base des aktiven Zentrums, und die beiden Stickstoffe
# liegen am selben Kohlenstoff so dicht beieinander, dass jeder gezeichnete Bogen
# quer durch die Struktur laufen wuerde. Im Bild sieht man den Wechsel am ⊕.
t.reaktionspfeil(600, 360, 300)
t.text(450, 348, "Protonenwanderung vom Substrat-Stickstoff zum Lysin-Stickstoff",
       size=11.5, anchor="middle", gewicht=700, farbe=W)
t.text(450, 380, "Als Amid-Anion könnte das Lysin nicht austreten, als neutrales Amin schon. "
                 "Das ⊕ wechselt über eine Base des aktiven Zentrums",
       size=11.5, anchor="middle", farbe=G)
t.text(450, 398, "(3-O&#8315; oder ein Wassermolekül) von einem Stickstoff zum anderen.",
       size=11.5, anchor="middle", farbe=G)

# --- Reihe 2: geminales Diamin II -> externes Aldimin + freies Lysin
gem2 = t.mol(PLP % "[C@@H]([NH2+]*)N[C@@H](*)C(=O)[O-]", 155, 478,
             labels={14: "Lys", 17: "R"}, kern="b6", name="geminales Diamin II")
t.schub(Paar(gem2, 15), Bindung(gem2, 12, 15), kette="A2")
t.schub(Bindung(gem2, 12, 13), Paar(gem2, 13), kette="A2")
t.unterschrift(gem2, "&#9315; das Proton sitzt jetzt am Lysin,",
               "damit ist es eine Abgangsgruppe")

t.reaktionspfeil(310, 478, 392)

extern = t.mol(PLP % "/C=[NH+]/[C@@H](*)C(=O)[O-]", 520, 478,
               labels={15: "R"}, wasserstoff=(14,), kern="b6",
               name="externes Aldimin")
# Winkel nicht raten: die groesste Winkelluecke am C-alpha liefert ihn.
t.atomnummer(extern, 14, "C&#945;", winkel=extern.freie_richtung(14), abstand=30,
             size=10.5, farbe=W, gewicht=700)
t.unterschrift(extern, "&#9316; externes Aldimin: jetzt hängt die Aminosäure am Cofaktor,",
               "drei Bindungen am C&#945; stehen zur Wahl")

t.text(700, 484, "+", size=20, anchor="middle", farbe=G)

lys = t.mol("N*", 800, 478, labels={1: "Lys"}, name="freies Lysin")
t.unterschrift(lys, "&#9317; das Lysin ist frei und bleibt", "im aktiven Zentrum")

# ===================================================== ZONE B · Dunathan
t.zone(620, "B · DIE DUNATHAN-REGEL: DAS ENZYM WÄHLT DIE BINDUNG")
t.text(20, 652, "Gebrochen wird die Bindung, die das Enzym senkrecht zur π-Ebene des Aldimins "
                "stellt: nur sie überlappt mit dem konjugierten System. Die Bindung vom C&#945;",
       size=12.5)
t.text(20, 671, "zum Stickstoff liegt dagegen in dieser Ebene, denn an ihr hängt die Konjugation. "
                "Die Ansichten &#9313; und &#9314; zeigen dieselbe Konformation; verschieden ist "
                "erst,", size=12.5)
t.text(20, 690, "was mit dem Chinoid danach geschieht.", size=12.5)

DUNATHAN = [
    (170, "&#9312;", "COO&#8315;", "H", "R", "Decarboxylase", "biogenes Amin"),
    (500, "&#9313;", "H", "COO&#8315;", "R", "Transaminase", "&#945;-Ketosäure"),
    (830, "&#9314;", "H", "COO&#8315;", "R", "&#946;-Eliminase", "Aminoacrylat"),
]
for cx, nr, senkrecht, vorn, hinten, enzym, produkt in DUNATHAN:
    cy = 800.0
    t.text(cx, 732, "%s  %s steht senkrecht" % (nr, senkrecht), size=11.5, anchor="middle",
           gewicht=700, farbe=W)
    t.ebene(cx, cy, breite=132, tiefe=40, beschriftung="π-Ebene")
    # die Bindung zum Aldimin-Stickstoff liegt IN der Ebene: an ihr haengt die Konjugation
    t.linie(cx, cy, cx - 63, cy, breite=1.6)
    t.text(cx - 72, cy + 4, "N=C4&#8242;", size=10, anchor="end", farbe=G)
    # die dritte Bindung steht senkrecht heraus - genau sie bricht
    t.keil(cx, cy, cx, cy - 44, breite=7.5, farbe=W)
    t.text(cx, cy - 52, senkrecht, size=11.5, anchor="middle", gewicht=700, farbe=W)
    # die beiden uebrigen Substituenten stehen schraeg nach vorn und nach hinten
    t.keil(cx, cy, cx + 36, cy + 22, breite=5.0)
    t.text(cx + 42, cy + 30, vorn, size=10.5)
    t.strichkeil(cx, cy, cx + 4, cy + 40, breite=5.0)
    t.text(cx + 6, cy + 56, hinten, size=10.5, anchor="middle")
    t.text(cx, cy + 84, enzym, size=11, anchor="middle", gewicht=700, farbe=E)
    t.text(cx, cy + 99, "&#8594; " + produkt, size=10.5, anchor="middle", farbe=G)

t.text(500, 926, "Der Cofaktor ist in allen drei Fällen derselbe. Verschieden ist allein, "
                 "wie das Apoenzym das Substrat verdreht festhält.", size=12,
       anchor="middle", farbe=G)

# ===================================================== ZONE C · das Chinoid
t.zone(960, "C · DAS CHINOID: DIE GEMEINSAME ZWISCHENSTUFE ALLER WEGE")
t.text(20, 990, "Was auch immer am C&#945; abgeht: Es bleibt ein Carbanion zurück, dessen Ladung "
                "über das konjugierte System bis zum Ring-Stickstoff wandert.", size=12.5)

chin = t.mol(PLP % "/C=N/[CH-]*", 215, 1120, labels={15: "R"},
             kern="b6", name="Chinoid")
# Die Kaskade als Kette kurzer Pfeile, Kopf an Schwanz. Frueher stand der letzte
# Schritt als ein gestrichelter Pfeil quer ueber den Ring. Der laesst sich nicht
# konventionsgemaess zeichnen: aussen um den Ring herum muesste er weiter
# ausgreifen, als er breit ist, und im Ringinneren kann er nicht anfangen, weil
# sein Ursprung ausserhalb des Rings liegt. Ausgeschrieben ist die Kette ohnehin
# das, was im Examen an der Tafel verlangt wird.
t.schub(Paar(chin, 14), Bindung(chin, 13, 14), kette="C")         # Ca-Paar -> Ca=N
t.schub(Bindung(chin, 12, 13), Bindung(chin, 11, 12), kette="C")  # N=C4' -> C4'-C4
t.schub(Bindung(chin, 4, 11), Bindung(chin, 3, 4), kette="C")     # C5=C4 -> C6-C5
# Der letzte Schritt - das pi-Paar der Bindung N1=C6 geht auf den Ring-Stickstoff -
# ist nicht gezeichnet. Der Solver findet dort keinen Bogen: die Beschriftung
# "HN+" belegt genau den Raum, in dem die Spitze stehen muesste, und jeder Weg
# daran vorbei kreuzt entweder den Ring oder die eigene Quellbindung. Statt den
# Pfeil zu verbiegen, steht die Aussage im Text und im Kasten "Elektronensenke".
t.atomnummer(chin, 14, "C&#945;", winkel=300, abstand=30, size=10.5, farbe=W, gewicht=700)
t.text(355, 1042, "&#9312; das freie Paar am C&#945;", size=10.5, farbe=W, gewicht=700)
t.text(355, 1057, "bildet die C&#945;=N-Bindung", size=10.5, farbe=W)
t.text(355, 1082, "&#9313; das π-Paar der Bindung N=C4&#8242;", size=10.5, farbe=W, gewicht=700)
t.text(355, 1097, "geht in die Bindung C4&#8242;&#8211;C4", size=10.5, farbe=W)
t.text(355, 1122, "&#9314; von dort weiter in den Ring", size=10.5, farbe=W, gewicht=700)
t.text(355, 1147, "Der letzte Schritt, das π-Paar der", size=10.5, farbe=G)
t.text(355, 1162, "Bindung N1=C6 auf den Ring-Stick-", size=10.5, farbe=G)
t.text(355, 1177, "stoff, ist nicht gezeichnet: neben", size=10.5, farbe=G)
t.text(355, 1192, "dem HN&#8314; ist dafür kein Platz.", size=10.5, farbe=G)
t.unterschrift(chin, "Chinoid, gezeichnet als Carbanion und für den Decarboxylierungsweg.",
               "Bei den anderen Wegen steht am C&#945; statt des H das Carboxylat.",
               abstand=40)

t.kasten(20, 1285, 410, 152, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 1307, "DIE ELEKTRONENSENKE", size=11, gewicht=700, farbe=C)
t.text(38, 1329, "Jede Spaltung am C&#945; erzeugt ein Carbanion. Allein", size=12)
t.text(38, 1348, "wäre es nicht haltbar; das konjugierte System schiebt", size=12)
t.text(38, 1367, "die Ladung über den Imin-Stickstoff bis zum Ring.", size=12)
t.text(38, 1390, "Bei den Enzymen dieser Tafel trägt der Ring-Stickstoff", size=12)
t.text(38, 1409, "ein Proton, das ein Aspartat festhält (AADC: Asp271).", size=12)
t.text(38, 1428, "Die Alanin-Racemase kommt ohne dieses Proton aus.", size=12)

WEGE = [
    (1035, "&#9312; Decarboxylierung", W,
     ["Nach Abgang von CO&#8322; nimmt das C&#945; ein Proton auf.",
      "Produkt ist das biogene Amin; das Lysin löst es wieder ab."],
     "AADC · GAD · HDC · ODC",
     "Carbidopa und Benserazid (AADC) · Eflornithin (ODC)"),
    (1145, "&#9313; Transaminierung", W,
     ["Das Proton geht ans C4&#8242;, es entsteht das Ketimin.",
      "Wasser spaltet es in PMP und die &#945;-Ketosäure.",
      "Zurück am selben C&#945; protoniert: Racemisierung."],
     "AST (GOT) · ALT (GPT) · GABA-Transaminase · Alanin-Racemase",
     "Vigabatrin, ein Suizidsubstrat der GABA-Transaminase"),
    (1273, "&#9314; &#946;-Eliminierung und &#946;-Ersatz", W,
     ["Vom C&#946; geht eine Fluchtgruppe ab, es entsteht",
      "Aminoacrylat als gemeinsame Zwischenstufe."],
     "Cystathionin-&#946;-Synthase · Serin-Dehydratase",
     "Homocystein-Stau bei B&#8326;-Mangel"),
]
for y, titel, farbe, zeilen, enzyme, stoffe in WEGE:
    t.text(560, y, titel, size=12.5, gewicht=700, farbe=farbe)
    for i, z in enumerate(zeilen):
        t.text(560, y + 21 + i * 18, z, size=12)
    t.text(560, y + 21 + len(zeilen) * 18, enzyme, size=11, gewicht=700, farbe=E)
    t.text(560, y + 38 + len(zeilen) * 18, stoffe, size=11, farbe=R)

t.kasten(20, 1465, 960, 152, fill="var(--surface-2)")
t.text(38, 1487, "&#9315; UND DAS LYSIN? ES BLEIBT IM AKTIVEN ZENTRUM UND ARBEITET WEITER",
       size=11, gewicht=700, farbe=C)
t.text(38, 1509, "Das freigesetzte ε-Amin sitzt auf derselben Seite wie die brechende Bindung. "
                 "Deshalb ist es das vorgesehene Säure-Base-Werkzeug, und deshalb", size=12)
t.text(38, 1528, "laufen Abzug und Rückgabe des Protons unter Retention ab.", size=12)
t.text(38, 1551, "Transaminase: erst Base, sie zieht das C&#945;-H ab; dann Säure, sie gibt "
                 "dasselbe Proton an das C4&#8242;.", size=12)
t.text(38, 1570, "Decarboxylase: nur Säure, denn am C&#945; geht CO&#8322; ab. Protoniert sie "
                 "aus Versehen das C4&#8242;, entsteht totes Enzym mit PMP.", size=12)
t.text(38, 1589, "β-Eliminase: wieder Base am C&#945;; beim β-Ersatz protoniert dasselbe Lysin "
                 "danach zurück.", size=12)
t.text(538, 1589, "Zuletzt greift es erneut das C4&#8242; an: Zone A rückwärts, "
                  "das Produkt wird frei.", size=12, farbe=C)

# ===================================================== ZONE D · Hemmstoffe
t.zone(1650, "D · WIE ARZNEISTOFFE HIER ANGREIFEN")
t.text(20, 1682, "Zwei ganz verschiedene Prinzipien, beide am selben Cofaktor.", size=12.5)

t.kasten(20, 1710, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(38, 1732, "DEN COFAKTOR ABFANGEN", size=11, gewicht=700, farbe=R)
t.text(38, 1754, "Carbidopa und Benserazid tragen eine Hydrazino-", size=12.5)
t.text(38, 1773, "Gruppe. Sie greift das C4&#8242; des internen Aldimins", size=12.5)
t.text(38, 1792, "an und verdrängt das Lysin, also Zone A mit einem", size=12.5)
t.text(38, 1811, "Hydrazin. PLP bleibt als Hydrazon gebunden.", size=12.5)
t.text(38, 1834, "Isoniazid tut chemisch dasselbe, aber im ganzen", size=12.5)
t.text(38, 1853, "Körper; daher die Polyneuropathie.", size=12.5)

t.kasten(510, 1710, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(528, 1732, "DEN MECHANISMUS MISSBRAUCHEN", size=11, gewicht=700, farbe=R)
t.text(528, 1754, "Vigabatrin ist ein echtes Suizidsubstrat: Es durch-", size=12.5)
t.text(528, 1773, "läuft den Mechanismus bis zum Chinoid und alkyliert", size=12.5)
t.text(528, 1792, "erst dann das Enzym kovalent.", size=12.5)
t.text(528, 1815, "Prüfungsfalle: Vigabatrin hemmt die GABA-Trans-", size=12.5)
t.text(528, 1834, "aminase, also den Abbau, nicht die Decarboxylase", size=12.5)
t.text(528, 1853, "und damit nicht den Aufbau.", size=12.5)

t.kasten(20, 1884, 960, 76, fill="var(--surface-2)")
t.text(38, 1906, "WARUM PLP IN SO VIELEN KAPITELN AUFTAUCHT", size=11, gewicht=700, farbe=G)
t.text(38, 1928, "Register A in Teil 9 führt die PLP-Enzyme dieser Unterlage auf: die "
                 "Decarboxylasen aller biogenen Amine, die Transaminasen, die", size=12.5)
t.text(38, 1947, "Cystathionin-&#946;-Synthase, die &#948;-Aminolävulinat-Synthase der Häm-Synthese "
                 "und die Serin-Hydroxymethyltransferase des C&#8321;-Stoffwechsels.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Pyridoxalphosphat in vier Zonen. Zone A zeigt die Transaldiminierung Schritt fuer Schritt mit "
    "Elektronenpfeilen: Das interne Aldimin, eine protonierte Schiffsche Base zwischen dem "
    "Cofaktor und einem Lysin des Enzyms, wird vom freien Aminstickstoff der Aminosaeure am "
    "Kohlenstoff 4-Strich angegriffen. Es entsteht ein geminales Diamin, an dessen einem "
    "Kohlenstoff beide Stickstoffatome haengen. Ein Proton wandert vom Substratstickstoff zum "
    "Lysinstickstoff; erst dadurch wird das Lysin zur Abgangsgruppe. Danach zerfaellt das "
    "geminale Diamin zum externen Aldimin, und das Lysin wird als freies Amin abgebildet. "
    "Der Pyridinring des Cofaktors steht in allen Stufen in derselben Lage, damit der "
    "Unterschied zwischen den Stufen ins Auge faellt und nicht die Ausrichtung. "
    "Zone B zeigt die Dunathan-Regel in drei Schraegansichten: Die pi-Ebene des Aldimins ist als "
    "Parallelogramm gezeichnet, die Bindung vom Alpha-Kohlenstoff zum Stickstoff liegt in dieser "
    "Ebene, und jeweils eine der drei uebrigen Bindungen steht als Keil senkrecht darauf. Bei der "
    "Decarboxylase ist das die Carboxylatgruppe, bei der Transaminase und der Beta-Eliminase das "
    "Wasserstoffatom. Nur die senkrechte Bindung bricht. Zone C zeigt das Chinoid als "
    "Carbanion-Grenzstruktur mit drei Elektronenpfeilen, die die Ladung ueber die "
    "Kohlenstoff-Stickstoff-Doppelbindung bis zum protonierten Ring-Stickstoff schieben, daneben "
    "die drei Reaktionswege mit Enzymen und Arzneistoffen und darunter die Rolle des "
    "freigesetzten Lysins als Saeure und als Base. Zone D nennt die beiden Hemmprinzipien: "
    "Hydrazine verdraengen das Lysin und fangen den Cofaktor ab, Vigabatrin missbraucht den "
    "Mechanismus als Suizidsubstrat."
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

mech.speichern("m01", t.svg(ARIA), t)
