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
REIHEN = {
    # 5.1  Glykolyse: Pyranose und Furanose auf dem gemeinsamen Zuckerteil.
    "hexose": dict(
        vorlage="O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O",   # g6p
        muster="[#8&!R]-&!@[#6&!R]-&!@[#6&R](-&@[#8&R]-&@[#6&R]-&!@[#8&!R])"
               "-&@[#6&R](-&@[#6&R]-&!@[#8&!R])-&!@[#8&!R]",
        bindung=34.0),

    # 5.1  Pyruvat/Lactat: gleich gross, es geht um eine einzige Reduktion.
    "c3": dict(
        vorlage="C[C@H](O)C(=O)O",                                        # lactat
        muster="[#6&!R]-&!@[#6&!R](=,-;!@[#8&!R])-&!@[#6&!R](=&!@[#8&!R])-&!@[#8&!R]"),

    # 5.2  Ribose-5-phosphat und PRPP teilen die ganze Furanose samt 5-Phosphat.
    "pentose": dict(
        vorlage="O=P(O)(O)OC[C@H]1O[C@H](OP(=O)(O)OP(=O)(O)O)[C@H](O)[C@@H]1O",  # prpp
        muster="[#8&!R]=&!@[#15&!R](-&!@[#8&!R])(-&!@[#8&!R])-&!@[#8&!R]-&!@[#6&!R]"
               "-&!@[#6]1-&@[#8]-&@[#6](-&@[#6](-&@[#6]-&@1-&!@[#8&!R])-&!@[#8&!R])-&!@[#8&!R]",
        bindung=34.0),

    # 5.3  Purin und Pyrazolo[3,4-d]pyrimidin uebereinander: nur so ist zu sehen,
    #      dass Allopurinol ein Isomer des Hypoxanthins ist (N7/C8 gegen C3/N2).
    #      Das Muster laesst am C6 Sauerstoff oder Schwefel zu, damit auch
    #      Mercaptopurin und Azathioprin in derselben Lage stehen.
    "purin": dict(
        vorlage="O=c1[nH]c2[nH]c(=O)[nH]c2c(=O)[nH]1",                    # harnsaeure
        muster="[#8,#16;!R]=,-;!@[#6]1:&@[#7]:&@[#6]:&@[#7]:&@[#6]2:&@[#6]:&@1"
               ":&@[#7,#6]:&@[#6,#7]:&@[#7]:&@2",
        bindung=28.0),

    # 5.4  Orotat traegt nur den Ring; es wird am Uracilring des UMP eingenordet.
    "pyrimidinring": dict(
        vorlage="O=c1ccn([C@@H]2O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]2O)c(=O)[nH]1",  # ump
        muster="[#8&!R]=&!@[#6]1:&@[#6,#7]:&@[#6]:&@[#7,#6]:&@[#6](:&@[#7]:&@1)=&!@[#8&!R]",
        bindung=22.0),

    # 5.4  UMP/dUMP/dTMP: Base, Zucker und Phosphat sind festgehalten, damit die
    #      2'-OH und die 5-Methylgruppe die einzigen Unterschiede bleiben.
    "pyrimidinnucleotid": dict(
        vorlage="O=c1ccn([C@@H]2O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]2O)c(=O)[nH]1",  # ump
        muster="[#8&!R]=&!@[#6]1:&@[#6]:&@[#6]:&@[#7](:&@[#6](:&@[#7]:&@1)=&!@[#8&!R])"
               "-&!@[#6]1-&@[#6]-&@[#6](-&@[#6](-&@[#8]-&@1)-&!@[#6&!R]-&!@[#8&!R]"
               "-&!@[#15&!R](=&!@[#8&!R])(-&!@[#8&!R])-&!@[#8&!R])-&!@[#8&!R]",
        bindung=22.0),

    # 5.5  ATP/ADP/cAMP/Adenosin teilen das ganze Adenosin.
    "adenylat": dict(
        vorlage="Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)"
                "[C@@H](O)[C@H]1O",                                       # atp
        muster="[#7&!R]-&!@[#6]1:&@[#7]:&@[#6]:&@[#7]:&@[#6]2:&@[#6]:&@1:&@[#7]:&@[#6]"
               ":&@[#7]:&@2-&!@[#6]1-&@[#8]-&@[#6]-&@[#6]-&@[#6]-&@1-&!@[#8&!R]",
        bindung=26.0),

    # 5.5  Coffein hat keine Ribose; es wird nur am Purinkern eingenordet -
    #      dieselbe Vorlage wie "adenylat", also dieselbe Lage des Rings.
    "purinkern": dict(
        vorlage="Nc1ncnc2n(cnc12)[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)"
                "[C@@H](O)[C@H]1O",                                       # atp
        muster="[#7]1:&@[#6](=,-;!@[#8,#7;!R]):&@[#6]2:&@[#6](:&@[#7]:&@[#6]:&@1)"
               ":&@[#7]:&@[#6]:&@[#7]:&@2",
        bindung=26.0),

    # 5.6  Inositol und IP3 teilen den ganzen Cyclohexanhexol-Ring.
    "inosit": dict(
        vorlage="O=P(O)(O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(=O)(O)O)"
                "[C@H](OP(=O)(O)O)[C@H]1O",                               # ip3
        muster="[#8&!R]-&!@[#6]1-&@[#6](-&!@[#8&!R])-&@[#6](-&!@[#8&!R])-&@[#6]"
               "(-&@[#6](-&@[#6]-&@1-&!@[#8&!R])-&!@[#8&!R])-&!@[#8&!R]",
        bindung=40.0),

    # 5.4  Leflunomid und sein offenkettiger Metabolit: Anilid und CF3 liegen fest,
    #      der geoeffnete Isoxazolring ist der ganze Unterschied.
    "flunomid": dict(
        vorlage="Cc1oncc1C(=O)Nc1ccc(cc1)C(F)(F)F",                       # leflunomid
        muster="[#6](=[#8])-[#7]-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#6](-[#9])(-[#9])-[#9]"),

    # 5.4  Cytarabin und Gemcitabin: gleicher Cytosin-Nucleosid-Rahmen,
    #      Unterschied nur an C2'.
    "cytidin": dict(
        vorlage="Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)C2(F)F)c(=O)n1",        # gemcitabin
        muster="[#7&!R]-&!@[#6]1:&@[#6]:&@[#6]:&@[#7](:&@[#6](:&@[#7]:&@1)=&!@[#8&!R])"
               "-&!@[#6]1-&@[#8]-&@[#6](-&@[#6](-&@[#6]-&@1)-&!@[#8&!R])-&!@[#6&!R]-&!@[#8&!R]"),
}

