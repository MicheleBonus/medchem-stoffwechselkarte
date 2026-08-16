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
REIHEN = {}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
SCHMUCK = {}

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
    "biotin":          ("O=C1N[C@@H]2CS[C@@H](CCCCC(=O)O)[C@@H]2N1", None),
    "carboxybiotin":   ("OC(=O)N1[C@@H]2CS[C@@H](CCCCC(=O)O)[C@@H]2NC1=O", None),
    "dhf":             ("Nc1nc2NCC(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)=Nc2c(=O)[nH]1", None),

    # -- nicht-Vitamin-Cofaktoren
    "dehydroascorbat": ("OC[C@H](O)[C@H]1OC(=O)C(=O)C1=O", None),
    "liponsaeure":     ("OC(=O)CCCC[C@@H]1CCSS1", None),
    "dihydroliponsaeure": ("OC(=O)CCCC[C@@H](S)CCS", None),

    # -- fettloesliche
    "retinol":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/CO)C(C)(C)CCC1", None),
    "retinal":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C=O)C(C)(C)CCC1", None),
    "tretinoin":       ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C(=O)O)C(C)(C)CCC1", None),
    "isotretinoin":    ("CC1=C(/C=C/C(C)=C/C=C\\C(C)=C/C(=O)O)C(C)(C)CCC1", None),
    "tocopherol":      ("Cc1c(C)c2c(c(C)c1O)CC[C@](C)(CCC[C@H](C)CCC[C@H](C)CCCC(C)C)O2", None),
    "phyllochinon":    ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c2ccccc2C1=O", None),
    "vitk_hydrochinon": ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)c(O)c2ccccc2c1O", None),
    "menadion":        ("CC1=CC(=O)c2ccccc2C1=O", None),

    # -- Wirkstoffe am Cofaktornetz
    "isoniazid":       ("O=C(NN)c1ccncc1", None),
    "warfarin":        ("CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),
    "phenprocoumon":   ("CCC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),
}
