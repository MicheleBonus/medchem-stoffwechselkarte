# -*- coding: utf-8 -*-
"""
M-14 · NO-Synthase, gebaut mit mech.py.

Die letzte der siebzehn Tafeln. Zone A ist bewusst ein Schema und keine
Strukturzeichnung: Es geht um die Anordnung zweier Untereinheiten, nicht um
Bindungen. Zone B dagegen zeigt die drei Substratstufen als echte Strukturen.
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

t = mech.Tafel(1000, 1344)

# ===================================================== ZONE A · das Dimer
t.zone(24, "A · WARUM NUR DAS DIMER ARBEITET")
t.text(20, 54, "Jedes Monomer trägt eine Reduktase- und eine Oxygenase-Hälfte. Die Elektronen "
               "wechseln zwischen den Hälften jedoch über Kreuz: vom Flavin des einen",
       size=12.5)
t.text(20, 73, "Monomers auf das Häm des anderen. Ein einzelnes Monomer kann deshalb keinen "
               "Sauerstoff aktivieren.", size=12.5)


def monomer(y, beschriftung):
    # Die Kaesten beginnen erst bei x=90: bei x=70 lief die Beschriftung
    # "Monomer A" unter den linken Rahmen.
    t.kasten(90, y, 260, 44, fill="var(--surface-2)", r=6)
    t.text(220, y + 20, "Reduktase-Domäne", size=11.5, anchor="middle", gewicht=700)
    t.text(220, y + 36, "NADPH → FAD → FMN", size=10.5, anchor="middle", farbe=C)
    t.kasten(356, y, 62, 44, fill="var(--cofaktor-bg)", stroke=C, r=6)
    t.text(387, y + 28, "CaM", size=11, anchor="middle", gewicht=700, farbe=C)
    t.kasten(426, y, 240, 44, fill="var(--enzym-bg)", stroke=E, r=6)
    t.text(546, y + 20, "Oxygenase-Domäne", size=11.5, anchor="middle", gewicht=700, farbe=E)
    t.text(546, y + 36, "Häm · BH&#8324; · L-Arginin", size=10.5, anchor="middle", farbe=E)
    t.text(20, y + 28, beschriftung, size=11.5, gewicht=700)


monomer(112, "Monomer A")
monomer(216, "Monomer B")

t.stuecke.append((1, "<path d='M 340 156 Q 411 186 482 216' fill='none' stroke='var(--warn)' "
                     "stroke-width='2' marker-end='url(#rxn)'/>"))
t.stuecke.append((1, "<path d='M 482 156 Q 411 186 340 216' fill='none' stroke='var(--warn)' "
                     "stroke-width='2' stroke-dasharray='5 3' marker-end='url(#rxn)'/>"))

t.kasten(680, 112, 300, 148, fill="var(--warn-bg)", stroke=W)
t.text(698, 134, "DIE ELEKTRONEN WECHSELN DIE SEITE", size=11, gewicht=700, farbe=W)
t.text(698, 156, "Das FMN des einen Monomers speist das", size=12.5)
t.text(698, 175, "Häm des anderen. Erst dadurch entsteht", size=12.5)
t.text(698, 194, "ein funktionsfähiges aktives Zentrum.", size=12.5)
t.text(698, 217, "Calmodulin ist der Schalter: Erst wenn es", size=12.5)
t.text(698, 236, "bindet, richtet sich die Reduktase so aus,", size=12.5)
t.text(698, 255, "dass der Elektronenfluss zustande kommt.", size=12.5)

t.kasten(20, 292, 960, 76, fill="var(--surface-2)")
t.text(38, 314, "DARAUS FOLGT DER UNTERSCHIED ZWISCHEN DEN DREI ISOFORMEN", size=11,
       gewicht=700, farbe=G)
t.text(38, 336, "nNOS und eNOS binden Calmodulin erst bei steigendem Calcium. Sie arbeiten "
                "in kurzen Stößen und regulieren. Die iNOS bindet Calmodulin schon", size=12.5)
t.text(38, 355, "bei basalem Calcium und läuft nach Induktion dauerhaft; ihre NO-Mengen sind "
                "um Größenordnungen höher und zytotoxisch gemeint.", size=12.5)

# ===================================================== ZONE B · die zwei Schritte
t.zone(404, "B · ZWEI OXIDATIONSSCHRITTE, EIN UNGEWÖHNLICHER ZWEITER")
t.text(20, 434, "Der erste Schritt ist eine gewöhnliche Monooxygenierung wie beim P450. Der "
                "zweite bewegt drei Elektronen auf einmal. Dafür gibt es kaum ein zweites",
       size=12.5)
t.text(20, 453, "Beispiel in der Biochemie. Ein voller Umsatz verbraucht zwei Sauerstoffmoleküle "
                "und 1,5 NADPH und setzt je Schritt ein Wasser frei.", size=12.5)

arg = mech.Molekuel("N[C@@H](CCCNC(N)=N)C(=O)O", 150, 566, stereo=True, name="L-Arginin")
t.mole.append(arg)
t.unterschrift(arg, "L-Arginin: die Guanidingruppe trägt", "den Stickstoff, aus dem NO wird",
               abstand=30)

t.reaktionspfeil(300, 566, 374)
t.text(337, 552, "+ O&#8322;, 1 NADPH, H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(337, 588, "&#8722; H&#8322;O, NADP&#8314;", size=10, anchor="middle", farbe=C)
t.text(337, 604, "gewöhnliche", size=10, anchor="middle", farbe=G)
t.text(337, 618, "Monooxygenierung", size=10, anchor="middle", farbe=G)

noha = mech.Molekuel("N[C@@H](CCCNC(N)=NO)C(=O)O", 540, 566, stereo=True, name="NOHA")
t.mole.append(noha)
t.unterschrift(noha, "N<tspan baseline-shift='super' font-size='8'>ω</tspan>-Hydroxy-L-arginin",
               abstand=30, farbe=W)

t.reaktionspfeil(680, 566, 754)
t.text(717, 552, "+ O&#8322;, ½ NADPH, H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(717, 588, "&#8722; H&#8322;O, ½ NADP&#8314;", size=10, anchor="middle", farbe=C)
t.text(717, 604, "Drei-Elektronen-", size=10, anchor="middle", farbe=W, gewicht=700)
t.text(717, 618, "Oxidation", size=10, anchor="middle", farbe=W, gewicht=700)

cit = mech.Molekuel("N[C@@H](CCCNC(N)=O)C(=O)O", 890, 566, stereo=True, name="L-Citrullin")
t.mole.append(cit)
t.unterschrift(cit, "L-Citrullin, daneben entsteht", "das freigesetzte NO", abstand=30, farbe=E)

# ===================================================== ZONE C · BH4
t.zone(716, "C · DIE SONDERROLLE DES BH&#8324;: WAS OHNE DIESEN COFAKTOR GESCHIEHT")
t.text(20, 746, "Derselbe Cofaktor wie in Tafel M-10, aber mit einer anderen Aufgabe. Das "
                "erklärt, warum ein BH&#8324;-Mangel zwei ganz verschiedene Bilder erzeugen "
                "kann.", size=12.5)

zh = t.zentrum(140, 852, "Fe(II)", axial=["O", "O"], unten="S&#8722;Cys", schritt=46,
               name="Oxy-Komplex")
t.text(140, 908, "Fe(II)&#8722;O&#8322;-Komplex", size=11, anchor="middle", gewicht=700, farbe=W)
t.text(140, 924, "wartet auf ein Elektron", size=10.5, anchor="middle", farbe=G)

# zeige={10:"links"} dreht das Pterin so, dass das N5 zum Haem hin zeigt. In der
# unveraenderten Lage laege die Dihydroxypropyl-Seitenkette genau im Weg des
# Fischhakens, und der Pfeil liefe durch eine OH-Gruppe.
bh4 = mech.Molekuel("CC(O)C(O)C1CNC2=C(N1)C(=O)NC(N)=N2", 380, 830,
                    zeige={10: "links"}, name="BH4")
t.mole.append(bh4)
# Das Elektron kommt vom N5 des Tetrahydropterins (Atomindex 10: der Ringstickstoff
# zwischen C4a und C6), nicht von der CH2-Gruppe C7. Zurueck bleibt das am N5
# lokalisierte Radikalkation BH4-Punkt-plus. Ein Methylenkohlenstoff haette weder
# ein freies Paar noch ein Einzelelektron abzugeben.
lp_b = t.elektronenpaar(bh4, 10, 180, abstand=21)
t.atomnummer(bh4, 10, "N5", winkel=237, abstand=25, size=9.5, farbe=R, gewicht=700)
t.pfeil(lp_b, zh.ax(1, winkel=20, abstand=36), bogen=0.18, seite=1, typ="fischhaken",
        farbe=R)
t.unterschrift(bh4, "BH&#8324; gibt ein einzelnes Elektron vom N5 ab",
               "und wird sofort wieder reduziert", abstand=26)

t.kasten(560, 784, 420, 138, fill="var(--cofaktor-bg)", stroke=C)
t.text(578, 806, "ZWEI ROLLEN FÜR DENSELBEN COFAKTOR", size=11, gewicht=700, farbe=C)
t.text(578, 828, "Bei der Phenylalanin- und der Tyrosinhydroxylase gibt", size=12.5)
t.text(578, 847, "BH&#8324; zwei Elektronen ab und wird dabei verbraucht; es", size=12.5)
t.text(578, 866, "muss über PCD und DHPR zurückgeführt werden.", size=12.5)
t.text(578, 889, "Hier gibt es nur eines ab und nimmt es sofort zurück.", size=12.5)
t.text(578, 908, "Es wirkt als Zwischenlager, nicht als Sauerstoffträger.", size=12.5)

t.kasten(20, 964, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 986, "ENTKOPPLUNG: WENN DAS ELEKTRON AUSBLEIBT", size=11, gewicht=700, farbe=W)
t.text(38, 1008, "Fehlt BH&#8324;, bleibt der Fe(II)&#8722;O&#8322;-Komplex ohne Elektron stehen. "
                "Er zerfällt und entlässt Superoxid statt NO. Aus dem gefäßschützenden", size=12.5)
t.text(38, 1027, "Enzym wird eine Quelle oxidativen Stresses, und das entstehende Peroxynitrit "
                "oxidiert weiteres BH&#8324;. Der Schaden verstärkt sich selbst.", size=12.5)

t.kasten(20, 1090, 470, 118, fill="var(--enzym-bg)", stroke=E)
t.text(38, 1112, "WO DIE ARZNEISTOFFE ANSETZEN", size=11, gewicht=700, farbe=E)
t.text(38, 1134, "Nicht am Enzym. Nitrate und Molsidomin liefern NO", size=12.5)
t.text(38, 1153, "von außen, Riociguat aktiviert die lösliche", size=12.5)
t.text(38, 1172, "Guanylatcyclase direkt, und die PDE-5-Hemmer", size=12.5)
t.text(38, 1191, "verlängern das Signal, indem sie cGMP schonen.", size=12.5)

t.kasten(510, 1090, 470, 118, fill="var(--surface-2)")
t.text(528, 1112, "WARUM MAN DAS ENZYM NICHT HEMMT", size=11, gewicht=700, farbe=G)
t.text(528, 1134, "Die drei Isoformen unterscheiden sich chemisch kaum.", size=12.5)
t.text(528, 1153, "Ein Hemmstoff, der die iNOS träfe, träfe auch die eNOS", size=12.5)
t.text(528, 1172, "und damit die Gefäßregulation. Genau daran sind die", size=12.5)
t.text(528, 1191, "Versuche in der Sepsistherapie gescheitert.", size=12.5)

t.text(20, 1262, "Die Nitrattoleranz erklärt sich aus derselben Chemie: Die Umsetzung von "
                 "Glyceroltrinitrat zu NO verbraucht Thiole, und mit sinkendem Glutathion "
                 "sinkt die", size=12.5, farbe=G)
t.text(20, 1282, "Wirkung. Deshalb das nitratfreie Intervall, und deshalb der Zusammenhang mit "
                 "Tafel M-17.", size=12.5, farbe=G)

# ===================================================== Ausgabe
ARIA = (
    "Stickstoffmonoxid-Synthase in drei Zonen. Zone A zeigt schematisch den Aufbau des Dimers: "
    "Jedes Monomer traegt eine Reduktase-Domaene mit FAD und FMN, eine Calmodulin-Bindestelle "
    "und eine Oxygenase-Domaene mit Haem, Tetrahydrobiopterin und Arginin. Zwei gekreuzte "
    "Pfeile zeigen, dass die Elektronen vom Flavin des einen Monomers auf das Haem des anderen "
    "uebergehen; nur das Dimer ist deshalb aktiv. Zone B zeigt die beiden Oxidationsschritte an "
    "gezeichneten Strukturen: L-Arginin, N-omega-Hydroxy-L-arginin und L-Citrullin. Der erste "
    "Schritt verbraucht ein Sauerstoffmolekuel und ein NADPH, der zweite ein Sauerstoffmolekuel "
    "und ein halbes NADPH; beide Schritte setzen je ein Wasser frei, und der zweite bewegt drei "
    "Elektronen auf einmal und entlaesst Stickstoffmonoxid. Zone C zeigt mit einem "
    "Fischhakenpfeil, wie das Tetrahydrobiopterin ein einzelnes Elektron vom Ringstickstoff N5 "
    "an den Sauerstoffkomplex am Haemeisen abgibt und dabei zum N5-Radikalkation wird, und "
    "erklaert die Entkopplung zu Superoxid, wenn dieser Cofaktor fehlt."
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

mech.speichern("m14", t.svg(ARIA), t)
