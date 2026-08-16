# -*- coding: utf-8 -*-
"""Strukturformeln fuer TEIL 1 : C2-Wurzel.

Acetyl-CoA, Mevalonatweg, Isoprenoide, Steroide, Vitamin D, Gallensaeuren

Eintragsform:  "id": ("SMILES", {dummy-index: "Beschriftung"})
"""

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
    # (3S): nur dieses Enantiomer ist Substrat der Oxidosqualen-Cyclase und
    # liefert das 3beta-OH des Lanosterols.  QYIMSPSDBYKPPY-RSKUXYSASA-N
    "squalenepoxid":   ("CC1(C)O[C@H]1CC/C(C)=C/CC/C(C)=C/CC/C=C(C)/CC/C=C(C)/CCC=C(C)C", None),
    "lanosterol":      ("CC(=CCC[C@@H](C)[C@H]1CC[C@@]2([C@@]1(CCC3=C2CC[C@@H]4[C@@]3(CC[C@@H](C4(C)C)O)C)C)C)C", None),
    "cholesterol":     ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "dehydrocholesterol": ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2C3=CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    # Vitamin D ist (5Z,7E).  Nur die 7,8-Bindung ist E; die 5,6-Bindung muss Z
    # sein, sonst steht dort trans-Vitamin-D, ein unwirksames UV-Nebenprodukt.
    "cholecalciferol": ("CC(C)CCC[C@@H](C)[C@H]1CC[C@H]2/C(=C/C=C3/C[C@@H](O)CCC3=C)/CCC[C@]12C", None),
    "calcitriol":      ("CC(C)(O)CCC[C@@H](C)[C@H]1CC[C@H]2/C(=C/C=C3/C[C@@H](O)C[C@H](O)C3=C)/CCC[C@]12C", None),
    "pregnenolon":     ("CC(=O)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "progesteron":     ("CC(=O)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    # 17alpha-OH: die Hydroxylgruppe alpha, der Acetylrest beta (C17 = R).
    # DBPWSSGDRRHUNT-CEGNMAFCSA-N
    "hydroxyprogesteron": ("CC(=O)[C@@]1(O)CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "dhea":            ("C[C@]12CC[C@H]3[C@@H](CC=C4C[C@@H](O)CC[C@]34C)[C@@H]1CCC2=O", None),
    "androstendion":   ("C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CCC2=O", None),
    "testosteron":     ("C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", None),
    "dht":             ("C[C@]12CC[C@H]3[C@@H](CC[C@H]4CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2O", None),
    "estradiol":       ("C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CC[C@@H]2O", None),
    "estron":          ("C[C@]12CC[C@H]3[C@@H](CCc4cc(O)ccc34)[C@@H]1CCC2=O", None),
    "cortisol":        ("C[C@]12C[C@H](O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@]2(O)C(=O)CO", None),
    "corticosteron":   ("C[C@]12C[C@H](O)[C@H]3[C@@H](CCC4=CC(=O)CC[C@]34C)[C@@H]1CC[C@@H]2C(=O)CO", None),
    # C17 = S: die Hydroxyaceton-Seitenkette steht beta wie in allen Corticoiden.
    # PQSUYGKTWSAVDQ-ZVIOFETBSA-N (offene Aldehydform, nicht das 11,18-Halbacetal)
    "aldosteron":      ("O=C(CO)[C@H]1CC[C@H]2[C@@H]3CCC4=CC(=O)CC[C@]4(C)[C@H]3[C@@H](O)C[C@]12C=O", None),
    "cholsaeure":      ("C[C@H](CCC(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3C[C@H](O)[C@]12C", None),
    "cdca":            ("C[C@H](CCC(=O)O)[C@H]1CC[C@H]2[C@@H]3[C@H](O)C[C@@H]4C[C@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", None),
    "ubichinon":       ("COC1=C(OC)C(=O)C(C)=C(C/C=C(C)/CC/C=C(C)/CCC=C(C)C)C1=O", None),
    "acetacetat":      ("CC(=O)CC(=O)O", None),
    "hydroxybutyrat":  ("C[C@@H](O)CC(=O)O", None),
    "aceton":          ("CC(C)=O", None),
    "malonyl_coa":     ("OC(=O)CC(=O)S*", None),
    "palmitat":        ("CCCCCCCCCCCCCCCC(=O)O", None),
    # Wirkstoffe Teil 1
    # (1S,3R,7S,8S,8aR); die 3-Methylgruppe war epimerisiert.
    # RYMZZMVNJRMUDD-HGQWONQESA-N
    "simvastatin":     ("CCC(C)(C)C(=O)O[C@H]1C[C@@H](C)C=C2C=C[C@H](C)[C@H](CC[C@@H]3C[C@@H](O)CC(=O)O3)[C@@H]12", None),
    "atorvastatin":    ("CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CC[C@@H](O)C[C@@H](O)CC(=O)O", None),
    "alendronat":      ("NCCCC(O)(P(=O)(O)O)P(=O)(O)O", None),
    "anastrozol":      ("CC(C)(C#N)c1cc(Cn2cncn2)cc(C(C)(C)C#N)c1", None),
    "letrozol":        ("N#Cc1ccc(cc1)C(n1cncn1)c1ccc(C#N)cc1", None),
    # 6-Methylenandrosta-1,4-dien-3,17-dion: das exocyclische Methylen sitzt an
    # C6, also direkt am sp2-C5 des Dienons - nur dort taugt es als Michael-
    # Akzeptor und macht Exemestan zum Suizidsubstrat.  BFYIZQONLCFLEV-DAELLWKTSA-N
    "exemestan":       ("C=C1C[C@@H]2[C@H](CC[C@]3(C)C(=O)CC[C@@H]23)[C@@]2(C)C=CC(=O)C=C12", None),
    "finasterid":      ("CC(C)(C)NC(=O)[C@H]1CC[C@H]2[C@@H]3CC[C@H]4NC(=O)C=C[C@]4(C)[C@H]3CC[C@]12C", None),
    # C13/C14 waren invertiert (13alpha-Methyl/14beta-H); Abirateron traegt wie
    # jedes Naturstoffsteroid die trans-anti-trans-Verknuepfung.
    # GZOSMCIZMLWJML-VJLLXTKPSA-N
    "abirateron":      ("C[C@]12CC[C@H](O)CC1=CC[C@@H]1[C@@H]2CC[C@@]2(C)[C@H]1CC=C2c1cccnc1", None),
    "aminoglutethimid": ("CCC1(c2ccc(N)cc2)CCC(=O)NC1=O", None),
}


def _s(mid):
    """SMILES eines Eintrags. Reihenvorlagen greifen so auf MOLS zu; damit kann
    eine Vorlage nicht von dem Molekuel abweichen, das sie ausrichten soll."""
    return MOLS[mid][0]


# --- Reihen: verwandte Strukturen, die nebeneinanderstehen, teilen Lage und
#     Massstab.  REIHEN[name] = dict(vorlage=SMILES, muster=SMARTS, bindung=px)
#     muster ist freiwillig; ohne es sucht der Builder die groesste gemeinsame
#     Teilstruktur selbst.  bindung setzt eine feste Bindungslaenge, damit das
#     laengste Glied nicht geschrumpft wird.
#
# Zwei Reihen duerfen dieselbe Vorlage tragen und trotzdem verschiedene Muster
# festhalten. Davon lebt der Uebergang zwischen Kaskaden: die Secosteroide
# haengen am Cholesterol-Bild wie die Steroide, nur eben am C/D-Ring, weil ihr
# Ring B offen ist.

# Gonan: A-B-C-D, 6-6-6-5, Bindungen offen gelassen (Δ4, Δ5, aromatischer Ring A
# und das 4-Aza des Finasterids muessen alle hineinpassen). Trifft jedes der
# zwanzig Steroide genau einmal - eindeutig, also auch spiegelungssicher.
_GONAN = ("[#6,#7]1~[#6]~[#6]~[#6]2~[#6](~[#6,#7]1)~[#6]~[#6]~[#6]1~[#6]2"
          "~[#6]~[#6]~[#6]2~[#6]1~[#6]~[#6]~[#6]2")
# Hydrindan: der C/D-Teil allein. Ihn haben Steroide und Secosteroide gemeinsam.
_HYDRINDAN = "[#6]1~[#6]~[#6]~[#6]~[#6]2~[#6]1~[#6]~[#6]~[#6]2"
# Die 3,5-Dihydroxyheptansaeure der Statine - im Lacton wie in der offenen Form.
# Der Ringsauerstoff bleibt draussen, sonst muesste er in Atorvastatin ein
# zweites Mal vorkommen.
_HMG_MIMIKRY = "[#8]~[#6](=[#8])~[#6]~[#6](~[#8])~[#6]~[#6]~[#6]~[#6]"

REIHEN = {
    # Mevalonatweg: alles haengt am HMG-CoA. Ohne Muster sucht der Builder je
    # Glied die groesste gemeinsame Teilstruktur - fuer Acetyl-CoA ist das der
    # Thioester, fuer Mevalonat das Glutaryl-Geruest.
    "coa": dict(vorlage=_s("hmg_coa"), bindung=17.0),
    # Isoprenoide: das Diphosphat liegt in allen Gliedern gleich, die Kette
    # waechst nach links. Feste Bindungslaenge, damit Farnesyl-PP neben IPP
    # nicht geschrumpft erscheint.
    "isopren": dict(vorlage=_s("fpp"),
                    muster="[CH2]OP(=O)(O)OP(=O)(O)O", bindung=17.0),
    # Squalen und sein Epoxid teilen 26 von 30 Atomen. Ohne Muster nimmt der
    # Builder genau diese 26; die Kette laeuft dann in beiden Bildern gleich,
    # und das Epoxid ist das Einzige, was auffaellt.
    "prenyl": dict(vorlage=_s("squalenepoxid"), bindung=17.0, drehung=180.0),
    # Die gesamte Steroidkaskade 1.3 und 1.4 samt der steroidalen Wirkstoffe.
    # Ohne Drehung liegt das Geruest so, wie es im Lehrbuch steht: A-Ring links
    # unten, D-Ring rechts oben.
    "steroid": dict(vorlage=_s("cholesterol"), muster=_GONAN, bindung=17.0),
    # Vitamin D: Ring B ist offen, das Gonan trifft nicht mehr. Vorlage und
    # Vorlage bleibt dieselbe wie bei den Steroiden, festgehalten wird nur der
    # C/D-Ring - so steht das Secosteroid genau dort, wo vorher das
    # geschlossene Steroid lag.
    "secosteroid": dict(vorlage=_s("cholesterol"), muster=_HYDRINDAN, bindung=17.0),
    "statin": dict(vorlage=_s("atorvastatin"), muster=_HMG_MIMIKRY, bindung=17.0),
    # Nichtsteroidale Aromatasehemmer: Triazol plus das tragende C.
    "azol": dict(vorlage=_s("anastrozol"), muster="[#7]1~[#6]~[#7]~[#6]~[#7]1~[#6]",
                 bindung=17.0),
    "keton": dict(vorlage=_s("acetacetat"), muster="[#6]-[#6](~[#8])-[#6]", bindung=17.0),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
# Hoechstens eine Farbe je Bild, und nur dort, wo die Aussage traegt.

# Die zuletzt angehaengte C5-Einheit sitzt immer am Diphosphat: Isopentenyl-PP
# behaelt bei der Verknuepfung sein eigenes Diphosphat, der allylische Partner
# gibt seines ab. Deshalb faerbt derselbe SMARTS in GPP und FPP das jeweils neu
# hinzugekommene Glied.
_NEUE_C5 = "[CH2;$([CH2]OP)][CH]=[C]([CH3])[CH2]"
# Squalen ist symmetrisch; die einzige CH2-CH2-Bindung, deren beide Nachbarn das
# unsubstituierte Alken-C tragen, ist die Kopf-Kopf-Naht der beiden Farnesylteile.
_KOPF_KOPF = "[CH2;$([CH2][CH]=[C][CH3])]-[CH2;$([CH2][CH]=[C][CH3])]"
# Lanosterol traegt drei Methylgruppen mehr als Cholesterol: das gem-Dimethyl an
# C4 und die 14alpha-Methylgruppe. Letztere sitzt als einzige Angularmethyl an
# einem C, das im Fuenfring liegt UND an der Doppelbindung haengt.
_DREI_METHYL = "[$([CH3][C]([CH3])[CH][OX2H1]),$([CH3][C;r5][CH0]=[CH0])]"
# C19: die Angularmethylgruppe am C10. Ihr C liegt nur in Sechsringen, die des
# C18 auch im Fuenfring. Die Aromatase spaltet genau diese als Formiat ab.
_C19 = "[CH3;$([CH3][C;r6])]"
# Calcitriol gegen Cholecalciferol: die 25-OH an der Seitenkette und die 1alpha-OH
# am Ring, erkennbar an ihrem Nachbarn, dem exocyclischen Methylen-C.
_NEUE_OH = "[$([OX2H1][CX4]([CH3])[CH3]),$([OX2H1][CH1;R][C;R]=[CH2])]"

SCHMUCK = {
    # ---- 1.1 Mevalonatweg
    "acetyl_coa_abbr": dict(reihe="coa"),
    "acetoacetyl_coa": dict(reihe="coa", hervor={"neu": "[CH3][C](=[#8])[CH2]"}),
    "hmg_coa":         dict(reihe="coa", hervor={"stelle": "[#6]-[#6](=[#8])-[#16]"}),
    "mevalonat":       dict(reihe="coa", hervor={"neu": "[OX2H1]-[CH2]"}),
    "mevalonat_pp":    dict(reihe="isopren"),
    # ---- 1.1 Statine
    "simvastatin":     dict(reihe="statin", hervor={"gerippe": _HMG_MIMIKRY}),
    "atorvastatin":    dict(reihe="statin", hervor={"gerippe": _HMG_MIMIKRY}),
    # ---- 1.2 Isoprenoide
    "ipp":   dict(reihe="isopren", hervor={"stelle": "[CH2]=[C]([CH3])"}),
    "dmapp": dict(reihe="isopren", hervor={"weg": "OP(=O)(O)OP(=O)(O)O"}),
    "gpp":   dict(reihe="isopren", hervor={"neu": _NEUE_C5}),
    "fpp":   dict(reihe="isopren", hervor={"neu": _NEUE_C5}),
    # ---- 1.3 Squalen bis Cholesterol
    "squalen":       dict(reihe="prenyl", hervor={"neu": _KOPF_KOPF}),
    "squalenepoxid": dict(reihe="prenyl", hervor={"neu": "[#6]1-[#8]-[#6]1"}),
    "lanosterol":    dict(reihe="steroid", hervor={"weg": _DREI_METHYL}),
    # Cholesterol steht in zwei Kaskaden zugleich (Ziel von 1.3, Ausgangsstoff
    # von 1.4). Eine Farbe waere in einer der beiden falsch, darum keine.
    "cholesterol":   dict(reihe="steroid"),
    # ---- 1.4 Steroidogenese
    "pregnenolon":   dict(reihe="steroid", hervor={"neu": "[CH3]-[C](=[#8])-[CH1;R]"}),
    "progesteron":   dict(reihe="steroid", hervor={"neu": "[#8]=[#6]-[#6]=[#6]"}),
    "hydroxyprogesteron": dict(reihe="steroid",
                              hervor={"stelle": "[OX2H1]-[C]-[C](=[#8])-[CH3]"}),
    "androstendion": dict(reihe="steroid", hervor={"stelle": "[#8]=[C;r5]"}),
    "testosteron":   dict(reihe="steroid", hervor={"weg": _C19}),
    "estradiol":     dict(reihe="steroid", hervor={"neu": "c1ccccc1"}),
    "dhea":          dict(reihe="steroid"),
    "dht":           dict(reihe="steroid"),
    "estron":        dict(reihe="steroid"),
    "cortisol":      dict(reihe="steroid"),
    "corticosteron": dict(reihe="steroid"),
    "aldosteron":    dict(reihe="steroid"),
    "cholsaeure":    dict(reihe="steroid"),
    "cdca":          dict(reihe="steroid"),
    # ---- 1.4 Wirkstoffe
    "anastrozol": dict(reihe="azol", hervor={"stelle": "[$([nX2](:c):c)]"}),
    "letrozol":   dict(reihe="azol", hervor={"stelle": "[$([nX2](:c):c)]"}),
    "exemestan":  dict(reihe="steroid", hervor={"stelle": "[CH2]=[C;R]"}),
    "finasterid": dict(reihe="steroid",
                       hervor={"stelle": "[NX3;R]-[C](=[#8])-[C]=[C]"}),
    "abirateron": dict(reihe="steroid", hervor={"stelle": "[nX2;R]"}),
    # ---- 1.5 Vitamin D
    "dehydrocholesterol": dict(reihe="steroid", hervor={"stelle": "[#6]=[#6]-[#6]=[#6]"}),
    "cholecalciferol":    dict(reihe="secosteroid", hervor={"neu": "[CH2]=[C;R]"}),
    "calcitriol":         dict(reihe="secosteroid", hervor={"neu": _NEUE_OH}),
    # ---- 1.7 Ketonkoerper
    "acetacetat":     dict(reihe="keton", hervor={"stelle": "[#8]=[#6](-[CH3])-[#6]"}),
    "hydroxybutyrat": dict(reihe="keton", hervor={"neu": "[OX2H1]-[CH1]"}),
    "aceton":         dict(reihe="keton"),
}
