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
    # 3-O-Methyl-L-DOPA: COMT-Produkt aus L-DOPA, alpha-C bleibt S (L).
    "omd":             ("COc1cc(C[C@H](N)C(=O)O)ccc1O", None),
    "methoxytyramin":  ("COc1cc(CCN)ccc1O", None),
    "dopac":           ("OC(=O)Cc1ccc(O)c(O)c1", None),
    "hva":             ("COc1cc(CC(=O)O)ccc1O", None),
    "normetanephrin":  ("COc1cc(C(O)CN)ccc1O", None),
    "metanephrin":     ("CNC[C@H](O)c1ccc(O)c(OC)c1", None),
    "vma":             ("COc1cc([C@@H](O)C(=O)O)ccc1O", None),
    "tyramin":         ("NCCc1ccc(O)cc1", None),
    # L-Dopachinon: die Tyrosinase oxidiert nur den Ring, alpha-C bleibt S (L).
    "dopachinon":      ("O=C1C(=O)C=C(C[C@H](N)C(=O)O)C=C1", None),
    "cyclodopa":       ("OC(=O)[C@@H]1Cc2cc(O)c(O)cc2N1", None),
    "dhi":             ("Oc1cc2[nH]ccc2cc1O", None),
    "dhica":           ("OC(=O)c1cc2cc(O)c(O)cc2[nH]1", None),
    "mit":             ("N[C@@H](Cc1ccc(O)c(I)c1)C(=O)O", None),
    "dit":             ("N[C@@H](Cc1cc(I)c(O)c(I)c1)C(=O)O", None),
    "t4":              ("N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)c(I)c1)C(=O)O", None),
    "t3":              ("N[C@@H](Cc1cc(I)c(Oc2ccc(O)c(I)c2)c(I)c1)C(=O)O", None),
    "rt3":             ("N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)cc1)C(=O)O", None),
    "tryptophan":      ("N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O", None),
    # Dieselbe Aminosaeure, zweite Lage: eine id traegt genau ein Bild, und
    # 2.6 (Indolamin-Reihe) und 2.7 (Kynureninweg) wollen verschiedene Lagen.
    "tryptophan_kyn":  ("N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O", None),
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
    # Sapropterin = (6R)-6-[(1R,2S)-1,2-Dihydroxypropyl]-BH4; die Seitenkette
    # ist (1'R,2'S), nicht umgekehrt.  Dieselbe Seitenkette in 4a-OH-BH4 und BH2.
    "bh4":             ("C[C@H](O)[C@H](O)[C@H]1CNc2nc(N)[nH]c(=O)c2N1", None),
    "bh4_4a_oh":       ("C[C@H](O)[C@H](O)[C@H]1CNC2=NC(N)=NC(=O)C2(O)N1", None),
    # 7,8-Dihydrobiopterin: C4a grenzt an C4=O, C8a an N1 (vorher verdreht).
    "bh2":             ("C[C@H](O)[C@H](O)C1=Nc2c(=O)[nH]c(N)nc2NC1", None),
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
    # Thion-Form: nur so ist die Thioharnstoff-Partialstruktur zu sehen,
    # und nur so passt das Bild zum Prodrug Carbimazol daneben.
    "thiamazol":       ("CN1C=CNC1=S", None),
    "carbimazol":      ("CCOC(=O)n1ccn(C)c1=S", None),
    "propylthiouracil": ("CCCc1cc(=O)[nH]c(=S)[nH]1", None),
    "fluoxetin":       ("CNCC[C@H](Oc1ccc(cc1)C(F)(F)F)c1ccccc1", None),
    "vigabatrin":      ("C=C[C@@H](N)CCC(=O)O", None),
}


# =====================================================================
#  REIHEN
# =====================================================================
# Der Catecholkern zieht sich durch 2.2, 2.3 und 2.4. Damit der Leser den
# Ring nicht in jedem Bild neu einnorden muss, liegen alle Glieder in der
# Lage von L-DOPA: Seitenkette rechts unten, 4-OH links oben, 3-OH links.
#
# Drei Muster, eine Vorlage: der Builder haelt je Molekuel nur die Atome
# fest, die sein Muster trifft, und die Vorlage ist fuer alle drei dieselbe
# (ein einziges Compute2DCoords auf ldopa). Damit liegen die Ringe der drei
# Gruppen aufeinander, obwohl sie verschieden viele Sauerstoffe tragen.
#
#   catechol        Brenzcatechinring: Alkyl-C, 3-O und 4-O.  Weil beide
#                   Sauerstoffe im Muster stehen, gibt es genau einen
#                   Treffer je Molekuel - kein Umklappen des Rings.
#   catechol_mono   dieselbe Lage fuer die Monophenole (Tyrosin, Metirosin,
#                   Tyramin); ihr Ring ist zur 1,4-Achse spiegelsymmetrisch,
#                   deshalb genuegt hier das 8-Atom-Muster.
#   catechol_ring   Phenylalanin, das noch gar keinen Sauerstoff traegt:
#                   Anker ist das Aminosaeuregeruest samt Ring.
_LDOPA = "N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O"
_BINDUNG = 17.0

