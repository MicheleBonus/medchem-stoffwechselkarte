# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 7 : Peptid- und Proteohormone.

Peptidwirkstoffe und Proteasehemmer

Eintragsform:  "id": ("SMILES", {dummy-index: "Beschriftung"})
"""

MOLS = {
    # ===================== TEIL 7 : Peptid- und Proteohormone =====================
    # -- RAAS und Kinine
    # Captopril ist (2S)-1-[(2S)-2-Methyl-3-sulfanylpropanoyl]pyrrolidin-2-
    # carbonsaeure.  Das (R)-Diastereomer am Thiolkohlenstoff ist Epicaptopril
    # und am Zink des ACE um Groessenordnungen schwaecher.
    # InChIKey FAKRSMQSSFJEIM-RQJHMYQMSA-N
    "captopril":       ("C[C@H](CS)C(=O)N1CCC[C@H]1C(=O)O", None),
    "enalapril":       ("CCOC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", None),
    "enalaprilat":     ("OC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", None),
    "lisinopril":      ("NCCCC[C@H](N[C@@H](CCc1ccccc1)C(=O)O)C(=O)N1CCC[C@H]1C(=O)O", None),
    "losartan":        ("CCCCc1nc(Cl)c(CO)n1Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1", None),
    "valsartan":       ("CCCCC(=O)N(Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1)[C@@H](C(C)C)C(=O)O", None),
    # Sacubitril = 4-{[(2S,4R)-5-Ethoxy-4-methyl-5-oxo-1-(4-phenylphenyl)-
    # pentan-2-yl]amino}-4-oxobutansaeure.  Der Ethylester haengt am
    # methyltragenden C4; zwischen C2 (Amid-Stickstoff) und C4 steht eine CH2.
    # InChIKey PYNXFZCZUAOOQC-UTKZUKDTSA-N
    "sacubitril":      ("CCOC(=O)[C@H](C)C[C@@H](Cc1ccc(-c2ccccc2)cc1)NC(=O)CCC(=O)O", None),

    # -- Opioidpeptide und ihre kleinmolekularen Verwandten
    "morphin":         ("CN1CC[C@]23[C@H]4Oc5c(O)ccc(C[C@@H]1[C@@H]2C=C[C@@H]4O)c35", None),
    "naloxon":         ("C=CCN1CC[C@]23[C@H]4Oc5c(O)ccc(C[C@@H]1[C@]2(O)CCC4=O)c35", None),

    # -- Gerinnung und Vitamin K
    "gla":             ("OC(=O)C(C(=O)O)C[C@H](N)C(=O)O", None),
    "vitk_epoxid":     ("CC12OC1(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c1ccccc1C2=O", None),
    # Tranexamsaeure ist die trans-konfigurierte Verbindung; nur so stehen
    # Aminomethyl und Carboxyl diaequatorial und passen in die Lysin-Tasche
    # des Plasminogens.  InChIKey GYDJEQRTZSCIOI-LJGSYFOKSA-N
    "tranexamsaeure":  ("NC[C@H]1CC[C@@H](CC1)C(=O)O", None),
    "rivaroxaban":     ("O=C(NC[C@H]1CN(c2ccc(N3CCOCC3=O)cc2)C(=O)O1)c1ccc(Cl)s1", None),
}


# --- Reihen: verwandte Strukturen, die nebeneinanderstehen, teilen Lage und
#     Massstab.  REIHEN[name] = dict(vorlage=SMILES, muster=SMARTS, bindung=px)
#     muster ist freiwillig; ohne es sucht der Builder die groesste gemeinsame
#     Teilstruktur selbst.  bindung setzt eine feste Bindungslaenge, damit das
#     laengste Glied nicht geschrumpft wird.
_BINDUNG = 17.0

# Das N-Acylprolin ist der gemeinsame Nenner aller vier ACE-Hemmer: Amid,
# Pyrrolidin und die Prolin-Carbonsaeure, die im Enzym die S2'-Tasche besetzt.
# Trifft captopril, enalapril, enalaprilat und lisinopril je genau einmal.
_ACYLPROLIN = "[#6]-[#6](=[#8])-[#7]1-[#6]-[#6]-[#6]-[#6]-1-[#6](=[#8])-[#8]"

# Biphenyl mit Tetrazol: das Erkennungsmotiv der Sartane am AT1-Rezeptor.
_BIPHENYL_TETRAZOL = "c1ccc(-c2ccccc2-c2nn[nH]n2)cc1"
_BIPHENYL = "c1ccc(-c2ccccc2)cc1"

REIHEN = {
    # Vorlage ist Lisinopril, das groesste Glied.  Damit steht das Acylprolin
    # in allen vier Bildern gleich, und der wechselnde Zinkligand (Thiol gegen
    # Carboxylat) faellt als Einziges auf.
    "ace": dict(vorlage=MOLS["lisinopril"][0], muster=_ACYLPROLIN,
                bindung=_BINDUNG),
    "sartan": dict(vorlage=MOLS["valsartan"][0], muster=_BIPHENYL_TETRAZOL,
                   bindung=_BINDUNG),
    # Sacubitril traegt dasselbe Biphenyl wie die Sartane, aber kein Tetrazol.
    # Eigene Reihe, gleiche Vorlage: so liegt sein Biphenyl dort, wo bei
    # Valsartan das Biphenyl liegt, und der Massstab bleibt derselbe.
    "biaryl": dict(vorlage=MOLS["valsartan"][0], muster=_BIPHENYL,
                   bindung=_BINDUNG),
    # Morphin und Naloxon teilen das 4,5-Epoxymorphinan bis auf den Ring C.
    "morphinan": dict(vorlage=MOLS["naloxon"][0], bindung=_BINDUNG),
}


# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.

# Der Ethylrest des Prodrug-Esters, als Einzelatome getroffen, damit der
# Carbonylkohlenstoff nicht mitgefaerbt wird: er bleibt beim Wirkstoff.
_ESTER_ETHYL = ("[$([CH3][CH2][OX2][CX3]=O),"
                "$([CH2]([CH3])[OX2][CX3]=O),"
                "$([OX2]([CH2][CH3])[CX3]=O)]")

# Die freie Carbonsaeure am Kohlenstoff neben dem offenkettigen Amin: das ist
# der Zinkligand der Carboxylat-Hemmer.  Die Prolin-Saeure sitzt am Ring und
# wird durch [CX4;!R][NX3;!R] ausgeschlossen.
_ZINK_CARBOXYLAT = ("[$([CX3](=O)([OX2H1])[CX4;!R][NX3;!R]),"
                    "$([OX1]=[CX3]([OX2H1])[CX4;!R][NX3;!R]),"
                    "$([OX2H1][CX3](=O)[CX4;!R][NX3;!R])]")

SCHMUCK = {
    # 7.5 Wirkstoffgalerie: was das Zink greift, und was beim Prodrug abgeht.
    "captopril":   dict(reihe="ace", hervor={"stelle": "[CH2][SX2H]"}),
    "enalapril":   dict(reihe="ace", hervor={"weg": _ESTER_ETHYL}),
    "enalaprilat": dict(reihe="ace", hervor={"stelle": _ZINK_CARBOXYLAT}),
    "lisinopril":  dict(reihe="ace", hervor={"stelle": _ZINK_CARBOXYLAT}),
    "losartan":    dict(reihe="sartan", hervor={"gerippe": "c1nn[nH]n1"}),
    "valsartan":   dict(reihe="sartan", hervor={"gerippe": "c1nn[nH]n1"}),
    "sacubitril":  dict(reihe="biaryl", hervor={"weg": _ESTER_ETHYL}),

    # 7.3 Opioide: der Allylrest am Stickstoff kehrt die Wirkung um.
    "morphin":     dict(reihe="morphinan"),
    "naloxon":     dict(reihe="morphinan", hervor={"neu": "[CH2]=[CH][CH2]"}),

    # 7.7 Gerinnung: die zweite Carboxylgruppe des Gla stammt von der
    # Vitamin-K-abhaengigen Carboxylase.  Indizes statt SMARTS, weil die beiden
    # Carboxylgruppen am C4 konstitutionell gleich sind und ein SMARTS
    # zwangslaeufig beide traefe.
    "gla":         dict(hervor={"neu": [4, 5, 6]}),
    # Der Epoxidsauerstoff ist das, was die VKOR wieder abraeumen muss.
    "vitk_epoxid": dict(hervor={"neu": "[#8;r3]"}),
}
