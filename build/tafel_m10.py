# -*- coding: utf-8 -*-
"""
M-10 · BH4-abhaengige Monooxygenasen, gebaut mit mech.py.

Kern ist der NIH-Shift: Das Wasserstoffatom wird nicht abgespalten, sondern an
den Nachbarkohlenstoff geschoben. Das laesst sich nur zeigen, wenn es als
eigenes Atom gezeichnet ist und der Pfeil an seiner Bindung ansetzt.
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

t = mech.Tafel(1000, 1260)

# ===================================================== ZONE A · Sauerstoffaktivierung
t.zone(24, "A · EISEN UND COFAKTOR TEILEN SICH DIE ARBEIT")
t.text(20, 54, "Anders als beim P450 sitzt hier kein Häm, sondern ein nacktes Nicht-Häm-Eisen. "
               "Den Sauerstoff aktiviert nicht das Metall allein, sondern das Pterin.", size=12.5)

zfe = t.zentrum(120, 168, "Fe(II)", unten="His", name="Nicht-Häm-Eisen")
t.text(120, 224, "Fe(II) im aktiven Zentrum", size=11, anchor="middle", gewicht=700, farbe=W)

bh4 = mech.Molekuel("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 380, 168, name="BH4")
t.mole.append(bh4)
t.unterschrift(bh4, "Tetrahydrobiopterin — als Arzneistoff Sapropterin", abstand=30)

t.reaktionspfeil(520, 168, 594)
t.text(557, 156, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(557, 190, "4a-Peroxo-Brücke", size=10, anchor="middle", farbe=G)
t.text(557, 204, "zwischen Pterin und Eisen", size=10, anchor="middle", farbe=G)

zfeo = t.zentrum(680, 168, "Fe(IV)", axial=["O"], doppelt=True, unten="His", schritt=46,
                 name="Ferryl")
t.text(680, 224, "Fe(IV)=O — dasselbe Oxidans", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(680, 240, "wie Compound I, nur ohne Porphyrin", size=10.5, anchor="middle", farbe=G)

t.kasten(790, 96, 190, 132, fill="var(--surface-2)")
t.text(808, 118, "DIE 2-HIS-1-", size=11, gewicht=700, farbe=G)
t.text(808, 134, "CARBOXYLAT-TRIADE", size=11, gewicht=700, farbe=G)
t.text(808, 158, "Zwei Histidine und ein", size=12)
t.text(808, 177, "Glutamat halten das Eisen", size=12)
t.text(808, 196, "an drei Stellen fest. Die", size=12)
t.text(808, 215, "drei übrigen bleiben frei.", size=12)

# ===================================================== ZONE B · NIH-Shift
t.zone(300, "B · DER NIH-SHIFT — DAS WASSERSTOFFATOM WIRD GESCHOBEN, NICHT ENTFERNT")
t.text(20, 330, "Das Ferryl greift den aromatischen Ring elektrophil an. Dabei entsteht ein "
                "kationisches σ-Addukt, in dem die Aromatizität kurz aufgehoben ist.", size=12.5)

arom = mech.Molekuel("*c1ccccc1", 130, 452, labels={0: "R"}, wasserstoff=[4],
                     zeige={0: "links"}, name="Aromat")
t.mole.append(arom)
ha = arom.h_index[4]
t.unterschrift(arom, "der Aromat — das markierte H sitzt dort,", "wo die OH-Gruppe eintreten wird",
               abstand=30)

t.reaktionspfeil(228, 452, 306)
t.text(267, 440, "Fe(IV)=O", size=10.5, anchor="middle", gewicht=700, farbe=W)
t.text(267, 476, "greift an", size=10, anchor="middle", farbe=G)

sigma = mech.Molekuel("OC1C=C[C+](*)C=C1", 420, 452, labels={5: "R"}, wasserstoff=[1],
                      zeige={5: "rechts"}, name="σ-Addukt")
t.mole.append(sigma)
hs = sigma.h_index[1]
t.pfeil((sigma, 1, hs), sigma.aussen(2, abstand=28), bogen=0.38, seite=1, farbe=W)
t.unterschrift(sigma, "das kationische σ-Addukt — hier wandert das H",
               "an den Nachbarkohlenstoff, statt abzugehen", abstand=30, farbe=W, gewicht=700)

t.reaktionspfeil(534, 452, 612)
t.text(573, 440, "Tautomerie", size=10.5, anchor="middle", gewicht=700, farbe=G)

phen = mech.Molekuel("Oc1ccc(*)cc1", 720, 452, labels={5: "R"}, zeige={5: "rechts"},
                     name="Phenol")
t.mole.append(phen)
t.unterschrift(phen, "das Phenol — Aromatizität wiederhergestellt", abstand=30)

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

bh4b = mech.Molekuel("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 150, 750, name="4a-Hydroxy-BH4")
t.mole.append(bh4b)
t.unterschrift(bh4b, "4a-Hydroxy-BH&#8324;", abstand=30, farbe=G)

t.reaktionspfeil(290, 750, 364)
t.text(327, 738, "PCD", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(327, 772, "&#8722; H&#8322;O", size=10, anchor="middle", farbe=G)

qbh2 = mech.Molekuel("CC(O)C(O)C1CN=C2C(=O)NC(N)=NC2N1", 500, 750, name="q-BH2")
t.mole.append(qbh2)
t.unterschrift(qbh2, "q-Dihydrobiopterin", abstand=30, farbe=G)

t.reaktionspfeil(640, 750, 714)
t.text(677, 738, "DHPR", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(677, 772, "+ NADH", size=10, anchor="middle", gewicht=700, farbe=C)

bh4c = mech.Molekuel("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 850, 750, name="BH4 zurueck")
t.mole.append(bh4c)
t.unterschrift(bh4c, "BH&#8324; — wieder einsatzbereit", abstand=30, farbe=E)

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
t.text(528, 1036, "Catecholamine und Serotonin aus — die Diät genügt nicht.", size=12.5)

t.kasten(20, 1080, 960, 96, fill="var(--drug-bg)", stroke=R)
t.text(38, 1102, "WAS DARAUS FÜR DIE PRÜFUNG FOLGT", size=11, gewicht=700, farbe=R)
t.text(38, 1124, "BH&#8324; ist Cofaktor von vier Enzymen: Phenylalanin-, Tyrosin- und "
                 "Tryptophanhydroxylase sowie der NO-Synthase (Tafel M-14). Ein", size=12.5)
t.text(38, 1143, "Cofaktordefekt trifft deshalb den Aromatenstoffwechsel und die "
                 "Gefäßregulation zugleich — ein Enzymdefekt nur einen Weg.", size=12.5)

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
    "Nachbarkohlenstoff schiebt, und schliesslich das Phenol mit wiederhergestellter "
    "Aromatizitaet. Zone C zeigt die Regeneration des Cofaktors ueber Pterin-4a-Carbinolamin-"
    "Dehydratase und Dihydropteridin-Reduktase. Zone D unterscheidet die haeufige "
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
