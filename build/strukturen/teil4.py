# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 4 : Lipidmediatoren.

Arachidonsaeure, Prostanoide, Leukotriene, Endocannabinoide

Eintragsform:  "id": ("SMILES", {dummy-index: "Beschriftung"})
"""

# --- Reihen: verwandte Strukturen, die nebeneinanderstehen, teilen Lage und
#     Massstab.  REIHEN[name] = dict(vorlage=SMILES, muster=SMARTS, bindung=px)
#     muster ist freiwillig; ohne es sucht der Builder die groesste gemeinsame
#     Teilstruktur selbst.  bindung setzt eine feste Bindungslaenge, damit das
#     laengste Glied nicht geschrumpft wird.

# Alle Prostanoidreihen teilen dieselbe Vorlage, damit die Bilder ueber die
# Abschnitte hinweg in derselben Lage stehen. Nur das Muster wechselt, weil
# die Glieder verschieden viel mit PGH2 gemeinsam haben.
_PGH2 = "CCCCC[C@@H](/C=C/[C@H]1[C@H]2C[C@@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)O"

# omega-Kette mit 15-OH, die beiden Ringkohlenstoffe C12/C8 und die alpha-Kette
# bis zur Saeure: trifft auch Thromboxane und Prostacyclin, deren Ring ein
# anderer ist.
_PROSTANOID = ("[#6]-[#6]-[#6]-[#6]-[#6]-[#6](-[#8])-[#6]=[#6]-[#6R]~[#6R]"
               "-[#6]-[#6]=[#6]-[#6]-[#6]-[#6]-[#6](=[#8])-[#8]")
# alpha-Kette C1-C8: das einzige, was die offenkettige Arachidonsaeure mit dem
# geschlossenen Prostanoidgeruest teilt.
_ALPHA = "[#8]-[#6](=[#8])-[#6]-[#6]-[#6]-[#6]=[#6]-[#6]-[#6]"
# alpha-Kette + Cyclopentanring + C13: fuer die Analoga, deren omega-Kette
# umgebaut ist (16-Methyl beim Misoprostol, Phenylrest beim Latanoprost).
_PROSTANRING = "[#8]-[#6](=[#8])-[#6]-[#6]-[#6]-[#6]~[#6]-[#6]-[#6]1~[#6]~[#6]~[#6]~[#6]1-[#6]"
# C1-C20 der Fettsaeurekette; haelt die offenkettigen Eicosanoide zusammen.
_C20 = ("[#8,#7]-[#6](=[#8])-[#6]-[#6]-[#6]-[#6]~[#6]~[#6]~[#6]~[#6]~[#6]"
        "~[#6]~[#6]~[#6]")

REIHEN = {
    # Kaskade 4.2, erster Teil: aus der offenen Kette wird der Bicyclus.
    "cox": dict(vorlage=_PGH2, muster=_ALPHA, bindung=22.0),
    # Kaskade 4.2, zweiter Teil: sechs Mediatoren, ein Bauplan.
    "prostanoid": dict(vorlage=_PGH2, muster=_PROSTANOID, bindung=22.0),
    # Die Prostaglandinanaloga aus der Wirkstoffgalerie in derselben Lage wie
    # ihre Vorbilder; nur so faellt auf, was am Molekuel geaendert wurde.
    "prostanoidanalog": dict(vorlage=_PGH2, muster=_PROSTANRING, bindung=22.0),
    # Kaskaden 4.1, 4.3 und 4.4: alles, was die offene C20-Kette behaelt.
    "eicosanoid": dict(vorlage="CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](NC(=O)CC[C@H](N)C(=O)O)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O",
                       muster=_C20, bindung=22.0),
    # Die sauren Antiphlogistika: Saeurefunktion und Arylrest in gleicher Lage.
    "saure_nsar": dict(vorlage="COc1ccc2c(c1)c(CC(=O)O)c(C)n2C(=O)c1ccc(Cl)cc1",
                       muster="[#8;H1]-[#6](=[#8])-[#6]", bindung=22.0),
    # Die Coxibe: der Sulfonylrest, der in die COX-2-Seitentasche reicht.
    "coxib": dict(vorlage="Cc1ccc(cc1)-c1cc(nn1-c1ccc(cc1)S(N)(=O)=O)C(F)(F)F",
                  muster="[#7,#6]-[#16](=[#8])(=[#8])-c1ccc(cc1)-[a]", bindung=22.0),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.

# Die bisallylische Stelle um C13, an der die Cyclooxygenase das Wasserstoffatom
# abstrahiert; das Radikal liegt danach ueber C11 bis C15. Der rekursive Teil
# haelt die Stelle fest, damit nicht auch die Pentadieneinheiten um C7 und C10
# gefaerbt werden.
_C13 = "[CH]=[CH][CH2;$([CH2][CH]=[CH][CH2][CH2][CH2][CH2][CH3])][CH]=[CH]"
# Sauerstoff am Ring: genau das, was die einzelnen Synthasen aus dem
# Endoperoxid machen. In jedem der sechs Prostanoide etwas anderes.
_RINGSAUERSTOFF = "[#8;$([#8;R]),$([#8]~[#6;R])]"

SCHMUCK = {
    # -- 4.1
    "arachidonsaeure": dict(reihe="eicosanoid"),
    "epa":        dict(reihe="eicosanoid", hervor={"neu": "[CH3][CH2][CH]=[CH]"}),
    # -- 4.2
    "arachidonsaeure_cox": dict(reihe="cox", hervor={"stelle": _C13}),
    "pgg2":       dict(reihe="prostanoid", hervor={"neu": "[#8]-[#8]"}),
    "pgh2":       dict(reihe="prostanoid", hervor={"stelle": "[#8]-[#8]"}),
    "pge2":       dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    "pgd2":       dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    "pgf2a":      dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    "pgi2":       dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    "txa2":       dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    "txb2":       dict(reihe="prostanoid", hervor={"stelle": _RINGSAUERSTOFF}),
    # -- 4.2 Wirkstoffe
    "aspirin":    dict(reihe="saure_nsar", hervor={"weg": "[CH3]-[#6](=[#8])-[#8]"}),
    "ibuprofen":  dict(reihe="saure_nsar"),
    "naproxen":   dict(reihe="saure_nsar"),
    "diclofenac": dict(reihe="saure_nsar"),
    "indometacin": dict(reihe="saure_nsar"),
    "celecoxib":  dict(reihe="coxib", hervor={"stelle": "[#16](=[#8])(=[#8])-[#7]"}),
    "etoricoxib": dict(reihe="coxib", hervor={"stelle": "[CH3]-[#16](=[#8])=[#8]"}),
    "misoprostol": dict(reihe="prostanoidanalog",
                        hervor={"neu": "[OX2H]-[#6]-[CH3]"}),
    "latanoprost": dict(reihe="prostanoidanalog",
                        hervor={"neu": "[CH3]-[CH](-[CH3])-[#8]-[#6]=[#8]"}),
    "alprostadil": dict(reihe="prostanoidanalog"),
    # -- 4.3
    "hpete5":     dict(reihe="eicosanoid", hervor={"neu": "[#8]-[#8]"}),
    "hete5":      dict(reihe="eicosanoid"),
    "lta4":       dict(reihe="eicosanoid", hervor={"stelle": "[#6]1[#8][#6]1"}),
    # Das 12-OH stammt aus dem Wasser, das die Hydrolase auf das Epoxid gibt;
    # der rekursive Teil trennt es vom 5-OH, das in beiden Nachbarn gleich sitzt.
    "ltb4":       dict(reihe="eicosanoid",
                       hervor={"neu": "[OX2H]-[CH;$([CH]([CH]=[CH])[CH2][CH]=[CH])]"}),
    "ltc4":       dict(reihe="eicosanoid",
                       hervor={"weg": "[#8]=[#6](-[#6]-[#6]-[#6](-[#7])-[#6](=[#8])-[#8])"}),
    "ltd4":       dict(reihe="eicosanoid", hervor={"weg": "[#7]-[#6]-[#6](=[#8])-[#8]"}),
    "lte4":       dict(reihe="eicosanoid"),
    "lipoxina4":  dict(reihe="eicosanoid"),
    "zileuton":   dict(hervor={"stelle": "[#7](-[#8])-[#6](=[#8])-[#7]"}),
    # -- 4.4
    "anandamid":  dict(reihe="eicosanoid", hervor={"neu": "[#7]-[#6]-[#6]-[#8]"}),
    "ag2":        dict(reihe="eicosanoid", hervor={"neu": "[#8]-[#6](-[#6]-[#8])-[#6]-[#8]"}),
}

MOLS = {
    # ===================== TEIL 4 : Lipidmediatoren =====================
    # -- Vorstufe und COX-Ast
    "arachidonsaeure": ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    # Dieselbe Saeure, zum COX-Ast hin an PGH2 ausgerichtet: die Kette liegt
    # dort vorgefaltet, so wie der Ringschluss sie braucht. Eine id traegt nur
    # eine Lage, deshalb der zweite Eintrag.
    "arachidonsaeure_cox": ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    "epa":             ("CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    # Achtung Schreibfalle: '[C@@H](O)/C=C/' und '[C@@H](/C=C/...)O' bedeuten an
    # C15 Gegenteiliges. Alle Prostanoide stehen deshalb in der zweiten Form,
    # die den PubChem-Referenzen entspricht (15S).
    "pgg2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@H]2C[C@@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)OO", None),
    "pgh2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@H]2C[C@@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)O", None),
    "pge2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](CC(=O)[C@@H]1C/C=C\\CCCC(=O)O)O)O", None),
    "pgd2":            ("CCCCC[C@@H](/C=C/[C@@H]1[C@H]([C@H](CC1=O)O)C/C=C\\CCCC(=O)O)O", None),
    "pgf2a":           ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](C[C@@H]([C@@H]1C/C=C\\CCCC(=O)O)O)O)O", None),
    "pgi2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](C[C@H]2[C@@H]1C/C(=C/CCCC(=O)O)/O2)O)O", None),
    # 2,6-Dioxabicyclo[3.1.1]heptan: Oxetan + Oxan, nicht zwei Fuenfringe
    "txa2":            ("CCCCC[C@@H](/C=C/[C@@H]1[C@H]([C@@H]2C[C@@H](O2)O1)C/C=C\\CCCC(=O)O)O", None),
    "txb2":            ("CCCCC[C@@H](/C=C/[C@@H]1[C@H]([C@H](CC(O1)O)O)C/C=C\\CCCC(=O)O)O", None),

    # -- LOX-Ast
    "hpete5":          ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](OO)CCCC(=O)O", None),
    "hete5":           ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](O)CCCC(=O)O", None),
    # (5S,6S)-trans-Epoxid. Schreibweise 'C1[C@@H](O1)' - ueber 'C1O[C@@H]1'
    # kehrt sich die Bedeutung der @-Marker um.
    "lta4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@H]1[C@@H](O1)CCCC(=O)O", None),
    "ltb4":            ("CCCCC/C=C\\C[C@@H](O)/C=C/C=C/C=C\\[C@@H](O)CCCC(=O)O", None),
    "ltc4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](NC(=O)CC[C@H](N)C(=O)O)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "ltd4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lte4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lipoxina4":       ("CCCCC[C@H](O)/C=C/C=C\\C=C\\C=C\\[C@@H](O)[C@@H](O)CCCC(=O)O", None),

    # -- Endocannabinoide und PAF
    "anandamid":       ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)NCCO", None),
    "ag2":             ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)OC(CO)CO", None),
    "paf":             ("CCCCCCCCCCCCCCCCOC[C@@H](OC(C)=O)COP(=O)([O-])OCC[N+](C)(C)C", None),
    # trans-verknuepft, (6aR,10aR) - cis waere ein anderes Cannabinoid
    "thc":             ("CCCCCc1cc(O)c2c(c1)OC(C)(C)[C@@H]1CCC(C)=C[C@@H]21", None),
    "rimonabant":      ("Cc1c(-c2ccc(Cl)cc2)n(-c2ccc(Cl)cc2Cl)nc1C(=O)NN1CCCCC1", None),

    # -- Wirkstoffe am Eicosanoidsystem
    "aspirin":         ("CC(=O)Oc1ccccc1C(=O)O", None),
    # als Racemat im Handel; gezeichnet ist das wirksame (S)-Enantiomer
    "ibuprofen":       ("CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O", None),
    "naproxen":        ("COc1ccc2cc(ccc2c1)[C@H](C)C(=O)O", None),
    "diclofenac":      ("OC(=O)Cc1ccccc1Nc1c(Cl)cccc1Cl", None),
    "indometacin":     ("COc1ccc2c(c1)c(CC(=O)O)c(C)n2C(=O)c1ccc(Cl)cc1", None),
    "celecoxib":       ("Cc1ccc(cc1)-c1cc(nn1-c1ccc(cc1)S(N)(=O)=O)C(F)(F)F", None),
    "etoricoxib":      ("Cc1ccc(cn1)-c1ncc(Cl)cc1-c1ccc(cc1)S(C)(=O)=O", None),
    "zileuton":        ("CC(N(O)C(N)=O)c1cc2ccccc2s1", None),
    "montelukast":     ("CC(C)(O)c1ccccc1CC[C@@H](SCC1(CC1)CC(=O)O)c1cccc(/C=C/c2ccc3ccc(Cl)cc3n2)c1", None),
    # C16 bleibt unbestimmt: Misoprostol ist ein Gemisch der beiden 16-Epimere
    "misoprostol":     ("CCCCC(C)(O)C/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1CCCCCCC(=O)OC", None),
    "alprostadil":     ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](CC(=O)[C@@H]1CCCCCCC(=O)O)O)O", None),
    "latanoprost":     ("CC(C)OC(=O)CCC/C=C\\C[C@H]1[C@@H](O)C[C@@H](O)[C@@H]1CC[C@@H](O)CCc1ccccc1", None),
}
