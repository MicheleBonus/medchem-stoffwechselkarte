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
import math
import re
import sys
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdCIPLabeler
from rdkit.Chem import rdFMCS

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


# ------------------------------------------------------- Ausrichtung in Reihen
# Verwandte Strukturen, die nebeneinander stehen, muessen dieselbe Lage haben.
# Sonst muss der Leser jedes Bild neu einnorden, bevor er den Unterschied sieht.
# Zu jeder Reihe gehoert eine Vorlage (deren 2D-Lage gilt) und ein Muster, das
# alle Glieder gemeinsam haben; nur die Muster-Atome werden festgehalten.
#   REIHEN[name] = dict(vorlage=SMILES, bindung=px, muster=SMARTS)
# vorlage  gibt die Lage vor; am besten das groesste Glied der Reihe
# bindung  feste Bindungslaenge in Bildpunkten, damit die Glieder massstabsgleich
#          nebeneinander stehen (ohne das wird das groesste Molekuel geschrumpft)
# muster   optional; ohne Angabe sucht der Builder selbst die groesste
#          gemeinsame Teilstruktur von Vorlage und Molekuel und haelt sie fest
REIHEN = {}
_VORLAGE = {}        # name -> Molekuel mit Konformer, einmal berechnet


def vorlage(name):
    if name not in _VORLAGE:
        ref = Chem.MolFromSmiles(REIHEN[name]["vorlage"])
        if ref is None:
            raise ValueError("Reihenvorlage nicht parsebar: %s" % REIHEN[name]["vorlage"])
        rdDepictor.Compute2DCoords(ref)
        rdDepictor.StraightenDepiction(ref)
        grad = REIHEN[name].get("drehung", 0.0)
        if grad:
            # Die Vorlage einmal drehen; alle Glieder erben die Lage. Am fertigen
            # Bild zu drehen ginge auch, machte aber die Groessenrechnung falsch.
            w = math.radians(grad)
            k = ref.GetConformer()
            for i in range(ref.GetNumAtoms()):
                p = k.GetAtomPosition(i)
                k.SetAtomPosition(i, (p.x * math.cos(w) - p.y * math.sin(w),
                                      p.x * math.sin(w) + p.y * math.cos(w), 0.0))
        _VORLAGE[name] = ref
    return _VORLAGE[name]


def gemeinsames_muster(mol, ref):
    """Groesste gemeinsame Teilstruktur als SMARTS-Molekuel."""
    res = rdFMCS.FindMCS(
        [Chem.Mol(mol), Chem.Mol(ref)],
        atomCompare=rdFMCS.AtomCompare.CompareElements,
        bondCompare=rdFMCS.BondCompare.CompareAny,
        ringMatchesRingOnly=True, completeRingsOnly=False,
        matchValences=False, timeout=20)
    if res.canceled or res.numAtoms < 3:
        return None
    return Chem.MolFromSmarts(res.smartsString)


# -------------------------------------------------------------- Hervorhebungen
# RDKit malt Hervorhebungen mit festen Farben. Damit sie in hell und dunkel
# taugen, werden vier unmoegliche Signalfarben gezeichnet und danach gegen
# CSS-Variablen getauscht: die Seite entscheidet, wie kraeftig der Ton wird.
SIGNAL = {
    "gerippe": ((0.0, 1.0, 1.0), "#00FFFF", "var(--hl-gerippe)"),
    "neu":     ((1.0, 0.0, 1.0), "#FF00FF", "var(--hl-neu)"),
    "weg":     ((1.0, 1.0, 0.0), "#FFFF00", "var(--hl-weg)"),
    "stelle":  ((0.0, 1.0, 0.0), "#00FF00", "var(--hl-stelle)"),
}


def _treffer(mol, was):
    """was: Liste von Atomindizes oder ein SMARTS -> Menge von Indizes."""
    if isinstance(was, str):
        patt = Chem.MolFromSmarts(was)
        if patt is None:
            raise ValueError("SMARTS nicht parsebar: %s" % was)
        gefunden = mol.GetSubstructMatches(patt)
        if not gefunden:
            raise ValueError("SMARTS trifft nicht: %s" % was)
        return set(i for m in gefunden for i in m)
    return set(int(i) for i in was)


