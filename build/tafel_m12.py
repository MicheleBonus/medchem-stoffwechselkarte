# -*- coding: utf-8 -*-
"""
M-12 · Cyclooxygenase, gebaut mit mech.py.

Die laengste Radikalkette des ganzen Satzes. Alle fuenf Zwischenstufen sind als
echte Strukturen gezeichnet, jeder Schritt mit Fischhakenpfeilen ausgefuehrt.
Die Zwischenstufen sind Ausschnitte C7 bis C16, gezeichnet im selben Massstab
wie alles andere, damit man die Kette von Bild zu Bild verfolgen kann.

Zwei Leitgerueste halten die Lage fest, statt jede Stufe einzeln einzunorden:

  KETTE   das Rueckgrat C7 bis C16. Es ist kein Ring, aber mech_kerne.eigener()
          braucht auch keinen: 'ring' ist schlicht die Atomliste, an deren
          Schwerpunkt die Lage haengt. Genannt sind hier die beiden Kettenenden,
          C7 zeigt nach links - damit liegt die Kette in jeder Stufe waagerecht
          und laeuft mit der Leserichtung. Vorher hielt zeige= nur die beiden
          Enden fest; wie die Kette dazwischen lag, entschied jedes Bild fuer
          sich, und der Blick musste jede Stufe neu einnorden.
  PHENOL  der Tyrosinring, der zweimal vorkommt - vor und nach der Abstraktion.
          Er steht schraeg, die Hydroxylgruppe nach oben links, der Proteinrest
          nach unten rechts. Das ist nicht Geschmack: liegt der Ring waagerecht,
          zeigen beide Fischhaken der Abstraktion in dieselbe Luecke neben der
          O-H-Bindung und laufen ineinander.

Die Pfeile sagen nur noch die Chemie an: aus welcher Bindung das Elektron kommt
und an welchem Atom es landet. Bogen, Seite und Ankerlage sucht der Solver in
mech_schub.py, geprueft wird gegen mech_regeln.py.

Zwei Stellen sind dabei anders geworden als zuvor, beide unten im Skript
begruendet: Schritt &#9312; steht jetzt in vier Fischhaken statt in zwei (die
alten zwei behaupteten das Radikal am C13, das naechste Bild zeigt es am C11),
und die beiden Ringschlusspfeile tragen art="inter", weil sie ueber drei
Bindungslaengen greifen und mech_schub fuer diesen Fall noch keine eigene
Laengenklasse kennt.
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

t = mech.Tafel(1000, 1500)

# --------------------------------------------------------------- Leitgerueste
# Das Rueckgrat C7 bis C16, als SMARTS ausgeschrieben: Platzhalter, acht
# Kohlenstoffe, Platzhalter. Es trifft alle fuenf Stufen - auch die beiden mit
# Ring, denn der Fuenfring haengt seitlich an derselben Kette.
KETTE_MUSTER = "[#0]~[#6]~[#6]~[#6]~[#6]~[#6]~[#6]~[#6]~[#6]~[#0]"
KETTE = mech_kerne.eigener(
    "aa-kette", r"*/C=C\CC=CCC=C*", muster=KETTE_MUSTER,
    ring=[0, 9], leit=0, folge=1, winkel=180.0)

PHENOL = mech_kerne.eigener(
    "tyr-phenol", "*c1ccc(O)cc1",
    muster="[#0]~[#6]1~[#6]~[#6]~[#6](~[#8])~[#6]~[#6]~1",
    ring=[1, 2, 3, 4, 6, 7], leit=4, folge=6, winkel=120.0)

# ===================================================== ZONE A · Initiation
t.zone(24, "A · DER START: DAS ENZYM ZÜNDET SEINE EIGENE RADIKALKETTE")
t.text(20, 54, "Die Cyclooxygenase trägt zwei aktive Zentren. Das Peroxidase-Zentrum am Häm "
               "erzeugt das Radikal, das die Cyclooxygenase-Reaktion überhaupt erst startet.",
       size=12.5)

zfe = t.zentrum(92, 158, "Fe(III)", unten="His", name="Peroxidase-Häm")
t.text(92, 214, "Ruhezustand", size=10.5, anchor="middle", farbe=G)

t.reaktionspfeil(152, 158, 216)
t.text(184, 148, "+ ROOH", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(184, 176, "&#8722; ROH", size=10, anchor="middle", farbe=G)

zcp = t.zentrum(284, 158, "Fe(IV)", axial=["O"], doppelt=True, radikal=True, unten="His",
                name="Compound I")
t.text(284, 214, "Compound I", size=10.5, anchor="middle", gewicht=700, farbe=W)

tyr = t.mol("*c1ccc(O)cc1", 486, 160, labels={0: "Protein"},
            wasserstoff=[5], kern=PHENOL, name="Tyr385")
hO = tyr.h_index[5]
# Homolyse der O&#8722;H-Bindung: das eine Elektron geht mit dem Wasserstoff ans
# Ferryl, das andere bleibt am Phenolsauerstoff und macht ihn zum Radikal. Beide
# Haken kommen aus derselben Bindung und laufen auseinander; sie haengen deshalb
# nicht Kopf an Schwanz und bilden keine Kette.
# Der Endpunkt ist ausdruecklich gesetzt, sonst steht die Spitze zu weit weg.
# Ohne winkel/abstand haengt sie an der Textellipse des O (halbe Textbreite plus
# 3 px), und dazu kommt der Zuschlag, den mech_schub.Fest fuer den Ursprung
# vorsieht: bis 0,45 L in Richtung der Quelle. Bei einer Sehne von sieben
# Bindungslaengen ist der Zuschlag dem Solver billiger als der laengere Bogen, er
# nimmt also immer den groessten - die Spitze stand 0,88 L neben dem O und
# schwebte im Leeren. Mit dem Ankerpunkt dicht am O (3 px) landet sie nach
# demselben Zuschlag 12 px rechts daneben: 0,37 L vor dem Glyphenrand, also im
# Fenster von Z1, und auf gleicher Hoehe wie das O.
t.schub(Bindung(tyr, 5, hO), zcp.ax(0, winkel=20, abstand=3), elektronen=1)
t.schub(Bindung(tyr, 5, hO), Atom(tyr, 5), elektronen=1)
t.unterschrift(tyr, "Tyrosin 385: das Wasserstoffatom seiner", "phenolischen OH-Gruppe geht ans Ferryl")

t.reaktionspfeil(614, 158, 678)

tyr2 = t.mol("*c1ccc([O])cc1", 782, 160, labels={0: "Protein"},
             kern=PHENOL, name="Tyr385-Radikal")
# Das ungepaarte Elektron steckt schon im SMILES ([O]); RDKit setzt den Punkt selbst.
# Ein zweiter, von Hand gesetzter Punkt stuende fuer ein zweites Elektron.
t.unterschrift(tyr2, "Tyrosylradikal: im Phenolring", "delokalisiert und dadurch langlebig",
               farbe=R)

t.kasten(20, 258, 960, 52, fill="var(--surface-2)")
t.text(38, 280, "Paracetamol setzt genau hier an: Es reduziert das Tyrosylradikal zurück zum "
                "Phenol. Weil ein hoher Peroxidspiegel es laufend neu erzeugt, bricht diese "
                "Hemmung im", size=12.5)
t.text(38, 299, "entzündeten Gewebe zusammen. Im ZNS mit niedrigem Peroxidtonus dagegen nicht. "
                "Daraus folgt: analgetisch und antipyretisch, kaum antiphlogistisch.", size=12.5)

# ===================================================== ZONE B · Schritte 1 bis 3
t.zone(350, "B · SCHRITT &#9312; BIS &#9314;: ABSTRAKTION, DELOKALISIERUNG, ERSTER SAUERSTOFF")
t.text(20, 380, "Gezeigt ist der Ausschnitt C7 bis C16 der Arachidonsäure. Alle Schritte laufen "
                "ohne Zwischenfreisetzung im selben Kanal ab.", size=12.5)

# Die Kette wird gestreckt gezeichnet, damit man C7 bis C16 von Bild zu Bild
# verfolgen kann. Nur C8=C9 traegt seine cis-Angabe: aus ihr wird in Schritt 4 die
# Endoperoxidbruecke, ihre Geometrie entscheidet also ueber die Ringgeometrie.
# Die tatsaechliche U-Form der ganzen Arachidonsaeure steht in § 4.1; die
# Bildunterschrift legt offen, dass die beiden anderen gestreckt gezeichnet sind.
AA = r"*/C=C\CC=CCC=C*"          # C7*, C8=C9, C10, C11=C12, C13, C14=C15, C16*

f1 = t.mol(AA, 168, 478, labels={0: "C7", 9: "C16"},
           wasserstoff=[6], kern=KETTE, name="Arachidonsäure")
h13 = f1.h_index[6]
# Das Tyrosylradikal steht rechts oberhalb des C13, nicht senkrecht darueber.
# Senkrecht darueber und weiter links liegen die drei anderen Fischhaken; zwei
# Pfeile im selben Feld sind nicht mehr auseinanderzuhalten.
tyrrad = t.marke(232, 402, "Tyr385-Radikal")
t.text(232, 398, "Tyr385&#8226;", size=11, anchor="middle", gewicht=700, farbe=R)
# Die Abstraktion, in vier Fischhaken ausgeschrieben. Frueher standen hier zwei:
# einer zum Tyrosylradikal, einer zurueck ans C13. Der zweite behauptete, das
# Radikal bleibe am C13 - das naechste Bild zeigt es aber am C11, mit
# verschobenen Doppelbindungen. Ausgeschrieben ist es die Kette, fuer die die
# beiden Haken standen: die C13&#8722;H-Bindung bricht homolytisch, ein Elektron geht
# mit dem Wasserstoff ans Tyrosylradikal, das andere in die werdende Doppel-
# bindung C12=C13; deren zweites Elektron kommt aus der alten Doppelbindung
# C11=C12, und das uebrige Elektron von dort bleibt am C11 zurueck. Genau diese
# Grenzstruktur steht daneben.
# Die beiden mittleren Haken sind gegenueber dieser Erzaehlung vertauscht
# angemeldet. Der Grund ist der Solver: er setzt in Reihenfolge und weicht dem
# schon gesetzten Pfeil aus. Kommt der kurze Haken von der C13-H-Bindung zuerst,
# draengt er den langen aus dem Feld unter der Kette, und beide liegen dann
# 0,18 L auseinander statt der geforderten 0,25.
t.schub(Bindung(f1, 6, h13), tyrrad, elektronen=1)
t.schub(Bindung(f1, 4, 5), Bindung(f1, 5, 6), elektronen=1)
t.schub(Bindung(f1, 6, h13), Bindung(f1, 5, 6), elektronen=1)
t.schub(Bindung(f1, 4, 5), Atom(f1, 4), elektronen=1)
# Senkrecht unter das C13. Schraeg (105 Grad) stand die Nummer zwischen C12 und
# C13 und war keinem der beiden zuzuordnen; in einer Zickzackkette ist die
# senkrechte Flucht der einzige Hinweis, der traegt, denn die beiden Nachbartaeler
# liegen immer aehnlich weit weg wie der Gipfel darueber.
t.atomnummer(f1, 6, "C13", winkel=90, abstand=30)
t.text(168, 428, "&#9312;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f1, "Abstraktion des 13-pro-S-Wasserstoffs", abstand=34)

t.reaktionspfeil(306, 478, 366)

f2 = t.mol(r"*/C=C\C[CH]C=CC=C*", 500, 478, labels={0: "C7", 9: "C16"},
           kern=KETTE, name="Pentadienyl-Radikal")
t.atomnummer(f2, 4, "C11", winkel=90, abstand=26)
t.atomnummer(f2, 8, "C15", winkel=90, abstand=26)
t.text(500, 428, "&#9313;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f2, "delokalisiert über C11 bis C15, deshalb greift der",
               "Sauerstoff nicht dort an, wo das H saß", abstand=34)

t.reaktionspfeil(638, 478, 698)
t.text(668, 468, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=E)

f3 = t.mol(r"*/C=C\CC(O[O])C=CC=C*", 832, 478, labels={0: "C7", 11: "C16"},
           kern=KETTE, name="11-Peroxylradikal")
# Nach links lag die Nummer auf der Bindung C10&#8722;C11; unter dem Scheitel ist Platz.
t.atomnummer(f3, 4, "C11", winkel=90, abstand=26)
t.text(832, 428, "&#9314;", size=13, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f3, "11-Peroxylradikal: Sauerstoff tritt von der",
               "Gegenseite des abstrahierten Wasserstoffs ein", abstand=34)

# ===================================================== ZONE C · Schritte 4 und 5
t.zone(608, "C · SCHRITT &#9315; BIS &#9317;: ZWEI RINGSCHLÜSSE, DANN DER ZWEITE SAUERSTOFF")
t.text(20, 638, "Zweimal dasselbe Muster: Ein Radikal addiert an eine Doppelbindung, und das "
                "Radikal wandert an deren anderes Ende.", size=12.5)

f3b = t.mol(r"*/C=C\CC(O[O])C=CC=C*", 168, 762, labels={0: "C7", 11: "C16"},
            kern=KETTE, name="11-Peroxylradikal")
# Der Fischhaken des Radikals zeigt auf das Atom, an dem die neue Bindung entsteht:
# C9, nicht auf die Mitte der Doppelbindung. Den Radikalpunkt am Sauerstoff zeichnet
# RDKit selbst, weil das Elektron im SMILES steht; deshalb steht hier Atom() und
# nicht Elektron(), das seinen Punkt noch einmal setzen wuerde.
#
# art="inter" ist hier keine Bequemlichkeit, sondern die einzige zutreffende
# Laengenklasse. Der Sauerstoff und das C9 liegen in der gestreckt gezeichneten
# Kette drei Bindungslaengen auseinander; erst die Haarnadelform des aktiven
# Zentrums bringt sie zusammen, und die laesst RDKit sich nicht vorschreiben
# (GenerateDepictionMatching2DStructure zieht eine Vorlage nur weich nach, siehe
# Meldung im Bericht). Das Fenster fuer "intra" endet bei 1,90 L und ist fuer
# einen Ringschluss ueber mehrere Atome zu eng; mech_schub kennt fuer diesen Fall
# noch keine eigene Klasse.
t.schub(Atom(f3b, 6), Atom(f3b, 2), elektronen=1, kette="C", art="inter")
t.schub(Bindung(f3b, 1, 2), Atom(f3b, 1), elektronen=1, kette="C")
t.atomnummer(f3b, 1, "C8", winkel=205, abstand=20)
t.atomnummer(f3b, 2, "C9", winkel=95, abstand=19)
t.text(168, 706, "&#9315; das Peroxylradikal greift C9 an", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.unterschrift(f3b, "es entsteht die O&#8722;O-Brücke C9&#8722;C11,",
               "das Radikal bleibt an C8 zurück", abstand=34)

t.reaktionspfeil(306, 762, 366)

f4 = t.mol(r"*[CH]C1CC(OO1)C=CC=C*", 500, 762, labels={0: "C7", 11: "C16"},
           kern=KETTE, name="C8-Radikal")
# Dasselbe Muster wie eben: das Radikal von C8 bildet die Bindung zu C12, das
# pi-Paar der Doppelbindung C12=C13 laeuft nach C13 aus. Auch hier greift der
# erste Haken ueber den halben Ausschnitt hinweg: C8 und C12 haengen an den
# beiden Ringkohlenstoffen C9 und C11, zwischen denen das C10 steht, und stehen
# deshalb dreieinhalb Bindungslaengen auseinander. Wieder art="inter".
t.schub(Atom(f4, 1), Atom(f4, 7), elektronen=1, kette="D", art="inter")
t.schub(Bindung(f4, 7, 8), Atom(f4, 8), elektronen=1, kette="D")
# Die Nummer des C8 steht jetzt darueber statt darunter: unter der Kette laeuft
# der Bogen von C8 nach C12, und dort stand vorher genau diese Beschriftung.
# Die Nummer des C12 steht senkrecht unter ihrem Atom. Schraeg nach rechts unten
# (40 Grad) stand sie genau unter dem *C13* und benannte damit im Bild das
# Nachbaratom - ausgerechnet die beiden, um die dieser Schritt geht. Das C12 ist
# ein Tal der Kette: senkrecht darunter ist viel Platz, und beide Nachbarn liegen
# oben, also ist die Zuordnung hier eindeutig.
t.atomnummer(f4, 1, "C8", winkel=250, abstand=22)
t.atomnummer(f4, 7, "C12", winkel=90, abstand=22)
t.text(500, 706, "&#9316; C8 greift C12 an", size=11, anchor="middle", gewicht=700, farbe=R)
t.unterschrift(f4, "der Fünfring schließt sich, das Radikal",
               "wandert allylisch nach C13 bis C15", abstand=34)

t.reaktionspfeil(638, 762, 698)
t.text(668, 748, "+ O&#8322;", size=10.5, anchor="middle", gewicht=700, farbe=E)
# Zwischen Peroxylradikal und fertigem Hydroperoxid fehlte ein Wasserstoffatom.
# Es kommt von Tyr385; damit entsteht das Tyrosylradikal neu und die Kette laeuft weiter.
t.text(668, 786, "dann H von Tyr385", size=10, anchor="middle", farbe=R)
t.text(668, 799, "die Kette schließt sich", size=10, anchor="middle", farbe=G)

f5 = t.mol(r"*C1C2CC(OO2)C1/C=C/C(OO)*", 832, 762, labels={0: "C7", 13: "C16"},
           kern=KETTE, name="PGG2-Kern")
# Um das C15 herum ist es eng: links oben die Doppelbindung, links unten die
# Hydroperoxidgruppe, rechts das C16. Nach links unten (130 Grad) stiess die
# Nummer an das O der O-OH-Gruppe - die beiden Kaesten beruehrten sich, im Bild
# stand da "C15O&#8722;OH" wie eine einzige Formel. Bleibt die Luecke nach oben,
# zwischen den Bindungen zum C14 und zum C16; dort ist das C15 auch das naechste
# Atom.
t.atomnummer(f5, 10, "C15", winkel=-75, abstand=15)
t.text(832, 688, "&#9317; Sauerstoff an C15", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.unterschrift(f5, "PGG&#8322;: Bicyclus aus Endoperoxid und Fünfring,",
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
t.text(528, 985, "Zentren. Deshalb kann Paracetamol das eine treffen.", size=12.5)

# ===================================================== ZONE D · Arzneistoffe
t.zone(1046, "D · WO DIE ARZNEISTOFFE ANSETZEN")

t.text(20, 1080, "Acetylsalicylsäure: kovalent", size=13, gewicht=700, farbe=R)
t.text(20, 1104, "Der Zugangskanal zum aktiven Zentrum wird von Ser530 verengt.", size=12.5)
t.text(20, 1123, "Aspirin überträgt seinen Acetylrest auf dessen Hydroxylgruppe und", size=12.5)
t.text(20, 1142, "versperrt den Kanal dauerhaft. In COX-2 ist der Kanal weiter: Das", size=12.5)
t.text(20, 1161, "acetylierte Enzym bleibt teilaktiv und bildet 15-<tspan font-style='italic'>R</tspan>-HETE,",
       size=12.5)
t.text(20, 1180, "aus dem die entzündungsauflösenden Aspirin-getriggerten Lipoxine", size=12.5)
t.text(20, 1199, "entstehen.", size=12.5)
t.text(20, 1226, "Alle übrigen NSAR binden nichtkovalent im selben Kanal und wirken", size=12, farbe=G)
t.text(20, 1245, "daher reversibel und konzentrationsabhängig.", size=12, farbe=G)

t.text(530, 1080, "Coxibe: eine Aminosäure entscheidet", size=13, gewicht=700, farbe=R)
t.text(530, 1104, "An Position 523 trägt COX-1 ein Isoleucin, COX-2 ein kleineres", size=12.5)
t.text(530, 1123, "Valin. Dadurch öffnet sich in COX-2 eine seitliche Tasche, in die", size=12.5)
t.text(530, 1142, "der Sulfonamid- oder Methylsulfonrest der Coxibe hineinreicht.", size=12.5)
t.text(530, 1161, "In COX-1 versperrt das Isoleucin sie.", size=12.5)
t.text(530, 1188, "Damit beruht die Selektivität nicht auf der Affinität zum", size=12, farbe=G)
t.text(530, 1207, "katalytischen Zentrum, sondern auf der Passform einer Neben-", size=12, farbe=G)
t.text(530, 1226, "tasche, ein Lehrbeispiel für strukturbasiertes Wirkstoffdesign.", size=12, farbe=G)

t.kasten(20, 1274, 960, 76, fill="var(--drug-bg)", stroke=R)
t.text(38, 1296, "DIE PRÜFUNGSFRAGE, DIE SICH AUS DER TAFEL BEANTWORTEN LÄSST", size=11,
       gewicht=700, farbe=R)
t.text(38, 1318, "Warum wirkt niedrig dosierte Acetylsalicylsäure im Thrombozyten endgültig? Weil "
                 "die Acetylierung kovalent ist und der kernlose Thrombozyt kein", size=12.5)
t.text(38, 1337, "neues Enzym bilden kann. Das Endothel hat einen Kern und synthetisiert seine "
                 "COX-2 nach. Daraus folgt die Selektivität der niedrigen Dosis.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Der Mechanismus der Cyclooxygenase in vier Zonen. Zone A: Das Peroxidase-Haem mit "
    "proximalem Histidin wird von einem Hydroperoxid zu Compound eins oxidiert, wobei der "
    "zugehoerige Alkohol frei wird; Compound eins abstrahiert mit Fischhakenpfeilen das "
    "Wasserstoffatom der phenolischen Hydroxylgruppe von "
    "Tyrosin 385, es entsteht das Tyrosylradikal. Zone B: Das Tyrosylradikal abstrahiert das "
    "13-pro-S-Wasserstoffatom der Arachidonsaeure, gezeigt am Ausschnitt C7 bis C16; das "
    "Radikal delokalisiert ueber C11 bis C15; "
    "Sauerstoff addiert an C11 zum Peroxylradikal. Zone C: Das Peroxylradikal greift C9 an und "
    "bildet die Endoperoxidbruecke, wobei das Radikal an C8 zurueckbleibt; C8 greift C12 an und "
    "schliesst den Fuenfring, das Radikal wandert allylisch nach C13 bis C15; ein zweites "
    "Sauerstoffmolekuel addiert an C15, und das entstandene Peroxylradikal holt sich das "
    "Wasserstoffatom von Tyrosin 385 zurueck. Damit ist die Radikalkette geschlossen und der "
    "Bicyclus PGG2 fertig. Zone D nennt die "
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

mech.speichern("m12", t.svg(ARIA), t)
