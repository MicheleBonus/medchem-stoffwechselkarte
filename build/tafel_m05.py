# -*- coding: utf-8 -*-
"""
M-05 · S-Adenosylmethionin, gebaut mit der Mechanismus-Sprache aus mech.py.

Musterfassung: alle Strukturen kommen von RDKit, alle Elektronenpfeile sind aus
den gemeldeten Atomkoordinaten konstruiert, alle Bildunterschriften sitzen an der
tatsaechlichen Ausdehnung des jeweiligen Molekuels. Ausgabe nach tafeln.json.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech

HERE = os.path.dirname(os.path.abspath(__file__))

W = "var(--warn)"       # Elektronenpaar-Pfeile
R = "var(--drug)"       # Radikalpfeile (Fischhaken)
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1160)

# ===================================================== ZONE A · Aktivierung
t.zone(24, "A · DIE AKTIVIERUNG: WOZU DAS ATP GEBRAUCHT WIRD")
t.text(20, 54, "Der Schwefel greift nicht am Phosphor an, sondern am C5&#8242; der Ribose. "
               "Deshalb geht das gesamte Triphosphat, unten als PPP abgekürzt, ab.", size=12.5)

# Methionin: Schwefel nach rechts, damit sein Elektronenpaar zum ATP zeigt
met = mech.Molekuel("CSCC[C@H]([NH3+])C(=O)[O-]", 128, 150,
                    zeige={1: "rechts"}, name="Methionin")
# ATP verkuerzt: C5' nach links, der Brueckensauerstoff darueber, die drei Phosphate
# als kurze Marke "PPP". Zwei Gruende fuer die Kuerze: die ausgeschriebene Marke
# "Triphosphat" ist so breit, dass sie sowohl in der Bahn des Pfeils von links auf das
# C5' liegt als auch dort, wo das Elektronenpaar der brechenden Bindung landet.
atp = mech.Molekuel("*OC[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O", 404, 150,
                    labels={0: "PPP", 6: "Adenin"},
                    zeige={2: "links", 1: "oben"}, name="ATP")
sam = mech.Molekuel("C[S+](CC[C@H]([NH3+])C(=O)[O-])C[C@H]1O[C@@H](*)[C@H](O)[C@@H]1O",
                    810, 152, labels={13: "Adenin"}, name="SAM")
t.mole += [met, atp, sam]

lp_s = t.elektronenpaar(met, 1, -55)
t.pfeil(lp_s, (atp, 2), bogen=0.22, seite=-1, farbe=W)          # S  -> C5'
# Das Paar bleibt am Brueckensauerstoff. Ein Pfeil bis in dessen Mitte waere kuerzer
# als sein eigener Kopf; er endet deshalb dicht daneben, auf der von C5' abgewandten
# Seite.
t.pfeil((atp, 2, 1), atp.abseits(1, 2, abstand=26), bogen=0.40, seite=1,
        farbe=W, mindestbogen=14)                               # C5'-O -> O

t.unterschrift(met, "L-Methionin, ein neutraler Thioether")
t.unterschrift(atp, "ATP: angegriffen wird der Zucker, nicht das Phosphat")
t.unterschrift(sam, "S-Adenosylmethionin", "drei Substituenten am Schwefel = Sulfonium",
               gewicht=700, farbe=R)

t.reaktionspfeil(604, 150, 690)
t.text(647, 140, "MAT", size=11.5, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(647, 168, "Methionin-Adenosyltransferase", size=9.5, anchor="middle", farbe=G)
# Das Tripolyphosphat zerfaellt erst durch Hydrolyse in PPi und Pi; ohne das
# Wasser geht die Atombilanz des zweiten Teilschritts nicht auf.
t.text(647, 186, "+ H&#8322;O", size=10.5, anchor="middle", farbe=C)
t.text(647, 202, "&#8722; P&#7522; &#8722; PP&#7522;", size=10.5, anchor="middle", farbe=C)

t.kasten(20, 244, 520, 76, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 266, "WAS DAS ATP BEWIRKT", size=11, gewicht=700, farbe=C)
t.text(38, 288, "Die Methylgruppe ist dieselbe wie im Methionin. Neu ist die Ladung am "
                "Schwefel: sie macht", size=12.5)
t.text(38, 307, "das Methyl elektrophil und den abgehenden Thioether ungeladen.", size=12.5)

# ===================================================== ZONE B · S_N2
t.zone(358, "B · DIE ÜBERTRAGUNG: S<tspan baseline-shift='sub' font-size='8.5'>N</tspan>2 "
            "AM METHYLKOHLENSTOFF")

cat = mech.Molekuel("Oc1ccccc1[O-]", 132, 472, zeige={7: "rechts"}, bindung=26,
                    name="Catecholat")
# Das C5' steht hier als eigenes Atom, der Rest heisst deshalb "Adenin-Ribose".
# Hiesse die Marke "Adenosyl", steckte das C5' zweimal im Bild und die Bilanz
# gegen das SAH der Produktzeile ginge um eine CH2-Gruppe daneben.
smk = mech.Molekuel("C[S+](CC[C@H]([NH3+])C(=O)[O-])C*", 396, 464,
                    labels={10: "Adenin-Ribose"}, zeige={0: "links"}, bindung=26,
                    name="SAM")
t.mole += [cat, smk]

lp_o = t.elektronenpaar(cat, 7, -25)
t.pfeil(lp_o, (smk, 0), bogen=0.24, seite=-1, farbe=W)          # Nu   -> CH3
# Der Ringpfeil um den Schwefel ist die uebliche Schreibweise, wenn das Paar am
# eigenen Atom bleibt: ein gerader Pfeil von der Bindungsmitte in die Mitte des
# Schwefelsymbols waere kuerzer als sein eigener Kopf.
t.pfeil((smk, 0, 1), (smk, 1), bogen=0.62, seite=-1, farbe=W,
        mindestbogen=22)                                        # C-S  -> S

t.unterschrift(cat, "Catecholat, das Nucleophil der COMT")
t.unterschrift(smk, "S-Adenosylmethionin")

t.reaktionspfeil(566, 468, 636)

# Uebergangszustand
t.ts_klammer(650, 410, 952, 524)
t.text(810, 430, "Angriff auf der abgewandten Seite", size=11, anchor="middle",
       gewicht=700, farbe=W)
t.text(700, 476, "ArO", size=13.5, anchor="end", gewicht=700, farbe=E)
t.text(706, 469, "&#948;&#8722;", size=9.5, farbe=G)
t.linie(712, 472, 772, 472, farbe=W, breite=1.6, strich="4 3")
t.text(792, 476, "CH&#8323;", size=13.5, anchor="middle", gewicht=700)
t.linie(814, 472, 874, 472, farbe=W, breite=1.6, strich="4 3")
t.text(886, 476, "S", size=14, gewicht=700, farbe=C)
t.text(896, 469, "&#948;+", size=9.5, farbe=G)
t.linie(792, 486, 792, 502, breite=1.3)
t.linie(792, 486, 778, 500, breite=1.3)
t.linie(792, 486, 806, 500, breite=1.3)
t.text(810, 514, "planare CH&#8323;-Gruppe, fünffach koordinierter Übergangszustand", size=10,
       anchor="middle", farbe=G)

t.text(20, 566, "Ein einziger Schritt: Bindungsbildung und Bindungsbruch laufen gleichzeitig. "
                "Weil das Nucleophil auf der dem", size=12.5)
t.text(20, 585, "Schwefel abgewandten Seite angreift, kehrt sich die Konfiguration am "
                "Methylkohlenstoff um. Mit dreifach isotopen-", size=12.5)
t.text(20, 604, "markiertem Methyl (H, D, T) ist diese Inversion nachgewiesen worden.",
       size=12.5)

# Produkte
t.text(20, 642, "PRODUKTE", size=11, gewicht=700, farbe=G)
gua = mech.Molekuel("COc1ccccc1O", 150, 706, name="Guajacol")
sah = mech.Molekuel("*SCC[C@H]([NH3+])C(=O)[O-]", 452, 700,
                    labels={0: "Adenosyl"}, zeige={1: "oben"}, name="SAH")
t.mole += [gua, sah]
t.text(300, 706, "+", size=17, anchor="middle", gewicht=700)
t.unterschrift(gua, "methyliertes Produkt")
t.unterschrift(sah, "S-Adenosylhomocystein, wieder ein neutraler Thioether",
               "hemmt seinerseits alle Methyltransferasen", farbe=R)

t.text(660, 676, "Der Schwefel trägt jetzt wieder nur zwei", size=12)
t.text(660, 695, "Substituenten. Damit ist er weder elektrophil", size=12)
t.text(660, 714, "aktiviert noch eine gute Abgangsgruppe. Die", size=12)
t.text(660, 733, "Aktivierung ist verbraucht und muss über den", size=12)
t.text(660, 752, "SAM-Zyklus mit neuem ATP erneuert werden.", size=12)

# ===================================================== ZONE C · Radikal-SAM
t.zone(818, "C · DIESELBE VERBINDUNG, HOMOLYTISCH GESPALTEN: QUERVERBINDUNG ZU M-16")
t.text(20, 848, "Radikal-SAM-Enzyme brechen nicht die Bindung zum Methyl, sondern die zum "
                "Adenosyl, und zwar homolytisch.", size=12.5)

# Groesser gezeichnet als die uebrigen Strukturen: an der C5'-S-Bindung setzen drei
# Fischhaken an, und bei 21 px Bindungslaenge entarten sie zu Schleifen. Gedreht ist so,
# dass die C5'-S-Bindung waagerecht liegt und die breite Marke "Adenin-Ribose" hinter
# das C5' rueckt; sonst faellt sie genau dorthin, wo der Fischhaken zum C5' endet.
rad = mech.Molekuel("C[S+](CC[C@H]([NH3+])C(=O)[O-])C*", 400, 932,
                    labels={10: "Adenin-Ribose"}, rotate=150.0,
                    bindung=38, name="SAM")
t.mole.append(rad)

# Der Cluster steht genau links vom Schwefel: nur aus dieser Richtung erreicht sein
# Pfeil das Schwefelatom, ohne die Aminosäureseitenkette zu durchqueren.
cluster = t.marke(250, 968, "[4Fe-4S]-Cluster")
t.text(250, 950, "[4Fe&#8722;4S]", size=13, anchor="middle", gewicht=700, farbe=W)
t.text(250, 990, "reduziert, gibt ein Elektron ab", size=10, anchor="middle", farbe=G)

# Drei Fischhaken, sonst geht die Elektronenbilanz nicht auf: das Clusterelektron
# geht auf den Schwefel, dazu je ein Elektron der C5'-S-Bindung auf den Schwefel
# und auf das C5'. Der Schwefel bekommt damit ein zweites freies Paar und wird
# zum neutralen Thioether, das C5' behaelt ein einzelnes Elektron; dieses steht als
# Punkt im Bild, damit der Fischhaken ein sichtbares Ziel hat.
e_c5 = t.einzelelektron(rad, 9, 300, abstand=24)
t.pfeil(cluster, (rad, 1), bogen=0.05, seite=-1, typ="fischhaken", farbe=R,
        mindestbogen=8)
t.pfeil((rad, 1, 9), rad.abseits(1, 0, abstand=30), bogen=0.40, seite=-1,
        typ="fischhaken", farbe=R, mindestbogen=12, gap=3)
t.pfeil((rad, 1, 9), e_c5, bogen=0.35, seite=1, typ="fischhaken", farbe=R,
        mindestbogen=11)

t.unterschrift(rad, "C5&#8242;&#8722;S bricht homolytisch: es entstehen L-Methionin",
               "und das 5&#8242;-Desoxyadenosyl-Radikal", farbe=R)

t.kasten(576, 872, 404, 116, fill="var(--drug-bg)", stroke=R)
t.text(594, 894, "WARUM DAS IN DIE PRÜFUNG GEHÖRT", size=11, gewicht=700, farbe=R)
t.text(594, 916, "Es entsteht dasselbe 5&#8242;-Desoxyadenosyl-Radikal wie aus", size=12.5)
t.text(594, 935, "Adenosylcobalamin (Tafel M-16). Zwei ganz verschiedene", size=12.5)
t.text(594, 954, "Cofaktoren liefern dasselbe Werkzeug für dieselbe Aufgabe:", size=12.5)
t.text(594, 973, "die Abstraktion eines nicht aktivierten Wasserstoffs.", size=12.5)

# ===================================================== ZONE D · Prüfung
t.zone(1086, "D · WORAUF ES IN DER PRÜFUNG ANKOMMT")
t.text(20, 1110, "SAM methyliert meist ein Heteroatom: O bei COMT und ASMT, N bei PNMT und "
                 "HNMT, S bei der Thiopurin-S-Methyltransferase. Die DNA-Methyltransferasen "
                 "sind die Ausnahme: sie", size=12)
t.text(20, 1128, "methylieren das C5 des Cytosins, und zwar über denselben Umweg wie die "
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
    "Kohlenstoff-Schwefel-Bindung bricht. Der Uebergangszustand traegt eine planare "
    "Methylgruppe zwischen zwei partiellen Bindungen. Produkte sind Guajacol und "
    "S-Adenosylhomocystein. Zone C: Radikal-SAM-Enzyme spalten stattdessen die Bindung "
    "zwischen Schwefel und C5-Strich homolytisch. Drei Fischhakenpfeile zeigen den "
    "Elektronenweg: das Elektron des reduzierten Vier-Eisen-Vier-Schwefel-Clusters geht auf "
    "den Schwefel, von den beiden Elektronen der Bindung geht eines ebenfalls auf den "
    "Schwefel und eines auf das C5-Strich, wo es als Punkt stehen bleibt. So entstehen "
    "das neutrale L-Methionin und das "
    "5-Strich-Desoxyadenosyl-Radikal, dasselbe wie aus Adenosylcobalamin."
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

mech.speichern("m05", t.svg(ARIA), t)
