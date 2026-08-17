# -*- coding: utf-8 -*-
"""
M-16 · Cobalamin, gebaut mit mech.py.

Die Tafel lebt von einem einzigen Gegensatz: dieselbe Kohlenstoff-Cobalt-Bindung,
einmal heterolytisch, einmal homolytisch gespalten. Zone A stellt beide Fassungen
nebeneinander - links ein Elektronenpaarpfeil, rechts zwei Fischhaken.

Alle elf Pfeile sind in der neuen Pfeilsprache angemeldet: schub(quelle, ziel)
nennt nur, welche Elektronen wohin gehen; Bauchseite, Oeffnungswinkel und
Ankerlage sucht der Solver in mech_schub.py, gemessen wird gegen mech_regeln.py.

Zwei Leitgerueste halten die wiederkehrenden Geruste fest (mech_kerne.eigener):
AS legt Homocystein und Methionin uebereinander - der Schwefel steht in beiden
links, sodass man die angekommene Methylgruppe sofort findet -, MM legt
Methylmalonyl-CoA und das Substratradikal uebereinander, mit der Methylgruppe
oben und dem Thioester rechts. Ohne das drehte RDKit jede Stufe fuer sich, und
der Leser muesste vor dem Vergleich erst jedes Bild neu einnorden.

Zwei Stellen sind gegenueber dem alten Stand anders besetzt:

  - Bei der Wanderung der Thioestergruppe zeigt der zweite Fischhaken nicht mehr
    auf den Nachbarkohlenstoff, an dem das Radikal zurueckbleibt, sondern auf
    die werdende Bindung. Ein Kohlenstoff mit drei gezeichneten Bindungen laesst
    fuer einen Pfeil, der auf ihn selbst zurueckzeigt, keinen Platz (Begruendung
    bei Zone C). Beide Haken laufen damit auf die neue Bindung zu, wie schon bei
    der Abstraktion darueber; wohin das Radikal geht, sagt die Bildunterschrift.
  - Das Bruchstueck des 5-Methyl-THF steht unter einer festen Drehung statt
    unter zeige=, weil nur wenige Lagen den Abgangspfeil ueberhaupt zulassen.
"""
import os
import re
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

t = mech.Tafel(1000, 1390)

# --------------------------------------------------------------- Leitgerueste
# Der Aminosaeurerest von Homocystein und Methionin. Der Schwefel zeigt nach
# links, also dorthin, woher die Methylgruppe kommt; das Rueckgrat laeuft nach
# rechts, die Aminosaeurefunktion steht rechts aussen.
AS = mech_kerne.eigener(
    "homocystein", "CSCCC(N)C(=O)O",
    muster="[#16]~[#6]~[#6]~[#6](~[#7])~[#6](~[#8])~[#8]",
    ring=[1, 2, 3, 4, 6], leit=1, folge=2, winkel=175.0)

# Methylmalonyl-CoA und das Substratradikal. Die Methylgruppe steht oben - dort
# holt das Adenosylradikal das Wasserstoffatom ab -, das Carboxylat unten links,
# der Thioester unten rechts. Genau zwischen diesen beiden wandert die Gruppe.
MM = mech_kerne.eigener(
    "methylmalonyl", "CC(C(=O)O)C(=O)C",
    muster="[#6]~[#6](~[#6](~[#8])~[#8])~[#6]~[#8]",
    ring=[0, 1, 2, 5], leit=0, folge=5, winkel=95.0)


def zentrum(x, y, metall, axial=(), unten="DMB", **kw):
    """Wie t.zentrum(), meldet dem Pfeil-Solver aber zusaetzlich, wo die Tinte
    liegt.

    Zentrum() legt seine Striche und Beschriftungen unmittelbar in die
    Zeichenliste; die Tintenkarte des Solvers kennt nur Molekuele und
    t.sperren. Ohne diesen Nachtrag zoege der Solver einen Bogen quer durch das
    Metallsymbol oder laengs auf der Cobalt-Kohlenstoff-Bindung, ohne es zu
    bemerken - und genau an dieser Bindung setzen vier der elf Pfeile an.
    """
    z = t.zentrum(x, y, metall, axial=list(axial), unten=unten, **kw)
    s = z.schritt

    def wort(mx, my, txt, size):
        w = len(re.sub(r"&#?\w+;", "x", txt)) * size * 0.52
        t.sperren.append((mx - w / 2.0, my - size * 0.76,
                          mx + w / 2.0, my + size * 0.22))

    wort(x, y + 4.5, metall, 12.5)
    for i, lab in enumerate(axial):
        wort(x, y - s * (i + 1) + 4.5, lab, 12.5)
        t.sperren.append((x - 1.2, y - s * (i + 1) + 9, x + 1.2, y - s * i - 8))
    if unten:
        wort(x, y + 33, unten, 11)
        t.sperren.append((x - 1.2, y + 8, x + 1.2, y + 20))
    if kw.get("ebene", True):
        for sg in (-1, 1):
            t.sperren.append((x + sg * 26 if sg < 0 else x + 14, y - 5,
                              x - 14 if sg < 0 else x + 26, y + 5))
    return z


