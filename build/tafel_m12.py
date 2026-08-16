# -*- coding: utf-8 -*-
"""
M-12 · Cyclooxygenase, gebaut mit mech.py.

Die laengste Radikalkette des ganzen Satzes. Alle fuenf Zwischenstufen sind als
echte Strukturen gezeichnet, jeder Schritt mit Fischhakenpfeilen ausgefuehrt.
Die Zwischenstufen sind Ausschnitte C7 bis C16 - im selben Massstab wie alles
andere, damit man die Kette von Bild zu Bild verfolgen kann.
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import mech

HERE = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HERE, "tafeln.json")

W = "var(--warn)"
R = "var(--drug)"
E = "var(--enzym)"
C = "var(--cofaktor)"
G = "var(--ink-3)"

t = mech.Tafel(1000, 1500)

# ===================================================== ZONE A · Initiation
t.zone(24, "A · DER START — DAS ENZYM ZÜNDET SEINE EIGENE RADIKALKETTE")
t.text(20, 54, "Die Cyclooxygenase trägt zwei aktive Zentren. Das Peroxidase-Zentrum am Häm "
               "erzeugt das Radikal, das die Cyclooxygenase-Reaktion überhaupt erst startet.",
       size=12.5)

zfe = t.zentrum(92, 158, "Fe(III)", unten="His", name="Peroxidase-Häm")
t.text(92, 214, "Ruhezustand", size=10.5, anchor="middle", farbe=G)

t.reaktionspfeil(152, 158, 216)
t.text(184, 148, "+ ROOH", size=10.5, anchor="middle", gewicht=700, farbe=C)

zcp = t.zentrum(284, 158, "Fe(IV)", axial=["O"], doppelt=True, radikal=True, unten="His",
                name="Compound I")
t.text(284, 214, "Compound I", size=10.5, anchor="middle", gewicht=700, farbe=W)

tyr = mech.Molekuel("*c1ccc(O)cc1", 486, 160, labels={0: "Protein"},
                    wasserstoff=[5], zeige={5: "links", 0: "rechts"}, name="Tyr385")
t.mole.append(tyr)
hO = tyr.h_index[5]
t.pfeil((tyr, 5, hO), zcp.ax(0), bogen=0.22, seite=-1, typ="fischhaken", farbe=R)
t.pfeil((tyr, 5, hO), tyr.abseits(5, hO), bogen=0.45, seite=1, typ="fischhaken", farbe=R)
t.unterschrift(tyr, "Tyrosin 385 — das Wasserstoffatom seiner", "phenolischen OH-Gruppe geht ans Ferryl")

t.reaktionspfeil(614, 158, 678)

tyr2 = mech.Molekuel("*c1ccc([O])cc1", 782, 160, labels={0: "Protein"},
                     zeige={5: "links", 0: "rechts"}, name="Tyr385-Radikal")
t.mole.append(tyr2)
t.einzelelektron(tyr2, 5, 200)
t.unterschrift(tyr2, "Tyrosyl-Radikal — im Phenolring", "delokalisiert und dadurch langlebig",
               farbe=R)

t.kasten(20, 258, 960, 52, fill="var(--surface-2)")
t.text(38, 280, "Paracetamol setzt genau hier an: Es reduziert das Tyrosyl-Radikal zurück zum "
                "Phenol. Weil ein hoher Peroxidspiegel es laufend neu erzeugt, bricht diese "
                "Hemmung im", size=12.5)
t.text(38, 299, "entzündeten Gewebe zusammen — im ZNS mit niedrigem Peroxidtonus dagegen nicht. "
                "Daraus folgt: analgetisch und antipyretisch, kaum antiphlogistisch.", size=12.5)

# ===================================================== ZONE B · Schritte 1 bis 3
t.zone(350, "B · SCHRITT &#9312; BIS &#9314; — ABSTRAKTION, DELOKALISIERUNG, ERSTER SAUERSTOFF")
t.text(20, 380, "Gezeigt ist der Ausschnitt C8 bis C15 der Arachidonsäure. Alle Schritte laufen "
                "ohne Zwischenfreisetzung im selben Kanal ab.", size=12.5)

# Die Kette wird gestreckt gezeichnet, damit man C7 bis C16 von Bild zu Bild
# verfolgen kann. Nur C8=C9 traegt seine cis-Angabe, weil diese Doppelbindung
# die ganze Kaskade ueberdauert; die tatsaechliche U-Form der Arachidonsaeure
# steht in § 4.1 und wird im Kasten unten erklaert.
AA = r"*/C=C\CC=CCC=C*"          # C7*, C8=C9, C10, C11=C12, C13, C14=C15, C16*

f1 = mech.Molekuel(AA, 168, 478, labels={0: "C7", 9: "C16"},
                   wasserstoff=[6], zeige={0: "links"}, name="Arachidonsäure")
t.mole.append(f1)
h13 = f1.h_index[6]
tyrrad = t.marke(168, 404, "Tyr385-Radikal")
t.text(168, 400, "Tyr385&#8226;", size=11, anchor="middle", gewicht=700, farbe=R)
t.pfeil((f1, 6, h13), tyrrad, bogen=0.24, seite=1, typ="fischhaken", farbe=R)
t.pfeil((f1, 6, h13), f1.abseits(6, h13), bogen=0.45, seite=-1, typ="fischhaken", farbe=R)
t.atomnummer(f1, 6, "C13", winkel=105, abstand=30)
t.text(168, 428, "&#9312;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f1, "Abstraktion des 13-pro-S-Wasserstoffs", abstand=34)

t.reaktionspfeil(306, 478, 366)

f2 = mech.Molekuel(r"*/C=C\C[CH]C=CC=C*", 500, 478, labels={0: "C7", 9: "C16"},
                   zeige={0: "links"}, name="Pentadienyl-Radikal")
t.mole.append(f2)
t.einzelelektron(f2, 4, 270)
t.atomnummer(f2, 4, "C11", winkel=90)
t.atomnummer(f2, 8, "C15", winkel=90)
t.text(500, 428, "&#9313;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f2, "delokalisiert über C11 bis C15 — der Sauerstoff",
               "greift deshalb nicht dort an, wo das H saß", abstand=34)

t.reaktionspfeil(638, 478, 698)
t.text(668, 468, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=E)

f3 = mech.Molekuel(r"*/C=C\CC(O[O])C=CC=C*", 832, 478, labels={0: "C7", 11: "C16"},
                   zeige={0: "links"}, name="11-Peroxylradikal")
t.mole.append(f3)
t.einzelelektron(f3, 6, 300)
t.atomnummer(f3, 4, "C11", winkel=110)
t.text(832, 428, "&#9314;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f3, "11-Peroxylradikal — Sauerstoff tritt von der",
               "Gegenseite des abstrahierten Wasserstoffs ein", abstand=34)

# ===================================================== ZONE C · Schritte 4 und 5
t.zone(608, "C · SCHRITT &#9315; BIS &#9317; — ZWEI RINGSCHLÜSSE, DANN DER ZWEITE SAUERSTOFF")
t.text(20, 638, "Zweimal dasselbe Muster: Ein Radikal addiert an eine Doppelbindung, und das "
                "Radikal wandert an deren anderes Ende.", size=12.5)

f3b = mech.Molekuel(r"*/C=C\CC(O[O])C=CC=C*", 168, 762, labels={0: "C7", 11: "C16"},
                    zeige={0: "links"}, name="11-Peroxylradikal")
t.mole.append(f3b)
e3 = t.einzelelektron(f3b, 6, 300)
t.pfeil(e3, (f3b, 1, 2), bogen=0.26, seite=1, typ="fischhaken", farbe=R)
t.pfeil((f3b, 1, 2), f3b.abseits(1, 2), bogen=0.45, seite=-1, typ="fischhaken", farbe=R)
t.atomnummer(f3b, 1, "C8", winkel=140, abstand=28)
t.atomnummer(f3b, 2, "C9", winkel=75, abstand=21)
t.text(168, 706, "&#9315; das Peroxylradikal greift C9 an", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.unterschrift(f3b, "es entsteht die O&#8722;O-Brücke C9&#8722;C11,",
               "das Radikal bleibt an C8 zurück", abstand=34)

t.reaktionspfeil(306, 762, 366)

f4 = mech.Molekuel(r"*[CH]C1CC(OO1)C=CC=C*", 500, 762, labels={0: "C7", 11: "C16"},
                   zeige={0: "links"}, name="C8-Radikal")
t.mole.append(f4)
e4 = t.einzelelektron(f4, 1, 250)
t.pfeil(e4, (f4, 7, 8), bogen=0.28, seite=1, typ="fischhaken", farbe=R)
t.pfeil((f4, 7, 8), f4.abseits(8, 7), bogen=0.45, seite=-1, typ="fischhaken", farbe=R)
t.atomnummer(f4, 1, "C8", winkel=100, abstand=26)
t.atomnummer(f4, 7, "C12", winkel=105, abstand=23)
t.text(500, 706, "&#9316; C8 greift C12 an", size=11, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f4, "der Fünfring schließt sich, das Radikal",
               "wandert allylisch nach C13 bis C15", abstand=34)

t.reaktionspfeil(638, 762, 698)
t.text(668, 752, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=E)

f5 = mech.Molekuel(r"*C1C2CC(OO2)C1/C=C/C(OO)*", 832, 762, labels={0: "C7", 13: "C16"},
                   zeige={0: "links"}, name="PGG2-Kern")
t.mole.append(f5)
t.atomnummer(f5, 9, "C15", winkel=200, abstand=20)
t.text(832, 688, "&#9317; Sauerstoff an C15", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.unterschrift(f5, "PGG&#8322; — Bicyclus aus Endoperoxid und Fünfring,",
               "dazu das 15-Hydroperoxid (§ 4.2 zeigt die ganze Struktur)",
               abstand=34, farbe=W, gewicht=700)

t.kasten(20, 880, 470, 122, fill="var(--surface-2)")
t.text(38, 906, "WARUM DAS PRODUKT EINHEITLICH IST", size=11, gewicht=700, farbe=G)
t.text(38, 928, "Das Enzym hält die Kette in einer Haarnadelform. Nur deshalb", size=12.5)
t.text(38, 947, "liegen C8 und C12 nahe genug beieinander, und nur deshalb tritt", size=12.5)
t.text(38, 966, "der Sauerstoff jedes Mal von derselben Seite ein. Freie Radikale", size=12.5)
t.text(38, 985, "in Lösung ergäben ein Produktgemisch.", size=12.5)

t.kasten(510, 880, 470, 122, fill="var(--cofaktor-bg)", stroke=C)
t.text(528, 906, "DER ZWEITE DURCHGANG AM HÄM", size=11, gewicht=700, farbe=C)
t.text(528, 928, "Dasselbe Peroxidase-Zentrum, das die Kette gezündet hat,", size=12.5)
t.text(528, 947, "reduziert am Ende das 15-Hydroperoxid zum Alkohol:", size=12.5)
t.text(528, 966, "PGG&#8322; → PGH&#8322;. Ein Enzym, zwei Aktivitäten, zwei getrennte", size=12.5)
t.text(528, 985, "Zentren — deshalb kann Paracetamol das eine treffen.", size=12.5)

# ===================================================== ZONE D · Arzneistoffe
t.zone(1046, "D · WO DIE ARZNEISTOFFE ANSETZEN")

t.text(20, 1080, "Acetylsalicylsäure — kovalent", size=13, gewicht=700, farbe=R)
t.text(20, 1104, "Der Zugangskanal zum aktiven Zentrum wird von Ser530 verengt.", size=12.5)
t.text(20, 1123, "Aspirin überträgt seinen Acetylrest auf dessen Hydroxylgruppe und", size=12.5)
t.text(20, 1142, "versperrt den Kanal dauerhaft. In COX-2 ist der Kanal weiter: Das", size=12.5)
t.text(20, 1161, "acetylierte Enzym bleibt teilaktiv und bildet 15-<tspan font-style='italic'>R</tspan>-HETE,",
       size=12.5)
t.text(20, 1180, "aus dem die entzündungsauflösenden Aspirin-getriggerten Lipoxine", size=12.5)
t.text(20, 1199, "entstehen.", size=12.5)
t.text(20, 1226, "Alle übrigen NSAR binden nichtkovalent im selben Kanal und wirken", size=12, farbe=G)
t.text(20, 1245, "daher reversibel und konzentrationsabhängig.", size=12, farbe=G)

t.text(530, 1080, "Coxibe — eine Aminosäure entscheidet", size=13, gewicht=700, farbe=R)
t.text(530, 1104, "An Position 523 trägt COX-1 ein Isoleucin, COX-2 ein kleineres", size=12.5)
t.text(530, 1123, "Valin. Dadurch öffnet sich in COX-2 eine seitliche Tasche, in die", size=12.5)
t.text(530, 1142, "der Sulfonamid- oder Methylsulfonrest der Coxibe hineinreicht.", size=12.5)
t.text(530, 1161, "In COX-1 versperrt das Isoleucin sie.", size=12.5)
t.text(530, 1188, "Damit beruht die Selektivität nicht auf der Affinität zum", size=12, farbe=G)
t.text(530, 1207, "katalytischen Zentrum, sondern auf der Passform einer Neben-", size=12, farbe=G)
t.text(530, 1226, "tasche — ein Lehrbeispiel für strukturbasiertes Wirkstoffdesign.", size=12, farbe=G)

t.kasten(20, 1274, 960, 76, fill="var(--drug-bg)", stroke=R)
t.text(38, 1296, "DIE PRÜFUNGSFRAGE, DIE SICH AUS DER TAFEL BEANTWORTEN LÄSST", size=11,
       gewicht=700, farbe=R)
t.text(38, 1318, "Warum wirkt niedrig dosierte Acetylsalicylsäure im Thrombozyten endgültig? Weil "
                 "die Acetylierung kovalent ist und der kernlose Thrombozyt kein", size=12.5)
t.text(38, 1337, "neues Enzym bilden kann. Das Endothel hat einen Kern und synthetisiert seine "
                 "COX-2 nach — daraus folgt die Selektivität der niedrigen Dosis.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Der Mechanismus der Cyclooxygenase in vier Zonen. Zone A: Das Peroxidase-Haem mit "
    "proximalem Histidin wird von einem Hydroperoxid zu Compound eins oxidiert; dieses "
    "abstrahiert mit Fischhakenpfeilen das Wasserstoffatom der phenolischen Hydroxylgruppe von "
    "Tyrosin 385, es entsteht das Tyrosylradikal. Zone B: Das Tyrosylradikal abstrahiert das "
    "13-pro-S-Wasserstoffatom der Arachidonsaeure; das Radikal delokalisiert ueber C11 bis C15; "
    "Sauerstoff addiert an C11 zum Peroxylradikal. Zone C: Das Peroxylradikal greift C9 an und "
    "bildet die Endoperoxidbruecke, wobei das Radikal an C8 zurueckbleibt; C8 greift C12 an und "
    "schliesst den Fuenfring, das Radikal wandert allylisch nach C13 bis C15; ein zweites "
    "Sauerstoffmolekuel addiert an C15. Es entsteht der Bicyclus PGG2. Zone D nennt die "
    "Angriffspunkte von Acetylsalicylsaeure an Serin 530 und der Coxibe an der Nebentasche, "
    "die durch Valin 523 in COX-2 zugaenglich wird."
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

daten = {}
if os.path.exists(ZIEL):
    daten = json.load(io.open(ZIEL, encoding="utf-8"))
daten["m12"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m12  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m12"]), len(t.mole), len(t.anker)))
