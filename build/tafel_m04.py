# -*- coding: utf-8 -*-
"""
M-04 · Tetrahydrofolat, gebaut mit mech.py.

Vorher war die Tafel ein reines Flussdiagramm ohne einen einzigen Elektronenpfeil.
Gezeichnet wird jetzt der Ausschnitt N5 bis N10 - nur dort sitzt die C1-Einheit,
und nur dort unterscheiden sich die Transportformen. Es sind vier Formen, aber
nur drei Oxidationsstufen: Methenyl und Formyl stehen beide auf der
Ameisensaeurestufe. Zone B fuehrt den Schritt aus, an dem 5-Fluoruracil angreift.
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
    m = mech.Molekuel(smi, x, 190, labels=lab, zeige={1: "links"}, name=titel)
    t.mole.append(m)
    mole.append(m)
    t.ueberschrift(m, titel, farbe=farbe, abstand=30)
    t.unterschrift(m, note, abstand=30)

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
                "Erst die Ringöffnung zum Iminium macht es angreifbar. Der Ausschnitt ist "
                "vergrößert.", size=12.5)

meth = mech.Molekuel("*N1C(*)CN(*)C1", 132, 556, labels={0: "C4a", 3: "C7", 6: "Aryl"},
                     zeige={1: "links"}, bindung=31, name="Methylen-THF")
t.mole.append(meth)
lp_n5 = t.elektronenpaar(meth, 1, 200, abstand=16)
t.pfeil(lp_n5, meth.aussen(1, 7, abstand=30), bogen=0.34, seite=1, farbe=W)
t.pfeil(meth.aussen(7, 5, abstand=28), meth.aussen(5, abstand=32), bogen=0.34,
        seite=-1, farbe=W)
t.unterschrift(meth, "der Fünfring öffnet sich", abstand=32)

t.reaktionspfeil(238, 560, 316)
t.text(277, 550, "+ H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=G)

imin = mech.Molekuel("*[N+](=C)C(*)CN(*)*", 424, 556,
                     labels={0: "C4a", 4: "C7", 7: "Aryl", 8: "H"},
                     zeige={1: "links"}, bindung=31, name="Iminium")
t.mole.append(imin)
t.atomnummer(imin, 2, "C&#8321;", winkel=200, abstand=26, size=10, farbe=W, gewicht=700)
t.unterschrift(imin, "Iminium: jetzt ist das C&#8321; elektrophil", abstand=32)

t.kasten(560, 494, 420, 132, fill="var(--surface-2)")
t.text(578, 516, "WARUM DIESER SCHRITT DEN COFAKTOR KOSTET", size=11, gewicht=700, farbe=G)
t.text(578, 538, "Die Thymidylatsynthase ist die einzige Reaktion, bei der", size=12.5)
t.text(578, 557, "THF nicht nur die C&#8321;-Einheit liefert, sondern auch noch", size=12.5)
t.text(578, 576, "das Hydrid für deren Reduktion zur Methylgruppe.", size=12.5)
t.text(578, 599, "Der Cofaktor wird dabei zu Dihydrofolat oxidiert, und nur", size=12.5)
t.text(578, 618, "die Dihydrofolat-Reduktase bringt ihn zurück.", size=12.5)

dump = mech.Molekuel("O=C1NC(=O)N(*)C(S*)[CH-]1", 146, 768,
                     labels={6: "dRib-P", 9: "Enzym"}, zeige={10: "rechts"},
                     bindung=26, name="dUMP")
t.mole.append(dump)
t.unterschrift(dump, "dUMP, nachdem ein Cystein des Enzyms", "an C6 addiert hat", abstand=32)
# Die Marke muss nach unten rechts: geradeaus ueber dem Carbanion sitzt das C6 mit
# dem Cystein, und dort gelesen hiesse "C5" genau den falschen Kohlenstoff.
t.atomnummer(dump, 10, "C5", winkel=35, abstand=22, size=10, farbe=W, gewicht=700)

imin2 = mech.Molekuel("*[N+](=C)C(*)CN(*)*", 428, 768,
                      labels={0: "C4a", 4: "C7", 7: "Aryl", 8: "H"},
                      zeige={1: "rechts"}, bindung=26, name="Iminium")
t.mole.append(imin2)
lp_c5 = t.elektronenpaar(dump, 10, 340)
t.pfeil(lp_c5, (imin2, 2), bogen=0.24, seite=-1, farbe=W)
# Gegenpfeil: das pi-Paar der C=N-Doppelbindung geht auf das N5. Ohne ihn haette
# der angegriffene Kohlenstoff fuenf Bindungen und die Ladung verschwaende.
t.pfeil(imin2.aussen(1, 2, abstand=14), (imin2, 1), bogen=0.6, seite=-1, farbe=W,
        mindestbogen=14)
t.unterschrift(imin2, "C5 greift das Iminium an", abstand=32)

t.reaktionspfeil(524, 764, 596)

tern = mech.Molekuel("O=C1NC(=O)N(*)C(S*)C1CN(*)C(*)CN(*)*", 786, 768,
                     labels={6: "dRib-P", 9: "Enzym", 13: "C4a", 15: "C7",
                             18: "Aryl", 19: "H"},
                     zeige={6: "links", 18: "rechts"}, bindung=24,
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
    "10-Formyl-Tetrahydrofolat. Eine Achse darunter ordnet sie drei Oxidationsstufen zu: "
    "Methanolstufe, Formaldehydstufe und Ameisensaeurestufe, wobei ein Balken anzeigt, dass "
    "Methenyl und Formyl beide auf der Ameisensaeurestufe liegen. Der Uebergang Methylen zu "
    "Methenyl verbraucht NADP plus und liefert NADPH, der Uebergang Methenyl zu Formyl "
    "verbraucht Wasser und setzt ein Proton frei; beide sind reversibel. Der Schritt zur "
    "Methylstufe ueber die Methylentetrahydrofolat-Reduktase verbraucht NADPH und ein Proton "
    "und ist irreversibel. Zone B fuehrt den Mechanismus der Thymidylatsynthase aus: Der "
    "Fuenfring des Methylentetrahydrofolats oeffnet sich mit Elektronenpaarpfeilen zum "
    "Iminium, dessen Kohlenstoff jetzt elektrophil ist; das Kohlenstoffatom C5 des dUMP, an "
    "dessen C6 zuvor ein Cystein des Enzyms addiert hat, greift dieses Iminium an, waehrend "
    "das Elektronenpaar der Doppelbindung auf das N5 zurueckgeht, und es entsteht der "
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
