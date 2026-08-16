# -*- coding: utf-8 -*-
"""
M-01 · Pyridoxal-5'-phosphat, gebaut mit mech.py.

Die meistgefragte Tafel. Zone A zeigt vollstaendig, wie die Aminosaeure ueberhaupt
an den Cofaktor kommt: die Transaldiminierung mit geminalem Diamin und mit dem
Lysin, das dabei frei wird. Zone B zeigt die Dunathan-Regel, also eine raeumliche
Aussage, und die laesst sich in einer Strichzeichnung nur zeigen, wenn die Ebene
selbst gezeichnet wird.
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

t = mech.Tafel(1000, 1950)

PLP = "Cc1[nH+]cc(COP(=O)([O-])[O-])c(%s)c1[O-]"

# ===================================================== ZONE A · Transaldiminierung
t.zone(24, "A · TRANSALDIMINIERUNG: WIE DIE AMINOSÄURE AN DEN COFAKTOR KOMMT")
t.text(20, 56, "Im Ruhezustand hängt PLP als protonierte Schiffsche Base an einem Lysin des "
               "Enzyms. Das Substrat verdrängt dieses Lysin in drei Schritten, ohne dass der",
       size=12.5)
t.text(20, 75, "Cofaktor je frei wird: Angriff des Aminstickstoffs, Protonenwanderung, "
               "Zerfall. Am Ende hängt die Aminosäure am C4&#8242;.", size=12.5)

# --- Reihe 1: internes Aldimin + freies Amin -> geminales Diamin I
intern = mech.Molekuel(PLP % "/C=[NH+]/*", 150, 200, labels={14: "Lys"},
                       zeige={2: "unten", 13: "rechts"}, name="internes Aldimin")
t.mole.append(intern)
t.atomnummer(intern, 12, "C4&#8242;", winkel=32, abstand=30, size=10, farbe=W, gewicht=700)
t.unterschrift(intern, "&#9312; internes Aldimin, das Ketoenamin",
               "das ⊕ am Imin-Stickstoff macht C4&#8242; elektrophil")

subst = mech.Molekuel("N[C@@H](*)C(=O)[O-]", 368, 152, labels={2: "R"},
                      zeige={0: "unten"}, name="Aminosäure")
t.mole.append(subst)
t.ueberschrift(subst, "&#9313; die Aminosäure greift als freies Amin an", abstand=15,
               size=10.5, farbe=G, gewicht=700)

lp1 = t.elektronenpaar(subst, 0, 195)
t.pfeil(lp1, intern.aussen(12, abstand=6), bogen=0.22, seite=1, farbe=W)
# Das pi-Paar der C4'=N-Bindung geht auf den Stickstoff. Der Weg ist kurz, deshalb
# ein kleiner Spalt (gap) - sonst frisst die Verkuerzung den ganzen Bogen auf.
t.pfeil((intern, 12, 13), intern.abseits(13, 12, abstand=24),
        bogen=0.5, seite=-1, gap=3, farbe=W)

t.reaktionspfeil(470, 200, 552)

gem1 = mech.Molekuel(
    PLP % "[C@@H](N*)[NH2+][C@@H](*)C(=O)[O-]", 660, 200,
    labels={14: "Lys", 17: "R"},
    zeige={2: "unten", 13: "oben"}, name="geminales Diamin I")
t.mole.append(gem1)
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
t.reaktionspfeil(590, 348, 300)
t.text(445, 336, "Protonenwanderung vom Substrat-Stickstoff zum Lysin-Stickstoff",
       size=11.5, anchor="middle", gewicht=700, farbe=W)
t.text(445, 366, "Als Amid-Anion könnte das Lysin nicht austreten, als neutrales Amin schon. "
                 "Das ⊕ wechselt über eine Base des aktiven Zentrums",
       size=11.5, anchor="middle", farbe=G)
t.text(445, 384, "(3-O&#8315; oder ein Wassermolekül) von einem Stickstoff zum anderen.",
       size=11.5, anchor="middle", farbe=G)

# --- Reihe 2: geminales Diamin II -> externes Aldimin + freies Lysin
gem2 = mech.Molekuel(
    PLP % "[C@@H]([NH2+]*)N[C@@H](*)C(=O)[O-]", 160, 480,
    labels={14: "Lys", 17: "R"},
    zeige={2: "unten", 13: "oben"}, name="geminales Diamin II")
t.mole.append(gem2)
lp3 = t.elektronenpaar(gem2, 15, 135, abstand=14)
t.pfeil(lp3, (gem2, 12, 15), bogen=0.9, seite=1, gap=3, farbe=W)
t.pfeil((gem2, 12, 13), gem2.abseits(13, 12, abstand=24),
        bogen=0.5, seite=-1, gap=3, farbe=W)
t.unterschrift(gem2, "&#9315; das Proton sitzt jetzt am Lysin,",
               "damit ist es eine Abgangsgruppe")

t.reaktionspfeil(310, 480, 392)

extern = mech.Molekuel(PLP % "/C=[NH+]/[C@@H](*)C(=O)[O-]", 520, 480,
                       labels={15: "R"}, wasserstoff=(14,),
                       zeige={2: "unten", 13: "oben"}, name="externes Aldimin")
t.mole.append(extern)
t.atomnummer(extern, 14, "C&#945;", winkel=152, abstand=27, size=10.5, farbe=W, gewicht=700)
t.unterschrift(extern, "&#9316; externes Aldimin: jetzt hängt die Aminosäure am Cofaktor,",
               "drei Bindungen am C&#945; stehen zur Wahl")

t.text(690, 486, "+", size=20, anchor="middle", farbe=G)

lys = mech.Molekuel("N*", 800, 480, labels={1: "Lys"}, name="freies Lysin")
t.mole.append(lys)
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

chin = mech.Molekuel(PLP % "/C=N/[CH-]*", 205, 1100, labels={15: "R"},
                     zeige={2: "unten", 13: "oben"}, name="Chinoid")
t.mole.append(chin)
# Drei Pfeile: das Carbanion bildet die Doppelbindung, das pi-Paar der alten
# Doppelbindung weicht auf C4' aus, und von dort geht es zusammengefasst zum Ring-N.
lp4 = t.elektronenpaar(chin, 14, 25, abstand=17)
t.pfeil(lp4, (chin, 13, 14), bogen=0.9, seite=-1, gap=1.5, farbe=W)
t.pfeil(chin.aussen(12, 13, abstand=14), chin.abseits(12, 13, abstand=20),
        bogen=0.45, seite=1, gap=3, farbe=W)
t.pfeil(chin.aussen(12, abstand=28), chin.aussen(2, abstand=30),
        bogen=0.55, seite=-1, farbe=W, strich="5 3")
t.atomnummer(chin, 14, "C&#945;", winkel=265, abstand=32, size=10.5, farbe=W, gewicht=700)
t.text(305, 1052, "&#9312; das freie Paar am C&#945;", size=10.5, farbe=W, gewicht=700)
t.text(305, 1067, "bildet die C&#945;=N-Bindung", size=10.5, farbe=W)
t.text(305, 1092, "&#9313; das π-Paar der Bindung", size=10.5, farbe=W, gewicht=700)
t.text(305, 1107, "N=C4&#8242; weicht auf das C4&#8242; aus", size=10.5, farbe=W)
t.text(305, 1132, "&#9314; von dort über den Ring", size=10.5, farbe=W, gewicht=700)
t.text(305, 1147, "bis zum Ring-Stickstoff N1", size=10.5, farbe=W)
t.unterschrift(chin, "Chinoid, gezeichnet als Carbanion und für den Decarboxylierungsweg.",
               "Bei den anderen Wegen steht am C&#945; statt des H das Carboxylat.")

t.kasten(20, 1225, 410, 152, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 1247, "DIE ELEKTRONENSENKE", size=11, gewicht=700, farbe=C)
t.text(38, 1269, "Jede Spaltung am C&#945; erzeugt ein Carbanion. Allein", size=12)
t.text(38, 1288, "wäre es nicht haltbar; das konjugierte System schiebt", size=12)
t.text(38, 1307, "die Ladung über den Imin-Stickstoff bis zum Ring.", size=12)
t.text(38, 1330, "Bei den Enzymen dieser Tafel trägt der Ring-Stickstoff", size=12)
t.text(38, 1349, "ein Proton, das ein Aspartat festhält (AADC: Asp271).", size=12)
t.text(38, 1368, "Die Alanin-Racemase kommt ohne dieses Proton aus.", size=12)

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
    t.text(470, y, titel, size=12.5, gewicht=700, farbe=farbe)
    for i, z in enumerate(zeilen):
        t.text(470, y + 21 + i * 18, z, size=12)
    t.text(470, y + 21 + len(zeilen) * 18, enzyme, size=11, gewicht=700, farbe=E)
    t.text(470, y + 38 + len(zeilen) * 18, stoffe, size=11, farbe=R)

t.kasten(20, 1410, 960, 152, fill="var(--surface-2)")
t.text(38, 1432, "&#9315; UND DAS LYSIN? ES BLEIBT IM AKTIVEN ZENTRUM UND ARBEITET WEITER",
       size=11, gewicht=700, farbe=C)
t.text(38, 1454, "Das freigesetzte ε-Amin sitzt auf derselben Seite wie die brechende Bindung. "
                 "Deshalb ist es das vorgesehene Säure-Base-Werkzeug, und deshalb", size=12)
t.text(38, 1473, "laufen Abzug und Rückgabe des Protons unter Retention ab.", size=12)
t.text(38, 1496, "Transaminase: erst Base, sie zieht das C&#945;-H ab; dann Säure, sie gibt "
                 "dasselbe Proton an das C4&#8242;.", size=12)
t.text(38, 1515, "Decarboxylase: nur Säure, denn am C&#945; geht CO&#8322; ab. Protoniert sie "
                 "aus Versehen das C4&#8242;, entsteht totes Enzym mit PMP.", size=12)
t.text(38, 1534, "β-Eliminase: wieder Base am C&#945;; beim β-Ersatz protoniert dasselbe Lysin "
                 "danach zurück.", size=12)
t.text(538, 1534, "Zuletzt greift es erneut das C4&#8242; an: Zone A rückwärts, "
                  "das Produkt wird frei.", size=12, farbe=C)

# ===================================================== ZONE D · Hemmstoffe
t.zone(1595, "D · WIE ARZNEISTOFFE HIER ANGREIFEN")
t.text(20, 1627, "Zwei ganz verschiedene Prinzipien, beide am selben Cofaktor.", size=12.5)

t.kasten(20, 1655, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(38, 1677, "DEN COFAKTOR ABFANGEN", size=11, gewicht=700, farbe=R)
t.text(38, 1699, "Carbidopa und Benserazid tragen eine Hydrazino-", size=12.5)
t.text(38, 1718, "Gruppe. Sie greift das C4&#8242; des internen Aldimins", size=12.5)
t.text(38, 1737, "an und verdrängt das Lysin, also Zone A mit einem", size=12.5)
t.text(38, 1756, "Hydrazin. PLP bleibt als Hydrazon gebunden.", size=12.5)
t.text(38, 1779, "Isoniazid tut chemisch dasselbe, aber im ganzen", size=12.5)
t.text(38, 1798, "Körper; daher die Polyneuropathie.", size=12.5)

t.kasten(510, 1655, 470, 152, fill="var(--drug-bg)", stroke=R)
t.text(528, 1677, "DEN MECHANISMUS MISSBRAUCHEN", size=11, gewicht=700, farbe=R)
t.text(528, 1699, "Vigabatrin ist ein echtes Suizidsubstrat: Es durch-", size=12.5)
t.text(528, 1718, "läuft den Mechanismus bis zum Chinoid und alkyliert", size=12.5)
t.text(528, 1737, "erst dann das Enzym kovalent.", size=12.5)
t.text(528, 1760, "Prüfungsfalle: Vigabatrin hemmt die GABA-Trans-", size=12.5)
t.text(528, 1779, "aminase, also den Abbau, nicht die Decarboxylase", size=12.5)
t.text(528, 1798, "und damit nicht den Aufbau.", size=12.5)

t.kasten(20, 1829, 960, 76, fill="var(--surface-2)")
t.text(38, 1851, "WARUM PLP IN SO VIELEN KAPITELN AUFTAUCHT", size=11, gewicht=700, farbe=G)
t.text(38, 1873, "Register A in Teil 9 führt die PLP-Enzyme dieser Unterlage auf: die "
                 "Decarboxylasen aller biogenen Amine, die Transaminasen, die", size=12.5)
t.text(38, 1892, "Cystathionin-&#946;-Synthase, die &#948;-Aminolävulinat-Synthase der Häm-Synthese "
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

mech.speichern("m01", t.svg(ARIA), t)
