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

# Der Cysteinrest selbst: N, C-alpha, C-beta, Chalkogen und die Carbonylgruppe.
# [#16,#34] laesst Schwefel und Selen zu, sodass das Selenocystein in derselben
# Lage sitzt wie der Cysteinrest im Glutathion und der Austausch S gegen Se das
# einzige ist, was auffaellt.
# Das freie Glutathion liegt in der Reihe "thiol" (Teil 3, Vorlage Glutathion,
# bindung 24). Vorlage und Drehung sind hier so gewaehlt, dass sich das ganze
# Tripeptid der ersten GSSG-Haelfte deckungsgleich ueber jenes Bild legt:
# nachgemessen 20 von 20 Atomen, Restdrehung 0,1 Grad, kein Spiegelbild.
_CYS = "[#7]-[#6](-[#6]-[#16,#34])-[#6]=[#8]"

REIHEN = {
    # 8.3  Das Redoxpaar der Zelle und die Chalkogen-Aminosaeure daneben.
    "glutathion_paar": dict(
        vorlage="N[C@@H](CCC(=O)N[C@@H](CSSC[C@H](NC(=O)CC[C@H](N)C(=O)O)"
                "C(=O)NCC(=O)O)C(=O)NCC(=O)O)C(=O)O",
        muster=_CYS, bindung=24, drehung=180),

    # 8.4  Diester gegen Monoester: dieselbe Fumarsaeure-Achse, ein Rest weniger.
    "fumarat": dict(
        vorlage="COC(=O)/C=C/C(=O)OC",
        muster="[#6]-[#8]-[#6](=[#8])-[#6]=[#6]-[#6](=[#8])-[#8]", bindung=26),

    # 8.5  Beide Nitroverbindungen werden am selben Ort reduziert. Das Muster
    #      fasst den Fuenfring samt Nitrogruppe; dadurch steht die Nitrogruppe
    #      in beiden Bildern an derselben Stelle.
    "nitroaromat": dict(
        vorlage="O=C1CN(/N=C/c2ccc(o2)[N+](=O)[O-])C(=O)N1",
        muster="a1aa(-[#7+](=[#8])[#8-])aa1", bindung=24),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.

# Nitrogruppe als Ganzes: hier setzt die Einelektronenreduktion an.
_NITRO = "[$([N+](=O)[O-])](=[OX1])[OX1]"

SCHMUCK = {
    # -- 8.3 Abwehrlinien
    # Die zweite, ueber die Disulfidbruecke angehaengte GSH-Einheit. Indizes
    # statt SMARTS, weil beide Haelften identisch sind und ein SMARTS deshalb
    # nicht zwischen der alten und der neuen unterscheiden koennte.
    "gssg":            dict(reihe="glutathion_paar",
                            hervor={"neu": list(range(10, 30))}),
    "selenocystein":   dict(reihe="glutathion_paar", hervor={"stelle": "[Se]"}),
    "ebselen":         dict(hervor={"stelle": "[Se]"}),
    # das Sauerstoffpaar, mit dem der Chelator das Fe(III) zangenartig fasst
    "deferipron":      dict(hervor={"stelle":
                                    "[$([OX1]=[#6;R]),$([OX2H1]-[#6;R])]"}),

    # -- 8.4 Nrf2 und Keap1
    # Die Esterase spaltet einen der beiden gleichwertigen Methylester; das
    # Methanol nimmt CH3 und den Estersauerstoff mit. Atome 8 und 9 sind das
    # Ende, das im Monomethylfumarat als freie Saeure erscheint (nachgerechnet:
    # beide liegen nach der Ausrichtung bei x = -2,2 bzw. -3,0).
    "dimethylfumarat": dict(reihe="fumarat", hervor={"weg": [8, 9]}),
    "monomethylfumarat": dict(reihe="fumarat", hervor={"neu": "[OX2H1]"}),

    # -- 8.5 Oxidativer Stress als Wirkprinzip
    # Durchgehend "stelle": in jeder Kachel die Gruppe, an der die reaktive
    # Spezies entsteht.
    "doxorubicin":     dict(hervor={"stelle":
                                    "[$([OX1]=[CX3](c)c),$([CX3](=[OX1])(c)c)]"}),
    "metronidazol":    dict(reihe="nitroaromat", hervor={"stelle": _NITRO}),
    "nitrofurantoin":  dict(reihe="nitroaromat", hervor={"stelle": _NITRO}),
    "artemisinin":     dict(hervor={"stelle": "[OX2]-[OX2]"}),
    "methylenblau":    dict(hervor={"stelle": "[s+,n]"}),
    "hydroxycarbamid": dict(hervor={"stelle": "[NX3][OX2H1]"}),
}

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
    # (1R,4S,5R,8S,9R,12S,13R): das Ketal-C des 1,2,4-Trioxans (Methyl, Ring-O,
    # Peroxid-O) ist R. BLUAFEHZUWYNDE-NNWCWBAJSA-N.
    "artemisinin":     ("C[C@@H]1CC[C@H]2[C@@H](C)C(=O)O[C@@H]3O[C@@]4(C)CC[C@@H]1[C@@]23OO4", None),
    "methylenblau":    ("CN(C)c1ccc2nc3ccc(cc3[s+]c2c1)N(C)C", None),
    "hydroxycarbamid": ("NC(=O)NO", None),
    "deferipron":      ("Cn1ccc(=O)c(O)c1C", None),
}
