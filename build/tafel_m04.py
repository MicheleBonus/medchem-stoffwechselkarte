# -*- coding: utf-8 -*-
"""
M-04 · Tetrahydrofolat, gebaut mit mech.py.

Gezeichnet wird nur der Ausschnitt N5 bis N10 - nur dort sitzt die C1-Einheit, und
nur dort unterscheiden sich die Transportformen. Es sind vier Formen, aber nur
drei Oxidationsstufen: Methenyl und Formyl stehen beide auf der Ameisensaeure-
stufe. Zone B fuehrt den Schritt aus, an dem 5-Fluoruracil angreift.

Zur neuen Pfeilsprache
----------------------
KERN legt alle sieben Strukturen mit dem Ausschnitt N5-N10 auf dieselbe Lage.
Vorher nordete RDKit jede Stufe einzeln ein, und die Vergleichsreihe der Zone A
verglich Drehungen statt Oxidationsstufen.

Von den vier frueheren Pfeilen sind zwei gezeichnet, und zwar die beiden, die eine
neue Bindung machen. Die beiden anderen enden an einem dreifach substituierten
Stickstoff - das Bindungspaar C1-N10 auf dem N10, das pi-Paar C1=N5 auf dem N5 -
und fuer die laesst sich kein regelkonformer Bogen legen: An einem Atom mit drei
Substituenten liegt jede der drei Luecken 60 Grad neben einer seiner Bindungen,
und die Spitze steht dort entweder so dicht an der Quellbindung, dass der Bauch
auf ihr laege, oder hinter einer der beiden anderen Bindungen. Das gilt bei jeder
Drehung und bei jeder Bindungslaenge; nachgerechnet mit einem freistehenden
Molekuel auf leerer Tafel. Beide Aussagen stehen deshalb im Text der Zone B, so
wie es M-01 mit seinem letzten Chinoid-Schritt haelt.

Der Mechanismus-Ausschnitt ist mit 23 px Bindungslaenge gezeichnet und nicht mehr
mit 26 bzw. 31: Die Strichbreite, die RDKit fuer die Bindungen setzt, waechst
nicht mit der Bindungslaenge, und ab etwa 23 px wird der Pfeilkopf breiter als die
3,6 Strichbreiten, die K4 zulaesst.
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

# Der Ausschnitt N5 bis N10 kommt in sieben Strukturen dieser Tafel vor - in den
# vier Transportformen der Zone A, im Methylen-THF und im Iminium der Zone B und
# im ternaeren Komplex. Ohne feste Lage einnordete RDKit jede einzeln, und die
# Vergleichsreihe der Zone A verglich dann Drehungen statt Oxidationsstufen.
# Das Muster fasst die Kette C4a-N5-C6(-C7)-C9-N10; die drei Ansatzstellen des
# uebrigen Molekuels sind in jeder Stufe Dummy-Atome, und genau das macht den
# Treffer eindeutig - ohne [#0] koennte die Methylenbruecke selbst als C4a
# durchgehen.
KERN = mech_kerne.eigener(
    "thf-n5-n10", "*N1C(*)CN(*)C1",
    muster="[#0]~[#7]~[#6](~[#0])~[#6]~[#7]",
    ring=[1, 2, 4, 5, 7], leit=1, folge=2, winkel=120.0)

t = mech.Tafel(1000, 1424)

# ===================================================== ZONE A · vier Stufen
t.zone(24, "A · VIER TRANSPORTFORMEN AUF DREI OXIDATIONSSTUFEN")
t.text(20, 54, "Gezeichnet ist nur der Ausschnitt N5 bis N10. Der Rest des Moleküls "
               "(Pterinring, <em>p</em>-Aminobenzoat, Glutamatschwanz) ändert sich "
               "nie.".replace("<em>", "").replace("</em>", ""), size=12.5)
t.text(20, 74, "Vier Transportformen, aber nur drei Oxidationsstufen: Methenyl und Formyl "
               "liegen beide auf der Ameisensäure-Stufe, denn die Cyclohydrolase zwischen "
               "ihnen bewegt keine Elektronen.", size=12.5)

STUFEN = [
    (140, "*N(C)C(*)CN*", {0: "C4a", 4: "C7", 7: "Aryl"},
     "5-Methyl-THF", "nur an N5, Sackgasse", E),
    (380, "*N1C(*)CN(*)C1", {0: "C4a", 3: "C7", 6: "Aryl"},
     "5,10-Methylen-THF", "Brücke, Fünfring", W),
    (620, "*N1C(*)C[N+](*)=C1", {0: "C4a", 3: "C7", 6: "Aryl"},
     "5,10-Methenyl-THF", "kationisch, Amidinium", "currentColor"),
    (860, "*NC(*)CN(C=O)*", {0: "C4a", 3: "C7", 8: "Aryl"},
     "10-Formyl-THF", "nur an N10", "currentColor"),
]
mole = []
for x, smi, lab, titel, note, farbe in STUFEN:
    m = mech.Molekuel(smi, x, 190, labels=lab, kern=KERN, name=titel)
    t.mole.append(m)
    mole.append((m, titel, note, farbe))

# Vier Formen nebeneinander sind nur dann eine Reihe, wenn auch die Schrift eine
# Linie haelt. ueberschrift und unterschrift messen vom Rand des einzelnen
# Molekuels, und das 10-Formyl-THF reicht oben wie unten weiter als die drei
# anderen: die Marke C4a steht dort ueber der Formel, die Formylgruppe haengt
# darunter. Der Abstand wird deshalb je Molekuel so gerechnet, dass alle vier
# Titel und alle vier Unterschriften auf je einer Hoehe stehen.
OBEN = min(m.rand()[1] for m, _, _, _ in mole) - 30
UNTEN = max(m.rand()[3] for m, _, _, _ in mole) + 24
for m, titel, note, farbe in mole:
    t.ueberschrift(m, titel, farbe=farbe, abstand=m.rand()[1] - OBEN)
    t.unterschrift(m, note, abstand=UNTEN - m.rand()[3])

t.linie(60, 300, 940, 300, farbe="currentColor", breite=1, z=0)
# Methyl und Methylen bekommen je einen Punkt. Methenyl und Formyl teilen sich
# eine Stufe; deshalb steht dort ein Balken ueber beiden statt zweier Punkte.
for x, farbe in ((140, STUFEN[0][5]), (380, STUFEN[1][5])):
    t.stuecke.append((1, "<circle cx='%.1f' cy='300' r='5' fill='%s'/>" % (x, farbe)))
t.stuecke.append((1, "<rect x='614' y='296.5' width='252' height='7' rx='3.5' "
                     "fill='currentColor'/>"))
t.text(140, 320, "Methanol-Stufe (&#8722;II)", size=10.5, anchor="middle", farbe=G)
t.text(380, 320, "Formaldehyd-Stufe (0)", size=10.5, anchor="middle", farbe=G)
t.text(740, 320, "Ameisensäure-Stufe (+II)", size=10.5, anchor="middle", farbe=G)
t.text(22, 294, "reduziert", size=10, farbe=G)
t.text(958, 294, "oxidiert", size=10, anchor="end", farbe=G)

COSUB = [(440, 560, "NADP&#8314; &#8594; NADPH"), (680, 800, "+ H&#8322;O &#8722; H&#8314;")]
for x0, x1, cosub in COSUB:
    t.reaktionspfeil(x0, 274, x1)
    t.reaktionspfeil(x1, 288, x0)
    t.text((x0 + x1) / 2, 252, cosub, size=10, anchor="middle", gewicht=700, farbe=C)
    t.text((x0 + x1) / 2, 266, "reversibel", size=10, anchor="middle", farbe=G)

t.reaktionspfeil(320, 288, 200, farbe=W)
t.text(260, 252, "+ NADPH + H&#8314;", size=10, anchor="middle", gewicht=700, farbe=C)
t.text(260, 266, "MTHFR", size=11, anchor="middle", gewicht=700, farbe=W, mono=True)
t.text(260, 280, "irreversibel, keine Rückkehr", size=10.5, anchor="middle",
       gewicht=700, farbe=W)

t.kasten(20, 336, 470, 58, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 358, "Woher die C&#8321;-Einheit kommt: L-Serin liefert über die Serin-Hydroxymethyl-",
       size=12.5)
t.text(38, 377, "transferase (PLP, Tafel M-01) die Methylen-Stufe.", size=12.5)

t.kasten(510, 336, 470, 58, fill="var(--surface-2)")
t.text(528, 358, "Wohin sie geht: Methylen in die Thymidylatsynthese, Formyl in den Purinring,",
       size=12.5)
t.text(528, 377, "Methyl ausschließlich zur Methioninsynthase (Tafel M-16).", size=12.5)

# ===================================================== ZONE B · Thymidylatsynthase
t.zone(428, "B · DIE THYMIDYLATSYNTHASE: DER SCHRITT, AN DEM 5-FLUORURACIL ANGREIFT")
t.text(20, 458, "Das Methylen-THF ist kein Elektrophil, solange der Fünfring geschlossen ist. "
                "Erst die Ringöffnung zum Iminium macht es angreifbar.", size=12.5)
t.text(20, 477, "Der Ausschnitt ist gegenüber der Vergleichsreihe der Zone A vergrößert. Von "
                "jedem der beiden Schritte ist der Pfeil gezeichnet, der die neue",
       size=12.5)
t.text(20, 496, "Bindung macht; den zweiten muss man mitdenken. Beim Ringöffnen geht das "
                "Bindungspaar C&#8321;&#8211;N10 auf das N10, beim Angriff das π-Paar "
                "der Bindung", size=12.5)
t.text(20, 515, "C&#8321;=N5 auf das N5. Neben einem dreifach substituierten Stickstoff "
                "bleibt für dessen Spitze kein Platz, der die Konvention einhält.",
       size=12.5)

meth = mech.Molekuel("*N1C(*)CN(*)C1", 150, 584, labels={0: "C4a", 3: "C7", 6: "Aryl"},
                     kern=KERN, bindung=23, name="Methylen-THF")
t.mole.append(meth)
# Das freie Paar am N5 schiebt sich in die Bindung N5-C1; daraus wird die
# Doppelbindung des Iminiums. Der Schwanz sitzt am Stickstoff selbst und nicht an
# einem gezeichneten Punktpaar: das Paar stuende 0,52 Bindungslaengen vom N5 weg
# und damit so dicht neben der Bindung N5-C1, dass die Sehne unter das
# Mindestmass faellt. Regel U2 verlangt den Schwanz nur dort am Paar, wo eines
# gezeichnet ist.
t.schub(Atom(meth, 1), Bindung(meth, 1, 7))
# Der Gegenpfeil - das Bindungspaar C1-N10 geht auf das N10 - ist nicht
# gezeichnet. Am dreifach substituierten N10 liegt jede zulaessige Spitzenlage
# entweder so dicht an der Quellbindung, dass der Bauch auf ihr laege, oder hinter
# einer der beiden anderen Bindungen. Die Aussage steht im Text der Zone.
t.unterschrift(meth, "der Fünfring öffnet sich", abstand=32)

t.reaktionspfeil(250, 588, 330)
t.text(290, 578, "+ H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=G)

imin = mech.Molekuel("*[N+](=C)C(*)CN(*)*", 430, 584,
                     labels={0: "C4a", 4: "C7", 7: "Aryl", 8: "H"},
                     kern=KERN, bindung=23, name="Iminium")
t.mole.append(imin)
t.atomnummer(imin, 2, "C&#8321;", winkel=200, abstand=17, size=10, farbe=W, gewicht=700)
t.unterschrift(imin, "Iminium: jetzt ist das C&#8321; elektrophil", abstand=32)

t.kasten(560, 530, 420, 132, fill="var(--surface-2)")
t.text(578, 552, "WARUM DIESER SCHRITT DEN COFAKTOR KOSTET", size=11, gewicht=700, farbe=G)
t.text(578, 574, "Die Thymidylatsynthase ist die einzige Reaktion, bei der", size=12.5)
t.text(578, 593, "THF nicht nur die C&#8321;-Einheit liefert, sondern auch noch", size=12.5)
t.text(578, 612, "das Hydrid für deren Reduktion zur Methylgruppe.", size=12.5)
t.text(578, 635, "Der Cofaktor wird dabei zu Dihydrofolat oxidiert, und nur", size=12.5)
t.text(578, 654, "die Dihydrofolat-Reduktase bringt ihn zurück.", size=12.5)

dump = mech.Molekuel("O=C1NC(=O)N(*)C(S*)[CH-]1", 195, 768,
                     labels={6: "dRib-P", 9: "Enzym"}, zeige={10: "rechts"},
                     bindung=23, name="dUMP")
t.mole.append(dump)
t.unterschrift(dump, "dUMP, nachdem ein Cystein", "des Enzyms an C6 addiert hat", abstand=32)
# Die Marke sitzt schraeg ueber dem Carbanion. Unten rechts stand sie zwar frei,
# war aber naeher am Carbonyl C4 und an dessen Sauerstoff als an dem C5, das sie
# benennt - eine Marke, deren naechstes Atom ein anderes ist, benennt das falsche.
# Waagerecht nach rechts geht es nicht, dort stehen das freie Paar und der
# Pfeilschwanz; nach links liegt das Ringinnere, schraeg darueber das C6 mit dem
# Cystein und darunter das Carbonyl. Frei bleibt nur der Keil nach rechts oben.
t.atomnummer(dump, 10, "C5", winkel=305, abstand=17, size=10, farbe=W, gewicht=700)

imin2 = mech.Molekuel("*[N+](=C)C(*)CN(*)*", 340, 768,
                      labels={0: "C4a", 4: "C7", 7: "Aryl", 8: "H"},
                      kern=KERN, bindung=23, name="Iminium")
t.mole.append(imin2)
# Das freie Paar am C5 des dUMP bildet die Bindung zum C1 des Iminiums. Der
# Gegenpfeil - das pi-Paar der Bindung C1=N5 geht auf das N5 zurueck - steht im
# Text der Zone: am dreifach substituierten N5 hat seine Spitze keinen Platz.
t.schub(Paar(dump, 10), Atom(imin2, 2))
t.unterschrift(imin2, "C5 greift das C&#8321; an", abstand=32)

t.reaktionspfeil(425, 764, 600)

tern = mech.Molekuel("O=C1NC(=O)N(*)C(S*)C1CN(*)C(*)CN(*)*", 740, 768,
                     labels={6: "dRib-P", 9: "Enzym", 13: "C4a", 15: "C7",
                             18: "Aryl", 19: "H"},
                     kern=KERN, bindung=23,
                     name="ternärer Komplex")
t.mole.append(tern)
t.unterschrift(tern, "der kovalente ternäre Komplex aus Enzym, Substrat und Cofaktor",
               abstand=32)

# ===================================================== ZONE C · Angriffspunkte
t.zone(890, "C · VIER ARZNEISTOFFE AN EINEM ZYKLUS")
t.text(20, 920, "Zwei treffen eine Reduktase, zwei eine Synthase. Die Selektivität entsteht "
                "jedes Mal an einer anderen Stelle.", size=12.5)

ANGRIFF = [
    (20, "Sulfonamide", "Dihydropteroat-Synthase",
     ["Bakterien bauen ihr Folat selbst, der Mensch nimmt es",
      "auf. Dieses Ziel gibt es im Menschen gar nicht: das ist",
      "die sauberste Form der Selektivität."]),
    (510, "Trimethoprim", "bakterielle Dihydrofolat-Reduktase",
     ["Dieselbe Reaktion in beiden Organismen, aber die",
      "Bindetaschen unterscheiden sich in Größe und Auskleidung.",
      "Trimethoprim passt um Zehnerpotenzen besser."]),
    (20, "Methotrexat", "menschliche Dihydrofolat-Reduktase",
     ["Ein Folatanalogon mit voller Glutamatseitenkette; es wird",
      "in der Zelle polyglutamyliert und dadurch festgehalten.",
      "Keine Selektivität, deshalb Zytostatikum."]),
    (510, "5-Fluoruracil", "Thymidylatsynthase",
     ["Als FdUMP durchläuft es Zone B bis zum ternären Komplex.",
      "Das Fluor an C5 kann nicht abgespalten werden, der",
      "Komplex bleibt stehen: das Enzym ist blockiert."]),
]
for i, (x, stoff, ziel, zeilen) in enumerate(ANGRIFF):
    y = 956 + (i // 2) * 106
    t.text(x, y, stoff, size=13, gewicht=700, farbe=R)
    t.text(x, y + 19, ziel, size=11, gewicht=700, farbe=E)
    for k, z in enumerate(zeilen):
        t.text(x, y + 40 + k * 19, z, size=12)

t.kasten(20, 1170, 960, 76, fill="var(--cofaktor-bg)", stroke=C)
t.text(38, 1192, "LEUCOVORIN STEHT ZWEIMAL IM BUCH, MIT ENTGEGENGESETZTEM ZWECK", size=11,
       gewicht=700, farbe=C)
t.text(38, 1214, "Nach Methotrexat <b>rettet</b> es die gesunde Zelle, weil es als fertiges "
                 "Formyl-THF die blockierte Reduktase umgeht.".replace("<b>", "").replace("</b>", ""),
       size=12.5)
t.text(38, 1233, "Zusammen mit 5-Fluoruracil <b>verstärkt</b> es die Wirkung, weil ein Überschuss "
                 "an Methylen-THF den ternären Komplex stabilisiert.".replace("<b>", "").replace("</b>", ""),
       size=12.5)

# ===================================================== ZONE D · Methylfalle
t.zone(1278, "D · DIE METHYLFALLE")
t.text(20, 1310, "Zwei Eigenschaften des Systems ergeben zusammen eine der wichtigsten "
                 "Verknüpfungen der Vitaminlehre: Die MTHFR-Reaktion ist irreversibel, und die "
                 "Methioninsynthase", size=12.5)
t.text(20, 1330, "ist der einzige Verbraucher von 5-Methyl-THF. Fehlt Cobalamin, steht dieser "
                 "eine Ausgang still, und das gesamte Folat sammelt sich als 5-Methyl-THF an: "
                 "ein funktioneller", size=12.5)
t.text(20, 1350, "Folatmangel bei normalem Folatspiegel. Folsäuregabe korrigiert dann das Blutbild, "
                 "nicht aber die neurologische Schädigung.", size=12.5)
t.text(20, 1378, "Deshalb muss vor jeder Folatsubstitution ein B&#8321;&#8322;-Mangel "
                 "ausgeschlossen werden. Die beiden Laborparameter, die das leisten, stehen auf "
                 "Tafel M-16.", size=12.5, farbe=W)

# ===================================================== Ausgabe
ARIA = (
    "Tetrahydrofolat in vier Zonen. Zone A zeigt den Ausschnitt zwischen den Stickstoffatomen "
    "N5 und N10 in vier Transportformen: 5-Methyl-Tetrahydrofolat, 5,10-Methylen-"
    "Tetrahydrofolat als Fuenfring, das kationische 5,10-Methenyl-Tetrahydrofolat und "
    "10-Formyl-Tetrahydrofolat. Alle vier stehen in derselben Lage, damit der Unterschied "
    "zwischen den Stufen ins Auge faellt und nicht die Ausrichtung. "
    "Eine Achse darunter ordnet sie drei Oxidationsstufen zu: "
    "Methanolstufe, Formaldehydstufe und Ameisensaeurestufe, wobei ein Balken anzeigt, dass "
    "Methenyl und Formyl beide auf der Ameisensaeurestufe liegen. Der Uebergang Methylen zu "
    "Methenyl verbraucht NADP plus und liefert NADPH, der Uebergang Methenyl zu Formyl "
    "verbraucht Wasser und setzt ein Proton frei; beide sind reversibel. Der Schritt zur "
    "Methylstufe ueber die Methylentetrahydrofolat-Reduktase verbraucht NADPH und ein Proton "
    "und ist irreversibel. Zone B fuehrt den Mechanismus der Thymidylatsynthase aus. Der "
    "Fuenfring des Methylentetrahydrofolats oeffnet sich zum Iminium: Ein Elektronenpfeil "
    "geht vom Stickstoff N5 in die Bindung zwischen N5 und der Kohlenstoffbruecke, aus der "
    "damit die Doppelbindung des Iminiums wird; das Bindungspaar zwischen der Bruecke und dem "
    "Stickstoff N10 geht dabei auf das N10 ueber. Am Iminium ist die Kohlenstoffbruecke jetzt "
    "elektrophil. Ein zweiter Elektronenpfeil geht vom freien Paar am Kohlenstoff C5 des dUMP, "
    "an dessen C6 zuvor ein Cystein des Enzyms addiert hat, auf diesen Kohlenstoff; das "
    "Elektronenpaar der Doppelbindung geht dabei auf das N5 zurueck. Es entsteht der "
    "kovalente ternaere Komplex aus Enzym, Substrat und Cofaktor. Zone C nennt die vier "
    "Arzneistoffe an diesem Zyklus, Zone D erklaert die Methylfalle."
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

mech.speichern("m04", t.svg(ARIA), t)
