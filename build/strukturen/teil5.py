# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 5 : Kohlenhydrat- und Nucleotidwurzel.

Zucker, Purine, Pyrimidine, cyclische Nucleotide

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
    # ===================== TEIL 5 : Kohlenhydrat- und Nucleotidwurzel =====================
    # -- 5.1 / 5.2 Glucose und Pentosephosphatweg
    "glucose":         ("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "g6p":             ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "fbp":             ("O=P(O)(O)OC[C@H]1O[C@](O)(COP(=O)(O)O)[C@@H](O)[C@@H]1O", None),
    "pyruvat":         ("CC(=O)C(=O)O", None),
    "lactat":          ("C[C@H](O)C(=O)O", None),
    "ribose5p":        ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H]1O", None),
    "prpp":            ("O=P(O)(O)OC[C@H]1O[C@@H](OP(=O)(O)OP(=O)(O)O)[C@H](O)[C@@H]1O", None),

    # -- 5.3 Purine
    "imp":             ("O=c1[nH]cnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]1O", None),
    "amp":             ("Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]1O", None),
    "gmp":             ("Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]1O", None),
    "atp":             ("Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)[C@@H](O)[C@H]1O", None),
    "adp":             ("Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)O)[C@@H](O)[C@H]1O", None),
    "camp":            ("Nc1ncnc2n(cnc12)[C@@H]1O[C@@H]2COP(=O)(O)O[C@H]2[C@H]1O", None),
    "adenosin":        ("Nc1ncnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O", None),
    "inosin":          ("O=c1[nH]cnc2n(cnc12)[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O", None),
    "hypoxanthin":     ("O=c1[nH]cnc2nc[nH]c12", None),
    "xanthin":         ("O=c1[nH]c(=O)c2[nH]cnc2[nH]1", None),
    "harnsaeure":      ("O=c1[nH]c2[nH]c(=O)[nH]c2c(=O)[nH]1", None),
    "coffein":         ("Cn1c(=O)c2c(ncn2C)n(C)c1=O", None),
    "theophyllin":     ("Cn1c(=O)c2[nH]cnc2n(C)c1=O", None),

    # -- 5.4 Pyrimidine
    "carbamoylphosphat": ("NC(=O)OP(=O)(O)O", None),
    "orotat":          ("O=c1cc([nH]c(=O)[nH]1)C(=O)O", None),
    "ump":             ("O=c1ccn([C@@H]2O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]2O)c(=O)[nH]1", None),
    "dump":            ("O=c1ccn([C@H]2C[C@H](O)[C@@H](COP(=O)(O)O)O2)c(=O)[nH]1", None),
    "dtmp":            ("Cc1cn([C@H]2C[C@H](O)[C@@H](COP(=O)(O)O)O2)c(=O)[nH]c1=O", None),

    # -- 5.5 / 5.6 Konjugation und Inositol
    "udp_glucuronat":  ("OC(=O)[C@H]1O[C@@H](OP(=O)(O)OP(=O)(O)OC[C@H]2O[C@@H](n3ccc(=O)[nH]c3=O)[C@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "inositol":        ("O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O", None),
    "ip3":             ("O[C@H]1[C@@H](OP(=O)(O)O)[C@H](O)[C@@H](OP(=O)(O)O)[C@H](O)[C@H]1OP(=O)(O)O", None),
    "dag":             ("CCCCCCCCCCCCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCCCCCCCCCCCC", None),

    # -- Wirkstoffe
    "allopurinol":     ("O=c1[nH]cnc2[nH]ncc12", None),
    "oxypurinol":      ("O=c1[nH]c(=O)[nH]c2[nH]ncc12", None),
    "febuxostat":      ("Cc1nc(-c2ccc(OCC(C)C)c(C#N)c2)sc1C(=O)O", None),
    "probenecid":      ("CCCN(CCC)S(=O)(=O)c1ccc(cc1)C(=O)O", None),
    "colchicin":       ("COc1cc2c(c(OC)c1OC)-c1ccc(OC)c(=O)cc1[C@@H](NC(C)=O)CC2", None),
    "azathioprin":     ("Cn1cnc(c1Sc1ncnc2[nH]cnc12)[N+](=O)[O-]", None),
    "mercaptopurin":   ("S=c1[nH]cnc2[nH]cnc12", None),
    "aciclovir":       ("Nc1nc2c(ncn2COCCO)c(=O)[nH]1", None),
    "tenofovir":       ("C[C@H](Cn1cnc2c(N)ncnc21)OCP(=O)(O)O", None),
    "cytarabin":       ("Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@@H]2O)c(=O)n1", None),
    "gemcitabin":      ("Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)C2(F)F)c(=O)n1", None),
    "leflunomid":      ("Cc1oncc1C(=O)Nc1ccc(cc1)C(F)(F)F", None),
    "teriflunomid":    ("C/C(O)=C(\\C#N)C(=O)Nc1ccc(cc1)C(F)(F)F", None),
    "metformin":       ("CN(C)C(=N)NC(N)=N", None),
    "empagliflozin":   ("OC[C@H]1O[C@@H](c2ccc(Cl)c(Cc3ccc(O[C@H]4CCOC4)cc3)c2)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "glibenclamid":    ("COc1ccc(Cl)cc1C(=O)NCCc1ccc(cc1)S(=O)(=O)NC(=O)NC1CCCCC1", None),
    "sitagliptin":     ("N[C@@H](CC(=O)N1CCn2c(C1)nnc2C(F)(F)F)Cc1cc(F)c(F)cc1F", None),
    "clopidogrel":     ("COC(=O)[C@H](c1ccccc1Cl)N1CCc2sccc2C1", None),
}
