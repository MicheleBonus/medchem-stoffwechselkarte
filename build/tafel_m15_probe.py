# -*- coding: utf-8 -*-
"""
M-15 · Vitamin K, gebaut mit mech.py.

Vorher stand die ganze Tafel als Text da - selbst der Glutamatrest war die
Zeichenkette "Protein-CH2-CH2-COO". Zone A fuehrt jetzt beide Schritte aus:
die Deprotonierung durch das Alkoxid und den Angriff des Carbanions auf CO2.

Beide Gerueste dieser Tafel kommen dreimal vor und haengen deshalb an einem
Leitgeruest (mech_kerne.eigener):

  NAPH  Naphthochinon in Hydrochinon, Epoxid und Chinon. Lehrbuchlage: der
        Benzoring links, der Chinonring rechts, die beiden Carbonyle oben und
        unten, das 2-Methyl oben rechts, die Seitenkette R unten rechts.
  GLU   der Glutamatrest in Ausgangsstoff, Carbanion und Gla. Das Protein
        liegt links, die Kette laeuft nach rechts, und das γ-C sitzt in der
        unteren Zacke - der γ-Wasserstoff zeigt dadurch nach unten, dorthin,
        wo das Alkoxid steht und wo spaeter das CO2 angreift.

Die Elektronenpfeile sind ueber schub() angemeldet; Bauchseite, Oeffnungswinkel
und Ankerlage sucht der Solver in mech_schub.py, geprueft wird gegen
mech_regeln.py.

Ein Pfeil des alten Bestandes ist nicht mehr gezeichnet: das Paar der
C-H-Bindung, das am γ-C zurueckbleibt. Am γ-C haengen drei Bindungen, die den
Vollkreis in drei Sektoren von je 120 Grad teilen. Der Schwanz eines solchen
Pfeils sitzt neben der C-H-Bindung, die Spitze hoechstens 0,45 L vom Atom
entfernt - beide liegen damit im selben Sektor, und die Sehne wird kuerzer als
die zugelassenen 0,60 L. Der einzige laengere Weg fuehrt ueber eine der beiden
anderen Bindungen hinweg. Das ist keine Frage der Lage: der Bau bricht bei jeder
Bindungslaenge von 21 bis 36 px und in jeder Drehung ab. Die Aussage steht
deshalb im Text der Zone, und das freie Paar ist am Carbanion gezeichnet, wo es
den naechsten Pfeil traegt.
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

# Der Chinonring traegt die Lage: C2 (mit dem Methyl) auf 30 Grad, C3 (mit der
# Seitenkette) 60 Grad dahinter. Damit steht die Ringfusion senkrecht links, und
# der Benzoring liegt links davon - so, wie das Naphthochinon im Buch steht.
# Das Muster verlangt den Substituenten an C3 ausdruecklich; ohne ihn traefe es
# den Ring auch in der Gegenrichtung, und die drei Stufen stuenden gespiegelt.
NAPH = mech_kerne.eigener(
    "naphthochinon", "CC1=C(CC)C(=O)c2ccccc2C1=O",
    muster=("[#6]~[#6]1~[#6](~[#0,#6])~[#6](~[#8])~[#6]2~[#6]~[#6]~[#6]~[#6]"
            "~[#6]~2~[#6]~1~[#8]"),
    ring=[1, 2, 5, 7, 12, 13], leit=1, folge=2, winkel=30.0)

# Die Lage des Glutamatrests haengt am Ladungszeichen des Carbanions. RDKit setzt
# es als Hochstellung rechts neben das "C" und schneidet die Bindung erst hinter
# der ganzen Beschriftung ab. Lag die Bindung zum Carboxylat wie zuvor nach
# rechts oben, begann ihr Strich 8,8 px vom Atom entfernt - hinter dem Minus, so
# dass das Zeichen im Austritt der Bindung stand und die Kette gebrochen wirkte.
# Bei dieser Drehung laufen beide Bindungen des γ-C nach links unten (160 Grad)
# und nach oben (281 Grad); ihre Striche setzen 3,6 bzw. 4,6 px vom Atom an, und
# das Minus steht frei in der Luecke, in der auch der γ-Wasserstoff sass.
GLU = mech_kerne.eigener(
    "glutamat", "CCCC(=O)[O-]",
    muster="[#0,#6]~[#6]~[#6]~[#6](~[#8])~[#8]",
    ring=[0, 1, 2, 3], leit=0, folge=1, winkel=240.0)

t = mech.Tafel(1000, 1260)

# ===================================================== ZONE A · die Carboxylierung
t.zone(24, "A · DAS PROBLEM: EIN PROTON, DAS NICHT WEG WILL")
t.text(20, 54, "Der γ-Wasserstoff eines Glutamatrests hat einen pK<tspan baseline-shift='sub' "
               "font-size='9'>a</tspan> um 28. Keine Seitenkette eines Proteins reicht als Base "
               "heran: Selbst dem stärksten", size=12.5)
t.text(20, 73, "Kandidaten, dem Serin-Alkoholat mit pK<tspan baseline-shift='sub' "
               "font-size='9'>a</tspan> um 16, fehlen zwölf Zehnerpotenzen. Die nötige "
               "Basenstärke entsteht erst bei der Vitamin-K-Oxygenierung.", size=12.5)
t.text(20, 92, "Der Pfeil der Base endet am Wasserstoffkern; das Paar der C&#8211;H-Bindung "
               "bleibt am γ-C zurück und steht unter dem γ-C des Carbanions als freies Paar.",
       size=12.5)

glu = t.mol("*CCC(=O)[O-]", 140, 176, labels={0: "Protein"}, wasserstoff=[2],
            kern=GLU, name="Glutamatrest")
hg = glu.h_index[2]
t.atomnummer(glu, 2, "γ-C", winkel=345, abstand=25, size=10.5, farbe=W, gewicht=700)
t.ueberschrift(glu, "Glutamatrest im unreifen Gerinnungsfaktor", abstand=26,
               size=10.5, farbe=G, gewicht=None)

# Die Base greift den Wasserstoffkern an, nicht die C-H-Bindung: Der Pfeil endet
# deshalb am H-Atom selbst. Der ausgeschriebene Wasserstoff steht rechts unter dem
# γ-C; das Alkoxid steht deshalb schraeg darunter, in der Verlaengerung der
# C-H-Bindung, sonst muesste sein Pfeil quer durch das Geruest greifen.
alkoxid = t.paar(196, 234, 224, "Alkoxid aus Vitamin K")
t.text(206, 254, "R&#8722;O&#8315;", size=12.5, anchor="middle", gewicht=700, farbe=C)
t.text(206, 270, "das Alkoxid aus Zone B", size=10, anchor="middle", farbe=G)
t.schub(alkoxid, Atom(glu, hg))

t.reaktionspfeil(268, 176, 336)
t.text(302, 166, "&#8722; H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

carb = t.mol("*C[CH-]C(=O)[O-]", 410, 176, labels={0: "Protein"}, kern=GLU,
             name="Carbanion")
t.ueberschrift(carb, "das Carbanion: kurzlebig, aber stark nucleophil", abstand=26,
               size=10.5, farbe=G, gewicht=None)

# CO2 steht senkrecht: das freie Paar des Carbanions zeigt nach schraeg unten,
# und der Pfeil trifft den Kohlenstoff dadurch quer zur O=C=O-Achse, nicht auf
# einen der beiden Sauerstoffe. Angriff und Ausweichen des pi-Paars sind ein
# Schritt und deshalb als Kette angemeldet: die Pruefung verlangt Kopf an Schwanz.
co2 = t.mol("O=C=O", 480, 240, zeige={0: "oben"}, name="Kohlendioxid")
t.schub(Paar(carb, 2), Atom(co2, 1), kette="b")
t.schub(Bindung(co2, 1, 2), Paar(co2, 2), kette="b")
t.unterschrift(co2, "CO&#8322;", abstand=24, farbe=G)

t.reaktionspfeil(566, 176, 706)

gla = t.mol("*CC(C(=O)[O-])C(=O)[O-]", 812, 176, labels={0: "Protein"},
            kern=GLU, name="Gla")
t.unterschrift(gla, "γ-Carboxyglutamat: zwei Carboxylate",
               "an einem Kohlenstoff binden Calcium", abstand=30)

t.kasten(20, 312, 960, 58, fill="var(--warn-bg)", stroke=W)
t.text(38, 334, "Erst der Gla-Rest macht den Gerinnungsfaktor funktionsfähig: Zwei benachbarte "
                "Carboxylate greifen ein Calciumion, und dieses vermittelt die Bindung", size=12.5)
t.text(38, 353, "an die negativ geladene Membranoberfläche aktivierter Thrombozyten. Ohne "
                "Carboxylierung schwimmt der Faktor wirkungslos im Plasma.", size=12.5)

# ===================================================== ZONE B · der Zyklus
t.zone(400, "B · WOHER DIE BASENSTÄRKE KOMMT UND WOHIN DER COFAKTOR GEHT")
t.text(20, 430, "Der Sauerstoff addiert sich an das Hydrochinon; über ein Peroxid und ein "
                "Dioxetan entsteht ein Alkoxid am Ring. Dieser Schritt ist stark exergon,",
       size=12.5)
t.text(20, 449, "und weil das Alkoxid in einer wasserfreien Tasche entsteht, steigt seine "
                "Basenstärke um viele Zehnerpotenzen. Carboxylierung und Epoxidbildung sind "
                "gekoppelt.", size=12.5)

kh2 = t.mol("Cc1c(*)c(O)c2ccccc2c1O", 156, 578, labels={3: "R"}, kern=NAPH,
            name="Hydrochinon")
t.unterschrift(kh2, "KH&#8322;, das Hydrochinon:", "die einzige wirksame Form", abstand=30)

t.reaktionspfeil(268, 578, 396)
t.text(332, 540, "+ O&#8322;", size=11, anchor="middle", gewicht=700, farbe=C)
t.text(332, 558, "über Peroxid und Dioxetan", size=10, anchor="middle", farbe=G)
t.text(332, 602, "&#8722; H&#8322;O. Hier entsteht das Alkoxid am C2,", size=10, anchor="middle",
       farbe=W, gewicht=700)

epox = t.mol("CC12OC1(*)C(=O)c1ccccc1C2=O", 520, 578, labels={4: "R"}, kern=NAPH,
             name="K-2,3-Epoxid")
t.unterschrift(epox, "K-2,3-Epoxid: der Cofaktor ist verbraucht", abstand=30)

t.reaktionspfeil(632, 578, 750)
t.text(691, 550, "VKORC1", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(691, 600, "&#8867; Cumarine", size=10.5, anchor="middle", gewicht=700, farbe=R)
t.text(691, 620, "+ 2 [H], &#8722; H&#8322;O", size=10, anchor="middle", farbe=C)

chin = t.mol("CC1=C(*)C(=O)c2ccccc2C1=O", 862, 578, labels={3: "R"}, kern=NAPH,
             name="Vitamin-K-Chinon")
t.unterschrift(chin, "Vitamin-K-Chinon: die Form,", "die im Präparat steckt", abstand=30)

# Rueckweg vom Chinon zum Hydrochinon: aussen herum, damit der Pfeil weder die
# Bildunterschriften kreuzt noch von unten in das Hydrochinon hineinsticht.
t.stuecke.append((1, "<path d='M 862 682 L 862 716 L 70 716 L 70 578 L 100 578' fill='none' "
                     "stroke='currentColor' stroke-width='1.5' marker-end='url(#rxn)'/>"))
t.text(509, 734, "VKORC1 führt auch diesen zweiten Schritt aus und wird ebenso von den "
                 "Cumarinen gehemmt.", size=11, anchor="middle", gewicht=700, farbe=E)
t.text(509, 752, "Beide Reduktionen verbrauchen je zwei Reduktionsäquivalente aus dem Dithiol "
                 "des Enzyms.", size=10.5, anchor="middle", farbe=G)

# Ein langer Pfeil quer ueber die Tafel wuerde durch drei Beschriftungen laufen.
# Der Verweis steht deshalb auf beiden Seiten im Text.
t.text(332, 616, "das oben das γ-Proton abzieht", size=10, anchor="middle",
       farbe=W, gewicht=700)

# ===================================================== ZONE C · Klinik
t.zone(786, "C · WAS SICH FÜR DIE THERAPIE DARAUS ERGIBT")

t.kasten(20, 818, 470, 158, fill="var(--drug-bg)", stroke=R)
t.text(38, 840, "CUMARINE HEMMEN DIE REDUKTASE, NICHT DIE CARBOXYLASE", size=11,
       gewicht=700, farbe=R)
t.text(38, 862, "Phenprocoumon und Warfarin blockieren die VKORC1 und", size=12.5)
t.text(38, 881, "damit die Rückgewinnung des Cofaktors. Die Carboxylase", size=12.5)
t.text(38, 900, "selbst bleibt unberührt, ihr geht nur das Substrat aus.", size=12.5)
t.text(38, 923, "Daraus folgt die Antidotwirkung von Vitamin K&#8321;: In hoher", size=12.5)
t.text(38, 942, "Dosis umgeht es die blockierte VKOR über eine zweite,", size=12.5)
t.text(38, 961, "NAD(P)H-abhängige Reduktase.", size=12.5)

t.kasten(510, 818, 470, 158, fill="var(--surface-2)")
t.text(528, 840, "WARUM DIE WIRKUNG ERST NACH TAGEN EINSETZT", size=11, gewicht=700, farbe=G)
t.text(528, 862, "Betroffen ist ausschließlich die Neusynthese. Die bereits", size=12.5)
t.text(528, 881, "carboxylierten Faktoren im Plasma arbeiten weiter, bis sie", size=12.5)
t.text(528, 900, "abgebaut sind. Beim Faktor II dauert das etwa drei Tage.", size=12.5)
t.text(528, 923, "Bei akuter Blutung nützt Vitamin K deshalb wenig; man", size=12.5)
t.text(528, 942, "ersetzt die Faktoren direkt durch ein Prothrombin-", size=12.5)
t.text(528, 961, "komplexkonzentrat.", size=12.5)

t.kasten(20, 1000, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1022, "DIE PRÜFUNGSFALLE", size=11, gewicht=700, farbe=W)
t.text(38, 1044, "Protein C ist ebenfalls Vitamin-K-abhängig und fällt mit einer Halbwertszeit um "
                 "acht Stunden fast so schnell ab wie Faktor VII, während die", size=12.5)
t.text(38, 1063, "Faktoren II, IX und X noch vorhanden sind. Zu Beginn einer Cumarintherapie "
                 "überwiegt deshalb kurzzeitig die gerinnungsfördernde Seite: die "
                 "Cumarinnekrose.", size=12.5)

t.kasten(20, 1120, 960, 96, fill="var(--surface-2)")
t.text(38, 1142, "WELCHE FAKTOREN BETROFFEN SIND", size=11, gewicht=700, farbe=G)
t.text(38, 1164, "II, VII, IX und X, dazu Protein C, S und Z. Merkhilfe: 1972, die vier Ziffern "
                 "sind die Faktoren. Faktor VII hat mit vier bis sechs Stunden die", size=12.5)
t.text(38, 1183, "kürzeste Halbwertszeit und bestimmt den frühen INR-Anstieg; Faktor II mit rund "
                 "drei Tagen die eigentliche antithrombotische Wirkung.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Vitamin K in drei Zonen. Zone A zeigt die Gamma-Carboxylierung an echten Strukturen: Ein "
    "Alkoxid zieht mit einem Elektronenpaarpfeil das Gamma-Wasserstoffatom eines Glutamatrests "
    "ab, dessen Saeurestaerke mit einem pKa um 28 eigentlich zu gering dafuer ist; selbst das "
    "Alkoholat eines Serins, die staerkste Base, die ein Protein bereitstellen kann, reicht mit "
    "einem pKa um 16 nicht heran. Das entstehende Carbanion greift Kohlendioxid an, und es "
    "entsteht Gamma-Carboxyglutamat mit zwei Carboxylatgruppen an einem Kohlenstoff. Zone B "
    "zeigt den Vitamin-K-Zyklus mit gezeichneten Strukturen: Das Hydrochinon reagiert mit "
    "Sauerstoff ueber ein Peroxid und ein Dioxetan; dabei entsteht am Ringkohlenstoff C2 das "
    "Alkoxid, das in Zone A als Base wirkt und dessen Basenstaerke in der wasserfreien Tasche "
    "des Enzyms stark erhoeht ist, und es bleibt das Vitamin-K-2,3-Epoxid zurueck. Die "
    "Epoxidreduktase VKORC1 fuehrt es ueber das Chinon zum Hydrochinon zurueck, jeweils unter "
    "Verbrauch von zwei Reduktionsaequivalenten; genau diese beiden Schritte hemmen die "
    "Cumarine. Zone C erklaert Antidotwirkung, Wirklatenz und die Rolle des Protein C."
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

mech.speichern("m15", t.svg(ARIA), t)
