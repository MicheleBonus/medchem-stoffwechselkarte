# -*- coding: utf-8 -*-
"""
Erzeugt SVG-Strukturformeln fuer die Metabolitkarte (Teil 0-3).
Ausgabe: structures.json  {id: svg-string}

Konventionen:
  - Stereodeskriptoren (R/S) werden automatisch annotiert (addStereoAnnotation)
  - Kohlenstoff/Bindungen werden auf 'currentColor' gemappt -> Theme-faehig
  - Heteroatome in einer Palette, die auf hellem UND dunklem Grund lesbar ist
  - '*'-Dummyatome tragen ein atomLabel (z.B. 'SCoA') fuer abgekuerzte Reste
"""
import json
import re
import sys
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdCIPLabeler

rdDepictor.SetPreferCoordGen(True)

# ---------------------------------------------------------------- Palette
# RGB 0..1 ; Kohlenstoff = reines Schwarz -> wird spaeter zu currentColor
PALETTE = {
    6:  (0.0, 0.0, 0.0),        # C  -> currentColor
    7:  (0.20, 0.55, 0.95),     # N  blau
    8:  (0.90, 0.25, 0.25),     # O  rot
    16: (0.80, 0.62, 0.10),     # S  ocker
    15: (0.95, 0.55, 0.15),     # P  orange
    9:  (0.25, 0.70, 0.45),     # F  gruen
    17: (0.25, 0.70, 0.45),     # Cl
    35: (0.70, 0.45, 0.20),     # Br
    53: (0.60, 0.35, 0.75),     # I  violett
    0:  (0.45, 0.45, 0.45),     # Dummy
}


