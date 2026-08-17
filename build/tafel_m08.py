# -*- coding: utf-8 -*-
"""
M-08 · Der Cytochrom-P450-Zyklus, gebaut mit mech.py.

Der Zyklus selbst ist ein Zustandsdiagramm - dafuer ist der Kreis die richtige
Darstellung. Neu ist, dass die acht Zustaende als gezeichnete Eisenzentren aus
einem Bausatz kommen statt als Textzeilen, und dass die drei Schritte, an denen
wirklich Chemie passiert, mit Elektronenpfeilen ausgefuehrt sind:
die heterolytische O-O-Spaltung, die Wasserstoffabstraktion und der Rebound.

Die Pfeile sind auf schub(quelle, ziel) umgestellt. Vier Besonderheiten dieser
Tafel:

  - Die Haem-Zustaende sind Zentrum()-Bausteine ohne SMILES. Ihre Ankerpunkte
    (fe, s, ax, axb) gehen als feste Orte durch den Solver; er bestimmt daran
    Bauchseite, Oeffnungswinkel und die genaue Lage von Schwanz und Spitze.
    Seit das Zentrum seine Striche und Beschriftungen in die Tintenkarte meldet,
    haelt er dort von sich aus Abstand.
  - Die Pfeilart steht dort von Hand, wo Quelle und Ziel zum selben Teilchen
    gehoeren, der Solver das aber nicht sehen kann. art="intra" beim Thiolat,
    das auf das Eisen desselben Komplexes schiebt; art="zurueck" bei den beiden
    Haken, die aus der Fe-O-Bindung auf eines ihrer eigenen Atome zurueckgehen.
    Ohne die Angabe raet er auf "inter" und verlangt eine Sehne von mindestens
    1,5 Bindungslaengen - fuer einen Schub im Metallzentrum ist das zu weit.
  - winkel=/abstand= an fe() und ax() sind kein Nachbessern von Hand, sondern
    die einzige Stellschraube, die ein fester Anker hat. Sie sagt nicht, wo die
    Spitze landet, sondern um welchen Ort herum der Solver seinen Faecher legt.
    Massgeblich ist, dass die Spitze vor dem Wort stehen bleibt: "Fe(III)" ist
    siebenmal so breit wie "O", und ein Anker im Wortmittelpunkt schoebe sie
    quer durch die Schrift. Nachgemessen steht jede Spitze 0,25 bis 0,40
    Bindungslaengen vor ihrem Glyphen, und vier der sechs Koepfe zeigen weniger
    als 3 Grad neben dem gemeinten Ort vorbei; der Rueckhaken aufs Eisen liegt
    bei 13 Grad, der Pfeil zum abgehenden Wasser bei 17 - dessen Ziel ist keine
    Atomlage, sondern die Stelle, an der das Wasser das Bild verlaesst.
  - Ibuprofen und sein Radikal liegen auf demselben Leitgeruest (mech_kerne).
    Vorher bekam jede Stufe ihr eigenes Compute2DCoords, und der Leser musste
    das zweite Bild erst neu einnorden, statt den Unterschied zu sehen.
"""
import math
import os

import mech
import mech_kerne
from mech import Bindung, Elektron

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