# --- Schmuck: was ausgerichtet und was farbig hinterlegt wird.
#     SCHMUCK["id"] = dict(reihe="name", hervor={"neu": SMARTS, ...})
#     gerippe = gemeinsames Geruest, neu = kommt in diesem Schritt hinzu,
#     weg = geht ab, stelle = hier findet die Reaktion statt.
SCHMUCK = {
    # -- 5.1 Glykolyse
    "glucose": dict(reihe="hexose"),
    "g6p":     dict(reihe="hexose",
                    # was die Hexokinase anhaengt
                    hervor={"neu": "[#15](=[#8])([#8])([#8])[#8]"}),
    "fbp":     dict(reihe="hexose",
                    # nur das C1-Phosphat ist neu; das C6-Phosphat stammt vom G6P
                    hervor={"neu": "[#15;$([#15][#8][CH2][#6;R]([#8H])[#8;R])]"
                                   "(=[#8])([#8])([#8])[#8]"}),
    "pyruvat": dict(reihe="c3",
                    # die Ketogruppe, die die LDH reduziert
                    hervor={"stelle": "[#6;$([#6](C)(=O)C(=O)O)]=[OX1]"}),
    "lactat":  dict(reihe="c3"),

    # -- 5.2 Pentosephosphatweg
    "ribose5p": dict(reihe="pentose"),
    "prpp":     dict(reihe="pentose",
                     # das anomere Diphosphat, die Abgangsgruppe aller PRTasen
                     hervor={"neu": "[#8]-[#15](=[#8])(-[#8])-[#8]-[#15](=[#8])(-[#8])-[#8]"}),

    # -- 5.3 Purinabbau und Gichttherapie
    "hypoxanthin":   dict(reihe="purin"),
    "xanthin":       dict(reihe="purin",
                          # die neue 2-Oxogruppe (C zwischen zwei Ring-N)
                          hervor={"neu": "[OX1]=[#6;r6;$([#6]([#7])[#7])]"}),
    "harnsaeure":    dict(reihe="purin",
                          # die neue 8-Oxogruppe sitzt im Fuenfring
                          hervor={"neu": "[OX1]=[#6;r5;$([#6]([#7])[#7])]"}),
    "allopurinol":   dict(reihe="purin",
                          # dieselbe Stelle, an der die XO auch das Xanthin angreift
                          hervor={"stelle": "[#6;H1;r6](:[#7]):[#7]"}),
    "oxypurinol":    dict(reihe="purin",
                          hervor={"neu": "[OX1]=[#6;r6;$([#6]([#7])[#7])]"}),
    "azathioprin":   dict(reihe="purin",
                          # das Nitroimidazol, das Glutathion abloest
                          hervor={"weg": "[#6]-[#7]1:[#6]:[#7]:[#6](-[#7+](=[#8])-[#8-]):[#6]:1"}),
    "mercaptopurin": dict(reihe="purin"),

    # -- 5.4 Pyrimidine
    "orotat": dict(reihe="pyrimidinring",
                   # die Carboxylgruppe, die die UMP-Synthase als CO2 abspaltet
                   hervor={"weg": "[CX3](=[OX1])[OX2H1]"}),
    "ump":    dict(reihe="pyrimidinnucleotid",
                   # die 2'-OH, die die Ribonucleotid-Reduktase entfernt
                   hervor={"weg": "[#6;R;$([#6;R]([#8])[#6;R]([#7])[#8;R])]-[#8;H1]"}),
    "dump":   dict(reihe="pyrimidinnucleotid"),
    "dtmp":   dict(reihe="pyrimidinnucleotid",
                   # die eine Methylgruppe der Thymidylat-Synthase
                   hervor={"neu": "[CH3]"}),
    "leflunomid":   dict(reihe="flunomid",
                         # die N-O-Bindung des Isoxazols, die sich oeffnet
                         hervor={"stelle": "[o;r5][n;r5]"}),
    "teriflunomid": dict(reihe="flunomid",
                         hervor={"neu": "[#6]#[#7]"}),
    "cytarabin":    dict(reihe="cytidin",
                         # die 2'-OH steht arabino, also auf der anderen Seite
                         hervor={"stelle": "[#6;R;$([#6;R]([#8])[#6;R]([#7])[#8;R])]-[#8;H1]"}),
    "gemcitabin":   dict(reihe="cytidin",
                         hervor={"neu": "[F]"}),
    "tenofovir":    dict(hervor={"neu": "[#6]-[#15](=[#8])(-[#8])-[#8]"}),

    # -- 5.5 Nucleotide als Signalmolekuele
    "atp":      dict(reihe="adenylat",
                     # der gamma-Phosphorylrest, den jede Kinase weitergibt
                     hervor={"weg": "[#15;$([#15](=[OX1])([OX2H1])([OX2H1])[OX2][#15])]"
                                    "(=[OX1])([OX2H1])[OX2H1]"}),
    "adp":      dict(reihe="adenylat"),
    "camp":     dict(reihe="adenylat",
                     # der 3',5'-Diester, den die Phosphodiesterase spaltet
                     hervor={"stelle": "[#8;R]-[#15;R](=[#8])(-[#8])-[#8;R]"}),
    "adenosin": dict(reihe="adenylat"),
    "coffein":  dict(reihe="purinkern"),

    # -- 5.6 Glucuronsaeure und Inositol
    "udp_glucuronat": dict(
        # der Glucuronylrest, den die UGT auf den Arzneistoff uebertraegt;
        # das UDP daneben ist nur die Abgangsgruppe
        hervor={"neu": "[#8]-[#6](=[#8])-[#6]1-[#8]-[#6]-[#6](-[#8])-[#6](-[#8])-[#6]-1-[#8]"}),
    "inositol": dict(reihe="inosit"),
    "ip3":      dict(reihe="inosit",
                     # die drei Phosphate an 1, 4 und 5
                     hervor={"neu": "[#8]-[#15](=[#8])(-[#8])-[#8]"}),
    "dag":      dict(),
}

