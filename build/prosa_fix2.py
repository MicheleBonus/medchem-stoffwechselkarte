# -*- coding: utf-8 -*-
"""Zweiter Durchgang: rhetorisch gesetzte Gedankenstriche und Restfloskeln."""
import io
import os
import re
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

R = [
# ---------------------------------------------------------------- Teil 0
("10_teil0.html",
 """Achten Sie beim Durchgehen auf drei wiederkehrende chemische Grundoperationen.""",
 """Beim Durchgehen fallen drei wiederkehrende chemische Grundoperationen auf."""),

# ---------------------------------------------------------------- Teil 1
("20_teil1.html",
 """<b>Warum Statine so wirken, wie sie wirken</b>""",
 """<b>Statine als Übergangszustandsanaloga</b>"""),

("20_teil1.html",
 """<p>Lactonstatine wie Simvastatin und Lovastatin sind <b>Prodrugs</b> — erst die Hydrolyse des
      Lactonrings zur offenkettigen β-Hydroxysäure erzeugt die aktive Form.""",
 """<p>Lactonstatine wie Simvastatin und Lovastatin sind <b>Prodrugs</b>; erst die Hydrolyse des
      Lactonrings zur offenkettigen β-Hydroxysäure erzeugt die aktive Form."""),

("20_teil1.html",
 """<b>Geranylgeranyl-PP</b> — und damit der posttranslationalen Prenylierung kleiner GTPasen""",
 """<b>Geranylgeranyl-PP</b>, und damit der posttranslationalen Prenylierung kleiner GTPasen"""),

("20_teil1.html",
 """Knochen an. Das ist der Grund für die extrem lange Verweildauer und die Möglichkeit
      wöchentlicher oder jährlicher Gabe.""",
 """Knochen an. Daraus erklären sich die lange Verweildauer und die Möglichkeit wöchentlicher
      oder jährlicher Gabe."""),

("20_teil1.html",
 """Genau deshalb sind die unerwünschten Wirkungen der Azole dosisabhängig
      endokrin — Ketoconazol hemmt in höherer Dosis auch das humane CYP17A1 und CYP11A1 und wurde
      historisch sogar als Antiandrogen eingesetzt.""",
 """Die unerwünschten Wirkungen der Azole sind deshalb dosisabhängig endokrin:
      Ketoconazol hemmt in höherer Dosis auch das humane CYP17A1 und CYP11A1 und wurde historisch
      als Antiandrogen eingesetzt."""),

("20_teil1.html",
 """<td>im Fettgewebe exprimiert — erklärt die Estrogenlast bei Adipositas</td>""",
 """<td>im Fettgewebe exprimiert; erklärt die Estrogenlast bei Adipositas</td>"""),

("20_teil1.html",
 """<p>Das ist der Grund, warum Abirateron als CYP17A1-Hemmer die Androgensynthese ausschaltet und
      zugleich einen Mineralocorticoid-Exzess auslöst:""",
 """<p>Abirateron schaltet als CYP17A1-Hemmer daher die Androgensynthese aus und löst zugleich
      einen Mineralocorticoid-Exzess aus:"""),

("20_teil1.html",
 """<p>Die 25-Hydroxylierung in der Leber ist praktisch unreguliert — deshalb ist
      <b>25-OH-D₃ (Calcidiol)</b> der Laborparameter für den Versorgungszustand.""",
 """<p>Die 25-Hydroxylierung in der Leber ist praktisch unreguliert; <b>25-OH-D₃ (Calcidiol)</b>
      ist deshalb der Laborparameter für den Versorgungszustand."""),

("20_teil1.html",
 """Deshalb ist Calcitriol <em>kein</em> geeigneter Parameter für einen
      Vitamin-D-Mangel — es kann bei Mangel durch PTH-Anstieg sogar normal oder erhöht sein.""",
 """Calcitriol ist deshalb <em>kein</em> geeigneter Parameter für einen Vitamin-D-Mangel; bei
      Mangel kann es durch den PTH-Anstieg sogar normal oder erhöht sein."""),

# ---------------------------------------------------------------- Teil 2
("30_teil2.html",
 """<b>Warum Levodopa und nicht Dopamin — und warum Carbidopa dazu muss</b>""",
 """<b>Levodopa statt Dopamin, und die Rolle des Decarboxylase-Hemmers</b>"""),

("30_teil2.html",
 """<td><b>im Vesikelinneren</b> — Dopamin muss erst über VMAT2 hinein</td>""",
 """<td><b>im Vesikelinneren</b>; Dopamin muss erst über VMAT2 hinein</td>"""),

("30_teil2.html",
 """<td><b>cytosolisch</b> — Noradrenalin muss das Vesikel wieder verlassen; Expression durch
              Cortisol aus dem Nebennierenrinden-Portalblut induziert</td>""",
 """<td><b>cytosolisch</b>; Noradrenalin muss das Vesikel wieder verlassen. Expression durch
              Cortisol aus dem Nebennierenrinden-Portalblut induziert</td>"""),

("30_teil2.html",
 """entleert deshalb nicht nur die Speicher, sondern verhindert bereits
      die Noradrenalinsynthese — das Dopamin kommt gar nicht erst an sein Enzym.""",
 """entleert deshalb nicht nur die Speicher, sondern verhindert bereits die Noradrenalinsynthese:
      Das Dopamin gelangt gar nicht erst an sein Enzym."""),

("30_teil2.html",
 """Peripherie zu Dopamin decarboxyliert — mit Übelkeit und Hypotonie als Folge, und ohne
      Wirkung im ZNS.""",
 """Peripherie zu Dopamin decarboxyliert, mit Übelkeit und Hypotonie als Folge und ohne Wirkung
      im ZNS."""),

("30_teil2.html",
 """Die Enzyme sind dieselben, nur ihre
    Reihenfolge unterscheidet sich — und daraus folgt, welcher Metabolit im Liquor oder Urin
    ansteigt, wenn man eines der beiden hemmt.""",
 """Die Enzyme sind dieselben, nur ihre Reihenfolge unterscheidet sich. Daraus folgt, welcher
    Metabolit im Liquor oder Urin ansteigt, wenn eines der beiden gehemmt wird."""),

("30_teil2.html",
 """erfordern keine Diätrestriktion — der reversible Hemmer
      wird vom Tyramin schlicht vom Enzym verdrängt.""",
 """erfordern keine Diätrestriktion; der reversible Hemmer wird vom Tyramin vom Enzym verdrängt."""),

("30_teil2.html",
 """Die Catecholgruppe
      ist für die Bindung ins aktive Zentrum essenziell — sie koordiniert dasselbe
      <b>Mg²⁺</b>, das im physiologischen Fall das Substrat ausrichtet.""",
 """Die Catecholgruppe ist für die Bindung ins aktive Zentrum essenziell; sie koordiniert dasselbe
      <b>Mg²⁺</b>, das im physiologischen Fall das Substrat ausrichtet."""),

("30_teil2.html",
 """<b>Tolcapon</b> überschreitet die Blut-Hirn-Schranke, wirkt stärker —
      ist aber wegen fulminanter Hepatotoxizität Reservemittel mit Leberwertkontrolle.""",
 """<b>Tolcapon</b> überschreitet die Blut-Hirn-Schranke und wirkt stärker, ist aber wegen
      fulminanter Hepatotoxizität Reservemittel mit Leberwertkontrolle."""),

("30_teil2.html",
 """<b>Eumelanin oder Phäomelanin — die Cysteinweiche</b>""",
 """<b>Eumelanin oder Phäomelanin: die Cystein-Weiche</b>"""),

("30_teil2.html",
 """Der MC1R-Rezeptor steuert
      dieses Verhältnis — Varianten mit gestörter MC1R-Funktion erklären rotes Haar und die
      erhöhte UV-Empfindlichkeit.""",
 """Der MC1R-Rezeptor steuert dieses Verhältnis; Varianten mit gestörter MC1R-Funktion erklären
      rotes Haar und die erhöhte UV-Empfindlichkeit."""),

("30_teil2.html",
 """verschiebt der Körper die Bilanz zugunsten von DIO3 — daraus resultiert das Low-T₃-Syndrom""",
 """verschiebt der Körper die Bilanz zugunsten von DIO3; daraus resultiert das Low-T₃-Syndrom"""),

("30_teil2.html",
 """rasch und nahezu vollständig zu
      Thiamazol hydrolysiert — 10 mg Carbimazol entsprechen etwa 6–7 mg Thiamazol.""",
 """rasch und nahezu vollständig zu Thiamazol hydrolysiert; 10 mg Carbimazol entsprechen etwa
      6–7 mg Thiamazol."""),

("30_teil2.html",
 """<b>Zwei Acylierungsstellen, zwei Enzyme — und die Reihenfolge ist fest</b>""",
 """<b>Zwei Modifikationen in fester Reihenfolge</b>"""),

("30_teil2.html",
 """Suchtest beim Karzinoidsyndrom — und der Grund, warum Patienten vor dem Test auf
      serotoninreiche Nahrungsmittel wie Bananen, Walnüsse und Ananas verzichten müssen.""",
 """Suchtest beim Karzinoidsyndrom; deshalb müssen Patienten vor dem Test auf serotoninreiche
      Nahrungsmittel wie Bananen, Walnüsse und Ananas verzichten."""),

("30_teil2.html",
 """wird stattdessen transaminiert und
      cyclisiert — zu <b>Xanthurensäure</b>, die im Urin ausgeschieden wird. Der
      Xanthurensäure-Belastungstest nach Tryptophangabe ist genau deshalb der klassische
      Funktionstest auf B₆-Mangel.""",
 """wird stattdessen transaminiert und zu <b>Xanthurensäure</b> cyclisiert, die im Urin
      ausgeschieden wird. Der Xanthurensäure-Belastungstest nach Tryptophangabe ist deshalb der
      klassische Funktionstest auf B₆-Mangel."""),

("30_teil2.html",
 """zugleich eine gestörte NAD⁺-Bildung aus Tryptophan —
      pellagraähnliche Hauterscheinungen unter INH sind beschrieben.""",
 """zugleich eine gestörte NAD⁺-Bildung aus Tryptophan; pellagraähnliche Hauterscheinungen unter
      INH sind beschrieben."""),

("30_teil2.html",
 """Seitenkettenaminogruppe vor; genau diese Ladung wird am H₁-Rezeptor von Asp107 gebunden.""",
 """Seitenkettenaminogruppe vor; diese Ladung wird am H₁-Rezeptor von Asp107 gebunden."""),
]


def loose(s):
    return re.compile(r"\s+".join(re.escape(p) for p in s.split()))


files, misses = {}, 0
for fn, old, new in R:
    p = os.path.join(SRC, fn)
    if fn not in files:
        files[fn] = io.open(p, encoding="utf-8").read()
    rx = loose(old)
    if not rx.search(files[fn]):
        print("NICHT GEFUNDEN in %s: %s ..." % (fn, " ".join(old.split())[:72]))
        misses += 1
        continue
    files[fn] = rx.sub(lambda m: new, files[fn], count=1)

for fn, s in files.items():
    io.open(os.path.join(SRC, fn), "w", encoding="utf-8").write(s)

print("\nDateien: %d   Fehlschlaege: %d" % (len(files), misses))
sys.exit(1 if misses else 0)
