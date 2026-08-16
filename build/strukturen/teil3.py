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

# Die C4/C5-Saeuren des GABA-Shunts und die GABA-Analoga teilen dieselbe
# Vorlage: die Kette Amin/Carbonyl - vier Kohlenstoffe - Saeure. Nur so faellt
# auf, dass Glutamat und GABA sich um genau ein CO2 unterscheiden.
_GABA_VORLAGE = "N[C@@H](CCC(=O)O)C(=O)O"          # L-Glutamat
_GABA_MUSTER = "[#7,#8]~[#6]~[#6]~[#6]~[#6](=[#8,#7])~[#8,#7]"

REIHEN = {
    "gabakette":   dict(vorlage=_GABA_VORLAGE, muster=_GABA_MUSTER, bindung=26),
    # gleiche Lage wie oben, aber ohne festen Massstab: die Wirkstoffgalerie
    # steht neben dem deutlich groesseren Tiagabin und soll nicht ausfransen.
    "gabaanalog":  dict(vorlage=_GABA_VORLAGE, muster=_GABA_MUSTER),

    # Aminosaeure-Rueckgrat N-C-C=O: haelt Serin, Glycin und ALA in einer Lage.
    "aminosaeure": dict(vorlage="NCC(=O)CCC(=O)O", muster="[#7]-[#6]-[#6]=[#8]"),

    # Protoporphyrin IX und Haem b unterscheiden sich nur um das Eisen; ohne
    # Muster sucht der Builder die groesste gemeinsame Teilstruktur (42 Atome).
    "tetrapyrrol": dict(vorlage="CC1=C(C2=CC3=NC(=CC4=NC(=CC5=C(C(=C(N5)C=C1N2)C=C)C)"
                                "C(=C4CCC(=O)O)C)C(=C3C)CCC(=O)O)C=C", bindung=18),
    # Biliverdin und Bilirubin haben dieselbe Konnektivitaet (43 von 43 Atomen);
    # der einzige Unterschied ist die reduzierte Methinbruecke in der Mitte.
    "bilin":       dict(vorlage=r"CC\1=C(/C(=C/C2=C(C(=C(N2)/C=C\3/C(=C(C(=O)N3)C)C=C)C)"
                                r"CCC(=O)O)/N/C1=C\C4=NC(=O)C(=C4C)C=C)CCC(=O)O", bindung=18),

    # Arginin, N-omega-Hydroxyarginin und Citrullin: das Guanidin bleibt an
    # derselben Stelle, nur sein rechter Rand wechselt N -> NOH -> O.
    "guanidin":    dict(vorlage="N[C@@H](CCCNC(N)=NO)C(=O)O",
                        muster="[#7]-[#6](-[#6]-[#6]-[#6]-[#7]-[#6](~[#7])~[#7,#8])"
                               "-[#6](=[#8])-[#8]", bindung=26),

    # Putrescin-Kern N-(CH2)4-N; in Spermidin und Spermin liegt er innen.
    "polyamin":    dict(vorlage="NCCCNCCCCNCCCN",
                        muster="[#7]-[#6]-[#6]-[#6]-[#6]-[#7]", bindung=22),
    "creatin":     dict(vorlage="CN(CC(=O)O)C(=N)NP(=O)(O)O",
                        muster="[#7]~[#6](~[#7])~[#7]~[#6]~[#6]=[#8]", bindung=22),

    # Cystein-Rueckgrat N-C-C-S: traegt auch Glutathion, Sulfinat und Taurin.
    "thiol":       dict(vorlage="N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(=O)O)C(=O)O",
                        muster="[#7]~[#6]~[#6]~[#16]", bindung=24),
    # Paracetamol und NAPQI sind atomgleich (11 von 11); die Zweielektronen-
    # oxidation ist nur zu sehen, wenn der Ring exakt gleich liegt.
    "chinonimin":  dict(vorlage="CC(=O)Nc1ccc(O)cc1",
                        muster="[#6]-[#6](=[#8])~[#7]~[#6]1~[#6]~[#6]~[#6](~[#8])~[#6]~[#6]1",
                        bindung=24),

    "methionin":   dict(vorlage="N[C@@H](CCSC[C@H](N)C(=O)O)C(=O)O",
                        muster="[#7]-[#6](-[#6]-[#6]-[#16])-[#6](=[#8])-[#8]", bindung=24),

    # Pteridin + p-Aminobenzoyl-Glutamat, 31 Atome. Nur so faellt am
    # 5-Methyl-THF die eine zusaetzliche Methylgruppe auf.
    "folat":       dict(vorlage="CN1C(CNC2=C1C(=O)NC(=N2)N)CNC3=CC=C(C=C3)C(=O)N"
                                "[C@@H](CCC(=O)O)C(=O)O",
                        muster="[#7&!R]-[#6]1:[#7]:[#6]2-,:[#7]-,:[#6]-,:[#6](-,:[#7]"
                               "-,:[#6]:2:[#6]:[#7]:1)-[#6&!R]-[#7&!R]-[#6]1:[#6]:[#6]"
                               ":[#6](:[#6]:[#6]:1)-[#6&!R](=[#8&!R])-[#7&!R]-[#6&!R]"
                               "(-[#6&!R]-[#6&!R]-[#6&!R](=[#8&!R])-[#8&!R])-[#6&!R]"
                               "(=[#8&!R])-[#8&!R]",
                        bindung=22),

    # Aminodiol-Motiv von Sphingosin; Fingolimod bildet es nach.
    # gedreht, damit die Fettsaeurekette waagerecht liegt und der Kopf rechts
    # steht; ungedreht laeuft sie diagonal durch die Kachel.
    "sphingo":     dict(vorlage="CCCCCCCCCCCCC/C=C/[C@@H](O)[C@@H](N)COP(=O)(O)O",
                        muster="[#6]~[#6]~[#6](~[#7])~[#6]~[#8]", drehung=-45),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.

# Die alpha-Carboxylgruppe einer Aminosaeure, und nur sie: der Nachbar traegt
# Amin und Kette. Ueber die Nachbarschaft formuliert, damit die zweite
# Carboxylgruppe (Glutamat, Ornithin) nicht mittrifft.
_ALPHA_COOH = ("[$([CX3](=[OX1])([OX2H1])[CX4]([NX3])[CX4]),"
               "$([OX1]=[CX3]([OX2H1])[CX4]([NX3])[CX4]),"
               "$([OX2H1][CX3](=[OX1])[CX4]([NX3])[CX4])]")

SCHMUCK = {
    # -- 3.1 GABA-Shunt: jede Kachel zeigt, was der naechste Schritt wegnimmt
    "glutamin":        dict(reihe="gabakette",
                            hervor={"weg": "[$([NX3H2][CX3]=[OX1])]"}),
    "glutamat":        dict(reihe="gabakette", hervor={"weg": _ALPHA_COOH}),
    "gaba":            dict(reihe="gabakette", hervor={"weg": "[NX3H2]"}),
    "succinatsemi":    dict(reihe="gabakette",
                            hervor={"neu": "[$([OX1]=[CX3H1])]"}),
    "succinat":        dict(reihe="gabakette"),
    # Wirkstoffe in derselben Lage wie GABA, damit das Rueckgrat wiederkehrt
    "vigabatrin":      dict(reihe="gabaanalog", hervor={"neu": "[CH2]=[CH]"}),
    "baclofen":        dict(reihe="gabaanalog"),
    "gabapentin":      dict(reihe="gabaanalog"),
    "pregabalin":      dict(reihe="gabaanalog"),

    # -- 3.2 Haem
    "glycin":          dict(reihe="aminosaeure"),
    "ala":             dict(reihe="aminosaeure",
                            hervor={"neu": "[CX3](=[OX1])[CH2][CH2][CX3](=[OX1])[OX2H1]"}),
    "porphobilinogen": dict(hervor={"neu": "[#7;R]1[#6;R][#6;R][#6;R][#6;R]1"}),
    "protoporphyrin":  dict(reihe="tetrapyrrol", hervor={"stelle": "[#7;R]"}),
    "haem":            dict(reihe="tetrapyrrol", hervor={"neu": "[Fe]"}),
    "biliverdin":      dict(reihe="bilin"),
    # die eine reduzierte Methinbruecke: ein sp3-CH2 zwischen zwei Ringen
    "bilirubin":       dict(reihe="bilin",
                            hervor={"neu": "[CH2;!R](-[#6;R])-[#6;R]"}),
    "bilirubindiglucuronid": dict(
        reihe="bilin",
        hervor={"neu": "[#6]1-[#8]-[#6](-[#6](=[#8])-[#8])-[#6](-[#8])"
                       "-[#6](-[#8])-[#6]-1-[#8]"}),

    # -- 3.3 Arginin
    "arginin":         dict(reihe="guanidin", hervor={"stelle": "[$([NX2]=[CX3])]"}),
    "noharginin":      dict(reihe="guanidin", hervor={"neu": "[$([OX2H1][NX2])]"}),
    "citrullin":       dict(reihe="guanidin",
                            hervor={"neu": "[$([OX1]=[CX3]([NX3])[NX3])]"}),
    "lnmma":           dict(reihe="guanidin"),
    "ornithin":        dict(reihe="polyamin",
                            hervor={"weg": "[CX3](=[OX1])[OX2H1]"}),
    "putrescin":       dict(reihe="polyamin"),
    # angehaengte Aminopropyleinheit; Indizes, weil beide Enden gleich aussehen
    # und ein SMARTS deshalb nicht zwischen alt und neu unterscheiden kann.
    "spermidin":       dict(reihe="polyamin", hervor={"neu": [6, 7, 8, 9]}),
    "spermin":         dict(reihe="polyamin", hervor={"neu": [0, 1, 2, 3]}),
    "agmatin":         dict(reihe="polyamin"),
    "guanidinoacetat": dict(reihe="creatin"),
    "creatin":         dict(reihe="creatin",
                            hervor={"neu": "[$([CH3][NX3]([CH2])[CX3])]"}),
    "phosphocreatin":  dict(reihe="creatin"),
    "creatinin":       dict(reihe="creatin",
                            hervor={"neu": "[NX3H1;R]-[CX3;R]=[OX1]"}),

    # -- 3.4 Cystein
    "cystein":         dict(reihe="thiol", hervor={"stelle": "[SX2H1]"}),
    "glutathion":      dict(reihe="thiol",
                            hervor={"neu": "[NX3H2][CX4]([CH2][CH2][CX3]=[OX1])"
                                           "[CX3](=[OX1])[OX2H1]"}),
    "cysteinsulfinat": dict(reihe="thiol", hervor={"weg": _ALPHA_COOH}),
    "hypotaurin":      dict(reihe="thiol"),
    "taurin":          dict(reihe="thiol"),
    "nac":             dict(reihe="thiol", hervor={"neu": "[CH3][CX3]=[OX1]"}),
    # die beiden Stellen, an denen die zwei Elektronen abgehen: Stickstoff und
    # Ringsauerstoff samt der Kohlenstoffe, an denen sie haengen
    "paracetamol":     dict(reihe="chinonimin",
                            hervor={"stelle": "[$([OX2H1][c]),$([NX3][c]),"
                                              "$([c][OX2H1]),$([c][NX3])]"}),
    "napqi":           dict(reihe="chinonimin",
                            hervor={"stelle": "[$([NX2]=[CX3;R]),$([OX1]=[CX3;R]),"
                                              "$([CX3;R]=[NX2]),$([CX3;R]=[OX1])]"}),

    # -- 3.5 Methionin
    "methionin":       dict(reihe="methionin", hervor={"stelle": "[SX2]"}),
    "sam":             dict(reihe="methionin", hervor={"stelle": "[CH3][S+]"}),
    "sah":             dict(reihe="methionin"),
    "homocystein":     dict(reihe="methionin", hervor={"neu": "[SX2H1]"}),
    # der aus Serin stammende Teil (C5-C10 der SMILES); der Schwefel selbst
    # kommt aus dem Homocystein und bleibt deshalb ungefaerbt.
    "cystathionin":    dict(reihe="methionin", hervor={"neu": [5, 6, 7, 8, 9, 10]}),

    # -- 3.6 Serin
    "serin":           dict(reihe="aminosaeure",
                            hervor={"weg": "[$([OX2H1][CH2][CX4]),$([CH2]([OX2H1])[CX4])]"}),
    "thf":             dict(reihe="folat"),
    "methylthf":       dict(reihe="folat", hervor={"neu": "[$([CH3][NX3;R])]"}),
    # folsaeure und methotrexat stehen nicht hier, sondern in der Galerie von
    # Teil 6; ihre Ausrichtung gehoert deshalb dorthin (Reihe "t6-antifolat").
    "sphingosin":      dict(reihe="sphingo"),
    "s1p":             dict(reihe="sphingo",
                            hervor={"neu": "[#8]-[PX4](=[#8])(-[#8])-[#8]"}),
    "fingolimod":      dict(reihe="sphingo",
                            hervor={"gerippe": "[#6]~[#6]~[#6](~[#7])~[#6]~[#8]"}),
}

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
    # (R)-Nipecotinsaeure-Rest: PBJUNZJWGZTSKL-MRXNPFEDSA-N
    "tiagabin":        ("Cc1ccsc1C(=CCCN1CCC[C@H](C1)C(=O)O)c1sccc1C", None),

    # -- 3.2 Haem / Porphyrine
    "succinyl_coa":    ("OC(=O)CCC(=O)S*", None),
    "ala":             ("NCC(=O)CCC(=O)O", None),
    "porphobilinogen": ("NCc1[nH]cc(CCC(=O)O)c1CC(=O)O", None),
    # Isomer IX (Fischer 1,3,5,8-Tetramethyl-2,4-divinyl-6,7-dipropionat):
    # die beiden Propionate stehen an benachbarten Ringen und zeigen auf
    # dieselbe Meso-Bruecke.  ZCFFYALKHPIRKJ-UHFFFAOYSA-N
    "protoporphyrin":  ("CC1=C(C2=CC3=NC(=CC4=NC(=CC5=C(C(=C(N5)C=C1N2)C=C)C)"
                        "C(=C4CCC(=O)O)C)C(=C3C)CCC(=O)O)C=C", None),
    # Haem b: Fe(II) im dianionischen Porphyrinkern, Gesamtladung 0.
    # KABFMIBPWCXCRK-UHFFFAOYSA-L
    "haem":            ("CC1=C(C2=CC3=NC(=CC4=NC(=CC5=C(C(=C([N-]5)C=C1[N-]2)C=C)C)"
                        "C(=C4CCC(=O)O)C)C(=C3C)CCC(=O)O)C=C.[Fe+2]", None),
    # Bilirubin IXalpha, (4Z,15Z): unsymmetrisch, beide Bruecken Z.
    # BPYKTIZUTYGOLE-IFADSCNNSA-N
    "bilirubin":       (r"CC1=C(NC(=C1CCC(=O)O)CC2=C(C(=C(N2)/C=C\3/C(=C(C(=O)N3)C)"
                        r"C=C)C)CCC(=O)O)/C=C\4/C(=C(C(=O)N4)C=C)C", None),
    # Biliverdin IXalpha: unsymmetrisch, alle drei Bruecken Z.
    # RCNSAJSGRJSBKK-NSQVQWHSSA-N
    "biliverdin":      (r"CC\1=C(/C(=C/C2=C(C(=C(N2)/C=C\3/C(=C(C(=O)N3)C)C=C)C)"
                        r"CCC(=O)O)/N/C1=C\C4=NC(=O)C(=C4C)C=C)CCC(=O)O", None),
    # beide Propionsaeuren als Acylglucuronid verestert.
    # SCJLWMXOOYZBTH-BTVQFETGSA-N
    "bilirubindiglucuronid": (
        r"CC1=C(NC(=C1CCC(=O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C(=O)O)O)O)O)"
        r"CC3=C(C(=C(N3)/C=C\4/C(=C(C(=O)N4)C)C=C)C)CCC(=O)O[C@H]5[C@@H]"
        r"([C@H]([C@@H]([C@H](O5)C(=O)O)O)O)O)/C=C\6/C(=C(C(=O)N6)C=C)C", None),

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
    # 5-Methyl-THF: die Benzoylglutamat-Seitenkette haengt an C6, also am
    # Nachbarn des methylierten N5.  ZNOVTXRBGFNYRX-ABLWVSNPSA-N
    "methylthf":       ("CN1C(CNC2=C1C(=O)NC(=N2)N)CNC3=CC=C(C=C3)C(=O)N"
                        "[C@@H](CCC(=O)O)C(=O)O", None),
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
