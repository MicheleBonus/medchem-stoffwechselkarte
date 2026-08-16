# -*- coding: utf-8 -*-
"""
M-09 · Aromatase, gebaut mit mech.py.

Kern der Tafel ist ein Gegensatz zwischen zwei Eisenspezies: Compound I ist
elektrophil, der Ferri-Peroxo-Komplex nucleophil. Beide werden mit demselben
Zentrum-Bausatz gezeichnet, damit man sieht, dass nur der axiale Ligand anders ist.
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

t = mech.Tafel(1000, 1330)

# ===================================================== ZONE A · drei Durchgaenge
t.zone(24, "A · DREI DURCHGÄNGE AN EINEM EINZIGEN KOHLENSTOFF")
t.text(20, 54, "Die Aromatase entfernt das C19 — die Methylgruppe am Ringübergang — und "
               "aromatisiert dabei den A-Ring. Jeder der drei Schritte kostet ein O&#8322; "
               "und ein NADPH.", size=12.5)

STUFEN = [
    (130, "CC12CCC3C(CCC4=CC(=O)CCC34C)C1CCC2=O", "Androstendion", "C19 als &#8722;CH&#8323;"),
    (380, "CC12CCC3C(CCC4=CC(=O)CCC34CO)C1CCC2=O", "19-Hydroxy", "C19 als &#8722;CH&#8322;OH"),
    (630, "CC12CCC3C(CCC4=CC(=O)CCC34C=O)C1CCC2=O", "19-Oxo", "C19 als &#8722;CHO"),
    (880, "CC12CCC3c4ccc(O)cc4CCC3C1CCC2=O", "Estron", "C19 abgespalten, Ring A aromatisch"),
]
for x, smi, titel, note in STUFEN:
    m = mech.Molekuel(smi, x, 216, name=titel)
    t.mole.append(m)
    t.ueberschrift(m, titel, abstand=28)
    t.unterschrift(m, note, abstand=28, farbe=G)

for i, (x0, x1) in enumerate(((222, 288), (472, 538), (722, 788))):
    t.reaktionspfeil(x0, 216, x1)
    t.text((x0 + x1) / 2, 204, "%d. Zyklus" % (i + 1), size=10, anchor="middle",
           gewicht=700, farbe=C)
t.text(755, 246, "&#8722; HCOOH", size=10, anchor="middle", gewicht=700, farbe=W)

# ===================================================== ZONE B · der Gegensatz
t.zone(322, "B · WARUM DER DRITTE ZYKLUS AUS DER REIHE FÄLLT")
t.text(20, 352, "In den ersten beiden Durchgängen läuft der P450-Zyklus aus Tafel M-08 bis zum "
                "Ende. Im dritten bricht er eine Stufe früher ab — und die Zwischenstufe,",
       size=12.5)
t.text(20, 371, "die dabei stehen bleibt, hat den umgekehrten elektronischen Charakter.",
       size=12.5)

zc1 = t.zentrum(150, 480, "Fe(IV)", axial=["O"], doppelt=True, radikal=True, unten="S&#8722;Cys",
                schritt=46, name="Compound I")
# Beide Ueberschriften unter die Glyphen: ueber dem Peroxo-Komplex sitzt
# bereits sein zweiter axialer Sauerstoff.
t.text(150, 566, "Compound I", size=12.5, anchor="middle", gewicht=700, farbe=W)
t.text(150, 586, "elektrophil — abstrahiert Wasserstoff", size=11, anchor="middle", farbe=G)
t.text(150, 602, "und macht Rebound · Zyklus 1 und 2", size=11, anchor="middle", farbe=G)

zc2 = t.zentrum(460, 480, "Fe(III)", axial=["O", "O&#8315;"], unten="S&#8722;Cys",
                schritt=46, name="Ferri-Peroxo")
lp_p = t.paar(504, 396, 20, "Peroxo-Sauerstoff")
t.text(460, 566, "Ferri-Peroxo-Komplex", size=12.5, anchor="middle", gewicht=700, farbe=E)
t.text(460, 586, "nucleophil — greift den Aldehyd-", size=11, anchor="middle", farbe=G)
t.text(460, 602, "kohlenstoff an · nur Zyklus 3", size=11, anchor="middle", farbe=G)

ald = mech.Molekuel("*C=O", 700, 440, labels={0: "C10"}, zeige={1: "links"},
                    name="19-Oxo-Gruppe")
t.mole.append(ald)
t.pfeil(lp_p, (ald, 1), bogen=0.24, seite=-1, farbe=W)
t.pfeil((ald, 1, 2), ald.abseits(2, 1), bogen=0.42, seite=1, farbe=W)
t.unterschrift(ald, "das C19 als Aldehyd —", "hier greift der Peroxo-Komplex an", abstand=28)

t.kasten(790, 396, 190, 152, fill="var(--warn-bg)", stroke=W)
t.text(808, 418, "WIE EINE BAEYER-", size=11, gewicht=700, farbe=W)
t.text(808, 434, "VILLIGER-REAKTION", size=11, gewicht=700, farbe=W)
t.text(808, 458, "Aus dem tetraedrischen", size=12)
t.text(808, 477, "Zwischenprodukt bricht", size=12)
t.text(808, 496, "die Bindung C10&#8722;C19.", size=12)
t.text(808, 519, "Das C19 geht als Ameisen-", size=12)
t.text(808, 538, "säure ab.", size=12)

t.kasten(20, 656, 960, 76, fill="var(--surface-2)")
t.text(38, 678, "UND DANN AROMATISIERT DER RING VON SELBST", size=11, gewicht=700, farbe=G)
t.text(38, 700, "Nach dem Verlust des C19 bleibt am C10 ein Enol zurück. Es tautomerisiert zum "
                "Phenol — und damit ist der A-Ring aromatisch. Aus dem C&#8321;&#8329;-Steroid",
       size=12.5)
t.text(38, 719, "ist ein C&#8321;&#8328;-Steroid geworden: der Schritt, der Androgene von "
                "Estrogenen trennt.", size=12.5)

# ===================================================== ZONE C · Hemmung
t.zone(778, "C · ZWEI WEGE, DAS ENZYM ZU HEMMEN")
t.text(20, 808, "Der eine besetzt das Eisen, der andere missbraucht den Mechanismus — dieselbe "
                "Zweiteilung wie bei den MAO-Hemmern in Tafel M-06.", size=12.5)

zc3 = t.zentrum(140, 936, "Fe(III)", axial=["N"], unten="S&#8722;Cys", schritt=46,
                name="Häm mit Triazol")
t.text(140, 858, "koordinativ", size=12.5, anchor="middle", gewicht=700, farbe=R)
t.text(140, 992, "der Triazol-Stickstoff besetzt", size=10.5, anchor="middle", farbe=G)
t.text(140, 1008, "die Bindestelle des Sauerstoffs", size=10.5, anchor="middle", farbe=G)

letr = mech.Molekuel("N#Cc1ccc(cc1)C(n1cncn1)c1ccc(cc1)C#N", 400, 930, name="Letrozol")
t.mole.append(letr)
t.unterschrift(letr, "Letrozol — Anastrozol trägt dieselbe Triazolgruppe",
               "an einem anderen Gerüst", abstand=30, farbe=R)

t.kasten(680, 862, 300, 152, fill="var(--drug-bg)", stroke=R)
t.text(698, 884, "MECHANISMUSBASIERT", size=11, gewicht=700, farbe=R)
t.text(698, 906, "Exemestan und Formestan sind", size=12.5)
t.text(698, 925, "Substratanaloga. Das Enzym nimmt sie", size=12.5)
t.text(698, 944, "an und oxidiert sie dabei zu einem", size=12.5)
t.text(698, 963, "reaktiven Zwischenprodukt, das", size=12.5)
t.text(698, 982, "kovalent bindet — irreversibel.", size=12.5)
t.text(698, 1005, "Deshalb wirken sie über die Halbwertszeit hinaus.", size=11, farbe=G)

t.kasten(20, 1064, 960, 96, fill="var(--surface-2)")
t.text(38, 1086, "WOFÜR MAN DAS IM EXAMEN BRAUCHT", size=11, gewicht=700, farbe=G)
t.text(38, 1108, "Aromatasehemmer wirken nur nach der Menopause. Vorher stammt das Estrogen "
                 "überwiegend aus dem Ovar und steht unter Rückkopplung der", size=12.5)
t.text(38, 1127, "Gonadotropine: Sinkt der Spiegel, steigen FSH und LH und treiben das Ovar zu "
                 "mehr Produktion. Nach der Menopause fällt diese Quelle weg, und", size=12.5)
t.text(38, 1146, "die periphere Aromatisierung im Fettgewebe ist die einzige — dort greift der "
                 "Hemmstoff.", size=12.5)

t.kasten(20, 1188, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1210, "DER UNTERSCHIED ZU TAMOXIFEN", size=11, gewicht=700, farbe=W)
t.text(38, 1232, "Tamoxifen blockiert den Rezeptor, der Aromatasehemmer die Synthese. Daraus "
                 "folgen verschiedene Nebenwirkungsprofile: Tamoxifen wirkt am", size=12.5)
t.text(38, 1251, "Endometrium agonistisch und erhöht das Thromboserisiko, Aromatasehemmer "
                 "senken den Estrogenspiegel systemisch und fördern die Osteoporose.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Aromatase in drei Zonen. Zone A zeigt die drei Durchgaenge an einem einzigen "
    "Kohlenstoffatom mit gezeichneten Steroidstrukturen: Androstendion, 19-Hydroxy-Verbindung, "
    "19-Oxo-Verbindung und schliesslich Estron mit aromatischem A-Ring. Zone B stellt die "
    "beiden Eisenspezies nebeneinander: links Compound I mit Eisen vier gleich Sauerstoff und "
    "Porphyrin-Radikalkation, elektrophil, zustaendig fuer die ersten beiden Zyklen; rechts der "
    "Ferri-Peroxo-Komplex, nucleophil, der mit einem Elektronenpaarpfeil den Aldehydkohlenstoff "
    "des C19 angreift wie bei einer Baeyer-Villiger-Reaktion. Die Bindung zwischen C10 und C19 "
    "bricht, Ameisensaeure geht ab, und der Ring aromatisiert. Zone C zeigt die beiden "
    "Hemmprinzipien: Letrozol koordiniert mit einem Triazol-Stickstoff das Haem-Eisen, "
    "Exemestan wirkt mechanismusbasiert."
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
daten["m09"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m09  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m09"]), len(t.mole), len(t.anker)))
