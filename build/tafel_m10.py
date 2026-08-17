# -*- coding: utf-8 -*-
"""
M-10 · BH4-abhaengige Monooxygenasen, gebaut mit mech.py.

Kern ist der NIH-Shift: Das Wasserstoffatom wird nicht abgespalten, sondern an
den Nachbarkohlenstoff geschoben. Das laesst sich nur zeigen, wenn es als
eigenes Atom gezeichnet ist und der Pfeil an seiner Bindung ansetzt.

Zwei Leitgerueste halten die Lage fest. Das Pterin kommt in vier Stufen vor - BH4,
das Carbinolamin, das chinoide Dihydrobiopterin und wieder BH4 -, der Benzolring
in drei. Ohne Leitgeruest bekommt jede Stufe ihre eigene Drehung, und der Leser
muss vor dem Vergleich erst jedes Bild neu einnorden. Mit ihm steht in allen
Stufen dasselbe an derselben Stelle, und der Unterschied zwischen den Stufen ist
das einzige, was ins Auge faellt.
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

# Pterin in der Lehrbuchlage: Pyrimidinon-Ring links, Pyrazin-Ring rechts, die
# 4-Oxo-Gruppe nach oben, das 2-Amin nach unten links, die Seitenkette am C6 nach
# rechts. Das Muster fasst das Bicyclus-Geruest ohne Ruecksicht auf Ladung und
# Aromatizitaet: C8a - N1 - C2 - N3 - C4 - C4a, dann weiter N5 - C6 - C7 - N8.
# Nur so trifft es auch das Carbinolamin, in dem das C4a sp3 ist.
PTERIN = mech_kerne.eigener(
    "pterin", "CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2",
    muster="[#6]12~[#7]~[#6]~[#7]~[#6]~[#6]~1~[#7]~[#6]~[#6]~[#7]~2",
    ring=[8, 9, 11, 13, 14, 16], leit=9, folge=8, winkel=30.0)

# Der Sechsring der Zone B, in allen drei Stufen gleich gelegt: der Rest R links,
# die Angriffsstelle rechts. Dadurch steht die eintretende OH-Gruppe genau dort,
# wo vorher das markierte Wasserstoffatom stand.
AREN = mech_kerne.eigener(
    "aren", "Oc1ccc(*)cc1",
    muster="[#0]~[#6]1~[#6]~[#6]~[#6](~[!#6])~[#6]~[#6]~1",
    ring=[1, 2, 3, 4, 6, 7], leit=1, folge=2, winkel=0.0)

t = mech.Tafel(1000, 1260)

# ===================================================== ZONE A · Sauerstoffaktivierung
t.zone(24, "A · EISEN UND COFAKTOR TEILEN SICH DIE ARBEIT")
t.text(20, 54, "Anders als beim P450 sitzt hier kein Häm, sondern ein nacktes Nicht-Häm-Eisen. "
               "Den Sauerstoff aktiviert nicht das Metall allein, sondern das Pterin.", size=12.5)

zfe = t.zentrum(120, 168, "Fe(II)", unten="His", name="Nicht-Häm-Eisen")
t.text(120, 224, "Fe(II) im aktiven Zentrum", size=11, anchor="middle", gewicht=700, farbe=W)

bh4 = t.mol("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 380, 168, kern=PTERIN, name="BH4")
t.unterschrift(bh4, "Tetrahydrobiopterin (als Arzneistoff Sapropterin)", abstand=30)

t.reaktionspfeil(520, 168, 594)
t.text(557, 156, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(557, 190, "4a-Peroxo-Brücke", size=10, anchor="middle", farbe=G)
t.text(557, 204, "zwischen Pterin und Eisen", size=10, anchor="middle", farbe=G)

zfeo = t.zentrum(680, 168, "Fe(IV)", axial=["O"], doppelt=True, unten="His", schritt=46,
                 name="Ferryl")
t.text(680, 224, "Fe(IV)=O: dasselbe Oxidans", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(680, 240, "wie Compound I, nur ohne Porphyrin", size=10.5, anchor="middle", farbe=G)

t.kasten(790, 96, 190, 132, fill="var(--surface-2)")
t.text(808, 118, "DIE 2-HIS-1-", size=11, gewicht=700, farbe=G)
t.text(808, 134, "CARBOXYLAT-TRIADE", size=11, gewicht=700, farbe=G)
t.text(808, 158, "Zwei Histidine und ein", size=12)
t.text(808, 177, "Glutamat halten das Eisen", size=12)
t.text(808, 196, "an drei Stellen fest. Die", size=12)
t.text(808, 215, "drei übrigen bleiben frei.", size=12)

# ===================================================== ZONE B · NIH-Shift
t.zone(300, "B · DER NIH-SHIFT: DAS WASSERSTOFFATOM WIRD GESCHOBEN, NICHT ENTFERNT")
t.text(20, 330, "Das Ferryl greift den aromatischen Ring elektrophil an. Dabei entsteht ein "
                "kationisches σ-Addukt, in dem die Aromatizität kurz aufgehoben ist.", size=12.5)

arom = t.mol("*c1ccccc1", 130, 452, labels={0: "R"}, wasserstoff=[4],
             kern=AREN, name="Aromat")
ha = arom.h_index[4]
t.unterschrift(arom, "der Aromat: das markierte H sitzt dort,", "wo die OH-Gruppe eintreten wird",
               abstand=30)

t.reaktionspfeil(228, 452, 306)
t.text(267, 440, "Fe(IV)=O", size=10.5, anchor="middle", gewicht=700, farbe=W)
t.text(267, 476, "greift an", size=10, anchor="middle", farbe=G)

# Die Grenzstruktur mit dem Kation direkt neben dem sp3-Zentrum ist die einzige, an
# der sich der Hydridpfeil lesen laesst: das H wandert an ein Kation, nicht an einen
# neutralen Kohlenstoff. Stuende das Kation in para-Stellung, wuerde das Zielatom des
# Pfeils fuenfbindig.
#
# Der Ring ist bewusst andersherum geschrieben als der Weg von C1 aus laeuft:
# derselbe Stoff, nur die Umlaufrichtung des SMILES gedreht. Am sp3-Kohlenstoff
# setzt RDKit die vier Substituenten in fester Reihenfolge, und nur in dieser
# Schreibweise landet das wandernde H unmittelbar neben dem Kation. Andernfalls
# steht die OH-Gruppe zwischen beiden, und der Pfeil muesste ueber ihre
# Beschriftung hinweg.
sigma = t.mol("OC1C=CC(*)=C[CH+]1", 420, 452, labels={5: "R"}, wasserstoff=[1],
              kern=AREN, name="σ-Addukt")
hs = sigma.h_index[1]
# Das Elektronenpaar der C-H-Bindung geht mitsamt dem Kern an das Nachbaratom:
# ein Hydridschub, kein Protonenabgang.
t.schub(Bindung(sigma, 1, hs), Atom(sigma, 7))
t.unterschrift(sigma, "das kationische σ-Addukt: das H wandert an den",
               "benachbarten Kationenkohlenstoff, statt abzugehen", abstand=30, farbe=W,
               gewicht=700)

t.reaktionspfeil(534, 452, 612)
t.text(573, 440, "Tautomerie", size=10.5, anchor="middle", gewicht=700, farbe=G)

phen = t.mol("Oc1ccc(*)cc1", 720, 452, labels={5: "R"}, kern=AREN, name="Phenol")
t.unterschrift(phen, "das Phenol, Aromatizität wiederhergestellt", abstand=30)

t.kasten(820, 386, 160, 152, fill="var(--warn-bg)", stroke=W)
t.text(838, 408, "DER BEWEIS", size=11, gewicht=700, farbe=W)
t.text(838, 430, "Setzt man an der", size=12)
t.text(838, 449, "Angriffsstelle Deuterium", size=12)
t.text(838, 468, "ein, findet man es", size=12)
t.text(838, 487, "hinterher nicht im", size=12)
t.text(838, 506, "Wasser, sondern am Nach-", size=12)
t.text(838, 525, "barkohlenstoff wieder.", size=12)

t.text(20, 552, "Der Name stammt von den National Institutes of Health, wo der Befund "
                "zuerst beschrieben wurde.", size=12, farbe=G)

# ===================================================== ZONE C · Regeneration
t.zone(596, "C · DER COFAKTOR MUSS ZURÜCKGEFÜHRT WERDEN")
t.text(20, 626, "Anders als das Häm bleibt das Pterin nicht unverändert: Es wird bei jedem Umsatz "
                "oxidiert und braucht zwei Enzyme, um wieder BH&#8324; zu werden.", size=12.5)

# Die drei Pterine der Zone unterscheiden sich wirklich, sonst waere der Zyklus
# stofflich leer: C9H15N5O4 (Carbinolamin, ein O mehr), C9H13N5O3 (q-BH2, zwei H
# weniger), C9H15N5O3 (BH4).
# Das Wasserstoffatom am N5 steht als eigenes Atom da. Zwei Gruende: Als
# Sammelzeichen "N" mit angehaengtem H stiess es an die OH-Gruppe des C4a - im
# fertigen Bild las sich das als "OHH". Und die PCD nimmt genau dieses H
# zusammen mit dem OH als Wasser weg; wer beide sieht, sieht auch, woraus das
# abgespaltene Wasser besteht.
bh4b = t.mol("CC(O)C(O)C1CN=C2N=C(N)NC(=O)C2(O)N1", 150, 750,
             kern=PTERIN, wasserstoff=[17], name="4a-Hydroxy-BH4")
t.unterschrift(bh4b, "4a-Hydroxy-BH&#8324;, das Carbinolamin:",
               "OH am sp&#179;-C4a, ein O mehr als BH&#8324;", abstand=30, farbe=G)

t.reaktionspfeil(290, 750, 364)
t.text(327, 738, "PCD", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(327, 772, "&#8722; H&#8322;O", size=10, anchor="middle", farbe=G)

qbh2 = t.mol("CC(O)C(O)C1CN=C2N=C(N)NC(=O)C2=N1", 500, 750, kern=PTERIN,
             name="q-BH2")
t.unterschrift(qbh2, "q-Dihydrobiopterin: chinoid, mit C4a=N5", "und zwei H weniger als BH&#8324;",
               abstand=30, farbe=G)

t.reaktionspfeil(640, 750, 714)
t.text(677, 738, "DHPR", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(677, 772, "+ NADH + H&#8314;", size=10, anchor="middle", gewicht=700, farbe=C)
t.text(677, 786, "&#8722; NAD&#8314;", size=10, anchor="middle", farbe=G)

bh4c = t.mol("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 850, 750, kern=PTERIN,
             name="BH4 zurueck")
t.unterschrift(bh4c, "BH&#8324;, wieder einsatzbereit", abstand=30, farbe=E)

# ===================================================== ZONE D · Klinik
t.zone(880, "D · WARUM NICHT JEDE HYPERPHENYLALANINÄMIE EINE PKU IST")

t.kasten(20, 912, 470, 138, fill="var(--surface-2)")
t.text(38, 934, "DER HÄUFIGE FALL: DEFEKT DER HYDROXYLASE", size=11, gewicht=700, farbe=G)
t.text(38, 956, "Etwa 98 % der Fälle. Die Phenylalanin-Hydroxylase", size=12.5)
t.text(38, 975, "selbst ist defekt, der Cofaktor ist in Ordnung.", size=12.5)
t.text(38, 998, "Therapie: phenylalaninarme Diät. Manche Varianten", size=12.5)
t.text(38, 1017, "sprechen zusätzlich auf hochdosiertes Sapropterin an,", size=12.5)
t.text(38, 1036, "das das fehlgefaltete Enzym stabilisiert.", size=12.5)

t.kasten(510, 912, 470, 138, fill="var(--warn-bg)", stroke=W)
t.text(528, 934, "DER SELTENE FALL: DEFEKT IM COFAKTOR", size=11, gewicht=700, farbe=W)
t.text(528, 956, "Etwa 2 %. Betroffen ist entweder die Neusynthese des", size=12.5)
t.text(528, 975, "BH&#8324; oder seine Regeneration über die DHPR.", size=12.5)
t.text(528, 998, "Weil BH&#8324; auch die Tyrosin- und die", size=12.5)
t.text(528, 1017, "Tryptophanhydroxylase versorgt, fallen zusätzlich", size=12.5)
t.text(528, 1036, "Catecholamine und Serotonin aus. Die Diät genügt nicht.", size=12.5)

t.kasten(20, 1080, 960, 96, fill="var(--drug-bg)", stroke=R)
t.text(38, 1102, "WAS DARAUS FÜR DIE PRÜFUNG FOLGT", size=11, gewicht=700, farbe=R)
t.text(38, 1124, "BH&#8324; ist Cofaktor von vier Enzymen: Phenylalanin-, Tyrosin- und "
                 "Tryptophanhydroxylase sowie der NO-Synthase (Tafel M-14). Ein", size=12.5)
t.text(38, 1143, "Cofaktordefekt trifft deshalb den Aromatenstoffwechsel und die "
                 "Gefäßregulation zugleich. Ein Enzymdefekt trifft nur einen Weg.", size=12.5)

t.text(20, 1216, "Bei der NO-Synthase hat BH&#8324; übrigens eine andere Rolle: Dort liefert es "
                 "ein Elektron und wird sofort zurückreduziert, statt Sauerstoff zu tragen.",
       size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "BH4-abhaengige Monooxygenasen in vier Zonen. Zone A zeigt das Nicht-Haem-Eisen, das von "
    "zwei Histidinen und einem Glutamat gehalten wird, daneben das gezeichnete "
    "Tetrahydrobiopterin; aus beiden und Sauerstoff entsteht ueber eine 4a-Peroxo-Bruecke das "
    "Ferryl-Ion Eisen vier gleich Sauerstoff. Zone B zeigt den NIH-Shift an gezeichneten "
    "Strukturen: Der Aromat mit einem eigens gezeichneten Wasserstoffatom, das kationische "
    "Sigma-Addukt, in dem ein Elektronenpaarpfeil das Wasserstoffatom an den "
    "benachbarten Kationenkohlenstoff schiebt, und schliesslich das Phenol mit "
    "wiederhergestellter Aromatizitaet. Zone C zeigt die Regeneration des Cofaktors an drei "
    "verschiedenen gezeichneten Pterinen: das 4a-Carbinolamin mit Hydroxylgruppe am "
    "Kohlenstoff vier a, daraus durch die Pterin-4a-Carbinolamin-Dehydratase unter "
    "Wasserabspaltung das chinoide Dihydrobiopterin, und daraus durch die "
    "Dihydropteridin-Reduktase mit NADH wieder Tetrahydrobiopterin. Zone D unterscheidet die haeufige "
    "Phenylketonurie durch Enzymdefekt von der seltenen Form durch Cofaktordefekt."
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

mech.speichern("m10", t.svg(ARIA), t)
