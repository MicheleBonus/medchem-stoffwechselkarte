# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 1 : C2-Wurzel.

Acetyl-CoA, Mevalonatweg, Isoprenoide, Steroide, Vitamin D, Gallensaeuren

Eintragsform:  "id": ("SMILES", {dummy-index: "Beschriftung"})
"""

# --- Reihen: verwandte Strukturen, die nebeneinanderstehen, teilen Lage und
#     Massstab.  REIHEN[name] = dict(vorlage=SMILES, muster=SMARTS, bindung=px)
#     muster ist freiwillig; ohne es sucht der Builder die groesste gemeinsame
#     Teilstruktur selbst.  bindung setzt eine feste Bindungslaenge, damit das
#     laengste Glied nicht geschrumpft wird.
REIHEN = {
    # Isoprenoide: das Diphosphat liegt in allen Gliedern gleich, die Kette
    # waechst nach links. Feste Bindungslaenge, damit Farnesyl-PP neben IPP
    # nicht geschrumpft erscheint.
    "isopren": dict(vorlage="CC(C)=CCC/C(C)=C/CC/C(C)=C/COP(=O)(O)OP(=O)(O)O",
                    muster="[CH2]OP(=O)(O)OP(=O)(O)O", bindung=17.0),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
# Die zuletzt angehaengte C5-Einheit sitzt immer am Diphosphat: Isopentenyl-PP
# behaelt bei der Verknuepfung sein eigenes Diphosphat, der allylische Partner
# gibt seines ab. Deshalb faerbt derselbe SMARTS in GPP und FPP das jeweils neu
# hinzugekommene Glied.
_NEUE_C5 = "[CH2;$([CH2]OP)][CH]=[C]([CH3])[CH2]"

SCHMUCK = {
    "ipp":   dict(reihe="isopren", hervor={"stelle": "[CH2]=[C]([CH3])"}),
    "dmapp": dict(reihe="isopren", hervor={"weg": "OP(=O)(O)OP(=O)(O)O"}),
    "gpp":   dict(reihe="isopren", hervor={"neu": _NEUE_C5}),
    "fpp":   dict(reihe="isopren", hervor={"neu": _NEUE_C5}),
}

MOLS = {
    # ===================== TEIL 1 : C2-Wurzel =====================
    "acetyl_coa":      ("CC(=O)SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O", None),
    # Beschriftung setzt die COA_IDS-Schleife auf das Dummy-Atom; kein manueller
    # Index hier, sonst landet das Label faelschlich auf dem Schwefel.
    "acetyl_coa_abbr": ("CC(=O)S*", None),
    "acetoacetyl_coa": ("CC(=O)CC(=O)S*", None),
    "hmg_coa":         ("OC(=O)C[C@](C)(O)CC(=O)S*", None),
    "mevalonat":       ("OC(=O)C[C@](C)(O)CCO", None),
    "mevalonat_pp":    ("OC(=O)C[C@](C)(O)CCOP(=O)(O)OP(=O)(O)O", None),
    "ipp":             ("CC(=C)CCOP(=O)(O)OP(=O)(O)O", None),
    "dmapp":           ("CC(C)=CCOP(=O)(O)OP(=O)(O)O", None),
    "gpp":             ("CC(C)=CCC/C(C)=C/COP(=O)(O)OP(=O)(O)O", None),
    "fpp":             ("CC(C)=CCC/C(C)=C/CC/C(C)=C/COP(=O)(O)OP(=O)(O)O", None),
    "squalen":         ("CC(C)=CCC/C(C)=C/CC/C(C)=C/CC/C=C(C)/CC/C=C(C)/CCC=C(C)C", None),
    "squalenepoxid":   ("CC1(C)O[C@@H]1CC/C(C)=C/CC/C(C)=C/CC/C=C(C)/CC/C=C(C)/CCC=C(C)C", None),
    "lanosterol":      ("CC(=CCC[C@@H](C)[C@H]1CC[C@@]2([C@@]1(CCC3=C2CC[C@@H]4[C@@]3(CC[C@@H](C4(C)C)O)C)C)C)C", None),
    "cholesterol":     ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "dehydrocholesterol": ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "cholecalciferol": ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2/C(=C/C=C3\\C[C@@H](O)CCC3=C)/CCC[C@]12C", None),
    "calcitriol":      ("CC(C)(O)CCC[C@@H](C)[C@H]1CC[C@H]2/C(=C/C=C3\\C[C@@H](O)C[C@H](O)C3=C)/CCC[C@]12C", None),
    "pregnenolon":     ("CC(=O)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "progesteron":     ("CC(=O)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "hydroxyprogesteron": ("CC(=O)[C@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "dhea":            ("C[C@]12CC[C@H]3[C@@H](CC=C4C[C@@H](O)CC[C@]34C)[C@@H]1CCC2=O", None),
    "androstendion":   ("C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CCC2=O", None),
    "testosteron":     ("C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", None),
    "dht":             ("C[C@]12CC[C@H]3[C@@H](CC[C@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", None),
    "estradiol":       ("C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CC[C@@H]2O", None),
    "estron":          ("C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CCC2=O", None),
    "cortisol":        ("C[C@]12C[C@H](O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@]2(O)C(=O)CO", None),
    "corticosteron":   ("C[C@]12C[C@H](O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2C(=O)CO", None),
    "aldosteron":      ("O=C(CO)[C@@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3[C@@H](O)C[C@]12C=O", None),
    "cholsaeure":      ("C[C@H](CCC(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C", None),
    "cdca":            ("C[C@H](CCC(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "ubichinon":       ("COC1=C(OC)C(=O)C(C)=C(C/C=C(C)/CC/C=C(C)/CCC=C(C)C)C1=O", None),
    "acetacetat":      ("CC(=O)CC(=O)O", None),
    "hydroxybutyrat":  ("C[C@@H](O)CC(=O)O", None),
    "aceton":          ("CC(C)=O", None),
    "malonyl_coa":     ("OC(=O)CC(=O)S*", None),
    "palmitat":        ("CCCCCCCCCCCCCCCC(=O)O", None),
    # Wirkstoffe Teil 1
    "simvastatin":     ("CCC(C)(C)C(=O)O[C@H]1C[C@H](C)C=C2C=C[C@H](C)[C@H](CC[C@@H]3C[C@@H](O)CC(=O)O3)[C@@H]12", None),
    "atorvastatin":    ("CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CC[C@@H](O)C[C@@H](O)CC(=O)O", None),
    "alendronat":      ("NCCCC(O)(P(=O)(O)O)P(=O)(O)O", None),
    "anastrozol":      ("CC(C)(C#N)c1cc(Cn2cncn2)cc(C(C)(C)C#N)c1", None),
    "letrozol":        ("N#Cc1ccc(cc1)C(n1cncn1)c1ccc(C#N)cc1", None),
    "exemestan":       ("C=C1CC2=CC(=O)C=C[C@]2(C)[C@@H]2CC[C@]3(C)C(=O)CC[C@H]3[C@@H]12", None),
    "finasterid":      ("CC(C)(C)NC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@H]4NC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C", None),
    "abirateron":      ("C[C@]12CC[C@H](O)CC1=CC[C@@H]1[C@@H]2CC[C@]2(C)[C@@H]1CC=C2c1cccnc1", None),
    "aminoglutethimid": ("CCC1(c2ccc(N)cc2)CCC(=O)NC1=O", None),
}