REIHEN["catechol"] = dict(
    vorlage=_LDOPA, bindung=_BINDUNG,
    muster="[#6]~[#6]1~[#6]~[#6](~[#8])~[#6](~[#8])~[#6]~[#6]1")
REIHEN["catechol_mono"] = dict(
    vorlage=_LDOPA, bindung=_BINDUNG,
    muster="[#6]~[#6]1~[#6]~[#6]~[#6](~[#8])~[#6]~[#6]1")
REIHEN["catechol_ring"] = dict(
    vorlage=_LDOPA, bindung=_BINDUNG,
    muster="[#7]~[#6](~[#6]~c1ccccc1)~[#6](~[#8])~[#8]")

# Der Schilddruesenast sagt nur eines: WELCHES Iod fehlt. Das ist nur
# ablesbar, wenn innerer und aeusserer Ring in allen fuenf Bildern an
# derselben Stelle liegen. Vorlage ist T4, das einzige Glied, das alle vier
# Iodatome traegt.
#   thyronin       das ganze Diphenyletherzeruest samt beider Iodpositionen
#                  (T4, T3, rT3) - so kann der aeussere Ring nicht wandern.
#   thyronin_mono  MIT und DIT haben noch keinen zweiten Ring; ihr Anker ist
#                  der innere Ring mit dem 4-Sauerstoff, der spaeter zur
#                  Etherbruecke wird.
_T4 = "N[C@@H](Cc1cc(I)c(Oc2cc(I)c(O)c(I)c2)c(I)c1)C(=O)O"

REIHEN["thyronin"] = dict(
    vorlage=_T4, bindung=_BINDUNG,
    muster="[#7]~[#6](~[#6](~[#8])~[#8])~[#6]~c1cc(-I)c(-[#8]-c2cc(-I)c(-[#8])cc2)cc1")
REIHEN["thyronin_mono"] = dict(
    vorlage=_T4, bindung=_BINDUNG,
    muster="[#7]~[#6](~[#6](~[#8])~[#8])~[#6]~c1cc(-I)c(~[#8])cc1")

# Indol-Ethylamin-Kern: vier Schritte, vier Farbflecken an vier Stellen
# desselben unveraenderten Kerns.
REIHEN["indolamin"] = dict(
    vorlage="COc1ccc2[nH]cc(CCNC(C)=O)c2c1", bindung=_BINDUNG,
    muster="[#6]~[#6]~c1c[nH]c2ccccc12")

# Kynureninweg: der geoeffnete Ring bleibt als Anthranilsaeure-Teilstueck
# erhalten - Aminogruppe und Carbonyl stehen ortho zueinander.
_FORMYLKYNURENIN = "O=CNc1ccccc1C(=O)C[C@H](N)C(=O)O"
REIHEN["kynurenin"] = dict(
    vorlage=_FORMYLKYNURENIN, bindung=_BINDUNG,
    muster="[#7]~c1ccccc1~[#6]~[#8]")
# Der Ringoeffnungsschritt: Indol-N1 wird zum Anilin-Stickstoff, Indol-C3 zum
# Ketokohlenstoff. Genau diese Zuordnung haelt das Muster fest, damit der
# geoeffnete Ring ueber dem geschlossenen liegt.
REIHEN["kynurenin_indol"] = dict(
    vorlage=_FORMYLKYNURENIN, bindung=_BINDUNG,
    muster="[#7]~c1ccccc1~[#6]")

# 4-Hydroxychinolin-2-carbonsaeure: Kynuren- und Xanthurensaeure
# unterscheiden sich nur in der 8-OH.
REIHEN["chinolin"] = dict(
    vorlage="OC(=O)c1cc(O)c2cccc(O)c2n1", bindung=_BINDUNG,
    muster="[#8]~[#6](~[#8])~c1cc(~[#8])c2ccccc2n1")

# Imidazol + Ethylamin. Das Muster laeuft vom Ringkohlenstoff aus ueber
# c-n-c-n und legt damit fest, welcher Ringstickstoff wo liegt; sonst
# koennte das N-Methylhistamin gespiegelt erscheinen.
REIHEN["imidazol"] = dict(
    vorlage="N[C@@H](Cc1c[nH]cn1)C(=O)O", bindung=_BINDUNG,
    muster="[#6]~[#6]~c1cncn1")

