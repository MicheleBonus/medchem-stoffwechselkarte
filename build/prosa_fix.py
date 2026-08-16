# -*- coding: utf-8 -*-
"""
Ersetzt rhetorisch ueberladene Formulierungen durch sachliche Darstellung.
Matcht whitespace-tolerant, damit Zeilenumbrueche in der Quelle egal sind.
"""
import io
import os
import re
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

R = [
# ---------------------------------------------------------------- Kopf
("00_head.html",
 """Rund zweihundert körpereigene Wirkstoffe — Neurotransmitter, Hormone, Mediatoren,
  Cofaktoren — entstammen einer Handvoll biosynthetischer Wurzeln. Wer die Wurzeln kennt, muss die
  Blätter nicht auswendig lernen. Und weil an jedem Verzweigungsenzym ein Arzneistoff sitzt, ist
  dieselbe Karte zugleich die Karte des Prüfungsstoffs.""",
 """Neurotransmitter, Hormone, Mediatoren und Cofaktoren lassen sich auf eine überschaubare Zahl
  biosynthetischer Ausgangsstoffe zurückführen. Diese Unterlage ordnet sie nach ihrer Herkunft
  statt nach Organsystemen und verzeichnet an jedem Syntheseschritt Enzym, Cofaktor, Regulation
  und die dort angreifenden Arzneistoffe."""),

# ---------------------------------------------------------------- Teil 0
("10_teil0.html",
 """Der Körper baut seine Signalmoleküle nicht aus zweihundert Ausgangsstoffen,
    sondern aus fünf. Alles Weitere ist Verzweigung — und jede Verzweigung ist ein Enzym, an dem
    ein Arzneistoff angreift.""",
 """Fünf Ausgangsstoffe genügen, um sämtliche körpereigenen Signalmoleküle aufzubauen. Alles
    Weitere sind Verzweigungen, und jede Verzweigung wird von einem Enzym katalysiert, an dem
    Arzneistoffe angreifen."""),

("10_teil0.html",
 """Diese Karte ist die Landkarte des gesamten Skripts. Lesen Sie sie einmal von links nach
    rechts: links die Wurzel, in der Mitte das Enzym, das die Verzweigung erzwingt, rechts das
    Produkt. Die Enzyme in der Mitte sind nicht Beiwerk — sie sind der Prüfungsstoff. Wenn Sie
    später im Examen gefragt werden, warum Carbidopa nicht ins Gehirn darf oder warum Allopurinol
    ausgerechnet an der Xanthin-Oxidase ansetzt, dann steht die Antwort in dieser mittleren Spalte.""",
 """Die Karte ist von links nach rechts zu lesen: links der Ausgangsstoff, in der Mitte das
    verzweigende Enzym, rechts die Produktklasse. Die mittlere Spalte trägt den größten Teil des
    prüfungsrelevanten Stoffs, weil sich dort die Angriffspunkte der Arzneistoffe befinden."""),

("10_teil0.html",
 """warum das Cofaktor-Netz keine eigene Zeile verdient hätte: es speist alle vier anderen Wurzeln
    zugleich. Ein B₆-Mangel trifft deshalb nicht einen Stoffwechselweg, sondern gleichzeitig die
    Catecholamin-, GABA-, Häm- und Cystein-Synthese — das ist der Grund, warum Isoniazid ohne
    Pyridoxin-Substitution eine Polyneuropathie auslöst.""",
 """warum das Cofaktor-Netz quer zu den übrigen vier liegt: es speist sie alle. Ein B₆-Mangel
    trifft daher gleichzeitig die Catecholamin-, GABA-, Häm- und Cystein-Synthese. Isoniazid, das
    Pyridoxalphosphat bindet, löst ohne Pyridoxin-Substitution eine Polyneuropathie aus."""),

("10_teil0.html",
 """<b>Wie Sie mit dieser Karte lernen</b>
      <p>Zeichnen Sie sie einmal aus dem Kopf nach. Wenn Sie an einer Stelle stocken, fehlt Ihnen
      nicht eine Vokabel, sondern ein Zusammenhang — und genau dort schlagen Sie im entsprechenden
      Teil nach. Das ist effizienter als jede Karteikarte, weil die Karte selbst die Fehlerdiagnose
      übernimmt.</p>""",
 """<b>Arbeit mit der Karte</b>
      <p>Die Karte einmal aus dem Gedächtnis nachzuzeichnen zeigt zuverlässig an, welche Kapitel
      noch nachzuarbeiten sind: Wo die Rekonstruktion stockt, fehlt in der Regel kein Einzelfakt,
      sondern der Zusammenhang.</p>"""),

("10_teil0.html",
 """drei sicher hat, kann sich die Hälfte der Karte herleiten statt sie zu erinnern.""",
 """drei Operationen und ihre Cofaktoren kennt, kann einen großen Teil der Karte herleiten."""),

# ---------------------------------------------------------------- Teil 1
("20_teil1.html",
 """Dreißig Moleküle Acetyl-CoA ergeben ein Molekül Cholesterol, und aus
    Cholesterol wird alles, was der Körper an Steroiden besitzt. Der Weg dorthin ist die am
    besten beforschte Biosynthese der Medizinischen Chemie — weil an fast jedem seiner Schritte
    eine Arzneistoffklasse hängt.""",
 """Achtzehn Moleküle Acetyl-CoA ergeben ein Molekül Cholesterol, und aus Cholesterol gehen
    sämtliche Steroide des Körpers hervor. An mehreren Schritten dieses Weges greifen
    therapeutisch genutzte Wirkstoffklassen an."""),

("20_teil1.html",
 """Die ersten drei Schritte sehen aus wie eine gewöhnliche Claisen-Kondensation
    plus Reduktion — und genau das sind sie auch. Entscheidend ist der dritte: Die HMG-CoA-Reduktase
    ist das geschwindigkeitsbestimmende Enzym der gesamten Cholesterolbiosynthese und damit das
    Target der meistverordneten Arzneistoffklasse überhaupt.""",
 """Die ersten beiden Schritte sind eine Claisen-Kondensation und eine Aldoladdition. Der dritte,
    die Reduktion von HMG-CoA zu Mevalonat, ist geschwindigkeitsbestimmend für die gesamte
    Cholesterolbiosynthese und der Angriffspunkt der Statine."""),

("20_teil1.html",
 """<p>HMG-CoA kommt an <em>zwei</em> Stellen des Stoffwechsels vor, und Prüfungsfragen leben von
      dieser Doppeldeutigkeit. Die <b>cytosolische</b> Synthase""",
 """<p>HMG-CoA tritt an <em>zwei</em> Stellen des Stoffwechsels auf. Die <b>cytosolische</b> Synthase"""),

("20_teil1.html",
 """<p>Daraus folgt unmittelbar: Statine hemmen die Ketogenese <em>nicht</em>. Sie greifen ein
      cytosolisches Enzym an, während die Ketonkörperbildung mitochondrial abläuft und über die
      Lyase, nicht die Reduktase, weitergeführt wird. Wer das im Examen sauber trennt, hat die Frage
      schon gewonnen.</p>""",
 """<p>Statine hemmen die Ketogenese daher nicht: Sie greifen ein cytosolisches Enzym an, während
      die Ketonkörperbildung mitochondrial abläuft und über die Lyase weitergeführt wird.</p>"""),

("20_teil1.html",
 """Ab hier zählt der Körper in Fünfergruppen. IPP ist der aktivierte
    Isopren-Baustein; jede Verlängerung ist dieselbe Reaktion — eine elektrophile Alkylierung, bei
    der ein Allyl-Kation aus DMAPP das nucleophile Alken des IPP angreift. Dass hier auch die
    Bisphosphonate ansetzen, überrascht viele Studierende, ist aber die Erklärung für deren
    Wirkmechanismus am Osteoklasten.""",
 """Ab hier verläuft der Aufbau in C₅-Einheiten. IPP ist der aktivierte Isopren-Baustein; jede
    Kettenverlängerung ist eine elektrophile Alkylierung, bei der ein Allyl-Kation aus DMAPP das
    Alken des IPP angreift. An der Farnesyl-diphosphat-Synthase dieses Wegs greifen die
    Bisphosphonate an."""),

("20_teil1.html",
 """Der spektakulärste Schritt der gesamten Biochemie steht hier: Die
    Oxidosqualen-Cyclase faltet ein völlig flexibles Kettenmolekül in eine Sesselkonformation und
    löst eine <b>kationische Kaskadenzyklisierung</b> aus, die in einem einzigen Schritt vier Ringe
    und sieben Stereozentren erzeugt — stereospezifisch, ohne jeden Cofaktor.""",
 """Die Oxidosqualen-Cyclase faltet das offenkettige Squalenepoxid in eine definierte Konformation
    und löst eine <b>kationische Kaskadenzyklisierung</b> aus. In einem Schritt entstehen vier Ringe
    und sieben Stereozentren, stereospezifisch und ohne Cofaktor."""),

("20_teil1.html",
 """<p>Merken Sie sich die Richtung der Fragestellung: Nicht „welches Enzym fehlt dem Menschen“,
      sondern „wie groß ist der Affinitätsunterschied“. Das gilt für Antimykotika ebenso wie für
      Antibiotika mit humanen Homologen.</p>""",
 """<p>Maßgeblich ist also nicht das Fehlen eines Enzyms beim Menschen, sondern die Größe des
      Affinitätsunterschieds zwischen den Isoformen. Dasselbe gilt für antibakterielle Wirkstoffe
      mit humanen Homologen.</p>"""),

("20_teil1.html",
 """Alle fünf Steroidhormonklassen entstehen aus einem einzigen Vorläufer:
    Pregnenolon. Welche davon eine Zelle produziert, entscheidet allein darüber, welche
    CYP-Enzyme sie exprimiert. Die Zona glomerulosa besitzt CYP11B2 und macht Aldosteron, die Zona
    fasciculata besitzt CYP17A1 und CYP11B1 und macht Cortisol, das Ovar besitzt CYP19A1 und macht
    Estradiol. Es ist derselbe Weg — nur unterschiedlich abgeschnitten.""",
 """Alle Steroidhormonklassen gehen auf Pregnenolon zurück. Welche davon eine Zelle bildet, hängt
    allein davon ab, welche CYP-Enzyme sie exprimiert: Die Zona glomerulosa besitzt CYP11B2 und
    bildet Aldosteron, die Zona fasciculata CYP17A1 und CYP11B1 und bildet Cortisol, das Ovar
    CYP19A1 und bildet Estradiol. Der Syntheseweg ist derselbe und wird lediglich an
    unterschiedlicher Stelle beendet."""),

("20_teil1.html",
 """Vitamin D ist chemisch kein Vitamin, sondern ein <b>Secosteroid</b> — ein
    Steroid, dessen Ring B aufgebrochen ist. Der Bruch geschieht photochemisch, nicht enzymatisch,
    und das macht diesen Ast einzigartig: Es ist der einzige Schritt im gesamten Skript, dessen
    „Cofaktor“ ein Photon ist.""",
 """Vitamin D ist chemisch ein <b>Secosteroid</b>, also ein Steroid mit geöffnetem Ring B. Die
    Ringöffnung erfolgt photochemisch statt enzymatisch: eine konrotatorische Elektrocyclisierung
    unter UV-B, gefolgt von einer [1,7]-sigmatropen Wasserstoffverschiebung."""),

("20_teil1.html",
 """Der Mensch kann den Steroidkern nicht abbauen. Die einzige Möglichkeit,
    Cholesterol wieder loszuwerden, ist die Umwandlung in Gallensäuren und deren Ausscheidung —
    und genau hier setzen die Gallensäurebinder therapeutisch an.""",
 """Der Mensch kann das Steroidgerüst nicht zu CO₂ abbauen. Cholesterol wird deshalb überwiegend
    nach Umwandlung in Gallensäuren ausgeschieden; an diesem Kreislauf setzen die
    Gallensäurebinder an."""),

("20_teil1.html",
 """Drei kleinere Äste, die im Examen regelmäßig auftauchen, weil sie
    Nebenwirkungen erklären.""",
 """Zwei kleinere Äste, die zur Beurteilung von Nebenwirkungen gebraucht werden."""),

("20_teil1.html",
 """populäre Erklärung für Statin-Myopathien. Der klinische Beweis für einen Nutzen der
    Q₁₀-Substitution steht allerdings bis heute aus; die Myopathie korreliert besser mit
    SLCO1B1-Polymorphismen, also mit der hepatischen Aufnahme.""",
 """gängige Erklärung für Statin-Myopathien. Ein Nutzen der Q₁₀-Substitution ist allerdings nicht
    belegt; die Myopathie korreliert besser mit SLCO1B1-Polymorphismen, also mit der hepatischen
    Aufnahme."""),

# ---------------------------------------------------------------- Teil 2
("30_teil2.html",
 """<h2>Vier Ringe, aus denen fast das ganze Nervensystem spricht</h2>""",
 """<h2>Die biogenen Amine und ihre Vorstufen</h2>"""),

("30_teil2.html",
 """Phenylalanin, Tyrosin, Tryptophan und Histidin. Aus diesen vier
    Aminosäuren entstehen sämtliche biogenen Amine — und mit ihnen die Angriffspunkte von
    Antidepressiva, Neuroleptika, Antiparkinsonmitteln, Antihistaminika, Triptanen und
    Thyreostatika. Kein anderer Teil dieses Skripts hat eine höhere Prüfungsdichte.""",
 """Aus Phenylalanin, Tyrosin, Tryptophan und Histidin entstehen sämtliche biogenen Amine. Die
    Enzyme dieser Wege sind die Angriffspunkte von Antidepressiva, Antipsychotika,
    Antiparkinsonmitteln, Antihistaminika, Triptanen und Thyreostatika."""),

("30_teil2.html",
 """<b>Das Bauprinzip, das alles trägt</b>""",
 """<b>Das gemeinsame Bauprinzip</b>"""),

("30_teil2.html",
 """<b>PLP-abhängig</b> (Pyridoxal-5′-phosphat). Wer im Examen „Vitamin B₆“ an eine Hydroxylase
      schreibt, verliert den Punkt. <a class="mref" href="#m01">M-01</a> zeigt, warum PLP das kann,
      was es kann.</p>""",
 """<b>PLP-abhängig</b> (Pyridoxal-5′-phosphat); diese Zuordnung wird häufig vertauscht.
      Tafel <a class="mref" href="#m01">M-01</a> zeigt, worauf die Vielseitigkeit des PLP beruht.</p>"""),

("30_teil2.html",
 """Tyrosin ist die einzige der vier, die der Körper selbst herstellen kann —
    aus Phenylalanin. Fällt dieser eine Schritt aus, entsteht die bekannteste angeborene
    Stoffwechselerkrankung überhaupt.""",
 """Tyrosin ist die einzige der vier Aminosäuren, die der Körper selbst bilden kann, und zwar aus
    Phenylalanin. Der Ausfall dieses Schritts führt zur Phenylketonurie."""),

("30_teil2.html",
 """<p>Der klinische Unterschied ist dramatisch, und er folgt direkt aus der Karte: BH₄ ist""",
 """<p>Der klinische Unterschied ergibt sich aus der Cofaktorbilanz: BH₄ ist"""),

("30_teil2.html",
 """<p>Merksatz: <b>Diät hilft nur bei der PAH-Form.</b> Deshalb gehört zum Neugeborenenscreening
      zwingend die Differenzierung über Pterinausscheidung und DHPR-Aktivität.</p>""",
 """<p>Eine phenylalaninarme Diät ist somit nur bei der PAH-Form ausreichend. Zum
      Neugeborenenscreening gehört deshalb die Differenzierung über Pterinausscheidung und
      DHPR-Aktivität.</p>"""),

("30_teil2.html",
 """Vier Enzyme, vier verschiedene Cofaktoren, und an jedem einzelnen hängt ein
    Arzneistoff. Wenn Sie eine Kaskade dieses Skripts vollständig beherrschen sollten, dann diese.""",
 """Vier aufeinanderfolgende Enzyme mit vier verschiedenen Cofaktoren. An jedem von ihnen greift
    mindestens ein therapeutisch eingesetzter Wirkstoff an."""),

("30_teil2.html",
 """<p>Die Kompartimentierung dieser vier Schritte ist eine beliebte Prüfungsfrage, weil sie
      pharmakologisch folgenreich ist. TH und AADC arbeiten im <b>Cytosol</b>.""",
 """<p>Die Kompartimentierung der vier Schritte ist pharmakologisch folgenreich. TH und AADC
      arbeiten im <b>Cytosol</b>."""),

("30_teil2.html",
 """<p>Zweite Falle: <b>Dopamin ist achiral.</b> Erst die DBH führt das Stereozentrum ein.
      Steinhilber hebt das in Abb. 3.3 eigens hervor, und es wird gern abgefragt.</p>""",
 """<p>Zu beachten ist außerdem, dass <b>Dopamin achiral</b> ist; das Stereozentrum wird erst
      durch die DBH eingeführt.</p>"""),

("30_teil2.html",
 """also nur die periphere AADC. Genau diese Asymmetrie ist der ganze Trick. Die Bioverfügbarkeit
      von Levodopa steigt dadurch von etwa 33 % auf 80–98 %.</p>""",
 """also nur die periphere AADC. Die Bioverfügbarkeit von Levodopa steigt dadurch von etwa 33 %
      auf 80–98 %.</p>"""),

("30_teil2.html",
 """Zwei Enzyme, zwei Reihenfolgen, vier Metaboliten. Diese Verzweigung ist
    vermutlich die am häufigsten falsch beantwortete Frage des gesamten Themengebiets — weil beide
    Wege zum selben Endprodukt führen, aber über verschiedene Zwischenstufen.""",
 """Zwei Enzyme, zwei mögliche Reihenfolgen, vier Metaboliten. Beide Wege führen zum selben
    Endprodukt, aber über unterschiedliche Zwischenstufen."""),

("30_teil2.html",
 """<p>Daraus folgt die gesamte Sicherheitslogik dieser Substanzklasse: <b>Selektive
      MAO-B-Hemmer</b>""",
 """<p>Daraus ergeben sich die Sicherheitsanforderungen der Substanzklasse. <b>Selektive
      MAO-B-Hemmer</b>"""),

("30_teil2.html",
 """<p>Entacapon und Tolcapon sind beide Nitrocatechole, und das ist kein Zufall. Die
      Catecholgruppe""",
 """<p>Entacapon und Tolcapon sind Nitrocatechole. Die Catecholgruppe"""),

("30_teil2.html",
 """Derselbe Ausgangsstoff, ein völlig anderes Enzym: Die <b>Tyrosinase</b> ist
    ein Kupferenzym und leistet beides — die Hydroxylierung von Tyrosin zu DOPA <em>und</em> dessen
    Oxidation zum Dopachinon. Ab da läuft die Raper-Mason-Sequenz weitgehend spontan.""",
 """Die <b>Tyrosinase</b> ist ein Kupferenzym und katalysiert zwei Reaktionen am selben aktiven
    Zentrum: die Hydroxylierung von Tyrosin zu DOPA und dessen Oxidation zum Dopachinon. Die
    anschließende Raper-Mason-Sequenz verläuft weitgehend spontan."""),

("30_teil2.html",
 """Der ungewöhnlichste Weg des ganzen Skripts: Die Synthese läuft nicht an
    freiem Tyrosin ab, sondern an Tyrosylresten <em>innerhalb</em> des Proteins Thyreoglobulin —
    extrazellulär, im Kolloid des Follikels. Erst die Proteolyse setzt das fertige Hormon frei.""",
 """Die Synthese läuft nicht an freiem Tyrosin ab, sondern an Tyrosylresten des Thyreoglobulins,
    und zwar extrazellulär im Kolloid des Follikels. Das fertige Hormon wird erst durch Proteolyse
    freigesetzt."""),

("30_teil2.html",
 """Formal derselbe Zweischritt wie beim Tyrosin — Hydroxylierung, dann
    Decarboxylierung, sogar mit demselben Enzym AADC. Danach folgen zwei weitere Schritte, die
    aus einem Neurotransmitter ein Hormon der inneren Uhr machen.""",
 """Hydroxylierung und Decarboxylierung wie beim Tyrosin, im zweiten Schritt sogar durch dasselbe
    Enzym. Zwei weitere Schritte führen vom Neurotransmitter Serotonin zum Hormon Melatonin."""),

("30_teil2.html",
 """circadian gesteuert und durch Licht supprimiert. Deshalb ist Melatonin ein chemisches
      <em>Dunkelsignal</em>, kein Schlafsignal.</p>""",
 """circadian gesteuert und durch Licht supprimiert. Melatonin signalisiert damit Dunkelheit und
      nicht Schlafbedürfnis.</p>"""),

("30_teil2.html",
 """Mengenmäßig ist der Serotoninast eine Randerscheinung: Über 95 % des
    Tryptophans laufen in den Kynureninweg. Dessen Endprodukt ist kein Neurotransmitter, sondern
    <b>NAD⁺</b> — und damit die Verbindung zwischen einer Aminosäure und einem Vitamin.""",
 """Über 95 % des Tryptophans werden über den Kynureninweg abgebaut; der Serotoninast ist
    mengenmäßig gering. Endprodukt des Kynureninwegs ist <b>NAD⁺</b>, womit dieser Weg den
    Aminosäure- mit dem Vitaminstoffwechsel verbindet."""),

("30_teil2.html",
 """<p>Dritter Zusammenhang, den Prüfer gern verknüpfen: Die Umrechnung <b>60 mg Tryptophan ≙
      1 mg Niacin-Äquivalent</b>.""",
 """<p>Damit hängt eine dritte Größe zusammen, die Umrechnung <b>60 mg Tryptophan ≙ 1 mg
      Niacin-Äquivalent</b>."""),

("30_teil2.html",
 """Der kürzeste Weg des Skripts: ein einziger Schritt. Interessant ist hier
    nicht die Synthese, sondern der Abbau — weil er über zwei völlig verschiedene Enzyme läuft und
    das die Histaminintoleranz erklärt.""",
 """Die Synthese besteht aus einem einzigen Schritt. Bemerkenswert ist der Abbau: Er verläuft über
    zwei verschiedene Enzyme in verschiedenen Kompartimenten und erklärt die Histaminintoleranz."""),

("30_teil2.html",
 """<b>Zwei Abbauwege, zwei Orte, eine Krankheit</b>""",
 """<b>Zwei Abbauwege in zwei Kompartimenten</b>"""),

("30_teil2.html",
 """<p>Chemisch merkenswert: Histamin besitzt <b>zwei basische Zentren</b>""",
 """<p>Histamin besitzt <b>zwei basische Zentren</b>"""),

# ---------------------------------------------------------------- Teil M
("40_mech.html",
 """Jeder Pfeil in diesem Skript ist einer von wenigen wiederkehrenden
    Elektronenverschiebungen. Die Tafeln lehren jede davon einmal; die Syntheseschritte verlinken
    darauf zurück. Hier die ersten beiden — die mit dem größten Erklärwert.""",
 """Die Syntheseschritte dieser Unterlage beruhen auf einer begrenzten Zahl wiederkehrender
    Elektronenverschiebungen. Jede wird einmal dargestellt; die Schritttabellen verweisen darauf.
    Die ersten beiden Tafeln liegen vor."""),

("40_mech.html",
 """Warum dasselbe Molekül einmal decarboxyliert, einmal transaminiert und
    einmal β-eliminiert: Es ist nicht das Coenzym, das entscheidet, sondern das Enzym — durch den
    Winkel, in dem es das Substrat festhält.""",
 """Ob dasselbe Coenzym decarboxyliert, transaminiert oder β-eliminiert, bestimmt das Apoenzym
    über den Winkel, in dem es das Substrat festhält."""),

("40_mech.html",
 """<h3>Flavin — und warum Selegilin sein eigenes Enzym tötet</h3>""",
 """<h3>Flavin und die Suizidinhibition der Monoaminoxidase</h3>"""),

("40_mech.html",
 """FAD kann etwas, das NAD⁺ nicht kann: Ein-Elektronen-Chemie. Genau daraus
    folgt der Wirkmechanismus der MAO-B-Hemmer — nicht als Vokabel, sondern zwingend.""",
 """FAD kann im Gegensatz zu NAD⁺ einzelne Elektronen übertragen. Daraus ergibt sich der
    Wirkmechanismus der irreversiblen MAO-B-Hemmer."""),

("40_mech.html",
 """B · SUIZIDINHIBITION — DIE PROPARGYLGRUPPE ALS FALLE""",
 """B · SUIZIDINHIBITION DURCH DIE PROPARGYLGRUPPE"""),

("40_mech.html",
 """<text x="20" y="316" font-size="12.5">Selegilin und Rasagilin sind ganz normale Substrate — bis zu
        dem Moment, in dem das Enzym sie oxidiert. Dann wird aus dem Substrat der Sprengsatz.</text>""",
 """<text x="20" y="316" font-size="12.5">Selegilin und Rasagilin sind zunächst gewöhnliche Substrate.
        Erst die Oxidation durch das Enzym erzeugt aus ihnen einen Michael-Akzeptor.</text>"""),

("40_mech.html",
 """irreversibel — das Enzym ist tot</text>""",
 """irreversibel inaktiviert</text>"""),

("40_mech.html",
 """π-Ebene stellt. Das ist die gesamte Erklärung dafür, warum ein einziger Cofaktor in vier
    Kapiteln dieses Skripts auftaucht — bei der Catecholaminsynthese (2.2.2), im Kynureninweg
    (2.7), bei GABA und bei der Häm-Synthese.""",
 """π-Ebene stellt. Damit erklärt sich, warum derselbe Cofaktor in mehreren Kapiteln auftritt:
    bei der Catecholaminsynthese (2.2.2), im Kynureninweg (2.7), bei GABA und bei der
    Häm-Synthese."""),

("40_mech.html",
 """unteren, was Selegilin daraus macht. Der entscheidende Punkt für die Prüfung: Die Propargylgruppe
    ist kein zufälliges Strukturmerkmal, sondern die notwendige Voraussetzung dafür, dass nach der
    Oxidation ein Michael-Akzeptor entsteht, den das nucleophile N5 angreift.""",
 """untere den Verlauf mit Selegilin. Die Propargylgruppe ist dabei Voraussetzung dafür, dass nach
    der Oxidation ein Michael-Akzeptor entsteht, den das nucleophile N5 angreift."""),

# ---------------------------------------------------------------- Fuss
("99_foot.html",
 """<p>Dieses Dokument ist die erste Etappe. Fertig sind die Meta-Karte, die vollständige C₂-Wurzel
    mit Steroidogenese und die aromatische Aminosäure-Wurzel mit allen acht Ästen — zusammen
    <b>113 Strukturformeln</b>, rund 60 dokumentierte Syntheseschritte und zwei
    Mechanismus-Tafeln.</p>""",
 """<p>Fertig sind die Übersichtskarte, die C₂-Wurzel mit der Steroidogenese und die aromatische
    Aminosäure-Wurzel mit allen acht Ästen, zusammen <b>113 Strukturformeln</b>, rund 60
    dokumentierte Syntheseschritte und zwei Mechanismus-Tafeln.</p>"""),
]