# ===================================================== ZONE A · der Gegensatz
t.zone(24, "A · DIESELBE BINDUNG, ZWEI ARTEN SIE ZU BRECHEN")
t.text(20, 54, "Die C&#8722;Co-Bindung ist schwach: beim Adenosylcobalamin rund 30 kcal/mol. Wohin "
               "ihre beiden Elektronen gehen, entscheidet über den Reaktionstyp.", size=12.5)

# ---- links: heterolytisch
zh = zentrum(230, 158, "Co(III)", axial=["CH&#8323;"], unten="DMB", schritt=48,
             name="Methylcobalamin")
t.schub(zh.axb(-1, 0), zh.fe(winkel=205, abstand=30), art="intra")
t.text(230, 84, "Methylcobalamin", size=12, anchor="middle", gewicht=700)
t.text(302, 132, "beide Elektronen", size=10.5, farbe=W, gewicht=700)
t.text(302, 146, "gehen ans Cobalt", size=10.5, farbe=W, gewicht=700)
t.text(230, 214, "heterolytisch", size=12.5, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(230, 228, 230, 270)

zh2 = zentrum(230, 322, "Co(I)", axial=[], unten="DMB", name="Co(I)")
t.text(230, 376, "Co(I): eines der stärksten Nucleophile", size=11, anchor="middle",
       gewicht=700, farbe=E)
t.text(230, 392, "der gesamten Biochemie", size=10.5, anchor="middle", farbe=G)
t.text(230, 412, "die Methylgruppe geht als CH&#8323;&#8314; weiter", size=10.5,
       anchor="middle", farbe=G)

# ---- rechts: homolytisch
# Homolyse: die beiden Fischhaken teilen sich den Schwanz an der Bindung und
# zeigen nach entgegengesetzten Seiten. Kopf an Schwanz ist hier begrifflich
# unmoeglich, deshalb bilden sie keine Kette.
zr = zentrum(730, 158, "Co(III)", axial=["Ado"], unten="DMB", schritt=48,
             name="Adenosylcobalamin")
t.schub(zr.axb(-1, 0), zr.fe(winkel=205, abstand=30), elektronen=1,
        art="intra")
t.schub(zr.axb(-1, 0), zr.ax(0, winkel=20, abstand=21), elektronen=1,
        art="intra")
t.text(730, 84, "Adenosylcobalamin", size=12, anchor="middle", gewicht=700)
t.text(802, 132, "je ein Elektron", size=10.5, farbe=R, gewicht=700)
t.text(802, 146, "nach jeder Seite", size=10.5, farbe=R, gewicht=700)
t.text(730, 214, "homolytisch", size=12.5, anchor="middle", gewicht=700, farbe=R)

t.reaktionspfeil(730, 228, 730, 270)

zr2 = zentrum(730, 322, "Co(II)", axial=[], unten="DMB", name="Co(II)")
t.text(730, 376, "Co(II), daneben das freie", size=11, anchor="middle",
       gewicht=700, farbe=R)
t.text(730, 392, "5&#8242;-Desoxyadenosyl-Radikal", size=10.5, anchor="middle", farbe=G)
t.text(730, 412, "das Enzym beschleunigt die Homolyse um 10&#185;&#178;", size=10.5,
       anchor="middle", farbe=G)

t.linie(480, 96, 480, 420, farbe="currentColor", breite=1, strich="4 4", z=0)

# ===================================================== ZONE B · Methylcobalamin
t.zone(456, "B · DER HETEROLYTISCHE WEG: METHIONINSYNTHASE")
t.text(20, 486, "Das Co(I) holt sich die Methylgruppe vom 5-Methyl-Tetrahydrofolat und gibt sie "
                "an Homocystein weiter. Zweimal derselbe "
                "S<tspan baseline-shift='sub' font-size='8.5'>N</tspan>2-Schritt am Methyl.",
       size=12.5)
t.text(20, 505, "Damit das Tetrahydrofolat als neutrales Molekül abgehen kann, muss sein N5 vorher "
                "protoniert werden.", size=12.5)

zb1 = zentrum(118, 590, "Co(I)", axial=[], unten="DMB", name="Co(I)")
lp_co = t.paar(118, 566, 270, "Cobalt(I)")
# Die Drehung steht hier als Zahl und nicht als zeige={...}, und zwar aus einem
# Grund, der erst der Solver zutage foerdert: Am dreifach substituierten
# Stickstoff sind alle drei Winkelluecken 120 Grad breit, und das abgehende Paar
# muss in die Luecke *gegenueber* der brechenden Bindung. Der Bogen dorthin
# faedelt zwischen den beiden Ringbindungen hindurch, und wie viel Platz er dabei
# hat, haengt an den achsenparallelen Glyphenrechtecken von "C4a" und "C6" - also
# an der Drehung. Durchgerechnet in Halbgradschritten: mit dem Methyl nach links
# traegt nur das schmale Band von 146 bis 155 Grad, und 146 Grad hat davon den
# groessten Freiraum (0,36 L statt 0,25 L am anderen Ende).
mthf = t.mol("*[NH+](*)C", 236, 574, labels={0: "C4a", 2: "C6"},
             rotate=146.0, name="5-Methyl-THF")
# Ein Schritt, zwei Pfeile: das Paar des Co(I) bildet die neue Bindung zum
# Methyl, das alte Bindungspaar geht auf den Stickstoff zurueck.
t.schub(lp_co, Atom(mthf, 3), kette="B1")
t.schub(Bindung(mthf, 3, 1), Paar(mthf, 1), kette="B1")
t.unterschrift(mthf, "5-Methyl-THF: nur das protonierte N5", "mit seinen zwei Nachbarn")
t.text(118, 646, "Co(I)", size=11, anchor="middle", gewicht=700, farbe=E)

t.reaktionspfeil(320, 578, 400)
t.text(360, 568, "&#8722; THF", size=10.5, anchor="middle", gewicht=700, farbe=G)

zb2 = zentrum(520, 586, "Co(III)", axial=["CH&#8323;"], unten="DMB", schritt=46,
              name="Methylcobalamin")
t.text(520, 650, "Methylcobalamin", size=11, anchor="middle", gewicht=700, farbe=W)

hcy = t.mol("[S-]CC[C@H]([NH3+])C(=O)[O-]", 640, 574, kern=AS, name="Homocystein")
# Derselbe Schritt noch einmal, jetzt mit dem Thiolat als Nucleophil. Die beiden
# Pfeile gehoeren zusammen, sind hier aber nicht als Kette angemeldet: sie treffen
# sich an der Methylgruppe des Cobalts, und fuer ein gemeinsames Atom laesst die
# Pruefung 1,45 L zu. Erkennen kann sie das gemeinsame Atom nur an Molekuel-
# ankern; ein Zentrum() liefert feste Punkte, und fuer die gilt das enge Fenster
# 0,95 L, das zwei Pfeile am selben Metall-Ligand-Paar nie einhalten koennen.
#
# Der Endpunkt liegt *ueber* der Methylgruppe, nicht daneben: das Cobalt geht
# nach unten weg, das Thiolat kommt von oben herein, und damit steht der
# Angriff dem Abgang gegenueber, wie es ein S_N2 verlangt. Die Lage ist eng
# gewaehlt - mit winkel=68 endete der Pfeil auf halber Hoehe zwischen Methyl
# und Cobalt, zeigte auf keines von beiden und liess offen, was hier angegriffen
# wird.
t.schub(Paar(hcy, 0), zb2.ax(0, winkel=330, abstand=15))
t.schub(zb2.axb(-1, 0), zb2.fe(winkel=205, abstand=30), art="intra")
t.unterschrift(hcy, "Homocystein: das Thiolat greift an")

t.reaktionspfeil(730, 578, 810)

met = t.mol("CSCC[C@H]([NH3+])C(=O)[O-]", 880, 574, kern=AS, name="Methionin")
t.unterschrift(met, "Methionin: das Cobalt steht", "wieder als Co(I) bereit")

# ===================================================== ZONE C · Adenosylcobalamin
t.zone(700, "C · DER HOMOLYTISCHE WEG: METHYLMALONYL-CoA-MUTASE")
t.text(20, 730, "Das Radikal holt sich ein Wasserstoffatom vom Substrat. Danach wandert die "
                "Thioestergruppe an den Nachbarkohlenstoff, und das H kommt zurück.", size=12.5)

# Substrat der Mutase ist (2R)-Methylmalonyl-CoA; das (2S)-Epimer aus der
# Propionyl-CoA-Carboxylase dreht erst die Epimerase um. [C@H] gibt genau diese
# raeumliche Anordnung wieder. Achtung beim Nachrechnen: rdCIPLabeler meldet hier
# "S", weil das Dummy-Atom * niedriger rangiert als das Schwefelatom des echten
# SCoA-Restes und damit die Prioritaeten 1 und 2 vertauscht.
mm = t.mol("C[C@H](C(=O)[O-])C(=O)*", 176, 838, labels={7: "SCoA"},
           wasserstoff=[0], kern=MM, name="Methylmalonyl-CoA")
h0 = mm.h_index[0]
ado = t.marke(118, 784, "Desoxyadenosyl-Radikal")
t.text(118, 768, "Ado&#8226;", size=11, anchor="middle", gewicht=700, farbe=R)
# Abstraktion in der ueblichen Kurzschreibweise: das Wasserstoffatom geht mit
# einem der beiden Bindungselektronen zum Radikal, das andere bleibt am
# Kohlenstoff zurueck. Beide Haken haengen am selben Schwanz, koennen also keine
# Kette bilden. Der dritte Haken - das ungepaarte Elektron des Adenosylradikals,
# das die neue Bindung mitbildet - haette daneben keinen Platz mehr: die drei
# Boegen kaemen sich auf 0,18 L nahe, gefordert sind 0,25 L.
t.schub(Bindung(mm, 0, h0), ado, elektronen=1)
t.schub(Bindung(mm, 0, h0), Atom(mm, 0), elektronen=1)
t.unterschrift(mm, "(2R)-Methylmalonyl-CoA: abstrahiert", "wird ein H der Methylgruppe")

t.reaktionspfeil(300, 842, 362)

rad = t.mol("[CH2]C(C(=O)[O-])C(=O)*", 500, 838, labels={7: "SCoA"},
            kern=MM, name="Substratradikal")
# Den Radikalpunkt zeichnet RDKit selbst - das Atom ist im SMILES als [CH2]
# codiert. Deshalb steht hier Atom() und nicht Elektron(): Elektron() setzte
# einen zweiten Punkt daneben.
#
# Zwei Haken, und beide zielen auf dieselbe werdende Bindung - genau die
# Buchfuehrung, die auch die Abstraktion oben verwendet: der eine bringt das
# ungepaarte Elektron des Radikals an den Thioesterkohlenstoff, der andere holt
# aus der brechenden Bindung C2-C(=O)SCoA das zweite Elektron der neuen Bindung
# heran. Beide Aussagen stimmen fuer sich.
#
# Der dritte Haken - das Elektron, das am C2 als neues Radikal zurueckbleibt -
# ist nicht gezeichnet, weil er sich nicht zeichnen laesst. Das C2 traegt drei
# Bindungen; die einzige von der Quellbindung aus erreichbare Winkelluecke liegt
# unmittelbar daneben, und die Sehne wird dort geometrisch nie laenger als
# 0,45 L, waehrend die Pruefung mindestens 0,60 L verlangt. Die Luecke gegenueber
# waere lang genug, aber jeder Bogen dorthin kreuzt eine der beiden anderen
# Bindungen. Durchgerechnet an 60 Drehungen und vier Zieltypen: kein Treffer.
# Wohin das Radikal wandert, sagt deshalb die Bildunterschrift. Der Haken darf
# aber nicht ersatzweise auf das Radikalzentrum zeigen - das hiesse, das
# Bindungspaar wanderte zum CH2 hinueber, und dann ginge die Elektronenbilanz
# an beiden Kohlenstoffen nicht mehr auf.
#
# Reihenfolge: erst der Haken des Radikals, dann der aus der brechenden Bindung.
# Umgekehrt legt der Solver den ersten Bogen dorthin, wo der zweite Platz
# braucht, und die beiden kommen sich auf 0,24 L nahe.
t.schub(Atom(rad, 0), Atom(rad, 5), elektronen=1)
# Der zweite Haken - ein Elektron aus der brechenden Bindung C2-C(O) in die
# werdende Bindung - laesst sich hier nicht zeichnen, und zwar aus einem Grund,
# der in der Struktur liegt und nicht im Zeichner. Die werdende Bindung
# verbindet das CH2 mit dem Thioesterkohlenstoff; ihre Mitte liegt bei
# (508, 824) und damit elf Pixel neben dem C2, also mitten im Dreieck aus C2,
# CH2 und Carbonyl. Jeder Bogen dorthin kreuzt eine der drei Bindungen; auf der
# freien Aussenseite bleiben zwischen Quell- und Zielanker nur 0,41
# Bindungslaengen, zu wenig fuer Kopf und Schaft. Nachgerechnet ueber 2568
# Kandidatenlagen und zusaetzlich mit vergroessertem Ausschnitt (28 und 32 px):
# kein Treffer. Solange Ausgangsstoff und Produkt nebeneinander stehen, ist die
# werdende Bindung eben noch nicht gezeichnet, und ein Pfeil, der auf sie zeigt,
# muss durch das Molekuel. Wohin dieses Elektron geht, sagt die Bildunterschrift.
t.unterschrift(rad, "die Thioestergruppe wandert an das Radikalzentrum.",
               "Das Radikal bleibt am Nachbarn zurück.")

t.reaktionspfeil(624, 842, 686)
t.text(655, 832, "+ H", size=10.5, anchor="middle", gewicht=700, farbe=G)

suc = t.mol("[O-]C(=O)CCC(=O)*", 832, 838, labels={7: "SCoA"},
            zeige={0: "links"}, name="Succinyl-CoA")
t.unterschrift(suc, "Succinyl-CoA: der Eingang", "in den Citratzyklus (§ 3.2)")

# ===================================================== ZONE D · Klinik
t.zone(958, "D · WARUM DER MANGEL ZWEI MARKER HAT")

t.kasten(20, 990, 470, 138, fill="var(--enzym-bg)", stroke=E)
t.text(38, 1012, "METHIONINSYNTHASE FÄLLT AUS", size=11, gewicht=700, farbe=E)
t.text(38, 1034, "Homocystein steigt.", size=12.5)
t.text(38, 1053, "Das Folat staut sich als 5-Methyl-THF (die", size=12.5)
t.text(38, 1072, "Methylfalle). Folge: megaloblastäre Anämie.", size=12.5)
t.text(38, 1095, "Dasselbe Bild entsteht bei reinem Folatmangel;", size=12, farbe=G)
t.text(38, 1114, "dieser Marker trennt also nicht.", size=12, farbe=G)

t.kasten(510, 990, 470, 138, fill="var(--drug-bg)", stroke=R)
t.text(528, 1012, "MUTASE FÄLLT AUS", size=11, gewicht=700, farbe=R)
t.text(528, 1034, "Methylmalonsäure steigt.", size=12.5)
t.text(528, 1053, "Diese Reaktion braucht kein Folat, deshalb steigt", size=12.5)
t.text(528, 1072, "der Wert nur bei B&#8321;&#8322;-Mangel.", size=12.5)
t.text(528, 1095, "Damit ist die Methylmalonsäure der spezifische", size=12, farbe=G)
t.text(528, 1114, "Parameter. Ihn misst man vor jeder Substitution.", size=12, farbe=G)

t.kasten(20, 1152, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1174, "LACHGAS TRIFFT NUR EINE DER BEIDEN FORMEN", size=11, gewicht=700, farbe=W)
t.text(38, 1196, "Distickstoffmonoxid oxidiert das Co(I) der Methioninsynthase irreversibel. Die "
                 "Mutase läuft über Co(II) und bleibt zunächst unberührt.", size=12.5)
t.text(38, 1215, "Deshalb steigt bei Lachgasschäden das Homocystein früher und deutlicher als die "
                 "Methylmalonsäure. Dieses Befundmuster lässt sich aus Zone A ablesen.", size=12.5)

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
    "jeder Seite ziehen, sodass Cobalt zwei und das Desoxyadenosyl-Radikal entstehen. Zone B "
    "zeigt den heterolytischen Weg der Methioninsynthase: Cobalt eins greift die Methylgruppe "
    "des am Stickstoff fuenf protonierten 5-Methyl-Tetrahydrofolats an, danach greift das "
    "Thiolat des Homocysteins die "
    "Methylgruppe am Cobalt an, es entsteht Methionin. Zone C zeigt den homolytischen Weg der "
    "Methylmalonyl-CoA-Mutase: Das Desoxyadenosyl-Radikal abstrahiert ein Wasserstoffatom der "
    "Methylgruppe, die Thioestergruppe wandert an den Nachbarkohlenstoff, das Wasserstoffatom "
    "kehrt zurueck, es entsteht Succinyl-CoA. Zone D erklaert, warum Homocystein und "
    "Methylmalonsaeure zwei verschiedene Marker sind und warum Lachgas nur die Cobalt-eins-Form "
    "trifft."
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

mech.speichern("m16", t.svg(ARIA), t)
