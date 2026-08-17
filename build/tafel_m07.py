# -*- coding: utf-8 -*-
"""
M-07 · Nicotinamid-Coenzyme, gebaut mit mech.py.

Zwei Leitgerueste halten die Tafel zusammen (mech_kerne.py):

  NIC   der Nicotinamid-Ring. Er steht dreimal in der Tafel - als NAD&#8314;, als
        NADH daneben und noch einmal in Zone B. Alle drei liegen jetzt auf
        derselben Referenzlage: C4 oben, das Carboxamid rechts, der Ring-
        stickstoff mit dem Riborest unten links. Der Leser sieht dadurch beim
        Vergleich NAD&#8314;/NADH nur noch den Unterschied, nicht die Drehung.
  RIB   die Adenosin-Ribose der Zone C. Vorher hing die zweite Ribose ueber
        vorlage= an der ersten; das leistet ein Leitgeruest gleich mit und
        haelt zusaetzlich die Haendigkeit fest.

Die Pfeile sind schub(quelle, ziel): der Aufruf sagt nur, welche Elektronen
wohin gehen, die Geometrie sucht der Solver in mech_schub.py und misst sie
gegen mech_regeln.py.

Zone B nutzt dieselben raeumlichen Mittel wie M-01: Die beiden Wasserstoffatome
am sp3-C4 werden als Keil und Strichkeil gezeichnet - anders laesst sich pro-R
gegen pro-S nicht zeigen.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech
import mech_kerne
from mech import Atom, Bindung

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

# Nicotinamid kekulisiert eingegeben. Der Grund ist nicht Kosmetik: der Ringpfeil
# der Zone A setzt an der Doppelbindung C4=C5 an, und aus der aromatischen
# Eingabe kann RDKit ebensogut die andere Kekule-Formel zeichnen - dann stuende
# der Pfeil an einer Einfachbindung. Der Nebeneffekt ist praktisch: die
# Atomnummern stimmen jetzt mit denen der reduzierten Form ueberein -
# 3 = C3, 4 = C2, 5 = N1, 6 = Riborest, 7 = C6, 8 = C5, 9 = C4.
NADOX = "NC(=O)C1=C[N+](*)=CC=C1"
NADRED = "NC(=O)C1=CN(*)C=CC1"

# Leitgeruest Nicotinamid. leit=4 ist das C4, folge=3 das C3 - damit laeuft der
# Ring im Bild im Uhrzeigersinn und das Carboxamid steht rechts. winkel=75 legt
# das C4 nach oben: nur dann bleibt der Platz darueber frei fuer die beiden
# Wasserstoffatome der Zone B, und der Riborest kommt unten links zu liegen,
# wo ihn keine Beschriftung stoert.
NIC = mech_kerne.eigener(
    "nicotinamid", "NC(=O)c1cccnc1",
    muster="[#7]~[#6](~[#8])~[#6]1~[#6]~[#7]~[#6]~[#6]~[#6]~1",
    ring=[3, 4, 5, 6, 7, 8], leit=4, folge=3, winkel=75.0)

# Leitgeruest Ribose. leit=6 ist das C2', an dem sich die beiden Coenzyme
# unterscheiden; winkel=-90 stellt es nach unten, wo der Blick des Lesers hin
# soll. folge=4 ist das C1' und legt damit die Haendigkeit fest: das Adenin
# bleibt links, der Phosphatrest am C5' oben rechts.
RIB = mech_kerne.eigener(
    "ribose", "OCC1OC(C)C(O)C1O",
    muster="[#8]~[#6]~[#6]1~[#8]~[#6](~[*])~[#6](~[#8])~[#6]~1~[#8]",
    ring=[2, 3, 4, 6, 8], leit=6, folge=4, winkel=-90.0)

t = mech.Tafel(1000, 1320)

# ===================================================== ZONE A · Hydridtransfer
t.zone(24, "A · DAS HYDRID GEHT AN C4")
t.text(20, 54, "Gezeigt ist die Lactat-Dehydrogenase. Vier Pfeile, ein einziger Schritt: Ein "
               "Histidin des Enzyms nimmt das Proton der OH-Gruppe auf, das Paar dieser "
               "O-H-Bindung", size=12.5)
t.text(20, 73, "bildet die C=O-Doppelbindung, und gleichzeitig geht das Hydrid vom selben "
               "Kohlenstoff an das C4 des Pyridiniumrings. Eine Zwischenstufe gibt es nicht.",
       size=12.5)
t.text(20, 92, "Der vierte Pfeil rückt die Ringelektronen nach. Der letzte Schritt, das π-Paar "
               "der Bindung C6=N1 auf den Ringstickstoff, ist nicht gezeichnet: neben dem N&#8314; "
               "und", size=12.5)
t.text(20, 111, "seinem Riborest ist dafür kein Platz. Dieser Schritt neutralisiert die "
                "Ringladung; das Proton bleibt am Histidin.", size=12.5)

# Stereodeskriptor: C[C@H](O)C(=O)[O-] ist (S) und damit L-Lactat, das einzige Substrat
# der LDH. Ohne ihn stuende in Zone B die Stereospezifitaet neben einem flachen Substrat.
# zeige={6:"rechts"} dreht das C-H nach rechts, dem Ring entgegen. Das Carboxylat
# steht dann senkrecht darueber und nicht mehr in der Flugbahn; mit der frueheren
# Lage fand der Solver fuer den Hydridpfeil ueberhaupt keinen freien Bogen. Die
# OH-Gruppe zeigt dabei nach unten, das Histidin steht deshalb unten links.
# Das Lactat steht eine halbe Zeile hoeher als der Ring: das C4 liegt an der
# Spitze des Pyridiniums, und nur von schraeg oben kommt der Hydridpfeil an
# seine freie Seite, ohne den Ring zu queren.
lac = t.mol("C[C@H](O)C(=O)[O-]", 175, 196, wasserstoff=[1, 2],
            zeige={6: "rechts"}, name="Lactat")
hl = lac.h_index[1]
ho = lac.h_index[2]

# x=282 statt der frueheren 300: der Hydridpfeil ist der laengste der Tafel, und
# bei 300 mass seine Sehne 4,70 L - das Buch laesst zwischen zwei Teilchen
# hoechstens 4,00 L zu. Mit 282 sind es 3,85 L. Zwischen der Tinte des Lactats
# und dem Ring bleiben immer noch 48 px Luft, und die beiden Unterschriften
# stehen weiterhin nebeneinander statt uebereinander.
nad = t.mol(NADOX, 282, 208, labels={6: "Ribose-ADP"}, kern=NIC, name="NAD+")

# Die Base gehoert ins Bild: ohne sie bliebe das Proton am Sauerstoff sitzen und aus dem
# Pyruvat wuerde ein Oxocarbenium. Mit ihr stimmt die Ladungsbilanz beider Seiten.
t.text(105, 218, "His", size=11.5, anchor="middle", gewicht=700, farbe=E)
lp_his = t.paar(105, 234, 90, "Histidin")

# Alle vier Pfeile sind ein einziger Schritt und stehen deshalb in einer Kette:
# die Pruefung verlangt dann Kopf an Schwanz.
t.schub(lp_his, Atom(lac, ho), kette="a")                     # Base holt das Proton
t.schub(Bindung(lac, 2, ho), Bindung(lac, 1, 2), kette="a")   # O-H wird zur C=O
t.schub(Bindung(lac, 1, hl), Atom(nad, 9), kette="a")         # das Hydrid ans C4
t.schub(Bindung(nad, 8, 9), Bindung(nad, 7, 8), kette="a")    # C4=C5 wird C5=C6
# Der fuenfte Schritt - das pi-Paar der Bindung C6=N1 geht auf den Ringstickstoff -
# ist nicht gezeichnet. Er ist als Rueckhaken angemeldet worden, seit es die
# Pfeilart "zurueck" gibt, und noch einmal ohne Beschriftung, mit Bindungslaengen
# von 21 bis 31 px und in sechs Ringdrehungen von 15 bis 195 Grad geprueft.
# Jedesmal derselbe Befund: alle 768 Bogenkandidaten kreuzen Tinte.
# Der Grund liegt am Stickstoff selbst und nicht am Layout. N1 traegt drei
# Substituenten, seine drei Winkelluecken sind je 120 Grad breit, und der
# Rueckhaken braucht eine Sehne von 0,50 bis 1,05 L:
#   - Luecke bei 165 Grad, zwischen Riborest und C6: die Sehne misst von dort
#     0,23 bis 0,44 L, wenn der Schwanz aussen an der Bindung N1=C6 sitzt. Lang
#     genug (0,71 bis 0,85 L) wird sie nur von einem Schwanz auf der Ringseite -
#     dann kreuzt der Bogen die eigene Bindung N1=C6 oder das Symbol N&#8314;.
#   - Luecke bei 45 Grad, gegenueber dem C6: die Sehne stimmt (0,86 bis 1,10 L),
#     aber zwischen Schwanz und Spitze liegt die Bindung N1-Riborest. Zwischen
#     ihrem Strich und der Unterkante des Symbols N&#8314; bleiben 0,7 px.
#   - Luecke bei 285 Grad zeigt ins Ringinnere; Sehne hoechstens 0,20 bis 0,76 L,
#     und der Bogen kreuzt dabei die Ringbindungen.
# Das ist Geometrie, kein Platzmangel: dieselbe Ablehnung kommt auch dann, wenn
# das Molekuel allein auf einer leeren Tafel steht. Statt den Pfeil zu verbiegen,
# steht die Aussage im Text.
# Der frueher hier stehende gestrichelte Sammelpfeil quer durch den Ring war
# ohnehin keine zulaessige Schreibweise: seine Sehne mass 1,8 L bei 1,3 L Grenze.

t.unterschrift(lac, "L-Lactat, (S)-konfiguriert:",
               "das Histidin nimmt das Proton der OH-Gruppe auf", abstand=16)
t.atomnummer(nad, 9, "C4", winkel=290, abstand=26, size=10.5, farbe=W, gewicht=700)
t.unterschrift(nad, "NAD&#8314;, aromatisch und elektronenarm:", "deshalb nimmt C4 das Hydrid auf",
               abstand=30)

t.reaktionspfeil(440, 208, 512)
t.text(476, 190, "ein Schritt", size=10, anchor="middle", farbe=G)
t.text(476, 228, "H&#8314; ans Histidin", size=10, anchor="middle", farbe=G)

pyr = t.mol("CC(=O)C(=O)[O-]", 630, 208, zeige={1: "links"}, name="Pyruvat")
t.unterschrift(pyr, "Pyruvat", abstand=28, farbe=G)

nadh = t.mol(NADRED, 840, 208, labels={6: "Ribose-ADP"}, kern=NIC, name="NADH")
t.unterschrift(nadh, "NADH: C4 ist jetzt sp&#179;,", "die Ringladung ist neutralisiert",
               abstand=28)

t.kasten(20, 300, 960, 76, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 322, "DER UNTERSCHIED ZUM FLAVIN", size=11, gewicht=700, farbe=C)
t.text(38, 344, "Das Nicotinamid bewegt zwei Elektronen auf einmal; eine stabile Zwischenstufe mit "
                "einem ungepaarten Elektron gibt es nicht. Deshalb kann NADH nicht", size=12.5)
t.text(38, 363, "mit Sauerstoff reagieren, das Flavin dagegen schon (Tafel M-06). Aus demselben "
                "Grund erzeugen NAD-abhängige Dehydrogenasen keinen oxidativen Stress.", size=12.5)

# ===================================================== ZONE B · Stereospezifitaet
t.zone(414, "B · JEDES ENZYM WÄHLT EINE SEITE")
t.text(20, 444, "Am sp&#179;-hybridisierten C4 sitzen zwei Wasserstoffatome. Chemisch sind sie "
                "gleich, räumlich nicht: Das eine steht über, das andere unter der Ringebene.",
       size=12.5)
t.text(20, 463, "Jede Dehydrogenase überträgt stets dasselbe von beiden.", size=12.5)

nadh2 = t.mol(NADRED, 200, 590, labels={6: "Ribose-ADP"}, kern=NIC, name="NADH sp3")
cx, cy = nadh2.atom(9)
rx = sum(nadh2.atom(i)[0] for i in (3, 4, 5, 7, 8, 9)) / 6.0
t.keil(cx, cy, cx - 30, cy - 34, breite=7.5, farbe=E)
t.text(cx - 34, cy - 42, "H<tspan baseline-shift='sub' font-size='8'>A</tspan> · pro-<tspan "
       "font-style='italic'>R</tspan>", size=11, anchor="end", gewicht=700, farbe=E)
t.strichkeil(cx, cy, cx + 30, cy - 34, breite=7.0)
t.text(cx + 34, cy - 42, "H<tspan baseline-shift='sub' font-size='8'>B</tspan> · pro-<tspan "
       "font-style='italic'>S</tspan>", size=11, gewicht=700, farbe=R)
t.ebene(rx, cy + 30, breite=150, tiefe=34, farbe=G, beschriftung="Ringebene")
t.unterschrift(nadh2, "dasselbe C4, von der Seite gesehen", abstand=64)

t.text(430, 512, "A-Seite: das pro-<tspan font-style='italic'>R</tspan>-Wasserstoffatom",
       size=12.5, gewicht=700, farbe=E)
t.text(430, 534, "Alkohol-Dehydrogenase · Lactat-Dehydrogenase · Malat-Dehydrogenase", size=12)

t.text(430, 570, "B-Seite: das pro-<tspan font-style='italic'>S</tspan>-Wasserstoffatom",
       size=12.5, gewicht=700, farbe=R)
t.text(430, 592, "Glutamat-Dehydrogenase · GAPDH · Glucose-6-phosphat-Dehydrogenase", size=12)

t.kasten(430, 616, 550, 96, fill="var(--surface-2)")
t.text(448, 638, "WIE MAN DAS GEZEIGT HAT", size=11, gewicht=700, farbe=G)
t.text(448, 660, "Mit deuteriertem Substrat. Das eingebaute Deuterium erscheint bei jedem", size=12.5)
t.text(448, 679, "Enzym reproduzierbar an derselben Position. Das belegt, dass das", size=12.5)
t.text(448, 698, "Coenzym im aktiven Zentrum in fester Orientierung gebunden wird.", size=12.5)

# ===================================================== ZONE C · NAD gegen NADP
t.zone(766, "C · EINE PHOSPHATGRUPPE TRENNT ZWEI STOFFWECHSELWELTEN")
t.text(20, 796, "NADP&#8314; unterscheidet sich von NAD&#8314; an genau einer Stelle: einer "
                "Phosphatgruppe an der 2&#8242;-Position der Adenosin-Ribose.", size=12.5)

# Die beiden Ribosen stehen nebeneinander, damit der Leser den einen Unterschied
# sieht. Das Leitgeruest legt beide auf dieselbe Lage, Drehung und Haendigkeit.
# Die zweite steht 15 px tiefer und 3 px weiter rechts angesetzt: t.mol() setzt
# den Schwerpunkt aller Atome, und die fuenf Atome der Phosphatgruppe ziehen ihn
# nach unten rechts. Ohne diesen Ausgleich staenden die beiden Ringe nicht auf
# derselben Hoehe - nachgemessen an den fuenf Ringatomen, nicht geschaetzt.
rib = t.mol("*OC[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O", 180, 918,
            labels={0: "P", 6: "Adenin"}, kern=RIB, name="NAD-Ribose")
t.unterschrift(rib, "NAD&#8314;: hier steht eine freie OH-Gruppe", abstand=30, farbe=E)

ribp = t.mol("*OC[C@H]1O[C@@H](*)[C@H](OP(=O)([O-])[O-])[C@@H]1O", 563, 933,
             labels={0: "P", 6: "Adenin"}, kern=RIB, name="NADP-Ribose")
t.unterschrift(ribp, "NADP&#8314;: und hier ein Phosphat", abstand=30, farbe=R)

t.kasten(760, 852, 220, 132, fill="var(--surface-2)")
t.text(778, 874, "KEINE CHEMIE,", size=11, gewicht=700, farbe=G)
t.text(778, 890, "NUR EIN KENNZEICHEN", size=11, gewicht=700, farbe=G)
t.text(778, 914, "Die Phosphatgruppe greift", size=12)
t.text(778, 933, "nicht in die Reaktion ein.", size=12)
t.text(778, 956, "Sie sagt dem Enzym nur,", size=12)
t.text(778, 975, "welchen Pool es benutzt.", size=12)

# ===================================================== ZONE D · die zwei Pools
t.zone(1042, "D · WARUM DAS ZWEI GETRENNTE POOLS ERGIBT")

t.kasten(20, 1074, 470, 118, fill="var(--enzym-bg)", stroke=E)
t.text(38, 1096, "NAD&#8314;: DER ABBAU", size=11, gewicht=700, farbe=E)
t.text(38, 1118, "Liegt zu etwa 700 : 1 oxidiert vor. Ein so hoher", size=12.5)
t.text(38, 1137, "Überschuss an Oxidationsmittel zieht jede", size=12.5)
t.text(38, 1156, "Dehydrogenase in Richtung Oxidation: Glykolyse,", size=12.5)
t.text(38, 1175, "β-Oxidation, Citratzyklus.", size=12.5)

t.kasten(510, 1074, 470, 118, fill="var(--drug-bg)", stroke=R)
t.text(528, 1096, "NADPH: DER AUFBAU", size=11, gewicht=700, farbe=R)
t.text(528, 1118, "Liegt zu etwa 75 : 1 reduziert vor. Der Überschuss", size=12.5)
t.text(528, 1137, "an Reduktionsmittel treibt die Fettsäure- und", size=12.5)
t.text(528, 1156, "Steroidsynthese, die Glutathionreduktase und die", size=12.5)
t.text(528, 1175, "Monooxygenasen aus Tafel M-08.", size=12.5)

t.kasten(20, 1216, 960, 76, fill="var(--warn-bg)", stroke=W)
t.text(38, 1238, "DAS EIGENTLICH BEMERKENSWERTE", size=11, gewicht=700, farbe=W)
t.text(38, 1260, "Beide Pools liegen im selben Zellkompartiment nebeneinander, ohne sich zu "
                 "vermischen. Möglich ist das nur, weil jedes Enzym über die eine", size=12.5)
t.text(38, 1279, "Phosphatgruppe entscheidet, welches der beiden Coenzyme es bindet. Ein "
                 "Erkennungsmerkmal ersetzt hier eine Membran.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Nicotinamid-Coenzyme in vier Zonen. Zone A zeigt am Beispiel der Lactat-Dehydrogenase den "
    "Hydridtransfer in vier gleichzeitigen Pfeilen: Ein Histidin des Enzyms nimmt mit seinem "
    "freien Elektronenpaar das Proton der Hydroxylgruppe des L-Lactats auf, das Paar der "
    "geloesten Sauerstoff-Wasserstoff-Bindung bildet die Doppelbindung zum Sauerstoff, und "
    "gleichzeitig wandert das Wasserstoffatom am selben Kohlenstoff als Hydrid an das "
    "Kohlenstoffatom vier des Pyridiniumrings. Ein vierter Pfeil rueckt die Ringelektronen "
    "nach: das Elektronenpaar der Doppelbindung zwischen C4 und C5 bildet die Doppelbindung "
    "zwischen C5 und C6. Der letzte Schritt, das Paar der Doppelbindung zwischen C6 und dem "
    "Ringstickstoff, ist nicht gezeichnet, weil neben dem Stickstoffsymbol und seinem "
    "Riborest kein Platz dafuer ist; er steht im Text. Es entstehen "
    "Pyruvat und NADH, dessen C4 nun sp3-hybridisiert "
    "ist. Zone B zeigt die Stereospezifitaet raeumlich: Die beiden Wasserstoffatome am C4 sind "
    "als Keil und als Strichkeil gezeichnet, das eine ueber, das andere unter der als Flaeche "
    "dargestellten Ringebene; jede Dehydrogenase uebertraegt stets dasselbe von beiden. Zone C "
    "zeigt den einzigen strukturellen Unterschied zwischen NAD und NADP: eine Phosphatgruppe an "
    "der 2-Strich-Position der Adenosin-Ribose. Zone D erklaert, warum daraus zwei getrennte "
    "Redoxpools entstehen."
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

mech.speichern("m07", t.svg(ARIA), t)