MOLS = {
    # ===================== TEIL 5 : Kohlenhydrat- und Nucleotidwurzel =====================
    # -- 5.1 / 5.2 Glucose und Pentosephosphatweg
    "glucose":         ("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "g6p":             ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "fbp":             ("O=P(O)(O)OC[C@H]1O[C@](O)(COP(=O)(O)O)[C@@H](O)[C@@H]1O", None),
    "pyruvat":         ("CC(=O)C(=O)O", None),
    "lactat":          ("C[C@H](O)C(=O)O", None),
    "ribose5p":        ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H]1O", None),
    # alpha-Anomer (PQGCEDQWHSBAJP-TXICZTDVSA-N, PubChem 7339): nur die alpha-
    # Stellung des Diphosphats erklaert, warum die Phosphoribosyltransferasen
    # unter Inversion die beta-N-Glycoside der Nucleotide liefern.
    "prpp":            ("O=P(O)(O)OC[C@H]1O[C@H](OP(=O)(O)OP(=O)(O)O)[C@H](O)[C@@H]1O", None),

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
    # UDP-alpha-D-Glucuronsaeure (HDYANYHVCAPMJV-LXQIFKJMSA-N, PubChem 17473):
    # erst die alpha-Stellung erklaert, warum die UGT unter Inversion
    # beta-Glucuronide bildet - die Substrate der bakteriellen beta-Glucuronidasen.
    "udp_glucuronat":  ("OC(=O)[C@H]1O[C@H](OP(=O)(O)OP(=O)(O)OC[C@H]2O[C@@H](n3ccc(=O)[nH]c3=O)[C@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "inositol":        ("O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O", None),
    # Ins(1,4,5)P3 (MMWCIQZXVOZEGG-XJTPDSDZSA-N, PubChem 439456): zwei
    # benachbarte Phosphate an 4 und 5, ein einzelnes an 1.
    "ip3":             ("O=P(O)(O)O[C@@H]1[C@H](O)[C@H](O)[C@@H](OP(=O)(O)O)[C@H](OP(=O)(O)O)[C@H]1O", None),
    # 1,2-Diacyl-sn-glycerol, C2 = (S) (JEJLGIQLPYYGEE-XIFFEERXSA-N):
    # so faellt es aus PIP2 an; (R) waere 2,3-Diacyl-sn-glycerol.
    "dag":             ("CCCCCCCCCCCCCCCC(=O)OC[C@H](CO)OC(=O)CCCCCCCCCCCCCCC", None),

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
