# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 6 : Cofaktoren.

Vitamine und Coenzyme

Eintragsform:  "id": ("SMILES", {dummy-index: "Beschriftung"})
"""

# --- Reihen: verwandte Strukturen, die nebeneinanderstehen, teilen Lage und
#     Massstab.  REIHEN[name] = dict(vorlage=SMILES, muster=SMARTS, bindung=px)
#     muster ist freiwillig; ohne es sucht der Builder die groesste gemeinsame
#     Teilstruktur selbst.  bindung setzt eine feste Bindungslaenge, damit das
#     laengste Glied nicht geschrumpft wird.
#
#     Die Namen tragen das Praefix "t6-", weil REIHEN ueber alle Teile hinweg in
#     einen Topf laufen und ein doppelt vergebener Name den fremden Teil still
#     umhaengen wuerde.
#
#     Alle Reihen dieses Teils haben dieselbe Bindungslaenge (17 px). Nur so
#     stimmen die Groessenverhaeltnisse auch zwischen zwei Reihen, die in
#     derselben Kaskade nebeneinanderstehen - etwa Thiamin/TPP neben
#     Riboflavin/FMN.
_BL = 17.0

# Thiamin -> TPP: das ganze Vitamin ist gemeinsam, nur das Diphosphat kommt hinzu.
_M_THIAMIN = "Cc1ncc(C[n+]2csc(CCO)c2C)c(N)n1"

# B6: Ring, beide exocyclischen C-Atome und das Phenol-OH sind allen drei
# Vitameren gemeinsam; was an C4 und C5 haengt, bleibt frei beweglich.
_M_B6 = "Cc1ncc(C)c(C)c1O"

# Isoniazid gegen Pyridoxal: beide tragen die Acylgruppe para zum Ring-N.
# Ueber dieselbe Vorlage (PLP) landen Hydrazid und Aldehyd in gleicher Lage.
_M_ACYLPYRIDIN = "C(=O)c1ccncc1"

# Riboflavin -> FMN: Isoalloxazin samt Ribitylkette; nur das Phosphat kommt dazu.
_M_FLAVIN = "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[CH](O)[CH](O)[CH](O)CO)c2cc1C"

# Pantothensaeure -> CoA und Nicotinamid -> NAD+: der Vitaminteil wird
# festgehalten, der angebaute Nucleotidteil darf sich legen, wie er mag.
_M_PANTO = "CC(C)(CO)C(O)C(=O)NCCC"
_M_NIACIN = "[#7][#6](=[#8])[#6]1:[#6]:[#6]:[#6]:[#7]:[#6]:1"

# Biotin -> Carboxybiotin: der ganze Bicyclus samt Valeriansaeurerest.
_M_BIOTIN = "O=C1NC2CSC(CCCCC(=O)O)C2N1"

# Liponsaeure -> Dihydroliponsaeure: nur die Saeurekette wird festgehalten.
# Wuerde man die Schwefelatome mitfixieren, zwaenge man die offene Form in die
# Ringlage des Dithiolans.
_M_LIPON = "OC(=O)CCCCC"

# Retinoide: Ring und Polyenkette bis einschliesslich C13. C14, C15 und die
# Kopfgruppe bleiben frei - sonst wuerde die 13-cis-Doppelbindung des
# Isotretinoins in die trans-Lage der Vorlage gezwungen und der Knick, um
# dessentwillen die vier Bilder nebeneinanderstehen, verschwaende.
_M_RETINOID = "CC1=C(C=CC(C)=CC=CC(C))C(C)(C)CCC1"

# Naphthochinon: der Chinonkern mit der 2-Methylgruppe. [CH3] statt C, weil
# sonst auch die Phytylkette des Phyllochinons als "Methyl" durchgeht und das
# Muster zweideutig wird.
_M_NAPHTHOCHINON = "[CH3]C1=CC(=O)c2ccccc2C1=O"

# Chromanol bzw. 4-Hydroxycumarin: Reihen mit einem einzigen Glied. Sie tragen
# keine Ausrichtung bei, sondern nur die feste Bindungslaenge, damit Tocopherol
# und Phenprocoumon in derselben Kaskade nicht groesser gezeichnet werden als
# die Retinoide und das Menadion daneben.
_M_CHROMANOL = "Cc1c(C)c2c(c(C)c1O)CCC(C)O2"
_M_CUMARIN = "c1c(O)c2ccccc2oc1=O"

# Methotrexat gegen Folsaeure: 31 der 33 Schweratome sind gleich (rdFMCS,
# CompareAny). Uebrig bleiben genau die beiden Unterschiede - 4-Amino statt
# 4-Oxo und die N10-Methylgruppe -, und die sind nur bei deckungsgleicher Lage
# als Unterschied zu erkennen.
_M_ANTIFOLAT = (
    "[#7&!R]-&!@[#6]1:&@[#7]:&@[#6]2:&@[#7]:&@[#6]:&@[#6](:&@[#7]:&@[#6]:&@2"
    ":&@[#6]:&@[#7]:&@1)-&!@[#6&!R]-&!@[#7&!R]-&!@[#6]1:&@[#6]:&@[#6]:&@[#6]"
    "(:&@[#6]:&@[#6]:&@1)-&!@[#6&!R](=&!@[#8&!R])-&!@[#7&!R]-&!@[#6&!R]"
    "(-&!@[#6&!R]-&!@[#6&!R]-&!@[#6&!R](=&!@[#8&!R])-&!@[#8&!R])-&!@[#6&!R]"
    "(=&!@[#8&!R])-&!@[#8&!R]"
)

REIHEN = {
    "t6-thiamin": dict(
        vorlage="Cc1ncc(C[n+]2csc(CCOP(=O)(O)OP(=O)(O)O)c2C)c(N)n1",
        muster=_M_THIAMIN, bindung=_BL),
    # Vorlage ist PLP (steht in strukturen/teil2.py). Pyridoxin und Pyridoxal
    # legen sich darauf, damit in 6.2 und 6.4 dasselbe Ringbild steht.
    "t6-b6": dict(
        vorlage="Cc1ncc(COP(=O)(O)O)c(C=O)c1O",
        muster=_M_B6, bindung=_BL),
    "t6-inh": dict(
        vorlage="Cc1ncc(COP(=O)(O)O)c(C=O)c1O",
        muster=_M_ACYLPYRIDIN, bindung=_BL),
    "t6-flavin": dict(
        vorlage="Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)O)c2cc1C",
        muster=_M_FLAVIN, bindung=_BL),
    "t6-panto": dict(
        vorlage="SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O",
        muster=_M_PANTO, bindung=_BL),
    "t6-niacin": dict(
        vorlage="NC(=O)c1ccc[n+](c1)[C@@H]1O[C@H](COP(=O)([O-])OP(=O)(O)OC[C@H]2O[C@@H](n3cnc4c(N)ncnc43)[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O",
        muster=_M_NIACIN, bindung=_BL),
    "t6-biotin": dict(
        vorlage="OC(=O)N1[C@H]2CS[C@@H](CCCCC(=O)O)[C@H]2NC1=O",
        muster=_M_BIOTIN, bindung=_BL),
    "t6-lipon": dict(
        vorlage="OC(=O)CCCC[C@@H]1CCSS1",
        muster=_M_LIPON, bindung=_BL),
    "t6-retinoid": dict(
        vorlage="CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C(=O)O)C(C)(C)CCC1",
        muster=_M_RETINOID, bindung=_BL),
    "t6-naphthochinon": dict(
        vorlage="CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c2ccccc2C1=O",
        muster=_M_NAPHTHOCHINON, bindung=_BL),
    "t6-chromanol": dict(
        vorlage="Cc1c(C)c2c(c(C)c1O)CC[C@@](C)(CCC[C@H](C)CCC[C@H](C)CCCC(C)C)O2",
        muster=_M_CHROMANOL, bindung=_BL),
    "t6-cumarin": dict(
        vorlage="CCC(c1ccccc1)c1c(O)c2ccccc2oc1=O",
        muster=_M_CUMARIN, bindung=_BL),
    # Vorlage ist die Folsaeure, nicht das Methotrexat: mit dem Methotrexat als
    # Vorlage legt CoordGen die Glutamatkette der Folsaeure trotzdem neu und
    # meldet das nicht. Umgekehrt sitzen beide Bilder deckungsgleich.
    "t6-antifolat": dict(
        vorlage="Nc1nc2ncc(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)nc2c(=O)[nH]1",
        muster=_M_ANTIFOLAT, bindung=_BL),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
#
# In 6.2 beantwortet die Farbe eine einzige Frage: Wo steckt in der Coenzymform
# noch das Vitamin, das man gegessen hat? Deshalb traegt dort jeweils das
# Coenzym die Farbe "gerippe", das Vitamin daneben bleibt grau. Bei den kleinen
# Paaren (B6) ist der Unterschied ohne Farbe zu sehen; dort bleibt es grau.
SCHMUCK = {
    # --- 6.2 Vitamin und Coenzymform
    "thiamin":            dict(reihe="t6-thiamin"),
    "tpp":                dict(reihe="t6-thiamin", hervor={"gerippe": _M_THIAMIN}),
    "riboflavin":         dict(reihe="t6-flavin"),
    "fmn":                dict(reihe="t6-flavin", hervor={"gerippe": _M_FLAVIN}),
    "pyridoxin":          dict(reihe="t6-b6"),
    # PLP wird in strukturen/teil2.py definiert und steht auch in
    # src/30_teil2.html. Dort ist es eine Einzelkachel, die Ausrichtung schadet
    # ihr nicht; Farbe bekommt es deshalb keine.
    "plp":                dict(reihe="t6-b6"),
    "pantothensaeure":    dict(reihe="t6-panto"),
    "coa":                dict(reihe="t6-panto", hervor={"gerippe": _M_PANTO}),
    "nicotinamid":        dict(reihe="t6-niacin"),
    "nad":                dict(reihe="t6-niacin", hervor={"gerippe": _M_NIACIN}),
    "biotin":             dict(reihe="t6-biotin"),
    # Hier lautet die Frage anders: was haengt die Carboxylase an? Also "neu",
    # und zwar nur der Carboxylkohlenstoff mit seinen beiden Sauerstoffen -
    # das N1' selbst war schon da.
    "carboxybiotin":      dict(reihe="t6-biotin",
                               hervor={"neu": "[CX3;$(C(=O)(O)[NX3])](=[OX1])[OX2H1]"}),
    "liponsaeure":        dict(reihe="t6-lipon", hervor={"stelle": "[#16]"}),
    "dihydroliponsaeure": dict(reihe="t6-lipon", hervor={"stelle": "[#16]"}),

    # --- 6.3 fettloesliche Vitamine
    "retinol":            dict(reihe="t6-retinoid"),
    "retinal":            dict(reihe="t6-retinoid", hervor={"stelle": "[CH]=O"}),
    "tretinoin":          dict(reihe="t6-retinoid", hervor={"neu": "[CX3](=O)[OX2H1]"}),
    # Nur die eine cis-Doppelbindung, nicht die Carboxylgruppe daneben: genau
    # sie unterscheidet Isotretinoin von Tretinoin.
    "isotretinoin":       dict(reihe="t6-retinoid",
                               hervor={"stelle": "[CX3;$(*([CH3])=[CX3][CX3](=O)[OX2H1])]"
                                                 "=[CX3H;$(*=[CX3][CH3])]"}),
    "tocopherol":         dict(reihe="t6-chromanol"),
    # Phyllochinon steht auch in src/39b_teil7.html. Dort ist der Epoxidzyklus
    # das Thema, hier der fehlende Phytylrest des Menadions - eine Farbe waere
    # nur in einer der beiden Kaskaden richtig, also bleibt es grau.
    "phyllochinon":       dict(reihe="t6-naphthochinon"),
    "menadion":           dict(reihe="t6-naphthochinon"),
    "phenprocoumon":      dict(reihe="t6-cumarin"),

    # --- 6.4 Arzneistoffe am Cofaktornetz
    "isoniazid":          dict(reihe="t6-inh", hervor={"stelle": "C(=O)[NH][NH2]"}),
    "pyridoxal":          dict(reihe="t6-b6", hervor={"stelle": "[CH]=O"}),
    # Genau die beiden Atome, die Folsaeure nicht hat: das 4-Amino-N und der
    # N10-Methylkohlenstoff. Beides Einzelatome - sie fallen nur auf, weil die
    # beiden Bilder deckungsgleich liegen.
    "methotrexat":        dict(reihe="t6-antifolat",
                               hervor={"neu": "[$([NX3H2][c;$(c(:n):c)]),"
                                              "$([CH3][NX3]([c])[CH2])]"}),
    "folsaeure":          dict(reihe="t6-antifolat"),
}

MOLS = {
    # ===================== TEIL 6 : Cofaktoren =====================
    # -- wasserloesliche
    "thiamin":         ("Cc1ncc(C[n+]2csc(CCO)c2C)c(N)n1", None),
    "tpp":             ("Cc1ncc(C[n+]2csc(CCOP(=O)(O)OP(=O)(O)O)c2C)c(N)n1", None),
    "riboflavin":      ("Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)CO)c2cc1C", None),
    "fmn":             ("Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)O)c2cc1C", None),
    "nicotinsaeure":   ("OC(=O)c1cccnc1", None),
    "nicotinamid":     ("NC(=O)c1cccnc1", None),
    "pantothensaeure": ("CC(C)(CO)[C@@H](O)C(=O)NCCC(=O)O", None),
    "coa":             ("SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O", None),
    "pyridoxin":       ("Cc1ncc(CO)c(CO)c1O", None),
    "pyridoxal":       ("Cc1ncc(CO)c(C=O)c1O", None),
    # D-Biotin ist (3aS,4S,6aR): alle drei Ringwasserstoffe stehen cis auf
    # derselben Seite des Bicyclus.  YBJHBAHKTGYVGT-ZKWXMUAHSA-N
    "biotin":          ("O=C1N[C@H]2CS[C@@H](CCCCC(=O)O)[C@H]2N1", None),
    # gleiche Ringverknuepfung wie Biotin.  WGIRSTDPYSLVEB-ZKWXMUAHSA-N
    "carboxybiotin":   ("OC(=O)N1[C@H]2CS[C@@H](CCCCC(=O)O)[C@H]2NC1=O", None),
    "dhf":             ("Nc1nc2NCC(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)=Nc2c(=O)[nH]1", None),

    # -- nicht-Vitamin-Cofaktoren
    "dehydroascorbat": ("OC[C@H](O)[C@H]1OC(=O)C(=O)C1=O", None),
    "liponsaeure":     ("OC(=O)CCCC[C@@H]1CCSS1", None),
    "dihydroliponsaeure": ("OC(=O)CCCC[C@@H](S)CCS", None),

    # -- fettloesliche
    "retinol":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/CO)C(C)(C)CCC1", None),
    "retinal":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C=O)C(C)(C)CCC1", None),
    "tretinoin":       ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C(=O)O)C(C)(C)CCC1", None),
    # Isotretinoin ist ausschliesslich 13-cis, also (2Z,4E,6E,8E) - genau eine
    # Z-Doppelbindung.  SHGAZHPCJJPHSC-XFYACQKRSA-N
    "isotretinoin":    ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C\\C(=O)O)C(C)(C)CCC1", None),
    # RRR-alpha-Tocopherol, das natuerliche Vitamin E: C2 ist R.
    # GVJHHUAWPYXKBD-IEOSBIPESA-N
    "tocopherol":      ("Cc1c(C)c2c(c(C)c1O)CC[C@@](C)(CCC[C@H](C)CCC[C@H](C)CCCC(C)C)O2", None),
    "phyllochinon":    ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c2ccccc2C1=O", None),
    "vitk_hydrochinon": ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)c(O)c2ccccc2c1O", None),
    "menadion":        ("CC1=CC(=O)c2ccccc2C1=O", None),

    # -- Wirkstoffe am Cofaktornetz
    "isoniazid":       ("O=C(NN)c1ccncc1", None),
    "warfarin":        ("CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),
    "phenprocoumon":   ("CCC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),
}
