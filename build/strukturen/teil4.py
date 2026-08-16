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
REIHEN = {}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
SCHMUCK = {}

MOLS = {
    # ===================== TEIL 4 : Lipidmediatoren =====================
    # -- Vorstufe und COX-Ast
    "arachidonsaeure": ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    "epa":             ("CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    "pgg2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)OO", None),
    "pgh2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)O", None),
    "pge2":            ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)CC(=O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgd2":            ("CCCCC[C@@H](O)/C=C/[C@H]1C(=O)C[C@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgf2a":           ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)C[C@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgi2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](C[C@H]2[C@@H]1C/C(=C\\CCCC(=O)O)/O2)O)O", None),
    "txa2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H](O1)O[C@@H]2C/C=C\\CCCC(=O)O)O", None),
    "txb2":            ("CCCCC[C@@H](O)/C=C/[C@H]1O[C@H](O)C[C@@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),

    # -- LOX-Ast
    "hpete5":          ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](OO)CCCC(=O)O", None),
    "hete5":           ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](O)CCCC(=O)O", None),
    "lta4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@H]1O[C@@H]1CCCC(=O)O", None),
    "ltb4":            ("CCCCC/C=C\\C[C@@H](O)/C=C/C=C/C=C\\[C@@H](O)CCCC(=O)O", None),
    "ltc4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](NC(=O)CC[C@H](N)C(=O)O)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "ltd4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lte4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lipoxina4":       ("CCCCC[C@H](O)/C=C/C=C\\C=C\\C=C\\[C@@H](O)[C@@H](O)CCCC(=O)O", None),

    # -- Endocannabinoide und PAF
    "anandamid":       ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)NCCO", None),
    "ag2":             ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)OC(CO)CO", None),
    "paf":             ("CCCCCCCCCCCCCCCCOC[C@@H](OC(C)=O)COP(=O)([O-])OCC[N+](C)(C)C", None),
    "thc":             ("CCCCCc1cc(O)c2c(c1)OC(C)(C)[C@@H]1CCC(C)=C[C@H]21", None),
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
    "montelukast":     ("CC(C)(O)c1ccccc1CC[C@H](SCC1(CC1)CC(=O)O)c1cccc(/C=C/c2ccc3ccc(Cl)cc3n2)c1", None),
    "misoprostol":     ("CCCC[C@](C)(O)C/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1CCCCCCC(=O)OC", None),
    "alprostadil":     ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)CC(=O)[C@@H]1CCCCCCC(=O)O", None),
    "latanoprost":     ("CC(C)OC(=O)CCC/C=C\\C[C@H]1[C@@H](O)C[C@@H](O)[C@@H]1CC[C@@H](O)CCc1ccccc1", None),
}
