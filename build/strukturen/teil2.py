# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 2 : Aromatische AS.

Catecholamine, Serotonin, Melatonin, Schilddruese, Histamin

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
    # ===================== TEIL 2 : Aromatische AS =====================
    "phenylalanin":    ("N[C@@H](Cc1ccccc1)C(=O)O", None),
    "tyrosin":         ("N[C@@H](Cc1ccc(O)cc1)C(=O)O", None),
    "ldopa":           ("N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O", None),
    "dopamin":         ("NCCc1ccc(O)c(O)c1", None),
    "noradrenalin":    ("NC[C@H](O)c1ccc(O)c(O)c1", None),
    "adrenalin":       ("CNC[C@H](O)c1ccc(O)c(O)c1", None),
    "omd":             ("COc1cc(C[C@@H](N)C(=O)O)ccc1O", None),
    "methoxytyramin":  ("COc1cc(CCN)ccc1O", None),
    "dopac":           ("OC(=O)Cc1ccc(O)c(O)c1", None),
    "hva":             ("COc1cc(CC(=O)O)ccc1O", None),
    "normetanephrin":  ("COc1cc(C(O)CN)ccc1O", None),
    "metanephrin":     ("CNC[C@H](O)c1ccc(O)c(OC)c1", None),
    "vma":             ("COc1cc([C@@H](O)C(=O)O)ccc1O", None),
    "tyramin":         ("NCCc1ccc(O)cc1", None),
    "dopachinon":      ("O=C1C(=O)C=C(C[C@@H](N)C(=O)O)C=C1", None),
    "cyclodopa":       ("OC(=O)[C@@H]1Cc2cc(O)c(O)cc2N1", None),
    "dhi":             ("Oc1cc2[nH]ccc2cc1O", None),
    "dhica":           ("OC(=O)c1cc2cc(O)c(O)cc2[nH]1", None),
    "mit":             ("N[C@@H](Cc1ccc(O)c(I)c1)C(=O)O", None),
    "dit":             ("N[C@@H](Cc1cc(I)c(O)c(I)c1)C(=O)O", None),
    "t4":              ("N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)c(I)c1)C(=O)O", None),
    "t3":              ("N[C@@H](Cc1cc(I)c(Oc2ccc(O)c(I)c2)c(I)c1)C(=O)O", None),
    "rt3":             ("N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)cc1)C(=O)O", None),
    "tryptophan":      ("N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O", None),
    "hydroxytryptophan": ("N[C@@H](Cc1c[nH]c2ccc(O)cc12)C(=O)O", None),
    "serotonin":       ("NCCc1c[nH]c2ccc(O)cc12", None),
    "nacetylserotonin": ("CC(=O)NCCc1c[nH]c2ccc(O)cc12", None),
    "melatonin":       ("COc1ccc2[nH]cc(CCNC(C)=O)c2c1", None),
    "hiaa":            ("OC(=O)Cc1c[nH]c2ccc(O)cc12", None),
    "tryptamin":       ("NCCc1c[nH]c2ccccc12", None),
    "formylkynurenin": ("O=CNc1ccccc1C(=O)C[C@H](N)C(=O)O", None),
    "kynurenin":       ("Nc1ccccc1C(=O)C[C@H](N)C(=O)O", None),
    "hydroxykynurenin": ("Nc1c(O)cccc1C(=O)C[C@H](N)C(=O)O", None),
    "hydroxyanthranilat": ("Nc1c(O)cccc1C(=O)O", None),
    "chinolinsaeure":  ("OC(=O)c1cccnc1C(=O)O", None),
    "kynurensaeure":   ("OC(=O)c1cc(O)c2ccccc2n1", None),
    "xanthurensaeure": ("OC(=O)c1cc(O)c2cccc(O)c2n1", None),
    "nad":             ("NC(=O)c1ccc[n+](c1)[C@@H]1O[C@H](COP(=O)([O-])OP(=O)(O)OC[C@H]2O[C@@H](n3cnc4c(N)ncnc43)[C@H](O)[C@@H]2O)[C@@H](O)[C@H]1O", None),
    "histidin":        ("N[C@@H](Cc1c[nH]cn1)C(=O)O", None),
    "histamin":        ("NCCc1c[nH]cn1", None),
    "methylhistamin":  ("Cn1cnc(CCN)c1", None),
    "imidazolessig":   ("OC(=O)Cc1c[nH]cn1", None),
    "urocanat":        ("OC(=O)/C=C/c1c[nH]cn1", None),

    # ===================== Cofaktoren =====================
    "plp":             ("Cc1ncc(COP(=O)(O)O)c(C=O)c1O", None),
    "pmp":             ("Cc1ncc(COP(=O)(O)O)c(CN)c1O", None),
    "bh4":             ("C[C@@H](O)[C@@H](O)[C@H]1CNc2nc(N)[nH]c(=O)c2N1", None),
    "bh4_4a_oh":       ("C[C@@H](O)[C@@H](O)C1CNC2=NC(N)=NC(=O)C2(O)N1", None),
    "bh2":             ("C[C@@H](O)[C@@H](O)C1=Nc2nc(N)[nH]c(=O)c2NC1", None),
    "sam":             ("C[S+](CC[C@H](N)C(=O)[O-])C[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1O", None),
    "sah":             ("N[C@@H](CCSC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1O)C(=O)O", None),
    "fad":             ("Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)OP(=O)(O)OC[C@H]3O[C@@H](n4cnc5c(N)ncnc54)[C@H](O)[C@@H]3O)c2cc1C", None),
    "ascorbat":        ("OC[C@H](O)[C@H]1OC(=O)C(O)=C1O", None),

    # ===================== Wirkstoffe Teil 2 =====================
    "carbidopa":       ("C[C@](NN)(Cc1ccc(O)c(O)c1)C(=O)O", None),
    "benserazid":      ("NC(CO)C(=O)NNCc1ccc(O)c(O)c1O", None),
    "entacapon":       ("CCN(CC)C(=O)/C(C#N)=C/c1cc(O)c(O)c([N+](=O)[O-])c1", None),
    "tolcapon":        ("Cc1ccc(cc1)C(=O)c1cc(O)c(O)c([N+](=O)[O-])c1", None),
    "selegilin":       ("C#CCN(C)[C@H](C)Cc1ccccc1", None),
    "rasagilin":       ("C#CCN[C@@H]1CCc2ccccc21", None),
    "metirosin":       ("C[C@](N)(Cc1ccc(O)cc1)C(=O)O", None),
    "methyldopa":      ("C[C@](N)(Cc1ccc(O)c(O)c1)C(=O)O", None),
    "tranylcypromin":  ("N[C@H]1C[C@@H]1c1ccccc1", None),
    "moclobemid":      ("O=C(NCCN1CCOCC1)c1ccc(Cl)cc1", None),
    "thiamazol":       ("Cn1ccnc1S", None),
    "carbimazol":      ("CCOC(=O)n1ccn(C)c1=S", None),
    "propylthiouracil": ("CCCc1cc(=O)[nH]c(=S)[nH]1", None),
    "fluoxetin":       ("CNCC[C@H](Oc1ccc(cc1)C(F)(F)F)c1ccccc1", None),
    "vigabatrin":      ("C=C[C@@H](N)CCC(=O)O", None),
}
