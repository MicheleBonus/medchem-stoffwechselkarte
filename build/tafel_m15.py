# -*- coding: utf-8 -*-
"""
M-15 · Vitamin K, gebaut mit mech.py.

Vorher stand die ganze Tafel als Text da - selbst der Glutamatrest war die
Zeichenkette "Protein-CH2-CH2-COO". Zone A fuehrt jetzt beide Schritte aus:
die Deprotonierung durch das Alkoxid und den Angriff des Carbanions auf CO2.
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

t = mech.Tafel(1000, 1260)

# ===================================================== ZONE A · die Carboxylierung
t.zone(24, "A · DAS PROBLEM — EIN PROTON, DAS NICHT WEG WILL")
t.text(20, 54, "Der γ-Wasserstoff eines Glutamatrests hat einen pK<tspan baseline-shift='sub' "
               "font-size='9'>a</tspan> um 28. Keine Seitenkette eines Proteins kommt als Base "
               "dafür in Frage — die stärkste, das Thiolat", size=12.5)
t.text(20, 73, "des Cysteins, liegt bei 8. Die nötige Basenstärke entsteht erst im Zuge der "
               "Vitamin-K-Oxygenierung.", size=12.5)

glu = mech.Molekuel("*CCC(=O)[O-]", 150, 196, labels={0: "Protein"},
                    wasserstoff=[2], zeige={0: "links"}, name="Glutamatrest")
t.mole.append(glu)
hg = glu.h_index[2]
t.atomnummer(glu, 2, "γ-C", winkel=90, abstand=30, size=10.5, farbe=W, gewicht=700)

alkoxid = t.paar(150, 122, 300, "Alkoxid aus Vitamin K")
t.text(150, 106, "R&#8722;O&#8315;", size=12.5, anchor="middle", gewicht=700, farbe=C)
t.text(150, 90, "das Alkoxid aus Zone B", size=10, anchor="middle", farbe=G)
t.pfeil(alkoxid, (glu, 2, hg), bogen=0.26, seite=1, farbe=W)
t.pfeil((glu, 2, hg), glu.abseits(2, hg), bogen=0.45, seite=-1, farbe=W)
t.unterschrift(glu, "Glutamatrest im unreifen Gerinnungsfaktor", abstand=30)

t.reaktionspfeil(258, 196, 326)
t.text(292, 186, "&#8722; H&#8314;", size=10.5, anchor="middle", gewicht=700, farbe=W)

carb = mech.Molekuel("*C[CH-]C(=O)[O-]", 420, 196, labels={0: "Protein"},
                     zeige={0: "links"}, name="Carbanion")
t.mole.append(carb)
lp_c = t.elektronenpaar(carb, 2, 30)
t.unterschrift(carb, "das Carbanion — nur kurzlebig,", "aber stark nucleophil", abstand=30)

# CO2 senkrecht stellen: das Nucleophil greift den Kohlenstoff quer zur
# O=C=O-Achse an, und der Pfeilkopf landet dann nicht auf einem Sauerstoff.
co2 = mech.Molekuel("O=C=O", 600, 150, zeige={0: "oben"}, name="Kohlendioxid")
t.mole.append(co2)
t.pfeil(lp_c, (co2, 1), bogen=0.30, seite=-1, farbe=W, gap=5)
t.pfeil((co2, 1, 2), co2.abseits(2, 1), bogen=0.45, seite=1, farbe=W)
t.unterschrift(co2, "CO&#8322;", abstand=24, farbe=G)

t.reaktionspfeil(654, 196, 716)

gla = mech.Molekuel("*CC(C(=O)[O-])C(=O)[O-]", 830, 196, labels={0: "Protein"},
                    zeige={0: "links"}, name="Gla")
t.mole.append(gla)
t.unterschrift(gla, "γ-Carboxyglutamat — zwei Carboxylate",
               "an einem Kohlenstoff binden Calcium", abstand=30)

t.kasten(20, 300, 960, 58, fill="var(--warn-bg)", stroke=W)
t.text(38, 322, "Erst der Gla-Rest macht den Gerinnungsfaktor funktionsfähig: Zwei benachbarte "
                "Carboxylate greifen ein Calciumion, und dieses vermittelt die Bindung", size=12.5)
t.text(38, 341, "an die negativ geladene Membranoberfläche aktivierter Thrombozyten. Ohne "
                "Carboxylierung schwimmt der Faktor wirkungslos im Plasma.", size=12.5)

# ===================================================== ZONE B · der Zyklus
t.zone(400, "B · WOHER DIE BASENSTÄRKE KOMMT — UND WOHIN DER COFAKTOR GEHT")
t.text(20, 430, "Die Oxygenierung des Hydrochinons ist stark exergon. Das Enzym nutzt diesen "
                "Energiegewinn nicht für eine Bindungsknüpfung, sondern um kurzzeitig", size=12.5)
t.text(20, 449, "eine Base bereitzustellen, die es sonst in keinem Protein gäbe. Carboxylierung "
                "und Epoxidbildung sind deshalb zwingend gekoppelt.", size=12.5)

kh2 = mech.Molekuel("Cc1c(*)c(O)c2ccccc2c1O", 156, 578, labels={3: "R"},
                    zeige={3: "rechts"}, name="Hydrochinon")
t.mole.append(kh2)
t.unterschrift(kh2, "KH&#8322; — das Hydrochinon,", "die einzige wirksame Form", abstand=30)

t.reaktionspfeil(268, 578, 396)
t.text(332, 540, "+ O&#8322;", size=11, anchor="middle", gewicht=700, farbe=C)
t.text(332, 558, "über ein Peroxid", size=10, anchor="middle", farbe=G)
t.text(332, 602, "hier entsteht das Alkoxid,", size=10, anchor="middle",
       farbe=W, gewicht=700)

epox = mech.Molekuel("CC12OC1(*)C(=O)c1ccccc1C2=O", 520, 578, labels={4: "R"},
                     zeige={4: "rechts"}, name="K-2,3-Epoxid")
t.mole.append(epox)
t.unterschrift(epox, "K-2,3-Epoxid — der Cofaktor ist verbraucht", abstand=30)

t.reaktionspfeil(632, 578, 750)
t.text(691, 560, "VKORC1", size=11, anchor="middle", gewicht=700, farbe=E, mono=True)
t.text(691, 596, "&#8867; Cumarine", size=10.5, anchor="middle", gewicht=700, farbe=R)

chin = mech.Molekuel("CC1=C(*)C(=O)c2ccccc2C1=O", 862, 578, labels={3: "R"},
                     zeige={3: "rechts"}, name="Vitamin-K-Chinon")
t.mole.append(chin)
t.unterschrift(chin, "Vitamin-K-Chinon — die Form,", "die im Präparat steckt", abstand=30)

# Rueckweg vom Chinon zum Hydrochinon
t.stuecke.append((1, "<path d='M 862 676 L 862 716 L 156 716 L 156 664' fill='none' "
                     "stroke='currentColor' stroke-width='1.5' marker-end='url(#rxn)'/>"))
t.text(509, 734, "VKORC1 — derselbe zweite Schritt, dieselbe Hemmung durch Cumarine",
       size=11, anchor="middle", gewicht=700, farbe=E)

# Ein langer Pfeil quer ueber die Tafel wuerde durch drei Beschriftungen laufen.
# Der Verweis steht deshalb auf beiden Seiten im Text.
t.text(332, 616, "das oben das γ-Proton abzieht", size=10, anchor="middle",
       farbe=W, gewicht=700)

# ===================================================== ZONE C · Klinik
t.zone(786, "C · WAS SICH FÜR DIE THERAPIE DARAUS ERGIBT")

t.kasten(20, 818, 470, 158, fill="var(--drug-bg)", stroke=R)
t.text(38, 840, "CUMARINE HEMMEN DIE REDUKTASE, NICHT DIE CARBOXYLASE", size=11,
       gewicht=700, farbe=R)
t.text(38, 862, "Phenprocoumon und Warfarin blockieren die VKORC1 und", size=12.5)
t.text(38, 881, "damit die Rückgewinnung des Cofaktors. Die Carboxylase", size=12.5)
t.text(38, 900, "selbst bleibt unberührt — ihr geht nur das Substrat aus.", size=12.5)
t.text(38, 923, "Daraus folgt die Antidotwirkung von Vitamin K&#8321;: In hoher", size=12.5)
t.text(38, 942, "Dosis umgeht es die blockierte VKOR über eine zweite,", size=12.5)
t.text(38, 961, "NAD(P)H-abhängige Reduktase.", size=12.5)

t.kasten(510, 818, 470, 158, fill="var(--surface-2)")
t.text(528, 840, "WARUM DIE WIRKUNG ERST NACH TAGEN EINSETZT", size=11, gewicht=700, farbe=G)
t.text(528, 862, "Betroffen ist ausschließlich die Neusynthese. Die bereits", size=12.5)
t.text(528, 881, "carboxylierten Faktoren im Plasma arbeiten weiter, bis sie", size=12.5)
t.text(528, 900, "abgebaut sind — beim Faktor II dauert das etwa drei Tage.", size=12.5)
t.text(528, 923, "Bei akuter Blutung nützt Vitamin K deshalb wenig; man", size=12.5)
t.text(528, 942, "ersetzt die Faktoren direkt durch ein Prothrombin-", size=12.5)
t.text(528, 961, "komplexkonzentrat.", size=12.5)

t.kasten(20, 1000, 960, 96, fill="var(--warn-bg)", stroke=W)
t.text(38, 1022, "DIE PRÜFUNGSFALLE", size=11, gewicht=700, farbe=W)
t.text(38, 1044, "Protein C und Protein S sind ebenfalls Vitamin-K-abhängig und haben eine kürzere "
                 "Halbwertszeit als die Gerinnungsfaktoren. Zu Beginn einer", size=12.5)
t.text(38, 1063, "Cumarintherapie fallen die Gerinnungshemmer deshalb zuerst aus — daraus die "
                 "vorübergehend prokoagulatorische Phase und die Cumarinnekrose.", size=12.5)

t.kasten(20, 1120, 960, 96, fill="var(--surface-2)")
t.text(38, 1142, "WELCHE FAKTOREN BETROFFEN SIND", size=11, gewicht=700, farbe=G)
t.text(38, 1164, "II, VII, IX und X, dazu Protein C, S und Z. Merkhilfe: 1972 — die vier Ziffern "
                 "sind die Faktoren. Faktor VII hat die kürzeste Halbwertszeit und", size=12.5)
t.text(38, 1183, "bestimmt deshalb den frühen INR-Anstieg, Faktor II die eigentliche "
                 "antithrombotische Wirkung.", size=12.5)

# ===================================================== Ausgabe
ARIA = (
    "Vitamin K in drei Zonen. Zone A zeigt die Gamma-Carboxylierung an echten Strukturen: Ein "
    "Alkoxid zieht mit einem Elektronenpaarpfeil das Gamma-Wasserstoffatom eines Glutamatrests "
    "ab, dessen Saeurestaerke mit einem pKa um 28 eigentlich zu gering dafuer ist; das "
    "entstehende Carbanion greift Kohlendioxid an, und es entsteht Gamma-Carboxyglutamat mit "
    "zwei Carboxylatgruppen an einem Kohlenstoff. Zone B zeigt den Vitamin-K-Zyklus mit "
    "gezeichneten Strukturen: Das Hydrochinon reagiert mit Sauerstoff ueber eine "
    "Peroxid-Zwischenstufe; dabei entsteht das Alkoxid, das in Zone A als Base wirkt, und es "
    "bleibt das Vitamin-K-2,3-Epoxid zurueck. Die Epoxidreduktase VKORC1 fuehrt es ueber das "
    "Chinon zum Hydrochinon zurueck; genau diese beiden Schritte hemmen die Cumarine. Zone C "
    "erklaert Antidotwirkung, Wirklatenz und die Rolle von Protein C und S."
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
daten["m15"] = t.svg(ARIA)
io.open(ZIEL, "w", encoding="utf-8").write(
    json.dumps(daten, ensure_ascii=False, indent=1))
print("geschrieben: tafeln.json / m15  (%d Zeichen, %d Molekuele, %d Pfeile)"
      % (len(daten["m15"]), len(t.mole), len(t.anker)))
