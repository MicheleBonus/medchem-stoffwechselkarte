# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 7 : Peptid- und Proteohormone.

Peptidwirkstoffe und Proteasehemmer

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
    # ===================== TEIL 7 : Peptid- und Proteohormone =====================
    # -- RAAS und Kinine
    "captopril":       ("C[C@@H](CS)C(=O)N1CCC[C@H]1C(=O)O", None),
    "enalapril":       ("CCOC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", None),
    "enalaprilat":     ("OC(=O)[C@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", None),
    "lisinopril":      ("NCCCC[C@H](N[C@@H](CCc1ccccc1)C(=O)O)C(=O)N1CCC[C@H]1C(=O)O", None),
    "losartan":        ("CCCCc1nc(Cl)c(CO)n1Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1", None),
    "valsartan":       ("CCCCC(=O)N(Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1)[C@@H](C(C)C)C(=O)O", None),
    "sacubitril":      ("CCOC(=O)C[C@@H](C)[C@@H](Cc1ccc(-c2ccccc2)cc1)NC(=O)CCC(=O)O", None),

    # -- Opioidpeptide und ihre kleinmolekularen Verwandten
    "morphin":         ("CN1CC[C@]23[C@H]4Oc5c(O)ccc(C[C@@H]1[C@@H]2C=C[C@@H]4O)c35", None),
    "naloxon":         ("C=CCN1CC[C@]23[C@H]4Oc5c(O)ccc(C[C@@H]1[C@]2(O)CCC4=O)c35", None),

    # -- Gerinnung und Vitamin K
    "gla":             ("OC(=O)C(C(=O)O)C[C@H](N)C(=O)O", None),
    "vitk_epoxid":     ("CC12OC1(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c1ccccc1C2=O", None),
    "tranexamsaeure":  ("NC[C@H]1CC[C@H](CC1)C(=O)O", None),
    "rivaroxaban":     ("O=C(NC[C@H]1CN(c2ccc(N3CCOCC3=O)cc2)C(=O)O1)c1ccc(Cl)s1", None),
}