# Thyreostatika. Das Methyl im Muster zwingt Thiamazol und sein Prodrug
# Carbimazol auf denselben Ringstickstoff; sonst laege der Carbamatrest
# auf der Seite, die im Thiamazol das freie NH traegt.
_CARBIMAZOL = "CCOC(=O)n1ccn(C)c1=S"
REIHEN["thioamid"] = dict(
    vorlage=_CARBIMAZOL, bindung=_BINDUNG,
    muster="[#16]~[#6]1~[#7](~[CH3])~[#6]~[#6]~[#7]1")
REIHEN["thioamid_ring6"] = dict(
    vorlage=_CARBIMAZOL, bindung=_BINDUNG,
    muster="[#7]~[#6](~[#16])~[#7]")

# Pterinbicyclus: BH4 und seine Carbinolamin-Stufe.
REIHEN["pterin"] = dict(
    vorlage="C[C@H](O)[C@H](O)[C@H]1CNc2nc(N)[nH]c(=O)c2N1", bindung=_BINDUNG,
    muster="[#6]~[#6]1~[#6]~[#7]~[#6]2~[#7]~[#6](~[#7])~[#7]~[#6](~[#8])~[#6]~2~[#7]~1")

# MAO-B-Hemmer: gemeinsam ist nur der Aromat mit einem Kohlenstoff daran.
REIHEN["propargylamin"] = dict(
    vorlage="C#CCN(C)[C@H](C)Cc1ccccc1", bindung=_BINDUNG,
    muster="[#6]#[#6]~[#6]~[#7]")


# =====================================================================
#  SCHMUCK  -  Ausrichtung und Farbe
# =====================================================================
# Farbregel: hoechstens eine Farbe je Kachel, und nur, wo die Aussage
# stimmt. Wiederkehrende Aussagen tragen immer dieselbe Farbe:
#   neu    was der Schritt bringt (jede SAM-Methylgruppe, jede neue OH)
#   weg    was abgeht (der Carbamatrest des Prodrugs)
#   stelle wo angegriffen wird (Mg-Koordination, Deiodierung, Thion-S)

# --- wiederkehrende Teilstrukturen ------------------------------------
_METHYL_O = "[CH3;$([CH3][OX2]c)]"          # COMT/ASMT: O-Methyl am Aromaten
_METHYL_N = "[CH3;$([CH3][NX3;H1])]"        # PNMT: N-Methyl
_METHYL_NAR = "[CH3;$([CH3]n)]"             # HNMT: N-Methyl am Imidazol
_PHENOL_OH = "[OX2H1;$([OX2H1]c)]"          # eine einzelne phenolische OH
_CARBOXYL = "[CX3](=[OX1])[OX2H1]"          # neue Saeurefunktion (MAO + ALDH)
_ALPHA_METHYL = "[CH3;$([CH3][CX4]([#7])([#6])C(=O)[OX2H1])]"


def _s(reihe, **hervor):
    d = dict(reihe=reihe)
    if hervor:
        d["hervor"] = hervor
    return d


# --- 2.1  Phenylalanin -> Tyrosin, BH4 --------------------------------
SCHMUCK["phenylalanin"] = _s("catechol_ring")
SCHMUCK["bh4"] = _s("pterin")
SCHMUCK["bh4_4a_oh"] = _s(
    "pterin", neu="[OX2H1;$([OX2H1][CX4]([#7])[#6]=[OX1])]")
SCHMUCK["bh2"] = _s("pterin")

# --- 2.2  Catecholaminstrang ------------------------------------------
SCHMUCK["tyrosin"] = _s("catechol_mono")
SCHMUCK["ldopa"] = _s(
    "catechol", neu="[OX2H1;$([OX2H1]c1cc(-[#6])ccc1-[#8])]")
SCHMUCK["dopamin"] = _s("catechol")
SCHMUCK["noradrenalin"] = _s(
    "catechol", neu="[OX2H1;$([OX2H1][CX4]([#6][#7])c)]")
SCHMUCK["adrenalin"] = _s("catechol", neu=_METHYL_N)
SCHMUCK["tyramin"] = _s("catechol_mono")
SCHMUCK["normetanephrin"] = _s("catechol", neu=_METHYL_O)
SCHMUCK["metanephrin"] = _s("catechol", neu=_METHYL_O)

SCHMUCK["carbidopa"] = _s("catechol", stelle="[NX3;H1,H2][NX3;H1,H2]")
SCHMUCK["benserazid"] = _s("catechol", stelle="[NX3;H1,H2][NX3;H1,H2]")
SCHMUCK["metirosin"] = _s("catechol_mono", neu=_ALPHA_METHYL)
SCHMUCK["methyldopa"] = _s("catechol", neu=_ALPHA_METHYL)

