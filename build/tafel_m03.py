# -*- coding: utf-8 -*-
"""
M-03 · Biotin, gebaut mit mech.py.

Die Tafel hatte bisher keine einzige Struktur - nur Kaesten und einen
schematischen Arm. Jetzt sind beide Halbreaktionen ausgefuehrt: die
Carboxylierung des Biotins und die Uebertragung auf das Enolat.
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

BIOTIN = "O=C1N[C@@H]2CS[C@@H](*)[C@@H]2N1"
CARBOXY = "OC(=O)N1C(=O)N[C@@H]2CS[C@@H](*)[C@@H]12"
# RDKit zeichnet Atomlabel aus einem eigenen Vektorfont, der weder
# HTML-Entitaeten noch Tiefstellungszeichen kennt - beides faellt im Bild aus.
# Deshalb hier nur "Lys"; die Amidbindung erklaert die Unterschrift.
KETTE = "Lys"

t = mech.Tafel(1000, 1420)

# ===================================================== ZONE A · Aktivierung
t.zone(24, "A · WARUM EINE CARBOXYLIERUNG ATP KOSTET")
t.text(20, 54, "Hydrogencarbonat ist kein Elektrophil. Erst das ATP macht daraus ein gemischtes "
               "Anhydrid, das in Kohlendioxid und Phosphat zerfällt.", size=12.5)

hco3 = mech.Molekuel("OC(=O)[O-]", 116, 170, zeige={1: "rechts"}, name="Hydrogencarbonat")
t.mole.append(hco3)
t.unterschrift(hco3, "Hydrogencarbonat", abstand=28, farbe=G)

t.reaktionspfeil(180, 170, 254)
t.text(217, 158, "+ ATP", size=10.5, anchor="middle", gewicht=700, farbe=C)
t.text(217, 192, "&#8722; ADP", size=10, anchor="middle", farbe=G)

cp = mech.Molekuel("OC(=O)OP(=O)([O-])[O-]", 356, 170, zeige={1: "links"},
                   name="Carboxyphosphat")
t.mole.append(cp)
t.unterschrift(cp, "Carboxyphosphat — ein gemischtes Anhydrid", abstand=28, farbe=G)

t.reaktionspfeil(468, 170, 542)
t.text(505, 158, "&#8722; P&#7522;", size=10.5, anchor="middle", gewicht=700, farbe=G)

co2 = mech.Molekuel("O=C=O", 604, 170, zeige={0: "oben"}, name="Kohlendioxid")
t.mole.append(co2)
t.unterschrift(co2, "CO&#8322;", abstand=24, farbe=G)

t.kasten(690, 104, 290, 116, fill="var(--cofaktor-bg)", stroke=C)
t.text(708, 126, "DIE BILANZ", size=11, gewicht=700, farbe=C)
t.text(708, 148, "Ein ATP wird zu ADP und Phosphat", size=12.5)
t.text(708, 167, "gespalten — und zwar hier, nicht bei", size=12.5)
t.text(708, 186, "der eigentlichen Carboxylierung.", size=12.5)
t.text(708, 209, "Der teure Schritt ist die Aktivierung.", size=12, farbe=G)

# ===================================================== ZONE B · Carboxylierung
t.zone(288, "B · DAS BIOTIN NIMMT DAS CO&#8322; AUF")
t.text(20, 318, "Von den beiden Stickstoffatomen des Ureidorings ist nur einer nucleophil genug: "
                "N1&#8242;, der dem Schwefelring benachbarte.", size=12.5)

bio = mech.Molekuel(BIOTIN, 190, 452, labels={7: KETTE}, zeige={9: "rechts"}, name="Biotin")
t.mole.append(bio)
# Welcher der beiden Ureido-Stickstoffe gemeint ist, zeigt das freie
# Elektronenpaar - eine Positionsnummer daneben behauptet mehr, als das
# Bild hergibt.
lp_n = t.elektronenpaar(bio, 9, 340)

co2b = mech.Molekuel("O=C=O", 428, 400, zeige={0: "oben"}, name="Kohlendioxid")
t.mole.append(co2b)
t.pfeil(lp_n, (co2b, 1), bogen=0.24, seite=-1, farbe=W)
t.pfeil((co2b, 1, 2), co2b.abseits(2, 1), bogen=0.42, seite=1, farbe=W)
t.unterschrift(bio, "Biotin — über (CH&#8322;)&#8324;&#8211;CO an ein Lysin gebunden;",
               "nur der markierte Stickstoff ist nucleophil genug", abstand=30)
t.unterschrift(co2b, "CO&#8322;", abstand=24, farbe=G)

t.reaktionspfeil(500, 452, 574)

cbio = mech.Molekuel(CARBOXY, 736, 452, labels={11: KETTE}, zeige={3: "links"},
                     name="Carboxybiotin")
t.mole.append(cbio)
t.unterschrift(cbio, "Carboxybiotin — das CO&#8322; ist jetzt gebunden",
               "und wird nicht mehr in die Lösung entlassen", abstand=30)

# ===================================================== ZONE C · Uebertragung
t.zone(596, "C · UND GIBT ES AM ZWEITEN ZENTRUM WIEDER AB")
t.text(20, 626, "Dort wartet das Substrat, vom Enzym als Enolat deprotoniert. Es greift den "
                "Carboxylkohlenstoff an, und die N&#8722;C-Bindung bricht.", size=12.5)

cbio2 = mech.Molekuel(CARBOXY, 190, 764, labels={11: KETTE}, zeige={3: "rechts"},
                      name="Carboxybiotin")
t.mole.append(cbio2)
t.pfeil((cbio2, 1, 3), cbio2.abseits(3, 1, abstand=22), bogen=0.42, seite=1, farbe=W)
t.unterschrift(cbio2, "die N&#8722;C-Bindung bricht,", "das Biotin wird frei", abstand=30)

enol = mech.Molekuel("[CH2-]C(=O)*", 470, 712, labels={3: "SCoA"}, zeige={0: "links"},
                     name="Acetyl-CoA-Enolat")
t.mole.append(enol)
lp_e = t.elektronenpaar(enol, 0, 200)
t.pfeil(lp_e, (cbio2, 1), bogen=0.26, seite=1, farbe=W)
t.unterschrift(enol, "Acetyl-CoA, als Enolat deprotoniert", abstand=28)

t.reaktionspfeil(560, 764, 634)

mal = mech.Molekuel("[O-]C(=O)CC(=O)*", 780, 764, labels={6: "SCoA"}, zeige={0: "links"},
                    name="Malonyl-CoA")
t.mole.append(mal)
t.unterschrift(mal, "Malonyl-CoA — der schrittbestimmende",
               "Baustein der Fettsäuresynthese", abstand=30)

# ===================================================== ZONE D · Arm und Enzyme
t.zone(880, "D · DER SCHWENKARM UND DIE VIER HUMANEN CARBOXYLASEN")

t.kasten(20, 912, 470, 118, fill="var(--surface-2)")
t.text(38, 934, "WARUM ZWEI ZENTREN UND EIN ARM", size=11, gewicht=700, farbe=G)
t.text(38, 956, "Beide Halbreaktionen laufen an verschiedenen Stellen des", size=12.5)
t.text(38, 975, "Enzyms. Biotin und Lysin bilden zusammen einen etwa", size=12.5)
t.text(38, 994, "16 Å langen Arm, der das gebundene CO&#8322; von einem", size=12.5)
t.text(38, 1013, "Zentrum zum anderen trägt, ohne es freizusetzen.", size=12.5)

t.kasten(510, 912, 470, 118, fill="var(--cofaktor-bg)", stroke=C)
t.text(528, 934, "DASSELBE PRINZIP AN ZWEI WEITEREN STELLEN", size=11, gewicht=700, farbe=C)
t.text(528, 956, "Das Liponamid im Pyruvat-Dehydrogenase-Komplex und", size=12.5)
t.text(528, 975, "das Phosphopantethein der Fettsäure-Synthase arbeiten", size=12.5)
t.text(528, 994, "genauso: ein reaktives Zwischenprodukt bleibt kovalent", size=12.5)
t.text(528, 1013, "gebunden und wandert zwischen den Zentren.", size=12.5)

CARBOXYLASEN = [
    (20, "Pyruvat-Carboxylase", "Pyruvat → Oxalacetat",
     "startet die Gluconeogenese"),
    (270, "Acetyl-CoA-Carboxylase", "→ Malonyl-CoA",
     "schrittbestimmend für die Fettsäuresynthese"),
    (540, "Propionyl-CoA-Carboxylase", "→ Methylmalonyl-CoA",
     "danach folgt die Mutase aus Tafel M-16"),
    (790, "Methylcrotonyl-CoA-Carboxylase", "im Leucinabbau",
     "der Marker im Neugeborenenscreening"),
]
for x, name, r1, r2 in CARBOXYLASEN:
    t.text(x, 1074, name, size=11.5, gewicht=700, farbe=E)
    t.text(x, 1094, r1, size=11)
    t.text(x, 1112, r2, size=11, farbe=G)

t.kasten(20, 1140, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1162, "WORAN ES IN DER PRAXIS SCHEITERT", size=11, gewicht=700, farbe=W)
t.text(38, 1184, "Ein alimentärer Biotinmangel ist selten, weil Darmbakterien Biotin bilden. "
                 "Klinisch zählen drei Sonderfälle: der Biotinidase-Mangel, bei dem Biotin", size=12.5)
t.text(38, 1203, "nicht aus dem Biocytin zurückgewonnen wird; große Mengen rohen Eiklars, dessen "
                 "Avidin das Biotin praktisch irreversibel bindet; und die", size=12.5)
t.text(38, 1222, "Langzeittherapie mit Antikonvulsiva.", size=12.5)

t.kasten(20, 1264, 960, 76, fill="var(--drug-bg)", stroke=R)
t.text(38, 1286, "EINE LABORFALLE, DIE IM EXAMEN GERN GEFRAGT WIRD", size=11, gewicht=700, farbe=R)
t.text(38, 1308, "Hochdosiertes Biotin als Nahrungsergänzung verfälscht Immunoassays, die auf der "
                 "Biotin-Streptavidin-Bindung beruhen — je nach Testaufbau", size=12.5)
t.text(38, 1327, "fallen TSH, Troponin oder die Schilddrüsenhormone falsch aus. Vor der Blutabnahme "
                 "muss Biotin deshalb abgesetzt werden.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Biotin in vier Zonen. Zone A zeigt, warum eine Carboxylierung ATP kostet: Hydrogencarbonat "
    "wird mit ATP zum gemischten Anhydrid Carboxyphosphat, das in Kohlendioxid und Phosphat "
    "zerfaellt. Zone B zeigt die Carboxylierung des Biotins: Das freie Elektronenpaar des "
    "Stickstoffs N1-Strich greift mit einem Elektronenpaarpfeil den Kohlenstoff des "
    "Kohlendioxids an, eine der beiden Doppelbindungen weicht auf den Sauerstoff aus, es "
    "entsteht Carboxybiotin. Zone C zeigt die Uebertragung am zweiten aktiven Zentrum: Das als "
    "Enolat deprotonierte Acetyl-CoA greift den Carboxylkohlenstoff an, die "
    "Stickstoff-Kohlenstoff-Bindung bricht, und es entsteht Malonyl-CoA. Zone D erklaert den "
    "sechzehn Angstroem langen Schwenkarm aus Biotin und Lysin, nennt die vier humanen "
    "Carboxylasen und die klinischen Sonderfaelle."
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

mech.speichern("m03", t.svg(ARIA), t)
