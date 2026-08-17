# -*- coding: utf-8 -*-
"""
M-03 · Biotin, gebaut mit mech.py.

Die Tafel hatte bisher keine einzige Struktur, nur Kaesten und einen
schematischen Arm. Jetzt sind beide Halbreaktionen ausgefuehrt: die
Carboxylierung des Biotins und die Uebertragung auf das Enolat.

Der Ureido-Bicyclus kommt in drei Stufen vor - Biotin, Carboxybiotin in Zone B,
dasselbe Carboxybiotin noch einmal in Zone C. Er haengt deshalb an einem eigenen
Leitgeruest (KERN, siehe unten), damit er in allen drei Bildern gleich steht.
Die Pfeile sind ueber schub() angemeldet; Bauchseite, Oeffnungswinkel und
Ankerlage kommen aus dem Solver in mech_schub.py.
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

# d-Biotin ist (3aS,4S,6aR): alle drei Ringprotonen stehen cis auf derselben
# Seite des cis-verknuepften Bicyclus. Die Stereodeskriptoren sind gegen
# PubChem CID 171548 geprueft; mit der Valeriansaeurekette statt des Dummys
# liefert rdCIPLabeler genau diese drei Zuordnungen.
BIOTIN = "O=C1N[C@H]2CS[C@@H](*)[C@H]2N1"
# Carboxyliert wird N1': der Ureidostickstoff am Ringfusionskohlenstoff C6a',
# also der von der Seitenkette abgewandte. Mit der Valeriansaeurekette statt des
# Dummys ist die Struktur kanonisch identisch mit dem PubChem-Eintrag zum
# 1'-N-Carboxybiotin. Hier ist das Atom 2. Bei pH 7,4 liegt das Carbamat als
# Anion vor, deshalb [O-].
CARBOXY = "O=C1N(C(=O)[O-])[C@H]2CS[C@@H](*)[C@H]2N1"
# RDKit zeichnet Atomlabel aus einem eigenen Vektorfont, der weder
# HTML-Entitaeten noch Tiefstellungszeichen kennt; beides faellt im Bild aus.
# Deshalb hier nur "Lys"; die Amidbindung erklaert die Unterschrift.
KETTE = "Lys"

# Das Leitgeruest des Bicyclus. Lehrbuchlage: der Harnstoff-Carbonyl zeigt nach
# oben, der Schwefel des Tetrahydrothiophens nach unten, die Valeriansaeurekette
# nach links unten - und damit steht N1' oben rechts, also auf der Seite, von der
# das Kohlendioxid kommt und auf der spaeter das Carbamat sitzt. Das Muster fasst
# den ganzen Bicyclus samt dem ersten Kettenatom; ohne dieses Atom waere der
# Bicyclus spiegelsymmetrisch und die Vorlage koennte umklappen.
KERN = mech_kerne.eigener(
    "biotin-bicyclus", "O=C1N[C@H]2CS[C@@H](CCCCC(=O)O)[C@H]2N1",
    muster="[#8]~[#6]1~[#7]~[#6]2~[#6]~[#16]~[#6](~*)~[#6]~2~[#7]~1",
    ring=[1, 2, 3, 14, 15], leit=2, folge=3, winkel=30.0)

t = mech.Tafel(1000, 1420)

# ===================================================== ZONE A · Aktivierung
t.zone(24, "A · WARUM EINE CARBOXYLIERUNG ATP KOSTET")
t.text(20, 54, "Hydrogencarbonat ist kein Elektrophil. Erst das ATP macht daraus ein gemischtes "
               "Anhydrid, das in Kohlendioxid und Phosphat zerfällt.", size=12.5)

hco3 = mech.Molekuel("OC(=O)[O-]", 116, 170, zeige={1: "rechts"}, name="Hydrogencarbonat")
t.mole.append(hco3)
t.unterschrift(hco3, "Hydrogencarbonat", abstand=28, farbe=G)

t.reaktionspfeil(180, 170, 254)
t.text(217, 158, "+ ATP", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(217, 192, "&#8722; ADP, &#8722; H&#8314;", size=10, anchor="middle", farbe=G)

cp = mech.Molekuel("[O-]C(=O)OP(=O)([O-])[O-]", 356, 170, zeige={1: "links"},
                   name="Carboxyphosphat")
t.mole.append(cp)
t.unterschrift(cp, "Carboxyphosphat, ein gemischtes Anhydrid", abstand=28, farbe=G)

t.reaktionspfeil(468, 170, 542)
t.text(505, 158, "&#8722; P&#7522;", size=10.5, anchor="middle", gewicht=700, farbe=G)

co2 = mech.Molekuel("O=C=O", 604, 170, zeige={0: "oben"}, name="Kohlendioxid")
t.mole.append(co2)
t.unterschrift(co2, "CO&#8322;", abstand=24, farbe=G)

t.kasten(690, 104, 290, 186, fill="var(--cofaktor-bg)", stroke=C)
t.text(708, 126, "DIE BILANZ", size=11, gewicht=700, farbe=C)
t.text(708, 148, "Ein ATP wird zu ADP und Phosphat", size=12.5)
t.text(708, 167, "gespalten, und zwar hier, nicht bei", size=12.5)
t.text(708, 186, "der eigentlichen Carboxylierung.", size=12.5)
t.text(708, 209, "Der teure Schritt ist die Aktivierung.", size=12, farbe=G)
t.text(708, 234, "Das freigesetzte Phosphat bleibt im", size=12, farbe=G)
t.text(708, 253, "Zentrum und wird gleich als Base", size=12, farbe=G)
t.text(708, 272, "gebraucht.", size=12, farbe=G)

# ===================================================== ZONE B · Carboxylierung
t.zone(300, "B · DAS BIOTIN NIMMT DAS CO&#8322; AUF")
t.text(20, 330, "Carboxyliert wird N1&#8242;: der Ureidostickstoff am Ringfusionskohlenstoff "
                "C6a&#8242;, also der von der Valeriansäurekette abgewandte. Als Amid-Stickstoff", size=12.5)
t.text(20, 349, "ist er von sich aus kein Nucleophil. Erst wenn das Phosphat aus Zone A ihm sein "
                "Proton abnimmt, greift er das Kohlendioxid an.", size=12.5)

bio = mech.Molekuel(BIOTIN, 270, 486, labels={7: KETTE},
                    wasserstoff=[2], kern=KERN, name="Biotin")
t.mole.append(bio)
hn = bio.h_index[2]

# Das Phosphat steht dicht ueber dem N-H: sein Pfeil kommt von oben herein, der
# Pfeil aus der N-H-Bindung zieht nach rechts oben zum Kohlendioxid ab. Stuende
# das Phosphat weiter rechts, kaemen sich die beiden ins Gehege.
pi = t.paar(320, 398, 105, "Phosphat")
t.text(320, 382, "P&#7522;", size=12.5, anchor="middle", gewicht=700, farbe=C)
t.text(320, 366, "das Phosphat aus Zone A", size=10, anchor="middle", farbe=G)

# Das Kohlendioxid steht rechts oberhalb, in der Verlaengerung der N-H-Bindung.
# Weiter unten geht es nicht: dort stehen die beiden gezeichneten Ringprotonen so
# eng, dass zwischen ihnen kein Bogen mit dem vorgeschriebenen Freiraum durchgeht.
co2b = mech.Molekuel("O=C=O", 365, 435, zeige={0: "oben"}, name="Kohlendioxid")
t.mole.append(co2b)
t.text(382, 440, "CO&#8322;", size=10.5, farbe=G)

# Ein Schritt, drei Pfeile: das Phosphat nimmt das Proton, das Paar der
# N-H-Bindung wird zur neuen N-C-Bindung, und ein pi-Paar des Kohlendioxids
# weicht auf den Sauerstoff aus.
t.schub(pi, Atom(bio, hn), kette="B")
t.schub(Bindung(bio, 2, hn), Atom(co2b, 1), kette="B")
t.schub(Bindung(co2b, 0, 1), Paar(co2b, 0), kette="B")
t.unterschrift(bio, "Biotin, über (CH&#8322;)&#8324;&#8722;CO an ein Lysin gebunden;",
               "das Elektronenpaar der N&#8722;H-Bindung wird zur neuen N&#8722;C-Bindung", abstand=30)

t.reaktionspfeil(560, 486, 634)

cbio = mech.Molekuel(CARBOXY, 790, 486, labels={10: KETTE},
                     kern=KERN, name="Carboxybiotin")
t.mole.append(cbio)
t.unterschrift(cbio, "Carboxybiotin: das CO&#8322; ist jetzt gebunden",
               "und wird nicht mehr in die Lösung entlassen", abstand=30)

# ===================================================== ZONE C · Uebertragung
t.zone(614, "C · UND GIBT ES AM ZWEITEN ZENTRUM WIEDER AB")
t.text(20, 644, "Dort zerfällt das Carboxybiotin, und das dabei frei werdende Biotin-Anion ist "
                "selbst die Base: es nimmt dem Acetyl-CoA das α-Proton ab. Deshalb laufen", size=12.5)
t.text(20, 663, "Deprotonierung und Carboxylierung praktisch gleichzeitig ab. Das Enolat greift den "
                "Carboxylkohlenstoff an, und die N&#8722;C-Bindung bricht.", size=12.5)

cbio2 = mech.Molekuel(CARBOXY, 200, 772, labels={10: KETTE},
                      kern=KERN, name="Carboxybiotin")
t.mole.append(cbio2)

# Der Carboxylkohlenstoff ist trigonal: seine drei Nachbarn stehen 120 Grad
# auseinander. Die einzige Luecke, die nicht auf den Ring zeigt, liegt zwischen
# den beiden Carboxylat-Sauerstoffen nach rechts oben; dort steht das Enolat.
# Gedreht statt waagerecht gelegt: RDKit setzt das Minuszeichen als Hochstellung
# dicht rechts neben das C, und bei waagerechter C-C-Bindung steht es genau im
# Abstand einer zweiten Bindungslinie darueber - das Minus und der Strich lesen
# sich dann zusammen als Doppelbindung. Mit 20 Grad Drehung laeuft die Bindung
# schraeg unter dem Zeichen weg.
enol = mech.Molekuel("[CH2-]C(=O)*", 326, 742, labels={3: "SCoA"}, rotate=20.0,
                     name="Acetyl-CoA-Enolat")
t.mole.append(enol)

# Wieder ein Schritt, und in dieser Reihenfolge, damit die Pfeile Kopf an
# Schwanz haengen: erst der Angriff des Enolats auf den Carboxylkohlenstoff,
# dann der Bruch der N-C-Bindung.
#
# Wohin das Paar dieser Bindung geht, ist ausgeschrieben. Am Stickstoff selbst
# laesst es sich nicht zeigen: er sitzt im Ring, seine beiden Ringbindungen
# lassen ihm nur zwei schmale Luecken nach aussen, und beide liegen so dicht an
# der brechenden Bindung, dass jeder Bogen dorthin kuerzer waere als das erlaubte
# Mindestmass - der Solver lehnt alle 840 Kandidaten ab. Ausgeschrieben ist es
# ohnehin die bessere Aussage: das Biotin-Anion ist ein Amid-Anion und damit
# mesomeriestabilisiert, das Paar wird vom Ureido-Carbonyl aufgenommen. Genau
# deshalb zerfaellt das Carbamat so bereitwillig.
#
# art="ring": der zweite Pfeil endet an einer Ringbindung des Ureido-Rings und
# ist der Resonanzpfeil des Amid-Anions. Regel F4 gibt dafuer 0,60-0,90 L vor,
# nicht die 0,75-1,20 L eines gewoehnlichen innermolekularen Pfeils. Mit dem
# weiteren Fenster waehlte der Solver eine Sehne von 1,02 L, und dabei setzte
# der Schwanz unterhalb der brechenden N-C-Bindung an: der Bogen kreuzte die
# Bindung, aus der er kommt. Mit dem Resonanzfenster liegen Schwanz und Bogen
# geschlossen oberhalb der Bindung.
t.schub(Paar(enol, 0), Atom(cbio2, 3), kette="C")
t.schub(Bindung(cbio2, 2, 3), Bindung(cbio2, 1, 2), kette="C", art="ring")
t.schub(Bindung(cbio2, 0, 1), Paar(cbio2, 0), kette="C")

t.unterschrift(cbio2, "die N&#8722;C-Bindung bricht, das Biotin-Anion",
               "wird frei und wirkt als Base; sein Paar",
               "wandert ins Ureido-Carbonyl", abstand=30)
# Wer die Base ist, steht im Zonentext: das Biotin-Anion aus dem Bild links.
# Eine laengere Beschriftung an dieser Stelle kreuzt den Angriffspfeil.
t.ueberschrift(enol, "Acetyl-CoA, als Enolat deprotoniert", abstand=26, size=10.5,
               farbe=G, gewicht=None)

t.reaktionspfeil(560, 772, 634)

mal = mech.Molekuel("[O-]C(=O)CC(=O)*", 790, 772, labels={6: "SCoA"}, zeige={0: "links"},
                    name="Malonyl-CoA")
t.mole.append(mal)
t.unterschrift(mal, "Malonyl-CoA: der Baustein, an dem",
               "die Fettsäuresynthese hängt", abstand=30)

# ===================================================== ZONE D · Arm und Enzyme
t.zone(898, "D · DER SCHWENKARM UND DIE VIER HUMANEN CARBOXYLASEN")

t.kasten(20, 930, 470, 118, fill="var(--surface-2)")
t.text(38, 952, "WARUM ZWEI ZENTREN UND EIN ARM", size=11, gewicht=700, farbe=G)
t.text(38, 974, "Beide Halbreaktionen laufen an verschiedenen Stellen des", size=12.5)
t.text(38, 993, "Enzyms. Biotin und Lysin bilden zusammen einen etwa", size=12.5)
t.text(38, 1012, "16 Å langen Arm, der das gebundene CO&#8322; von einem", size=12.5)
t.text(38, 1031, "Zentrum zum anderen trägt, ohne es freizusetzen.", size=12.5)

t.kasten(510, 930, 470, 118, fill="var(--cofaktor-bg)", stroke=C)
t.text(528, 952, "DASSELBE PRINZIP AN ZWEI WEITEREN STELLEN", size=11, gewicht=700, farbe=C)
t.text(528, 974, "Das Liponamid im Pyruvat-Dehydrogenase-Komplex und", size=12.5)
t.text(528, 993, "das Phosphopantethein der Fettsäure-Synthase arbeiten", size=12.5)
t.text(528, 1012, "genauso: ein reaktives Zwischenprodukt bleibt kovalent", size=12.5)
t.text(528, 1031, "gebunden und wandert zwischen den Zentren.", size=12.5)

CARBOXYLASEN = [
    (20, "Pyruvat-Carboxylase", "Pyruvat → Oxalacetat",
     "startet die Gluconeogenese"),
    (270, "Acetyl-CoA-Carboxylase", "→ Malonyl-CoA",
     "schrittbestimmend für die Fettsäuresynthese"),
    (540, "Propionyl-CoA-Carboxylase", "→ Methylmalonyl-CoA",
     "danach folgt die Mutase aus Tafel M-16"),
    (790, "Methylcrotonyl-CoA-Carboxylase", "im Leucinabbau",
     "der Marker im Neugeborenenscreening"),
]
for x, name, r1, r2 in CARBOXYLASEN:
    t.text(x, 1092, name, size=11.5, gewicht=700, farbe=E)
    t.text(x, 1112, r1, size=11)
    t.text(x, 1130, r2, size=11, farbe=G)

t.kasten(20, 1158, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1180, "WORAN ES IN DER PRAXIS SCHEITERT", size=11, gewicht=700, farbe=W)
t.text(38, 1202, "Ein alimentärer Biotinmangel ist selten, weil Darmbakterien Biotin bilden. "
                 "Klinisch zählen drei Sonderfälle: der Biotinidase-Mangel, bei dem Biotin", size=12.5)
t.text(38, 1221, "nicht aus dem Biocytin zurückgewonnen wird; große Mengen rohen Eiklars, dessen "
                 "Avidin das Biotin praktisch irreversibel bindet; und die", size=12.5)
t.text(38, 1240, "Langzeittherapie mit Antikonvulsiva.", size=12.5)

t.kasten(20, 1282, 960, 76, fill="var(--drug-bg)", stroke=R)
t.text(38, 1304, "EINE LABORFALLE, DIE IM EXAMEN GERN GEFRAGT WIRD", size=11, gewicht=700, farbe=R)
t.text(38, 1326, "Hochdosiertes Biotin als Nahrungsergänzung verfälscht Immunoassays, die auf der "
                 "Biotin-Streptavidin-Bindung beruhen. Je nach Testaufbau", size=12.5)
t.text(38, 1345, "fallen TSH, Troponin oder die Schilddrüsenhormone falsch aus. Vor der Blutabnahme "
                 "muss Biotin deshalb abgesetzt werden.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Biotin in vier Zonen. Zone A zeigt, warum eine Carboxylierung ATP kostet: Hydrogencarbonat "
    "wird mit ATP zum gemischten Anhydrid Carboxyphosphat, das in Kohlendioxid und Phosphat "
    "zerfaellt. Zone B zeigt die Carboxylierung des Biotins am Ureidostickstoff N1-Strich, dem "
    "Stickstoff am Ringfusionskohlenstoff C6a-Strich, der von der Valeriansaeurekette abgewandt "
    "ist. Der Bicyclus traegt die Konfiguration des natuerlichen d-Biotins: alle drei Ringprotonen "
    "stehen cis auf derselben Seite. Drei Elektronenpaarpfeile: "
    "Das Phosphat aus Zone A nimmt dem Stickstoff sein Proton ab, "
    "das Elektronenpaar der Stickstoff-Wasserstoff-Bindung greift den Kohlenstoff des "
    "Kohlendioxids an, und eine der beiden Doppelbindungen weicht auf den Sauerstoff aus. Es "
    "entsteht Carboxybiotin als Carbamat-Anion. Zone C zeigt die Uebertragung am zweiten aktiven "
    "Zentrum: Das als Enolat deprotonierte Acetyl-CoA greift den Carboxylkohlenstoff an, die "
    "Stickstoff-Kohlenstoff-Bindung bricht, und ihr Elektronenpaar bleibt nicht am Stickstoff "
    "stehen, sondern geht weiter in das Ureido-Carbonyl. Das frei werdende Biotin-Anion ist "
    "deshalb ein mesomeriestabilisiertes Amid-Anion und dabei selbst die Base. "
    "Es entsteht Malonyl-CoA. Zone D erklaert den sechzehn Angstroem langen Schwenkarm "
    "aus Biotin und Lysin, nennt die vier humanen Carboxylasen und die klinischen Sonderfaelle."
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

mech.speichern("m03", t.svg(ARIA), t)
