# -*- coding: utf-8 -*-
"""
M-05 · S-Adenosylmethionin, gebaut mit der Mechanismus-Sprache aus mech.py.

Alle Strukturen kommen von RDKit, alle Bildunterschriften sitzen an der
tatsaechlichen Ausdehnung des jeweiligen Molekuels, und alle Elektronenpfeile
sind ueber t.schub(quelle, ziel) nur noch chemisch beschrieben: Bauchseite,
Oeffnungswinkel, Ankerlage und der Winkel jedes freien Elektronenpaars kommen
aus dem Solver in mech_schub.py, geprueft wird gegen mech_regeln.py.

Das Methionin-Geruest steht fuenfmal auf der Tafel - als freie Aminosaeure, als
Sulfonium in drei Fassungen und als S-Adenosylhomocystein. Ein tafeleigenes
Leitgeruest (METHIONIN, siehe unten) legt alle fuenf auf dieselbe Lage: die
Kette laeuft von der Carboxylatgruppe links zum Schwefel rechts, der dritte
Substituent am Sulfonium haengt nach unten. Damit steht in Zone A das freie
Paar des Schwefels nach rechts, wo das ATP wartet, in Zone B die Methylgruppe
nach unten, wo das Catecholat angreift, und in Zone C die C5'-S-Bindung frei
nach oben rechts, wo die Fischhaken Platz brauchen.

Zwei Elektronenbewegungen der Tafel sind nicht gezeichnet, und zwar aus einem
Grund, der nichts mit dieser Tafel zu tun hat: beide enden am Sulfonium-
Schwefel und kommen aus einer seiner eigenen Bindungen. Um ein dreifach
substituiertes Atom herum stehen die Bindungen 120 Grad auseinander. Der
Schwanz sitzt seitlich neben der Quellbindung, die Spitze in einer der drei
Luecken; die beiden Luecken neben der Quellbindung liegen so dicht daneben,
dass die Sehne nur etwa 0,4 L lang wird (gefordert sind 0,60 L), und in die
dritte kommt kein Bogen, ohne eine der beiden anderen Bindungen zu kreuzen.
Mit einem zweifach substituierten Sauerstoff oder Schwefel gelingt derselbe
Pfeil anstandslos - in Zone A ist er gezeichnet. Was die beiden fehlenden
Pfeile sagen wuerden, steht im Fliesstext der Zonen B und C.
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

# Leitgeruest: die Methioninkette S-CH2-CH2-CH(N)-COO. ring nennt die Atome,
# an denen die Lage haengt (Schwefel, beide Methylenkohlenstoffe, C-alpha und
# der Carboxylkohlenstoff), leit den Schwefel, folge den Carboxylkohlenstoff -
# das Paar legt die Haendigkeit fest, so dass die Kette nach links laeuft und
# der Schwefel rechts aussen steht.
METHIONIN = mech_kerne.eigener(
    "methionin", "CSCC[C@H]([NH3+])C(=O)[O-]",
    muster="[#16]~[#6]~[#6]~[#6](~[#7])~[#6](~[#8])~[#8]",
    ring=[1, 2, 3, 4, 6], leit=1, folge=6, winkel=353.0)

t = mech.Tafel(1000, 1330)

# ===================================================== ZONE A · Aktivierung
t.zone(24, "A · DIE AKTIVIERUNG: WOZU DAS ATP GEBRAUCHT WIRD")
t.text(20, 54, "Der Schwefel greift nicht am Phosphor an, sondern am C5&#8242; der Ribose. "
               "Deshalb geht das gesamte Triphosphat, unten als PPP abgekürzt, ab.", size=12.5)

met = t.mol("CSCC[C@H]([NH3+])C(=O)[O-]", 150, 168, kern=METHIONIN,
            name="Methionin")
# ATP verkuerzt: C5' nach links, der Brueckensauerstoff darueber, die drei
# Phosphate als kurze Marke "PPP". Die ausgeschriebene Marke "Triphosphat" ist
# so breit, dass sie sowohl in der Bahn des Pfeils von links auf das C5' liegt
# als auch dort, wo das Elektronenpaar der brechenden Bindung landet.
atp = t.mol("*OC[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O", 295, 208,
            labels={0: "PPP", 6: "Adenin"},
            zeige={2: "links", 1: "oben"}, name="ATP")
sam = t.mol("C[S+](CC[C@H]([NH3+])C(=O)[O-])C[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O",
            760, 213, labels={13: "Adenin"}, kern=METHIONIN, name="SAM")

# Ein Schritt: das freie Paar des Schwefels bildet die Bindung zum C5', und
# gleichzeitig geht das Paar der Bindung C5'-O auf den Brueckensauerstoff, mit
# dem das Triphosphat abgeht. Die beiden stehen ohne kette= da, obwohl sie
# zusammengehoeren. Der Grund ist geometrisch: die Kette zieht den Schwanz des
# zweiten Pfeils an die Spitze des ersten, und die liegt links neben der Bindung
# C5'-O. Von dort muss der Bogen quer ueber die eigene Quellbindung, um rechts
# am Sauerstoff zu enden. Ohne die Kette setzt der Solver den Schwanz rechts
# neben die Bindung, und der Pfeil legt sich sauber um den Sauerstoff. Die beiden
# Spitzen liegen trotzdem 0,98 L auseinander und teilen sich das C5'.
t.schub(Paar(met, 1), Atom(atp, 2))
t.schub(Bindung(atp, 2, 1), Paar(atp, 1))

t.unterschrift(met, "L-Methionin, ein neutraler Thioether")
t.unterschrift(atp, "ATP: angegriffen wird der Zucker, nicht das Phosphat")
t.unterschrift(sam, "S-Adenosylmethionin", "drei Substituenten am Schwefel = Sulfonium",
               gewicht=700, farbe=R)

t.reaktionspfeil(420, 198, 520)
t.text(470, 188, "MAT", size=11.5, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(470, 216, "Methionin-Adenosyltransferase", size=9.5, anchor="middle", farbe=G)
# Das Tripolyphosphat zerfaellt erst durch Hydrolyse in PPi und Pi; ohne das
# Wasser geht die Atombilanz des zweiten Teilschritts nicht auf.
t.text(470, 234, "+ H&#8322;O", size=10.5, anchor="middle", farbe=C)
t.text(470, 250, "&#8722; P&#7522; &#8722; PP&#7522;", size=10.5, anchor="middle", farbe=C)

t.kasten(20, 336, 520, 76, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 358, "WAS DAS ATP BEWIRKT", size=11, gewicht=700, farbe=C)
t.text(38, 380, "Die Methylgruppe ist dieselbe wie im Methionin. Neu ist die Ladung am "
                "Schwefel: sie macht", size=12.5)
t.text(38, 399, "das Methyl elektrophil und den abgehenden Thioether ungeladen.", size=12.5)

# ===================================================== ZONE B · S_N2
t.zone(468, "B · DIE ÜBERTRAGUNG: S<tspan baseline-shift='sub' font-size='8.5'>N</tspan>2 "
            "AM METHYLKOHLENSTOFF")

# Das C5' steht hier als eigenes Atom, der Rest heisst deshalb "Adenin-Ribose".
# Hiesse die Marke "Adenosyl", steckte das C5' zweimal im Bild und die Bilanz
# gegen das SAH der Produktzeile ginge um eine CH2-Gruppe daneben.
smk = t.mol("C[S+](CC[C@H]([NH3+])C(=O)[O-])C*", 340, 560,
            labels={10: "Adenin-Ribose"}, kern=METHIONIN, name="SAM, Zone B")
cat = t.mol("Oc1ccccc1[O-]", 297, 648, zeige={7: "rechts"}, name="Catecholat")

# Gezeichnet ist der angreifende Pfeil. Der zweite Pfeil desselben Schrittes -
# das Paar der Bindung Methyl-Schwefel bleibt am Schwefel - ist nicht gezeichnet:
# um ein dreifach substituiertes Atom herum stehen die drei Bindungen 120 Grad
# auseinander, und in die Luecke daneben passt kein Bogen, der die Mindestlaenge
# einhaelt, ohne eine der beiden anderen Bindungen zu kreuzen. Die Aussage steht
# im Uebergangszustand (gestrichelte Bindung, delta plus am Schwefel), im
# Fliesstext darunter und in der Unterschrift des SAH.
t.schub(Paar(cat, 7), Atom(smk, 0))

t.ueberschrift(smk, "S-Adenosylmethionin", abstand=24,
               size=11, farbe=G, gewicht=700)
t.unterschrift(cat, "Catecholat, das Nucleophil der COMT")

t.reaktionspfeil(540, 566, 610)

# Uebergangszustand
t.ts_klammer(652, 503, 954, 617)
t.text(812, 523, "Angriff auf der abgewandten Seite", size=11, anchor="middle",
       gewicht=700, farbe=W)
t.text(702, 569, "ArO", size=13.5, anchor="end", gewicht=700, farbe=E)
t.text(708, 562, "&#948;&#8722;", size=9.5, farbe=G)
t.linie(714, 565, 781, 565, farbe=W, breite=1.6, strich="4 3")
# Der angegriffene Kohlenstoff steht als "C" da, seine drei Wasserstoffe stehen
# einzeln daneben. Stuende hier "CH3" und darunter noch drei Striche, waeren die
# Wasserstoffe zweimal im Bild und der Kohlenstoff traege acht Bindungen. Die
# drei Striche stehen im Winkel von 120 Grad um das C - einer nach oben, zwei
# nach unten -, denn genau das ist die planare Anordnung, von der die Zeile
# darunter spricht. Nach unten allein waere sie pyramidal, also der sp3-Zustand
# vor und nach dem Uebergang.
t.text(794, 569, "C", size=13.5, anchor="middle", gewicht=700)
t.linie(808, 565, 876, 565, farbe=W, breite=1.6, strich="4 3")
t.text(888, 569, "S", size=14, gewicht=700, farbe=C)
t.text(898, 562, "&#948;+", size=9.5, farbe=G)
t.linie(794, 556, 794, 545, breite=1.3)
t.text(794, 542, "H", size=10.5, anchor="middle")
t.linie(788, 574, 778, 584, breite=1.3)
t.text(771, 594, "H", size=10.5, anchor="middle")
t.linie(800, 574, 810, 584, breite=1.3)
t.text(817, 594, "H", size=10.5, anchor="middle")
t.text(812, 607, "planare CH&#8323;-Gruppe, fünffach koordinierter Übergangszustand", size=10,
       anchor="middle", farbe=G)

t.text(20, 736, "Ein einziger Schritt: Bindungsbildung und Bindungsbruch laufen gleichzeitig. "
                "Weil das Nucleophil auf der dem", size=12.5)
t.text(20, 755, "Schwefel abgewandten Seite angreift, kehrt sich die Konfiguration am "
                "Methylkohlenstoff um. Mit dreifach isotopen-", size=12.5)
t.text(20, 774, "markiertem Methyl (H, D, T) ist diese Inversion nachgewiesen worden. "
                "Gezeichnet ist der Pfeil des Angriffs; das Paar der", size=12.5)
t.text(20, 793, "brechenden Bindung bleibt am Schwefel und macht ihn zum neutralen "
                "Thioether &#8211; im Übergangszustand steht dafür das &#948;+.", size=12.5)

# Produkte
t.text(20, 826, "PRODUKTE", size=11, gewicht=700, farbe=G)
gua = t.mol("COc1ccccc1O", 170, 875, name="Guajacol")
sah = t.mol("*SCC[C@H]([NH3+])C(=O)[O-]", 470, 872, labels={0: "Adenosyl"},
            kern=METHIONIN, name="SAH")
t.text(310, 875, "+", size=17, anchor="middle", gewicht=700)
t.unterschrift(gua, "methyliertes Produkt")
t.unterschrift(sah, "S-Adenosylhomocystein, wieder ein neutraler Thioether",
               "hemmt seinerseits alle Methyltransferasen", farbe=R)

t.text(660, 850, "Der Schwefel trägt jetzt wieder nur zwei", size=12)
t.text(660, 869, "Substituenten. Damit ist er weder elektrophil", size=12)
t.text(660, 888, "aktiviert noch eine gute Abgangsgruppe. Die", size=12)
t.text(660, 907, "Aktivierung ist verbraucht und muss über den", size=12)
t.text(660, 926, "SAM-Zyklus mit neuem ATP erneuert werden.", size=12)

# ===================================================== ZONE C · Radikal-SAM
t.zone(985, "C · DIESELBE VERBINDUNG, HOMOLYTISCH GESPALTEN: QUERVERBINDUNG ZU M-16")
t.text(20, 1013, "Radikal-SAM-Enzyme brechen nicht die Bindung zum Methyl, sondern die zum "
                 "Adenosyl, und zwar homolytisch. Von den beiden Elektronen dieser Bindung "
                 "geht eines", size=12.5)
t.text(20, 1031, "auf das C5&#8242;; das andere bleibt am Schwefel und macht ihn zusammen mit "
                 "dem Elektron des Clusters zum neutralen Thioether.", size=12.5)

# Dieselbe Struktur wie in Zone B und in derselben Lage: der Leser soll sehen,
# dass es dieselbe Bindung ist, die hier anders bricht.
rad = t.mol("C[S+](CC[C@H]([NH3+])C(=O)[O-])C*", 340, 1130,
            labels={10: "Adenin-Ribose"}, kern=METHIONIN, name="SAM, Zone C")
# Die Beschriftung steht ausnahmsweise ueber der Struktur: unter ihr liegt der
# Weg des Clusterpfeils.
t.text(344, 1056, "C5&#8242;&#8722;S bricht homolytisch: es entstehen L-Methionin",
       size=10.5, anchor="middle", farbe=R)
t.text(344, 1071, "und das 5&#8242;-Desoxyadenosyl-Radikal", size=10.5,
       anchor="middle", farbe=R)

# Der Cluster steht unten links vom Schwefel. Am Schwefel haengen drei Bindungen:
# die Kette nach links oben, das Methyl nach unten, die C5'-Bindung nach rechts
# oben. Von den drei Luecken dazwischen ist die nach links unten die einzige, die
# weit genug von der C5'-S-Bindung wegfuehrt; sonst kaemen der Clusterpfeil und
# der Fischhaken an dieser Bindung einander ins Gehege.
t.text(278, 1190, "[4Fe&#8722;4S]", size=13, anchor="middle", gewicht=700, farbe=W)
t.text(278, 1208, "reduziert, gibt ein Elektron ab", size=10, anchor="middle", farbe=G)
cluster = t.marke(302, 1170, "[4Fe-4S]-Cluster")

# Drei Elektronen bewegen sich: das Clusterelektron geht auf den Schwefel, dazu
# je ein Elektron der C5'-S-Bindung auf den Schwefel und auf das C5'. Der
# Schwefel bekommt damit ein zweites freies Paar und wird zum neutralen
# Thioether, das C5' behaelt ein einzelnes Elektron und wird zum Radikal.
# Gezeichnet sind zwei der drei Fischhaken. Der dritte - das zweite Elektron der
# Bindung bleibt am Schwefel - laesst sich nicht setzen: der Schwefel traegt drei
# Bindungen, die 120 Grad auseinander stehen, und in die Luecke daneben passt
# kein Bogen, der die Mindestlaenge einhaelt, ohne eine der beiden anderen
# Bindungen zu kreuzen. Der Verbleib dieses Elektrons steht daneben im Text.
t.schub(cluster, Atom(rad, 1), elektronen=1, kette="c")
t.schub(Bindung(rad, 1, 9), Atom(rad, 9), elektronen=1, kette="c")

t.kasten(576, 1058, 404, 116, fill="var(--drug-bg)", stroke=R)
t.text(594, 1080, "WARUM DAS IN DIE PRÜFUNG GEHÖRT", size=11, gewicht=700, farbe=R)
t.text(594, 1102, "Es entsteht dasselbe 5&#8242;-Desoxyadenosyl-Radikal wie aus", size=12.5)
t.text(594, 1121, "Adenosylcobalamin (Tafel M-16). Zwei ganz verschiedene", size=12.5)
t.text(594, 1140, "Cofaktoren liefern dasselbe Werkzeug für dieselbe Aufgabe:", size=12.5)
t.text(594, 1159, "die Abstraktion eines nicht aktivierten Wasserstoffs.", size=12.5)

# ===================================================== ZONE D · Prüfung
t.zone(1250, "D · WORAUF ES IN DER PRÜFUNG ANKOMMT")
t.text(20, 1274, "SAM methyliert meist ein Heteroatom: O bei COMT und ASMT, N bei PNMT und "
                 "HNMT, S bei der Thiopurin-S-Methyltransferase. Die DNA-Methyltransferasen "
                 "sind die Ausnahme: sie", size=12)
t.text(20, 1292, "methylieren das C5 des Cytosins, und zwar über denselben Umweg wie die "
                 "Thymidylatsynthase auf Tafel M-04.", size=12)

# ===================================================== Ausgabe
ARIA = (
    "S-Adenosylmethionin in vier Zonen. Zone A: Der Schwefel des Methionins greift mit einem "
    "freien Elektronenpaar das C5-Strich der Ribose des ATP an; gleichzeitig bricht die Bindung "
    "zwischen C5-Strich und dem Brueckensauerstoff, das gesamte Triphosphat, in der "
    "Zeichnung als PPP abgekuerzt, geht ab. Es "
    "entsteht das Sulfonium S-Adenosylmethionin; Wasser wird verbraucht, Phosphat und "
    "Diphosphat gehen ab. Zone B: Ein Nucleophil, hier Catecholat, "
    "greift die Methylgruppe von der dem Schwefel abgewandten Seite an, waehrend die "
    "Kohlenstoff-Schwefel-Bindung bricht und ihr Elektronenpaar am Schwefel bleibt; gezeichnet "
    "ist der Pfeil des Angriffs. Der Uebergangszustand traegt eine planare "
    "Methylgruppe zwischen zwei partiellen Bindungen. Produkte sind Guajacol und "
    "S-Adenosylhomocystein. Zone C: Radikal-SAM-Enzyme spalten stattdessen die Bindung "
    "zwischen Schwefel und C5-Strich homolytisch. Zwei Fischhakenpfeile zeigen den "
    "Elektronenweg: das Elektron des reduzierten Vier-Eisen-Vier-Schwefel-Clusters geht auf "
    "den Schwefel, und von den beiden Elektronen der Bindung geht eines auf das C5-Strich. "
    "Das zweite Elektron der Bindung bleibt am Schwefel; das steht im Text. So entstehen "
    "das neutrale L-Methionin und das "
    "5-Strich-Desoxyadenosyl-Radikal, dasselbe wie aus Adenosylcobalamin. "
    "Das Methioningeruest steht in allen fuenf Strukturen in derselben Lage, damit der "
    "Unterschied zwischen den Stufen ins Auge faellt und nicht die Ausrichtung."
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

mech.speichern("m05", t.svg(ARIA), t)
