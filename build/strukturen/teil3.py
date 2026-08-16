# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 3 : Nicht-aromatische AS.

GABA, Haem, Stickstoffmonoxid, Glutathion, SAM-Zyklus

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
    # ===================== TEIL 3 : Nicht-aromatische AS =====================
    # -- 3.1 Glutamat / GABA
    "glutamat":        ("N[C@@H](CCC(=O)O)C(=O)O", None),
    "glutamin":        ("N[C@@H](CCC(N)=O)C(=O)O", None),
    "gaba":            ("NCCCC(=O)O", None),
    "succinatsemi":    ("O=CCCC(=O)O", None),
    "succinat":        ("OC(=O)CCC(=O)O", None),
    "ketoglutarat":    ("OC(=O)CCC(=O)C(=O)O", None),
    "glycin":          ("NCC(=O)O", None),
    "gabapentin":      ("NCC1(CC(=O)O)CCCCC1", None),
    "pregabalin":      ("CC(C)C[C@H](CN)CC(=O)O", None),
    # therapeutisch als Racemat; gezeichnet ist das wirksame (R)-(-)-Enantiomer
    "baclofen":        ("NC[C@H](CC(=O)O)c1ccc(Cl)cc1", None),
    "tiagabin":        ("Cc1ccsc1C(=CCCN1CCC[C@@H](C1)C(=O)O)c1sccc1C", None),

    # -- 3.2 Haem / Porphyrine
    "succinyl_coa":    ("OC(=O)CCC(=O)S*", None),
    "ala":             ("NCC(=O)CCC(=O)O", None),
    "porphobilinogen": ("NCc1[nH]cc(CCC(=O)O)c1CC(=O)O", None),
    "protoporphyrin":  ("Cc1c(C=C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(C)c5CCC(O)=O)c(C)c4CCC(O)=O)c(C=C)c3C", None),
    "haem":            ("Cc1c(C=C)c2cc3[nH]c(cc4nc(cc5[nH]c(cc1n2)c(C)c5CCC(O)=O)c(C)c4CCC(O)=O)c(C=C)c3C.[Fe+2]", None),
    "bilirubin":       ("CC1=C(C=C)/C(=C\\C2=C(C)C(CCC(O)=O)=C(N2)CC2=C(CCC(O)=O)C(C)=C(N2)/C=C2\\NC(=O)C(C)=C2C=C)NC1=O", None),
    "biliverdin":      ("CC1=C(C=C)/C(=C\\c2[nH]c(/C=C3\\N=C(/C=C4\\NC(=O)C(C)=C4C=C)C(C)=C3CCC(O)=O)c(CCC(O)=O)c2C)NC1=O", None),

    # -- 3.3 Arginin
    "arginin":         ("N[C@@H](CCCNC(N)=N)C(=O)O", None),
    "noharginin":      ("N[C@@H](CCCNC(N)=NO)C(=O)O", None),
    "citrullin":       ("N[C@@H](CCCNC(N)=O)C(=O)O", None),
    "ornithin":        ("NCCC[C@H](N)C(=O)O", None),
    "putrescin":       ("NCCCCN", None),
    "spermidin":       ("NCCCCNCCCN", None),
    "spermin":         ("NCCCNCCCCNCCCN", None),
    "agmatin":         ("NC(=N)NCCCCN", None),
    "guanidinoacetat": ("NC(=N)NCC(=O)O", None),
    "creatin":         ("CN(CC(=O)O)C(N)=N", None),
    "phosphocreatin":  ("CN(CC(=O)O)C(=N)NP(=O)(O)O", None),
    "creatinin":       ("CN1CC(=O)NC1=N", None),
    "lnmma":           ("CN=C(N)NCCC[C@H](N)C(=O)O", None),
    "eflornithin":     ("NC(CCCN)(C(F)F)C(=O)O", None),
    "cgmp":            ("Nc1nc2n(cnc2c(=O)[nH]1)[C@@H]1O[C@@H]2COP(=O)(O)O[C@H]2[C@H]1O", None),
    "gtn":             ("O=[N+]([O-])OCC(CO[N+](=O)[O-])O[N+](=O)[O-]", None),
    "sildenafil":      ("CCCc1nn(C)c2c1nc([nH]c2=O)-c1cc(ccc1OCC)S(=O)(=O)N1CCN(C)CC1", None),

    # -- 3.4 Cystein / Glutathion / Taurin
    "cystein":         ("N[C@@H](CS)C(=O)O", None),
    "glutathion":      ("N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(=O)O)C(=O)O", None),
    "cysteinsulfinat": ("N[C@@H](CS(=O)O)C(=O)O", None),
    "hypotaurin":      ("NCCS(=O)O", None),
    "taurin":          ("NCCS(=O)(=O)O", None),
    "nac":             ("CC(=O)N[C@@H](CS)C(=O)O", None),
    "paracetamol":     ("CC(=O)Nc1ccc(O)cc1", None),
    "napqi":           ("CC(=O)N=C1C=CC(=O)C=C1", None),

    # -- 3.5 Methionin / SAM-Zyklus
    "methionin":       ("CSCC[C@H](N)C(=O)O", None),
    "homocystein":     ("N[C@@H](CCS)C(=O)O", None),
    "cystathionin":    ("N[C@@H](CCSC[C@H](N)C(=O)O)C(=O)O", None),
    "betain":          ("C[N+](C)(C)CC(=O)[O-]", None),
    "folsaeure":       ("Nc1nc2ncc(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)nc2c(=O)[nH]1", None),
    "thf":             ("Nc1nc2NCC(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)Nc2c(=O)[nH]1", None),
    "methylthf":       ("CN1c2c(NC(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)C1)nc(N)[nH]c2=O", None),
    "methotrexat":     ("CN(Cc1cnc2nc(N)nc(N)c2n1)c1ccc(cc1)C(=O)N[C@@H](CCC(=O)O)C(=O)O", None),
    "trimethoprim":    ("COc1cc(Cc2cnc(N)nc2N)cc(OC)c1OC", None),
    "fluorouracil":    ("O=c1[nH]cc(F)c(=O)[nH]1", None),

    # -- 3.6 Serin / Sphingosin / Cholin
    "serin":           ("N[C@@H](CO)C(=O)O", None),
    "sphingosin":      ("CCCCCCCCCCCCC/C=C/[C@@H](O)[C@@H](N)CO", None),
    "s1p":             ("CCCCCCCCCCCCC/C=C/[C@@H](O)[C@@H](N)COP(=O)(O)O", None),
    "fingolimod":      ("CCCCCCCCc1ccc(CCC(N)(CO)CO)cc1", None),
    "cholin":          ("C[N+](C)(C)CCO", None),
    "acetylcholin":    ("CC(=O)OCC[N+](C)(C)C", None),
}