def render(smiles, labels=None, scale=1.0, rotate=0.0, reihe=None, hervor=None):
    """SMILES -> SVG-String.

    labels  {atom_idx: 'SCoA'}   Beschriftung fuer Dummy-Atome
    reihe   Name aus REIHEN      richtet die Struktur an der Reihenvorlage aus
    hervor  {'neu': SMARTS oder [idx], ...}  hinterlegt Molekuelteile farbig
    """
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

    gelegt = False
    if reihe:
        if reihe not in REIHEN:
            raise ValueError("unbekannte Reihe: %s" % reihe)
        ref = vorlage(reihe)
        vorgabe = REIHEN[reihe].get("muster")
        muster = Chem.MolFromSmarts(vorgabe) if vorgabe else gemeinsames_muster(mol, ref)
        if muster is None:
            raise ValueError("Reihe %r: keine gemeinsame Teilstruktur gefunden" % reihe)
        if not mol.GetSubstructMatch(muster) or not ref.GetSubstructMatch(muster):
            raise ValueError("Reihe %r: Muster trifft nicht" % reihe)
        rdDepictor.GenerateDepictionMatching2DStructure(
            mol, ref, refPatt=muster, acceptFailure=False)
        gelegt = True

    if not gelegt:
        rdDepictor.Compute2DCoords(mol)
        rdDepictor.StraightenDepiction(mol)

    fest = REIHEN.get(reihe, {}).get("bindung") if reihe else None
    if fest:
        # Massstabsgleich: die Leinwand waechst mit dem Molekuel, nicht umgekehrt.
        # Ohne das schrumpft RDKit das groesste Glied einer Reihe, und der
        # Vergleich, um dessentwillen die Bilder nebeneinanderstehen, geht verloren.
        k = mol.GetConformer()
        xs = [k.GetAtomPosition(i).x for i in range(mol.GetNumAtoms())]
        ys = [k.GetAtomPosition(i).y for i in range(mol.GetNumAtoms())]
        rand = 2.0
        w = int((max(xs) - min(xs) + rand) * fest * scale)
        h = int((max(ys) - min(ys) + rand) * fest * scale)
    else:
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
    o.rotate = 0.0 if reihe else rotate
    o.updateAtomPalette(PALETTE)
    if fest:
        o.centreMoleculesBeforeDrawing = True
        o.fixedBondLength = fest * scale

    atome, atomfarben, bindungen, bindfarben = [], {}, [], {}
    if hervor:
        for schluessel, was in hervor.items():
            if schluessel not in SIGNAL:
                raise ValueError("unbekannte Hervorhebung: %s" % schluessel)
            rgb = SIGNAL[schluessel][0]
            idx = _treffer(mol, was)
            for i in idx:
                atome.append(i)
                atomfarben[i] = rgb
            for b in mol.GetBonds():
                if b.GetBeginAtomIdx() in idx and b.GetEndAtomIdx() in idx:
                    bindungen.append(b.GetIdx())
                    bindfarben[b.GetIdx()] = rgb
        o.highlightRadius = 0.30
        o.highlightBondWidthMultiplier = 14

    if hervor:
        rdMolDraw2D.PrepareAndDrawMolecule(
            d, mol, highlightAtoms=atome, highlightAtomColors=atomfarben,
            highlightBonds=bindungen, highlightBondColors=bindfarben)
    else:
        rdMolDraw2D.PrepareAndDrawMolecule(d, mol)
    d.FinishDrawing()
    svg = d.GetDrawingText()

    # Theme-Faehigkeit: reines Schwarz -> currentColor
    svg = svg.replace("#000000", "currentColor").replace("#000", "currentColor")
    for _, sentinel, css in SIGNAL.values():
        svg = svg.replace(sentinel, css).replace(sentinel.lower(), css)
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = svg.replace("<svg:", "<").replace("</svg:", "</").replace("xmlns:svg=", "xmlns=")
    # Feste Masse ganz entfernen: viewBox + CSS steuern die Groesse.
    # (height='auto' waere als SVG-Attribut ungueltig und wirft einen Konsolenfehler.)
    svg = re.sub(r"\s+height='\d+px'", "", svg)
    if fest:
        # In einer Reihe traegt das Bild seine Groesse selbst: der Kasten richtet
        # sich nach dem Molekuel, damit die Bindungslaengen nebeneinander gleich
        # bleiben. Ohne feste Bindungslaenge bestimmt die Spaltenbreite den
        # Massstab, und das breiteste Molekuel wird das kleinste.
        svg = re.sub(r"\s+width='(\d+)px'", r" width='\1'", svg)
    else:
        svg = re.sub(r"\s+width='\d+px'", "", svg)
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

# Die Strukturen liegen nach Teilen getrennt in strukturen/.
MOLS, _REIHEN, _SCHMUCK = {}, {}, {}
for _t in ("teil1", "teil2", "teil3", "teil4", "teil5", "teil6", "teil7", "teil8"):
    _mod = __import__("strukturen.%s" % _t, fromlist=["MOLS"])
    _doppelt = set(_mod.MOLS) & set(MOLS)
    if _doppelt:
        raise SystemExit("ABBRUCH: id doppelt vergeben: %s" % ", ".join(sorted(_doppelt)))
    MOLS.update(_mod.MOLS)
    _REIHEN.update(getattr(_mod, "REIHEN", {}))
    _SCHMUCK.update(getattr(_mod, "SCHMUCK", {}))


# Dummy-Atome ('*') automatisch mit 'CoA' beschriften
COA_IDS = {"acetyl_coa_abbr", "acetoacetyl_coa", "hmg_coa", "malonyl_coa"}


REIHEN.update(_REIHEN)
SCHMUCK = _SCHMUCK


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
            out[mid] = render(smi, lbl, **SCHMUCK.get(mid, {}))
        except Exception as e:
            fails.append((mid, smi, str(e)))

    unbekannt = sorted(set(SCHMUCK) - set(MOLS))
    if unbekannt:
        fails.append(("SCHMUCK", "", "ids ohne Struktur: %s" % ", ".join(unbekannt)))

    with open("structures.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)

    print("OK: %d Strukturen, davon %d ausgerichtet oder hervorgehoben"
          % (len(out), len([k for k in SCHMUCK if k in out])))
    if fails:
        print("\nFEHLER (%d):" % len(fails))
        for mid, smi, e in fails:
            print("  %-22s %s\n      %s" % (mid, e, smi))
        sys.exit(1)


if __name__ == "__main__":
    main()
