# -*- coding: utf-8 -*-
"""
M-16 · Cobalamin, gebaut mit mech.py.

Die Tafel lebt von einem einzigen Gegensatz: dieselbe Kohlenstoff-Cobalt-Bindung,
einmal heterolytisch, einmal homolytisch gespalten. Zone A stellt beide Fassungen
nebeneinander - links ein Elektronenpaarpfeil, rechts zwei Fischhaken.
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

t = mech.Tafel(1000, 1390)

# ===================================================== ZONE A · der Gegensatz
t.zone(24, "A · DIESELBE BINDUNG, ZWEI ARTEN SIE ZU BRECHEN")
t.text(20, 54, "Die C&#8722;Co-Bindung ist mit rund 30 kcal/mol ungewöhnlich schwach. Wohin ihre "
               "beiden Elektronen gehen, entscheidet über den ganzen Reaktionstyp.", size=12.5)

# ---- links: heterolytisch
zh = t.zentrum(230, 158, "Co(III)", axial=["CH&#8323;"], unten="DMB", schritt=48,
               name="Methylcobalamin")
t.pfeil(zh.axb(-1, 0), zh.fe(winkel=203, abstand=46), bogen=0.45, seite=-1, farbe=W)
t.text(230, 84, "Methylcobalamin", size=12, anchor="middle", gewicht=700)
t.text(302, 132, "beide Elektronen", size=10.5, farbe=W, gewicht=700)
t.text(302, 146, "gehen ans Cobalt", size=10.5, farbe=W, gewicht=700)
t.text(230, 214, "heterolytisch", size=12.5, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(230, 228, 230, 270)

zh2 = t.zentrum(230, 322, "Co(I)", axial=[], unten="DMB", name="Co(I)")
t.text(230, 376, "Co(I) — eines der stärksten Nucleophile", size=11, anchor="middle",
       gewicht=700, farbe=E)
t.text(230, 392, "der gesamten Biochemie", size=10.5, anchor="middle", farbe=G)
t.text(230, 412, "die Methylgruppe geht als CH&#8323;&#8314; weiter", size=10.5,
       anchor="middle", farbe=G)

# ---- rechts: homolytisch
zr = t.zentrum(730, 158, "Co(III)", axial=["Ado"], unten="DMB", schritt=48,
               name="Adenosylcobalamin")
t.pfeil(zr.axb(-1, 0), zr.fe(winkel=195, abstand=56), bogen=0.30, seite=-1,
        typ="fischhaken", farbe=R)
t.pfeil(zr.axb(-1, 0), zr.ax(0, winkel=10, abstand=36), bogen=0.30, seite=1,
        typ="fischhaken", farbe=R)
t.text(730, 84, "Adenosylcobalamin", size=12, anchor="middle", gewicht=700)
t.text(802, 132, "je ein Elektron", size=10.5, farbe=R, gewicht=700)
t.text(802, 146, "nach jeder Seite", size=10.5, farbe=R, gewicht=700)
t.text(730, 214, "homolytisch", size=12.5, anchor="middle", gewicht=700, farbe=R)

t.reaktionspfeil(730, 228, 730, 270)

zr2 = t.zentrum(730, 322, "Co(II)", axial=[], unten="DMB", name="Co(II)")
t.text(730, 376, "Co(II) — und daneben das freie", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.text(730, 392, "5&#8242;-Desoxyadenosyl-Radikal", size=10.5, anchor="middle", farbe=G)
t.text(730, 412, "das Enzym beschleunigt die Homolyse um 10&#185;&#178;", size=10.5,
       anchor="middle", farbe=G)

t.linie(480, 96, 480, 420, farbe="currentColor", breite=1, strich="4 4", z=0)

# ===================================================== ZONE B · Methylcobalamin
t.zone(456, "B · DER HETEROLYTISCHE WEG — METHIONINSYNTHASE")
t.text(20, 486, "Das Co(I) holt sich die Methylgruppe vom 5-Methyl-Tetrahydrofolat und gibt sie "
                "an Homocystein weiter. Zweimal derselbe "
                "S<tspan baseline-shift='sub' font-size='8.5'>N</tspan>2-Schritt am Methyl.",
       size=12.5)

zb1 = t.zentrum(96, 590, "Co(I)", axial=[], unten="DMB", name="Co(I)")
lp_co = t.paar(96, 566, 270, "Cobalt(I)")
mthf = mech.Molekuel("CN(*)*", 254, 574, labels={2: "C4a", 3: "C6"},
                     zeige={0: "links"}, name="5-Methyl-THF")
t.mole.append(mthf)
t.pfeil(lp_co, (mthf, 0), bogen=0.24, seite=-1, farbe=W)
t.pfeil((mthf, 0, 1), (mthf, 1), bogen=0.50, seite=1, farbe=W, mindestbogen=22)
t.unterschrift(mthf, "5-Methyl-THF — nur der Stickstoff N5", "mit seinen zwei Nachbarn")
t.text(96, 646, "Co(I)", size=11, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(362, 578, 424)
t.text(393, 568, "&#8722; THF", size=10.5, anchor="middle", gewicht=700, farbe=G)

zb2 = t.zentrum(492, 586, "Co(III)", axial=["CH&#8323;"], unten="DMB", schritt=46,
                name="Methylcobalamin")
t.text(492, 642, "Methylcobalamin", size=11, anchor="middle", gewicht=700, farbe=W)

hcy = mech.Molekuel("[S-]CC[C@H]([NH3+])C(=O)[O-]", 672, 574,
                    zeige={0: "links"}, name="Homocystein")
t.mole.append(hcy)
lp_s = t.elektronenpaar(hcy, 0, 200)
t.pfeil(lp_s, zb2.ax(0), bogen=0.24, seite=1, farbe=W)
t.pfeil(zb2.axb(-1, 0), zb2.fe(winkel=203, abstand=46), bogen=0.45, seite=-1, farbe=W)
t.unterschrift(hcy, "Homocystein — das Thiolat greift an")

t.reaktionspfeil(786, 578, 848)

met = mech.Molekuel("CSCC[C@H]([NH3+])C(=O)[O-]", 896, 574, name="Methionin")
t.mole.append(met)
t.unterschrift(met, "Methionin — das Cobalt steht", "wieder als Co(I) bereit")

# ===================================================== ZONE C · Adenosylcobalamin
t.zone(700, "C · DER HOMOLYTISCHE WEG — METHYLMALONYL-CoA-MUTASE")
t.text(20, 730, "Das Radikal holt sich ein Wasserstoffatom vom Substrat. Danach wandert die "
                "Thioestergruppe an den Nachbarkohlenstoff, und das H kommt zurück.", size=12.5)

mm = mech.Molekuel("CC(C(=O)[O-])C(=O)*", 176, 838, labels={7: "SCoA"},
                   wasserstoff=[0], zeige={0: "oben"}, name="Methylmalonyl-CoA")
t.mole.append(mm)
h0 = mm.h_index[0]
ado = t.marke(176, 754, "Desoxyadenosyl-Radikal")
t.text(176, 750, "Ado&#8226;", size=11, anchor="middle", gewicht=700, farbe=R)
t.pfeil((mm, 0, h0), ado, bogen=0.24, seite=1, typ="fischhaken", farbe=R)
t.pfeil((mm, 0, h0), mm.abseits(0, h0), bogen=0.45, seite=-1, typ="fischhaken", farbe=R)
t.unterschrift(mm, "Methylmalonyl-CoA — abstrahiert wird", "ein H der Methylgruppe")

t.reaktionspfeil(300, 842, 362)

rad = mech.Molekuel("[CH2]C(C(=O)[O-])C(=O)*", 500, 838, labels={7: "SCoA"},
                    zeige={0: "oben"}, name="Substratradikal")
t.mole.append(rad)
e_rad = t.einzelelektron(rad, 0, 300)
t.pfeil(e_rad, rad.aussen(1, 5, abstand=22), bogen=0.34, seite=1, typ="fischhaken", farbe=R)
t.pfeil(rad.aussen(1, 5, abstand=22), rad.aussen(1, abstand=24), bogen=0.42, seite=-1,
        typ="fischhaken", farbe=R)
t.unterschrift(rad, "die Thioestergruppe wandert 1,2 —", "das Radikal bleibt am Nachbarn zurück")

t.reaktionspfeil(624, 842, 686)
t.text(655, 832, "+ H", size=10.5, anchor="middle", gewicht=700, farbe=G)

suc = mech.Molekuel("[O-]C(=O)CCC(=O)*", 832, 838, labels={7: "SCoA"},
                    zeige={0: "links"}, name="Succinyl-CoA")
t.mole.append(suc)
t.unterschrift(suc, "Succinyl-CoA — der Eingang", "in den Citratzyklus (§ 3.2)")

# ===================================================== ZONE D · Klinik
t.zone(958, "D · WARUM DER MANGEL ZWEI MARKER HAT")

t.kasten(20, 990, 470, 138, fill="var(--enzym-bg)", stroke=E)
t.text(38, 1012, "METHIONINSYNTHASE FÄLLT AUS", size=11, gewicht=700, farbe=E)
t.text(38, 1034, "Homocystein steigt.", size=12.5)
t.text(38, 1053, "Das Folat staut sich als 5-Methyl-THF — die", size=12.5)
t.text(38, 1072, "Methylfalle. Folge: megaloblastäre Anämie.", size=12.5)
t.text(38, 1095, "Dasselbe Bild entsteht bei reinem Folatmangel;", size=12, farbe=G)
t.text(38, 1114, "dieser Marker trennt also nicht.", size=12, farbe=G)

t.kasten(510, 990, 470, 138, fill="var(--drug-bg)", stroke=R)
t.text(528, 1012, "MUTASE FÄLLT AUS", size=11, gewicht=700, farbe=R)
t.text(528, 1034, "Methylmalonsäure steigt.", size=12.5)
t.text(528, 1053, "Diese Reaktion braucht kein Folat, deshalb steigt", size=12.5)
t.text(528, 1072, "der Wert nur bei B&#8321;&#8322;-Mangel.", size=12.5)
t.text(528, 1095, "Damit ist die Methylmalonsäure der spezifische", size=12, farbe=G)
t.text(528, 1114, "Parameter — und der, den man vor Substitution misst.", size=12, farbe=G)

t.kasten(20, 1152, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1174, "LACHGAS TRIFFT NUR EINE DER BEIDEN FORMEN", size=11, gewicht=700, farbe=W)
t.text(38, 1196, "Distickstoffmonoxid oxidiert das Co(I) der Methioninsynthase irreversibel. Die "
                 "Mutase läuft über Co(II) und bleibt zunächst unberührt.", size=12.5)
t.text(38, 1215, "Deshalb steigt bei Lachgasschäden das Homocystein früher und deutlicher als die "
                 "Methylmalonsäure — ein Befundmuster, das sich aus Zone A ablesen lässt.", size=12.5)

t.kasten(20, 1270, 960, 96, fill="var(--surface-2)")
t.text(38, 1292, "WAS SICH DARAUS FÜR DIE PRÜFUNG ERGIBT", size=11, gewicht=700, farbe=G)
t.text(38, 1314, "Wer Folsäure gibt, ohne B&#8321;&#8322; bestimmt zu haben, korrigiert das Blutbild "
                 "und lässt die funikuläre Myelose weiterlaufen: Die Thymidylatsynthese", size=12.5)
t.text(38, 1333, "bekommt wieder Nachschub, die Mutase nicht. Dasselbe Radikal, das die Mutase "
                 "braucht, entsteht übrigens auch aus SAM (Tafel M-05).", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Cobalamin in vier Zonen. Zone A stellt die beiden Spaltungsweisen derselben "
    "Kohlenstoff-Cobalt-Bindung nebeneinander: links Methylcobalamin, bei dem ein "
    "Elektronenpaarpfeil beide Bindungselektronen ans Cobalt gibt, sodass Cobalt eins "
    "entsteht; rechts Adenosylcobalamin, bei dem zwei Fischhakenpfeile je ein Elektron nach "
    "jeder Seite ziehen, sodass Cobalt zwei und das Desoxyadenosylradikal entstehen. Zone B "
    "zeigt den heterolytischen Weg der Methioninsynthase: Cobalt eins greift die Methylgruppe "
    "des 5-Methyl-Tetrahydrofolats an, danach greift das Thiolat des Homocysteins die "
    "Methylgruppe am Cobalt an, es entsteht Methionin. Zone C zeigt den homolytischen Weg der "
    "Methylmalonyl-CoA-Mutase: Das Adenosylradikal abstrahiert ein Wasserstoffatom der "
    "Methylgruppe, die Thioestergruppe wandert an den Nachbarkohlenstoff, das Wasserstoffatom "
    "kehrt zurueck, es entsteht Succinyl-CoA. Zone D erklaert, warum Homocystein und "
    "Methylmalonsaeure zwei verschiedene Marker sind und warum Lachgas nur die Cobalt-eins-Form "
    "trifft."
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

mech.speichern("m16", t.svg(ARIA), t)
