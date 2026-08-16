# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 8 : Gasotransmitter und Redoxsysteme.

NO-Donatoren, Redoxsysteme, Antioxidanzien

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
    # ===================== TEIL 8 : Gasotransmitter und Redoxsysteme =====================
    "gssg":            ("N[C@@H](CCC(=O)N[C@@H](CSSC[C@H](NC(=O)CC[C@H](N)C(=O)O)C(=O)NCC(=O)O)C(=O)NCC(=O)O)C(=O)O", None),
    "selenocystein":   ("N[C@@H](C[SeH])C(=O)O", None),
    "ebselen":         ("O=C1N(c2ccccc2)[Se]c2ccccc21", None),
    "dimethylfumarat": ("COC(=O)/C=C/C(=O)OC", None),
    "monomethylfumarat": ("COC(=O)/C=C/C(=O)O", None),
    "doxorubicin":     ("COc1cccc2c1C(=O)c1c(O)c3c(c(O)c1C2=O)C[C@@](O)(C(=O)CO)C[C@@H]3O[C@H]1C[C@H](N)[C@H](O)[C@H](C)O1", None),
    "nitrofurantoin":  ("O=C1CN(/N=C/c2ccc(o2)[N+](=O)[O-])C(=O)N1", None),
    "metronidazol":    ("Cc1ncc([N+](=O)[O-])n1CCO", None),
    "artemisinin":     ("C[C@@H]1CC[C@H]2[C@@H](C)C(=O)O[C@@H]3O[C@]4(C)CC[C@@H]1[C@@]23OO4", None),
    "methylenblau":    ("CN(C)c1ccc2nc3ccc(cc3[s+]c2c1)N(C)C", None),
    "hydroxycarbamid": ("NC(=O)NO", None),
    "deferipron":      ("Cn1ccc(=O)c(O)c1C", None),
}