# --- 2.3  Abbau ueber MAO und COMT ------------------------------------
SCHMUCK["dopac"] = _s("catechol", neu=_CARBOXYL)
SCHMUCK["methoxytyramin"] = _s("catechol", neu=_METHYL_O)
SCHMUCK["hva"] = _s("catechol", neu=_METHYL_O)
SCHMUCK["omd"] = _s("catechol", neu=_METHYL_O)
SCHMUCK["vma"] = _s("catechol", neu=_METHYL_O)

SCHMUCK["entacapon"] = _s("catechol", stelle=_PHENOL_OH)
SCHMUCK["tolcapon"] = _s("catechol", stelle=_PHENOL_OH)
SCHMUCK["selegilin"] = _s("propargylamin", stelle="[CH0]#[CH1]")
SCHMUCK["rasagilin"] = _s("propargylamin", stelle="[CH0]#[CH1]")

# --- 2.4  Melaninast ---------------------------------------------------
SCHMUCK["dopachinon"] = _s("catechol", stelle="[OX1]=[#6]~[#6]=[OX1]")
SCHMUCK["cyclodopa"] = _s("catechol", neu="[NX3;R]~c")
SCHMUCK["dhi"] = _s("catechol")
SCHMUCK["dhica"] = _s("catechol")

# --- 2.5  Schilddruese -------------------------------------------------
SCHMUCK["mit"] = _s("thyronin_mono")
SCHMUCK["dit"] = _s("thyronin_mono")
SCHMUCK["t4"] = _s("thyronin")
# Das entfernte Iod laesst sich nicht malen - wohl aber die Stelle, an der
# es sass. Bei T3 ist das ein CH des aeusseren (phenolischen) Rings, bei
# rT3 eines des inneren. Genau daran haengt "aussen aktiviert, innen
# inaktiviert".
SCHMUCK["t3"] = _s(
    "thyronin", stelle="[cH1;$([cH1]:[c](-[OX2H1]):[c]-I)]")
SCHMUCK["rt3"] = _s(
    "thyronin", stelle="[cH1;$([cH1]:[c](-[OX2]-[c]):[c]-I)]")

SCHMUCK["thiamazol"] = _s("thioamid", stelle="[SX1]~[#6]")
SCHMUCK["carbimazol"] = _s("thioamid", weg="[CH3][CH2][OX2][CX3]=[OX1]")
SCHMUCK["propylthiouracil"] = _s("thioamid_ring6", stelle="[SX1]~[#6]")

# --- 2.6  Tryptophan -> Serotonin -> Melatonin -------------------------
SCHMUCK["tryptophan"] = _s("indolamin")
SCHMUCK["hydroxytryptophan"] = _s("indolamin", neu=_PHENOL_OH)
SCHMUCK["serotonin"] = _s("indolamin")
SCHMUCK["nacetylserotonin"] = _s("indolamin", neu=(
    "[$([CH3][CX3](=[OX1])[NX3]),"
    "$([CX3](=[OX1])([CH3])[NX3]),"
    "$([OX1]=[CX3]([CH3])[NX3])]"))
SCHMUCK["melatonin"] = _s("indolamin", neu=_METHYL_O)
SCHMUCK["hiaa"] = _s("indolamin", neu=_CARBOXYL)
SCHMUCK["tryptamin"] = _s("indolamin")

# --- 2.7  Kynureninweg -------------------------------------------------
# Beide Sauerstoffatome stammen aus demselben O2-Molekuel: TDO/IDO ist
# eine Dioxygenase, das ist die Aussage der Kachel.
# Die C2-C3-Bindung des Indols ist die Bindung, die TDO/IDO spaltet.
SCHMUCK["tryptophan_kyn"] = _s(
    "kynurenin_indol", stelle="[c;$(c[nH])]~[c;$(c[CH2])]")
SCHMUCK["formylkynurenin"] = _s("kynurenin", neu=(
    "[OX1;$([OX1]=[CX3H1][NX3]),$([OX1]=[CX3]([#6])[#6])]"))
SCHMUCK["kynurenin"] = _s("kynurenin")
SCHMUCK["hydroxykynurenin"] = _s("kynurenin", neu=_PHENOL_OH)
SCHMUCK["hydroxyanthranilat"] = _s("kynurenin")
SCHMUCK["kynurensaeure"] = _s("chinolin")
SCHMUCK["xanthurensaeure"] = _s(
    "chinolin", neu="[OX2H1;$([OX2H1]c:c:n)]")

# --- 2.8  Histidin -> Histamin -----------------------------------------
SCHMUCK["histidin"] = _s("imidazol")
SCHMUCK["histamin"] = _s("imidazol")
SCHMUCK["methylhistamin"] = _s("imidazol", neu=_METHYL_NAR)
SCHMUCK["imidazolessig"] = _s("imidazol", neu=_CARBOXYL)
SCHMUCK["urocanat"] = _s("imidazol")