def render(smiles, labels=None, scale=1.0, rotate=0.0):
    """SMILES -> SVG-String. labels: {atom_idx: 'SCoA'}"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("SMILES nicht parsebar: %s" % smiles)
    Chem.rdmolops.AssignStereochemistry(mol, cleanIt=True, force=True)
    try:
        rdCIPLabeler.AssignCIPLabels(mol)
    except Exception:
        pass

    if labels:
        for idx, txt in labels.items():
            mol.GetAtomWithIdx(int(idx)).SetProp("atomLabel", txt)

    rdDepictor.Compute2DCoords(mol)
    rdDepictor.StraightenDepiction(mol)

    n = mol.GetNumHeavyAtoms()
    w = int(min(760, max(200, 34 * (n ** 0.62))) * scale)
    h = int(w * 0.72)

    # CIP-Deskriptoren nur dort einblenden, wo sie etwas lehren. Bei Steroiden
    # und anderen Polycyclen ueberfrachten acht (R)/(S)-Marker das Ringgeruest;
    # dort traegt die Keil-Strich-Schreibweise die Information ohnehin.
    n_stereo = len(Chem.FindMolChiralCenters(mol, includeUnassigned=False, useLegacyImplementation=False))

    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.clearBackground = False
    o.addStereoAnnotation = (n_stereo <= 3)
    o.annotationFontScale = 0.62
    o.bondLineWidth = 1.6
    o.multipleBondOffset = 0.14
    o.padding = 0.06
    o.rotate = rotate
    o.updateAtomPalette(PALETTE)

    rdMolDraw2D.PrepareAndDrawMolecule(d, mol)
    d.FinishDrawing()
    svg = d.GetDrawingText()

    # Theme-Faehigkeit: reines Schwarz -> currentColor
    svg = svg.replace("#000000", "currentColor").replace("#000", "currentColor")
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = svg.replace("<svg:", "<").replace("</svg:", "</").replace("xmlns:svg=", "xmlns=")
    # Feste Masse ganz entfernen: viewBox + CSS steuern die Groesse.
    # (height='auto' waere als SVG-Attribut ungueltig und wirft einen Konsolenfehler.)
    svg = re.sub(r"\s+width='\d+px'", "", svg)
    svg = re.sub(r"\s+height='\d+px'", "", svg)
    return minify(svg)


def minify(svg):
    """RDKit-SVG entschlacken: ~60 % kleiner, optisch identisch."""
    # Header/Kommentare/Namespaces raus
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\s+xmlns:(rdkit|xlink)='[^']*'", "", svg)
    svg = re.sub(r"\s+xml:space='preserve'", "", svg)
    svg = re.sub(r"\s+version='1\.1'|\s+baseProfile='full'", "", svg)
    # RDKit-Debugklassen raus
    svg = re.sub(r"\s+class='(bond|atom)[^']*'", "", svg)
    # Inline-style -> knappe Praesentationsattribute
    def style_attr(m):
        st = dict(
            kv.split(":", 1) for kv in m.group(1).split(";") if ":" in kv
        )
        out = []
        if st.get("fill", "none") != "none":
            out.append("fill='%s'" % st["fill"].strip())
        else:
            out.append("fill='none'")
        if "stroke" in st and st["stroke"].strip() != "none":
            out.append("stroke='%s'" % st["stroke"].strip())
            sw = st.get("stroke-width", "").strip().replace("px", "")
            if sw:
                out.append("stroke-width='%s'" % sw)
        return " ".join(out)

    svg = re.sub(r"style='([^']*)'", style_attr, svg)
    # Koordinaten auf 1 Nachkommastelle
    svg = re.sub(r"(\d+)\.(\d)\d+", lambda m: "%s.%s" % (m.group(1), m.group(2)), svg)
    # Whitespace kollabieren
    svg = re.sub(r"\s*\n\s*", " ", svg)
    svg = re.sub(r"\s{2,}", " ", svg)
    return svg.strip()


# ---------------------------------------------------------------- Molekuele
# (id, SMILES, {dummy-label})
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

    # ===================== TEIL 4 : Lipidmediatoren =====================
    # -- Vorstufe und COX-Ast
    "arachidonsaeure": ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    "epa":             ("CC/C=C\\C/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", None),
    "pgg2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)OO", None),
    "pgh2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H]([C@@H]1C/C=C\\CCCC(=O)O)OO2)O", None),
    "pge2":            ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)CC(=O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgd2":            ("CCCCC[C@@H](O)/C=C/[C@H]1C(=O)C[C@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgf2a":           ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)C[C@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),
    "pgi2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H](C[C@H]2[C@@H]1C/C(=C\\CCCC(=O)O)/O2)O)O", None),
    "txa2":            ("CCCCC[C@@H](/C=C/[C@H]1[C@@H]2C[C@H](O1)O[C@@H]2C/C=C\\CCCC(=O)O)O", None),
    "txb2":            ("CCCCC[C@@H](O)/C=C/[C@H]1O[C@H](O)C[C@@H](O)[C@@H]1C/C=C\\CCCC(=O)O", None),

    # -- LOX-Ast
    "hpete5":          ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](OO)CCCC(=O)O", None),
    "hete5":           ("CCCCC/C=C\\C/C=C\\C/C=C\\C=C\\[C@@H](O)CCCC(=O)O", None),
    "lta4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@H]1O[C@@H]1CCCC(=O)O", None),
    "ltb4":            ("CCCCC/C=C\\C[C@@H](O)/C=C/C=C/C=C\\[C@@H](O)CCCC(=O)O", None),
    "ltc4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](NC(=O)CC[C@H](N)C(=O)O)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "ltd4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)NCC(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lte4":            ("CCCCC/C=C\\C/C=C\\C=C\\C=C\\[C@@H](SC[C@H](N)C(=O)O)[C@@H](O)CCCC(=O)O", None),
    "lipoxina4":       ("CCCCC[C@H](O)/C=C/C=C\\C=C\\C=C\\[C@@H](O)[C@@H](O)CCCC(=O)O", None),

    # -- Endocannabinoide und PAF
    "anandamid":       ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)NCCO", None),
    "ag2":             ("CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)OC(CO)CO", None),
    "paf":             ("CCCCCCCCCCCCCCCCOC[C@@H](OC(C)=O)COP(=O)([O-])OCC[N+](C)(C)C", None),
    "thc":             ("CCCCCc1cc(O)c2c(c1)OC(C)(C)[C@@H]1CCC(C)=C[C@H]21", None),
    "rimonabant":      ("Cc1c(-c2ccc(Cl)cc2)n(-c2ccc(Cl)cc2Cl)nc1C(=O)NN1CCCCC1", None),

    # -- Wirkstoffe am Eicosanoidsystem
    "aspirin":         ("CC(=O)Oc1ccccc1C(=O)O", None),
    # als Racemat im Handel; gezeichnet ist das wirksame (S)-Enantiomer
    "ibuprofen":       ("CC(C)Cc1ccc(cc1)[C@H](C)C(=O)O", None),
    "naproxen":        ("COc1ccc2cc(ccc2c1)[C@H](C)C(=O)O", None),
    "diclofenac":      ("OC(=O)Cc1ccccc1Nc1c(Cl)cccc1Cl", None),
    "indometacin":     ("COc1ccc2c(c1)c(CC(=O)O)c(C)n2C(=O)c1ccc(Cl)cc1", None),
    "celecoxib":       ("Cc1ccc(cc1)-c1cc(nn1-c1ccc(cc1)S(N)(=O)=O)C(F)(F)F", None),
    "etoricoxib":      ("Cc1ccc(cn1)-c1ncc(Cl)cc1-c1ccc(cc1)S(C)(=O)=O", None),
    "zileuton":        ("CC(N(O)C(N)=O)c1cc2ccccc2s1", None),
    "montelukast":     ("CC(C)(O)c1ccccc1CC[C@H](SCC1(CC1)CC(=O)O)c1cccc(/C=C/c2ccc3ccc(Cl)cc3n2)c1", None),
    "misoprostol":     ("CCCC[C@](C)(O)C/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1CCCCCCC(=O)OC", None),
    "alprostadil":     ("CCCCC[C@@H](O)/C=C/[C@H]1[C@@H](O)CC(=O)[C@@H]1CCCCCCC(=O)O", None),
    "latanoprost":     ("CC(C)OC(=O)CCC/C=C\\C[C@H]1[C@@H](O)C[C@@H](O)[C@@H]1CC[C@@H](O)CCc1ccccc1", None),

    # ===================== TEIL 5 : Kohlenhydrat- und Nucleotidwurzel =====================
    # -- 5.1 / 5.2 Glucose und Pentosephosphatweg
    "glucose":         ("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "g6p":             ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "fbp":             ("O=P(O)(O)OC[C@H]1O[C@](O)(COP(=O)(O)O)[C@@H](O)[C@@H]1O", None),
    "pyruvat":         ("CC(=O)C(=O)O", None),
    "lactat":          ("C[C@H](O)C(=O)O", None),
    "ribose5p":        ("O=P(O)(O)OC[C@H]1O[C@@H](O)[C@H](O)[C@@H]1O", None),
    "prpp":            ("O=P(O)(O)OC[C@H]1O[C@@H](OP(=O)(O)OP(=O)(O)O)[C@H](O)[C@@H]1O", None),

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
    "udp_glucuronat":  ("OC(=O)[C@H]1O[C@@H](OP(=O)(O)OP(=O)(O)OC[C@H]2O[C@@H](n3ccc(=O)[nH]c3=O)[C@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O", None),
    "inositol":        ("O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@H](O)[C@@H]1O", None),
    "ip3":             ("O[C@H]1[C@@H](OP(=O)(O)O)[C@H](O)[C@@H](OP(=O)(O)O)[C@H](O)[C@H]1OP(=O)(O)O", None),
    "dag":             ("CCCCCCCCCCCCCCCC(=O)OC[C@@H](CO)OC(=O)CCCCCCCCCCCCCCC", None),

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

    # ===================== TEIL 6 : Cofaktoren =====================
    # -- wasserloesliche
    "thiamin":         ("Cc1ncc(C[n+]2csc(CCO)c2C)c(N)n1", None),
    "tpp":             ("Cc1ncc(C[n+]2csc(CCOP(=O)(O)OP(=O)(O)O)c2C)c(N)n1", None),
    "riboflavin":      ("Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)CO)c2cc1C", None),
    "fmn":             ("Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(C[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)O)c2cc1C", None),
    "nicotinsaeure":   ("OC(=O)c1cccnc1", None),
    "nicotinamid":     ("NC(=O)c1cccnc1", None),
    "pantothensaeure": ("CC(C)(CO)[C@@H](O)C(=O)NCCC(=O)O", None),
    "coa":             ("SCCNC(=O)CCNC(=O)[C@H](O)C(C)(C)COP(=O)(O)OP(=O)(O)OC[C@H]1O[C@@H](n2cnc3c(N)ncnc32)[C@H](O)[C@@H]1OP(=O)(O)O", None),
    "pyridoxin":       ("Cc1ncc(CO)c(CO)c1O", None),
    "pyridoxal":       ("Cc1ncc(CO)c(C=O)c1O", None),
    "biotin":          ("O=C1N[C@@H]2CS[C@@H](CCCCC(=O)O)[C@@H]2N1", None),
    "carboxybiotin":   ("OC(=O)N1[C@@H]2CS[C@@H](CCCCC(=O)O)[C@@H]2NC1=O", None),
    "dhf":             ("Nc1nc2NCC(CNc3ccc(cc3)C(=O)N[C@@H](CCC(=O)O)C(=O)O)=Nc2c(=O)[nH]1", None),

    # -- nicht-Vitamin-Cofaktoren
    "dehydroascorbat": ("OC[C@H](O)[C@H]1OC(=O)C(=O)C1=O", None),
    "liponsaeure":     ("OC(=O)CCCC[C@@H]1CCSS1", None),
    "dihydroliponsaeure": ("OC(=O)CCCC[C@@H](S)CCS", None),

    # -- fettloesliche
    "retinol":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/CO)C(C)(C)CCC1", None),
    "retinal":         ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C=O)C(C)(C)CCC1", None),
    "tretinoin":       ("CC1=C(/C=C/C(C)=C/C=C/C(C)=C/C(=O)O)C(C)(C)CCC1", None),
    "isotretinoin":    ("CC1=C(/C=C/C(C)=C/C=C\\C(C)=C/C(=O)O)C(C)(C)CCC1", None),
    "tocopherol":      ("Cc1c(C)c2c(c(C)c1O)CC[C@](C)(CCC[C@H](C)CCC[C@H](C)CCCC(C)C)O2", None),
    "phyllochinon":    ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)C(=O)c2ccccc2C1=O", None),
    "vitk_hydrochinon": ("CC1=C(C/C=C(C)/CCC[C@H](C)CCC[C@H](C)CCCC(C)C)c(O)c2ccccc2c1O", None),
    "menadion":        ("CC1=CC(=O)c2ccccc2C1=O", None),

    # -- Wirkstoffe am Cofaktornetz
    "isoniazid":       ("O=C(NN)c1ccncc1", None),
    "warfarin":        ("CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),
    "phenprocoumon":   ("CCC(c1ccccc1)c1c(O)c2ccccc2oc1=O", None),

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

# Dummy-Atome ('*') automatisch mit 'CoA' beschriften
COA_IDS = {"acetyl_coa_abbr", "acetoacetyl_coa", "hmg_coa", "malonyl_coa"}


def main():
    out, fails = {}, []
    for mid, (smi, labels) in MOLS.items():
        try:
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                raise ValueError("Parse-Fehler")
            lbl = dict(labels) if labels else {}
            if mid in COA_IDS:
                for a in mol.GetAtoms():
                    if a.GetAtomicNum() == 0:
                        lbl[a.GetIdx()] = "CoA"
            out[mid] = render(smi, lbl)
        except Exception as e:
            fails.append((mid, smi, str(e)))

    with open("structures.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)

    print("OK: %d Strukturen" % len(out))
    if fails:
        print("\nFEHLER (%d):" % len(fails))
        for mid, smi, e in fails:
            print("  %-22s %s\n      %s" % (mid, e, smi))
        sys.exit(1)


if __name__ == "__main__":
    main()