# Kastenpaare nebeneinander stellen
PAIRS = [
    ("20_teil1.html", "Prüfungsfalle · zwei HMG-CoA-Synthasen"),
    ("30_teil2.html", "Prüfungsfalle · das Vesikel als Ortsangabe"),
    ("30_teil2.html", "Prüfungsfalle · der Cheese-Effekt und warum er MAO-A betrifft"),
]


def loose(s):
    """Regex, der beliebige Whitespace-Laeufe toleriert."""
    return re.compile(r"\s+".join(re.escape(p) for p in s.split()))


def main():
    files = {}
    misses = 0
    for fn, old, new in R:
        p = os.path.join(SRC, fn)
        if fn not in files:
            files[fn] = io.open(p, encoding="utf-8").read()
        rx = loose(old)
        if not rx.search(files[fn]):
            print("NICHT GEFUNDEN in %s: %s ..." % (fn, " ".join(old.split())[:70]))
            misses += 1
            continue
        files[fn] = rx.sub(lambda m: new, files[fn], count=1)

    for fn, title in PAIRS:
        p = os.path.join(SRC, fn)
        if fn not in files:
            files[fn] = io.open(p, encoding="utf-8").read()
        rx = re.compile(r'<div class="spalte">(\s*<div class="falle">\s*<b>'
                        + re.escape(title) + r'</b>)')
        if not rx.search(files[fn]):
            print("PAAR NICHT GEFUNDEN in %s: %s" % (fn, title))
            misses += 1
            continue
        files[fn] = rx.sub(r'<div class="boxen">\1', files[fn], count=1)

    for fn, s in files.items():
        io.open(os.path.join(SRC, fn), "w", encoding="utf-8").write(s)

    print("\nDateien geschrieben: %d   Fehlschlaege: %d" % (len(files), misses))
    sys.exit(1 if misses else 0)


if __name__ == "__main__":
    main()