# Leitgeruest fuer Ibuprofen und sein Radikal: der Aromat liegt fest, das Atom 4
# (Ringkohlenstoff mit der Isobutylkette) zeigt nach links. Damit steht die
# angegriffene tertiaere C-H-Bindung in beiden Stufen auf der Seite des Haems,
# und die Reaktion laeuft mit der Leserichtung von links nach rechts.
IBU = mech_kerne.eigener(
    "ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    muster="[#6]~[#6](~[#6])~[#6]~[#6]1~[#6]~[#6]~[#6](~[#6]~[#6]~1)~[#6]",
    ring=[4, 5, 6, 7, 8, 9], leit=4, folge=5, winkel=180.0)

t = mech.Tafel(1000, 1400)

# ===================================================== ZONE A · der Zyklus
t.zone(24, "A · DER KATALYTISCHE ZYKLUS: ACHT ZUSTÄNDE, ZWEI ELEKTRONEN")
t.text(20, 50, "Alle acht Zustände unterscheiden sich in der Oxidationsstufe des Eisens und in "
               "dem, was axial daran hängt.", size=12.5)
t.text(20, 68, "Bei Compound I kommt das Porphyrin hinzu: es trägt dort ein Elektron weniger.",
       size=12.5)

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
    # Compound II: das aufgenommene H-Atom reduziert das Porphyrin-Radikalkation,
    # nicht das Eisen. Erst der Rebound bringt Fe(IV) auf Fe(III) zurueck.
    (315, "&#9319;", "Fe(IV)",  ["OH"],        False, False),
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
    (270, "+ H&#8226;", "aus R&#8722;H"),
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
    ("&#9318;", "Fe(IV)=O, Porphyrin&#8226;&#8314;", "Compound I, das Oxidans"),
    ("&#9319;", "Fe(IV)&#8722;OH, R&#8226;", "Compound II, Radikalpaar im Käfig"),
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
t.text(638, 622, "Kompetitiv: zwei Substrate am selben Enzym.", size=12.5)
t.text(638, 645, "Koordinativ: Azole binden mit einem Ring-", size=12.5)
t.text(638, 664, "Stickstoff direkt ans Häm-Eisen.", size=12.5)
t.text(638, 687, "Mechanismusbasiert: Ritonavir, Clarithromycin.", size=12.5)

# ===================================================== ZONE B · O-O-Spaltung
t.zone(748, "B · &#9317; → &#9318;  DIE HETEROLYTISCHE SPALTUNG: HIER ENTSTEHT DAS OXIDANS")
t.text(20, 778, "Das distale Sauerstoffatom wird protoniert und geht als Wasser ab. Beide "
                "Elektronen der O&#8722;O-Bindung nehmen es mit.", size=12.5)

z0 = t.zentrum(150, 890, "Fe(III)", axial=["O", "OH&#8322;"],
               name="Compound 0, protoniert")

# Das Paar der O-O-Bindung geht mit der Abgangsgruppe: die Spitze steht dort, wo
# das Wasser hin verschwindet. Kein Molekuel, also eine benannte Marke.
wasser = t.marke(236, 828, "abgehendes Wasser")
t.schub(z0.axb(0, 1), wasser)
t.text(246, 822, "geht als H&#8322;O ab", size=10.5, farbe=W, gewicht=700)
t.text(246, 838, "mit beiden Bindungselektronen", size=10.5, farbe=G)

# Das freie Paar des Cystein-Thiolats schiebt auf das Eisen. Beides gehoert zum
# selben Komplex, deshalb art="intra". Der Anker liegt nicht im Eisensymbol,
# sondern links daneben: "Fe(III)" ist ein breites Wort, und die Spitze gehoert
# davor. Nachgemessen steht sie 0,32 Bindungslaengen vor dem Wortrand und der
# Kopf zeigt 1,0 Grad neben dem Metallmittelpunkt vorbei.
lp_s = t.paar(118, 910, 180, "Cystein-Thiolat")
t.schub(lp_s, z0.fe(winkel=155, abstand=10), art="intra")
t.text(20, 944, "Schub vom Thiolat", size=10.5, farbe=W, gewicht=700)
t.text(150, 968, "protonierter Hydroperoxo-Komplex", size=10.5, anchor="middle", farbe=G)

t.reaktionspfeil(370, 890, 440)
t.text(405, 880, "&#8722; H&#8322;O", size=11, anchor="middle", gewicht=700, farbe=E)

z1 = t.zentrum(506, 890, "Fe(IV)", axial=["O"], doppelt=True, radikal=True,
               name="Compound I")
t.text(506, 946, "Compound I", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(506, 960, "Fe(IV)=O, Porphyrin&#8226;&#8314;", size=10.5, anchor="middle", farbe=G)

t.kasten(578, 800, 402, 168, fill="var(--surface-2)")
t.text(596, 822, "WARUM NICHT HOMOLYTISCH", size=11, gewicht=700, farbe=G)
t.text(596, 844, "Bräche die O&#8722;O-Bindung homolytisch, entstünden zwei", size=12.5)
t.text(596, 863, "Radikale und das Enzym würde sich selbst zerstören.", size=12.5)
t.text(596, 886, "Das Thiolat verhindert das: Es stabilisiert die höhere", size=12.5)
t.text(596, 905, "Oxidationsstufe am Eisen so weit, dass der heterolytische", size=12.5)
t.text(596, 924, "Weg günstiger wird. Die zweite Oxidationsäquivalenz", size=12.5)
t.text(596, 943, "lagert das Porphyrin als Radikalkation zwischen.", size=12.5)

# ===================================================== ZONE C · Abstraktion und Rebound
t.zone(1006, "C · &#9318; → &#9319; → &#9312;  ABSTRAKTION UND REBOUND: BEIDE SCHRITTE RADIKALISCH")
t.text(20, 1036, "Compound I holt sich zuerst ein Wasserstoffatom. Dessen Elektron reduziert das "
                 "Porphyrin-Radikalkation und nicht das Eisen: es entsteht", size=12.5)
t.text(20, 1056, "Compound II, Fe(IV)&#8722;OH. Erst der Rebound der Hydroxylgruppe auf das "
                 "Kohlenstoffradikal bringt das Eisen auf Fe(III) zurück. Wo angegriffen wird,",
       size=12.5)
t.text(20, 1076, "entscheidet die Bindetasche und nicht die Bindungsstärke: beim Ibuprofen sind "
                 "die benzylischen C&#8722;H-Bindungen die schwächeren. Der Rebound läuft",
       size=12.5)
t.text(20, 1096, "so schnell, dass sich das Radikal in aller Regel nicht umlagert. Daran lässt "
                 "sich der Mechanismus experimentell prüfen.", size=12.5)
t.text(20, 1120, "Das zweite Elektron der C&#8722;H-Bindung bleibt am tertiären Kohlenstoff; "
                 "zwischen dessen vier Bindungen ist für einen eigenen Pfeil kein Platz.",
       size=11.5, farbe=G)

zc1 = t.zentrum(84, 1196, "Fe(IV)", axial=["O"], doppelt=True, radikal=True,
                schritt=62, name="Compound I")
ibu = mech.Molekuel("CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O", 201, 1192,
                    wasserstoff=[1], kern=IBU, name="Ibuprofen")
t.mole.append(ibu)
hidx = ibu.h_index[1]

# Homolyse der C-H-Bindung: ein Elektron geht mit dem Wasserstoff auf den
# Oxo-Sauerstoff, das andere bleibt am tertiaeren Kohlenstoff zurueck.
#
# Gezeichnet ist nur der erste Haken. Der zweite - der Rueckhaken aus derselben
# Bindung auf das eigene Kohlenstoffatom - laesst sich hier nicht setzen, und
# zwar aus einem Grund, der mit der Pfeilart "zurueck" nichts zu tun hat: das
# tertiaere C traegt vier Bindungen, gezeichnet bei 60, 150, 210 und 300 Grad.
# Neben der C-H-Bindung (210 Grad) bleiben damit nur ein Sektor von 60 und einer
# von 90 Grad frei. U4 setzt den Schwanz auf 0,47-0,64 L vom Kohlenstoff, rund
# 21-34 Grad neben der Bindung, Z1 die Spitze auf hoechstens 0,46 L; innerhalb
# eines 90-Grad-Sektors ergibt das eine Sehne von hoechstens 0,30 L. Der Schaft
# braucht 0,38 L, das Sehnenfenster von "zurueck" 0,55 L. Wer weiter ausholt,
# kreuzt eine der vier Bindungen. Der Solver verwirft alle 1020 Kandidaten mit
# derselben Begruendung ("kreuzt eine Bindung oder ein Atomsymbol") und kommt
# ueber eine Sehne von 0,14 L nicht hinaus; warum_pfeil.py nennt als naechste
# Stoerelemente die drei Bindungen des Kohlenstoffs selbst (6,5 und zweimal
# 9,2 px) und sein eigenes Wasserstoffsymbol (9,2 px). Das naechste fremde
# Stueck - die Beschriftung des Haems - liegt 40,3 px entfernt. Es ist also
# allein die Nachbarschaft dieses einen Atoms: Verschieben hilft nicht, und
# Vergroessern auch nicht, weil alle Masse in Bindungslaengen zaehlen. Die
# Aussage steht deshalb im Text; das Radikal in der rechten Struktur zeigt sie
# ohnehin.
t.schub(Bindung(ibu, 1, hidx), zc1.ax(0, winkel=-40, abstand=4), elektronen=1)
t.unterschrift(ibu, "Ibuprofen: angegriffen wird das tertiäre C-Atom",
               "der Isobutylgruppe, es entsteht 2-Hydroxyibuprofen", abstand=44)
t.text(84, 1258, "Compound I", size=10.5, anchor="middle", gewicht=700, farbe=W)

t.reaktionspfeil(432, 1192, 496)
t.text(464, 1182, "H&#8226;", size=11, anchor="middle", gewicht=700, farbe=E)

zc2 = t.zentrum(566, 1196, "Fe(IV)", axial=["OH"], schritt=62, name="Compound II")
# Die Radikalstelle steht im SMILES: das Kohlenstoffatom hat wirklich nur drei
# Bindungen und ein Einzelelektron. Elektron(ibr, 1) zeichnet den Punkt selbst
# und setzt den Schwanz daran an.
ibr = mech.Molekuel("C[C](C)Cc1ccc(cc1)[C@H](C)C(=O)O", 691, 1192,
                    kern=IBU, name="Ibuprofen-Radikal")
t.mole.append(ibr)

# Drei Fischhaken, weil drei Elektronen ihren Platz wechseln: das Radikalelektron
# und ein Elektron der Fe-O-Bindung bilden die neue C-O-Bindung, das zweite Elektron
# dieser Bindung bleibt am Eisen und macht aus Fe(IV) wieder Fe(III).
#
# Die beiden Haken aus der Fe-O-Bindung setzen je einer links und einer rechts
# vom Bindungsstrich an und laufen nach entgegengesetzten Seiten auseinander -
# das ist die uebliche Schreibweise fuer eine Homolyse.
#
# axb() liefert die Bindungsmitte selbst, also einen Punkt *auf* dem Strich; U4
# verlangt den Schwanz seitlich daneben. Die Koordinationsstriche des Zentrums
# stehen inzwischen in der Tintenkarte, der Solver haelt also von sich aus
# Abstand; der Punkt hier gibt nur die Seite vor, links oder rechts.
#
# art="zurueck": beide Haken kommen aus der Fe-O-Bindung und enden an einem ihrer
# eigenen Atome. Der Solver erkennt das an Molekuelbindungen selbst, an den
# gezeichneten Zentren kann er es nicht - dort steht es hier.
def fe_o(seite):
    """Schwanz neben der Fe-O-Bindung von Compound II, seite = -1 links, +1 rechts."""
    return mech.Punkt(zc2.x + seite * 4.5, zc2.y - 29.0,
                      ("zentrum-bindung", zc2.name, (-1, 0)))


t.schub(Elektron(ibr, 1), zc2.ax(0, winkel=-30, abstand=4), elektronen=1)
t.schub(fe_o(+1), zc2.ax(0, winkel=40, abstand=10), elektronen=1, art="zurueck")
t.schub(fe_o(-1), zc2.fe(winkel=205, abstand=10), elektronen=1, art="zurueck")
t.unterschrift(ibr, "Kohlenstoffradikal: die Hydroxylgruppe fällt zurück,",
               "das Eisen wird dabei zu Fe(III) reduziert", abstand=44)
t.text(566, 1258, "Compound II, Fe(IV)&#8722;OH", size=10.5, anchor="middle",
       gewicht=700, farbe=W)

# ===================================================== ZONE D · Bilanz
t.zone(1310, "D · WAS SICH DARAUS ABLEITEN LÄSST")
t.text(20, 1340, "Die Bilanz lautet R&#8722;H + O&#8322; + NADPH + H&#8314; → R&#8722;OH + "
                 "H&#8322;O + NADP&#8314;. Von den beiden Sauerstoffatomen geht eines ins "
                 "Substrat, eines ins Wasser.", size=12.5)
t.text(20, 1360, "Daher der Name Monooxygenase, und daher der NADPH-Verbrauch, der die "
                 "Biotransformation an den Pentosephosphatweg koppelt.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Der katalytische Zyklus des Cytochrom P450 in vier Zonen. Zone A zeigt acht Eisenzentren "
    "im Kreis, jedes mit dem Porphyrin als Balken, dem Cystein-Thiolat darunter und dem "
    "axialen Liganden darueber: wassergebundenes Eisen drei, dann Substratbindung, erste "
    "Reduktion zu Eisen zwei, Sauerstoffanlagerung, zweite Reduktion zum Peroxokomplex, "
    "Protonierung zum Hydroperoxo, Compound eins mit Eisen vier gleich Sauerstoff und "
    "Porphyrin-Radikalkation, schliesslich Compound zwei mit Eisen vier und Hydroxid neben "
    "dem Substratradikal. Zone B zeigt mit Elektronenpaarpfeilen, wie die "
    "Sauerstoff-Sauerstoff-Bindung heterolytisch bricht, wobei das Thiolat Elektronendichte "
    "auf das Eisen schiebt und Wasser abgeht. Zone C zeigt mit Fischhakenpfeilen die "
    "Abstraktion eines Wasserstoffatoms vom tertiaeren Kohlenstoff des Ibuprofens, wodurch "
    "aus Compound eins Compound zwei wird, und den anschliessenden Rebound der Hydroxylgruppe "
    "auf das Kohlenstoffradikal, bei dem ein Elektron der Eisen-Sauerstoff-Bindung am Eisen "
    "bleibt und es von Eisen vier auf Eisen drei zurueckfuehrt."
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
