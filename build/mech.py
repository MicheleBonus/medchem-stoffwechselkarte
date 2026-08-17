# -*- coding: utf-8 -*-
"""
Mechanismus-Sprache fuer die Tafeln der Metabolitkarte.

Grundgedanke: Strukturen werden nicht von Hand aus <line>- und <text>-Elementen
zusammengesetzt, sondern von RDKit gezeichnet - derselbe Zeichner wie fuer die
306 Strukturformeln im Fliesstext. RDKit meldet ueber GetDrawCoords(idx) die
exakte Pixelposition jedes Atoms; Elektronenpfeile werden daraus konstruiert und
sitzen deshalb per Konstruktion am richtigen Atom bzw. an der richtigen Bindung.

Alle Molekuele einer Tafel werden mit derselben festen Bindungslaenge gezeichnet
(fixedBondLength), damit die Geometrie ueber die ganze Tafel einheitlich ist.

Konventionen, die die Sprache erzwingt:
  - Elektronenpaar-Pfeil  = voller Pfeilkopf
  - Einzelelektron        = Fischhaken, halber Kopf
  - Uebergangszustand     = eckige Klammern mit Doppelkreuz
  - freie Elektronenpaare werden als Punktpaar gesetzt und sind Pfeilursprung

Zwei Wege stehen nebeneinander:

  schub(Paar(m,0), Atom(m2,12))   beschreibt nur die Chemie. Bauchseite,
      Oeffnungswinkel und Ankerlage sucht der Solver in mech_schub.py, geprueft
      wird gegen den Regelkatalog in mech_regeln.py. Die Lage der Molekuele kommt
      aus dem Leitgeruest-Register mech_kerne.py (kern="b6").

  pfeil(von, nach, bogen=, seite=, gap=)  ist der aeltere Weg mit von Hand
      gesetzter Geometrie. Er bleibt, solange die Tafeln M-02 bis M-17 ihn
      benutzen, und ist fuer neue Tafeln nicht mehr gedacht.
"""
import math
import re

from rdkit import Chem
from rdkit.Chem import rdDepictor, rdCIPLabeler, rdFMCS
from rdkit.Chem.Draw import rdMolDraw2D

import mech_kerne
import mech_regeln
import mech_schub
from mech_schub import Atom, Bindung, Elektron, Fest, Paar   # noqa: F401

rdDepictor.SetPreferCoordGen(True)

# Beide Buecher fuehren alle Schiebepfeile in einer Farbe; unterschieden wird
# ueber die Kopfform. Die frueher zweifarbige Fuehrung lud dazu ein, die Farbe zu
# lesen statt den Kopf.
SIGNAL = "var(--warn)"

# Palette wie in gen_structures.py: C wird spaeter zu currentColor
PALETTE = {
    6: (0.0, 0.0, 0.0),
    7: (0.20, 0.55, 0.95),
    8: (0.90, 0.25, 0.25),
    16: (0.80, 0.62, 0.10),
    15: (0.95, 0.55, 0.15),
    9: (0.25, 0.70, 0.45),
    17: (0.25, 0.70, 0.45),
    26: (0.72, 0.35, 0.20),
    27: (0.55, 0.40, 0.80),
    0: (0.45, 0.45, 0.45),
}

BINDUNG = 21.0        # Pixel je Bindung, tafelweit einheitlich
GAP = 7.0             # Abstand des Pfeilendes vom Atom bzw. von der Bindung


def _norm(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


class Punkt(object):
    """Ein Ort in der Tafel, der weiss, woher er stammt - z. B. ein Elektronenpaar.

    rx/ry beschreiben, wie weit die Beschriftung an diesem Ort reicht. Ein Pfeil,
    der hier endet, hoert am Rand dieser Ellipse auf, statt durch die Schrift zu
    laufen; ein fester Abstand genuegt nicht, weil 'Fe(III)' viermal so breit ist
    wie 'O'.
    """

    def __init__(self, x, y, herkunft, rx=0.0, ry=0.0):
        self.x, self.y, self.herkunft = x, y, herkunft
        self.rx, self.ry = rx, ry


def _textbreite(s, px=7.2):
    """Grobe Textbreite in Pixel. Zeichenentitaeten zaehlen als ein Zeichen."""
    return len(re.sub(r"&#?\w+;", "x", s)) * px


def _bogenlaenge(p0, c, p1, n=24):
    """Laenge einer quadratischen Bezierkurve, abgetastet."""
    laenge, vor = 0.0, p0
    for i in range(1, n + 1):
        t = float(i) / n
        u = 1.0 - t
        pt = (u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
              u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])
        laenge += math.hypot(pt[0] - vor[0], pt[1] - vor[1])
        vor = pt
    return laenge


def _ellipse(ux, uy, rx, ry):
    """Abstand vom Mittelpunkt bis zum Ellipsenrand in Richtung (ux, uy)."""
    if rx <= 0 and ry <= 0:
        return 0.0
    rx, ry = max(rx, 0.5), max(ry, 0.5)
    return 1.0 / math.sqrt((ux / rx) ** 2 + (uy / ry) ** 2)


def _gemeinsames_muster(mol, ref):
    """Groesste gemeinsame Teilstruktur zweier Molekuele als SMARTS-Molekuel."""
    res = rdFMCS.FindMCS([Chem.Mol(mol), Chem.Mol(ref)],
                         atomCompare=rdFMCS.AtomCompare.CompareElements,
                         bondCompare=rdFMCS.BondCompare.CompareAny,
                         ringMatchesRingOnly=True, completeRingsOnly=False,
                         matchValences=False, timeout=20)
    if res.canceled or res.numAtoms < 3:
        return None
    return Chem.MolFromSmarts(res.smartsString)


class Molekuel(object):
    """Ein von RDKit gezeichnetes Molekuel an fester Position in der Tafel."""

    # Richtungen fuer die Ausrichtung: Zielwinkel in Grad, 0 = rechts, 90 = unten
    RICHTUNG = {"rechts": 0.0, "unten": 90.0, "links": 180.0, "oben": 270.0}

    def __init__(self, smiles, x, y, labels=None, rotate=0.0, stereo=False,
                 bindung=BINDUNG, name=None, zeige=None, wasserstoff=(),
                 vorlage=None, muster=None, kern=None):
        """kern="b6" legt die Struktur auf die feste Referenzlage dieses
        Leitgeruests (mech_kerne.py). Damit steht derselbe Kern in jeder Stufe
        einer Tafel und in jeder Tafel gleich - gedreht *und* gespiegelt. Das ist
        der Weg fuer neue Tafeln; zeige= und vorlage= sind die aelteren.

        zeige={atom_idx: 'links'|'rechts'|'oben'|'unten'} dreht die Darstellung so,
        dass dieses Atom in die genannte Richtung weist - damit Pfeile zwischen zwei
        Molekuelen kurze Wege haben, statt quer ueber die Struktur zu laufen.

        vorlage=<Molekuel> legt die Struktur auf die Lage eines frueher gebauten
        Molekuels. Ohne das bekommt jede Zwischenstufe ihr eigenes Compute2DCoords,
        und zwei aufeinanderfolgende Stufen stehen gedreht oder gespiegelt
        nebeneinander; der Leser muss dann jedes Bild neu einnorden, statt den
        Unterschied zu sehen. zeige= dreht nur, es spiegelt nicht, und kann das
        deshalb nicht leisten.
        muster=SMARTS bestimmt, welcher Teil festgehalten wird; ohne Angabe sucht
        der Builder die groesste gemeinsame Teilstruktur beider Molekuele."""
        self.name = name or smiles
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("SMILES nicht parsebar: %s" % smiles)
        Chem.rdmolops.AssignStereochemistry(mol, cleanIt=True, force=True)
        try:
            rdCIPLabeler.AssignCIPLabels(mol)
        except Exception:
            pass
        # Ein Wasserstoff, an dem ein Pfeil ansetzen soll, muss ein eigenes Atom sein.
        # RDKit haelt ihn sonst implizit und meldet keine Koordinate dafuer.
        self.h_index = {}
        if wasserstoff:
            mol = Chem.AddHs(mol, onlyOnAtoms=[int(i) for i in wasserstoff])
            # AddHs macht an einer CH2-Gruppe beide Wasserstoffe sichtbar. Gemeint ist
            # aber genau einer - der, an dem der Pfeil ansetzt. Der Rest wird wieder
            # implizit, sonst steht ein zweites H im Bild und die Kette knickt.
            rw = Chem.RWMol(mol)
            zuviel = []
            for idx in wasserstoff:
                hs = [n.GetIdx() for n in mol.GetAtomWithIdx(int(idx)).GetNeighbors()
                      if n.GetAtomicNum() == 1]
                zuviel += hs[1:]
            for i in sorted(zuviel, reverse=True):
                rw.RemoveAtom(i)
            for idx in wasserstoff:
                a = rw.GetAtomWithIdx(int(idx))
                a.SetNoImplicit(False)
                a.SetNumExplicitHs(0)
            mol = rw.GetMol()
            Chem.SanitizeMol(mol)
            for idx in wasserstoff:
                self.h_index[int(idx)] = [
                    n.GetIdx() for n in mol.GetAtomWithIdx(int(idx)).GetNeighbors()
                    if n.GetAtomicNum() == 1][0]
        if labels:
            for idx, txt in labels.items():
                # atomLabel landet unveraendert im SVG-Text; RDKit maskiert nichts
                # und der Browser dekodiert dort keine Entitaeten. "CH&#8322;" stuende
                # woertlich im Bild. Das ist mir zweimal passiert - jetzt bricht es ab.
                if re.search(r"&#?\w+;", txt):
                    raise ValueError(
                        "atomLabel %r enthaelt eine HTML-Entitaet. In Atomlabeln muss "
                        "echter Unicode stehen (z. B. CH₂ statt CH&#8322;)." % txt)
                mol.GetAtomWithIdx(int(idx)).SetProp("atomLabel", txt)
        self.gelegt = False
        if kern is not None:
            if vorlage is not None or zeige:
                raise ValueError("%s: kern= bestimmt die Lage bereits; vorlage= "
                                 "und zeige= sind daneben ohne Wirkung."
                                 % (name or smiles))
            mech_kerne.kern(kern).lege(mol)
            self.gelegt = True
        elif vorlage is not None:
            ref = vorlage.mol if isinstance(vorlage, Molekuel) else vorlage
            if isinstance(ref, str):
                ref = Chem.MolFromSmiles(ref)
                if ref is None:
                    raise ValueError("Vorlage nicht parsebar: %s" % vorlage)
                rdDepictor.Compute2DCoords(ref)
                rdDepictor.StraightenDepiction(ref)
            patt = Chem.MolFromSmarts(muster) if muster else _gemeinsames_muster(mol, ref)
            if patt is None:
                raise ValueError("%s: keine gemeinsame Teilstruktur mit der Vorlage"
                                 % (name or smiles))
            if not mol.GetSubstructMatch(patt) or not ref.GetSubstructMatch(patt):
                raise ValueError("%s: Muster trifft nicht" % (name or smiles))
            rdDepictor.GenerateDepictionMatching2DStructure(
                mol, ref, refPatt=patt, acceptFailure=False)
            self.gelegt = True
        else:
            rdDepictor.Compute2DCoords(mol)
            rdDepictor.StraightenDepiction(mol)
        self.mol = mol

        self.stereo = stereo and len(
            Chem.FindMolChiralCenters(mol, includeUnassigned=False,
                                      useLegacyImplementation=False)) <= 3
        self.bindung_px = bindung

        if zeige:
            if self.gelegt:
                raise ValueError("%s: vorlage= und zeige= schliessen einander aus. "
                                 "Die Vorlage bestimmt die Lage bereits."
                                 % (name or smiles))
            rotate = self._drehwinkel(zeige)
        if self.gelegt:
            rotate = 0.0
        if rotate:
            # Die Drehung in den Konformer schreiben statt sie nur dem Zeichner
            # mitzugeben. Sonst zeigt mol eine andere Lage als das Bild, und ein
            # spaeteres Molekuel mit vorlage=dieses richtet sich an der ungedrehten
            # Fassung aus. Das Vorzeichen ist gemessen: o.rotate=+g entspricht einer
            # Konformerdrehung um -g (die Bildachse zeigt nach unten).
            w = math.radians(-rotate)
            k = self.mol.GetConformer()
            for i in range(self.mol.GetNumAtoms()):
                p = k.GetAtomPosition(i)
                k.SetAtomPosition(i, (p.x * math.cos(w) - p.y * math.sin(w),
                                      p.x * math.sin(w) + p.y * math.cos(w), 0.0))
            rotate = 0.0
        d = self._zeichner(rotate)
        roh = [(d.GetDrawCoords(i).x, d.GetDrawCoords(i).y)
               for i in range(mol.GetNumAtoms())]
        cx = sum(p[0] for p in roh) / len(roh)
        cy = sum(p[1] for p in roh) / len(roh)
        self.ox, self.oy = x - cx, y - cy
        self.koord = [(self.ox + px, self.oy + py) for px, py in roh]
        gezeichnet = d.GetDrawingText()
        self.strecken, self.glyphen, self.strichbreite = self._geometrie(gezeichnet)
        self.inhalt = self._inhalt(gezeichnet)

    # -------------------------------------------------- Tinte
    _ZAHL = re.compile(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?")

    def _geometrie(self, svg):
        """Bindungsstrecken und Glyphenrechtecke aus dem RDKit-SVG lesen.

        RDKit annotiert jedes Element: class='bond-3 atom-2 atom-4' fuer eine
        Bindungslinie, class='atom-13' fuer die Glyphen eines Atomsymbols. Damit
        kennt der Pfeil-Solver seine Hindernisse genau, statt Textbreiten zu
        schaetzen. Die alte Schaetzung gab fuer "NH+" 36x18 px an; gemessen sind
        es 21,1x9,0, und aus dieser Differenz stammten die groessten Fehlbilder.
        """
        strecken, glyphen = [], {}
        breiten = []
        for tag, attr in re.findall(r"<(path|ellipse)([^>]*)/>", svg):
            m = re.search(r"class='(bond-(\d+)|atom-(\d+))[^']*'", attr)
            if not m:
                continue
            dm = re.search(r"d='([^']*)'", attr)
            if dm:
                punkte = []
                for teil in dm.group(1).split("M")[1:]:
                    v = [float(z) for z in self._ZAHL.findall(teil)]
                    punkte.append([(v[i] + self.ox, v[i + 1] + self.oy)
                                   for i in range(0, len(v) - 1, 2)])
            else:
                g = dict((k, float(v)) for k, v in
                         re.findall(r"\b(cx|cy|rx|ry|r)='([-\d.]+)'", attr))
                rx = g.get("rx", g.get("r", 1.0))
                ry = g.get("ry", g.get("r", 1.0))
                punkte = [[(g["cx"] - rx + self.ox, g["cy"] - ry + self.oy),
                           (g["cx"] + rx + self.ox, g["cy"] + ry + self.oy)]]
            if m.group(2) is not None:                      # Bindung
                sw = re.search(r"stroke-width:([\d.]+)", attr)
                if sw:
                    breiten.append(float(sw.group(1)))
                for zug in punkte:
                    for a, b in zip(zug, zug[1:]):
                        strecken.append((a[0], a[1], b[0], b[1], int(m.group(2))))
            else:                                           # Atomsymbol
                i = int(m.group(3))
                xs = [p[0] for zug in punkte for p in zug]
                ys = [p[1] for zug in punkte for p in zug]
                if not xs:
                    continue
                alt = glyphen.get(i)
                box = (min(xs), min(ys), max(xs), max(ys))
                glyphen[i] = box if alt is None else (
                    min(alt[0], box[0]), min(alt[1], box[1]),
                    max(alt[2], box[2]), max(alt[3], box[3]))
        breite = sorted(breiten)[len(breiten) // 2] if breiten else 2.0
        return strecken, glyphen, breite

    def freie_richtung(self, idx, hin=None):
        """Richtung der groessten Winkelluecke zwischen den Bindungen am Atom."""
        return mech_schub._freie_richtungen(
            self, int(idx), hin or (self.koord[0] if self.koord else (0, 0)), 1)[0][0]

    def _zeichner(self, rotate):
        d = rdMolDraw2D.MolDraw2DSVG(1400, 1000)
        o = d.drawOptions()
        o.clearBackground = False
        o.fixedBondLength = self.bindung_px
        o.centreMoleculesBeforeDrawing = True
        o.addStereoAnnotation = self.stereo
        o.annotationFontScale = 0.65
        o.bondLineWidth = 1.7
        o.multipleBondOffset = 0.15
        o.rotate = rotate
        o.updateAtomPalette(PALETTE)
        rdMolDraw2D.PrepareAndDrawMolecule(d, self.mol)
        d.FinishDrawing()
        return d

    def _drehwinkel(self, zeige):
        """Beste Drehung suchen, damit die geforderten Atome in ihre Richtung weisen."""
        ziele = [(int(i), math.radians(self.RICHTUNG[r])) for i, r in zeige.items()]
        best, bestwert = 0.0, 1e9
        for grad in range(0, 360, 5):
            d = self._zeichner(float(grad))
            pts = [(d.GetDrawCoords(i).x, d.GetDrawCoords(i).y)
                   for i in range(self.mol.GetNumAtoms())]
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            wert = 0.0
            for idx, soll in ziele:
                ist = math.atan2(pts[idx][1] - cy, pts[idx][0] - cx)
                diff = abs((ist - soll + math.pi) % (2 * math.pi) - math.pi)
                wert += diff
            if wert < bestwert:
                best, bestwert = float(grad), wert
        return best

    # -------------------------------------------------- Geometrie
    def atom(self, idx):
        return self.koord[idx]

    def bindung(self, i, j):
        (ax, ay), (bx, by) = self.koord[i], self.koord[j]
        return ((ax + bx) / 2.0, (ay + by) / 2.0)

    def abseits(self, idx, weg_von, abstand=16.0):
        """Ein Punkt dicht neben einem Atom, auf der von 'weg_von' abgewandten Seite.

        Gebraucht fuer den zweiten Fischhaken einer Homolyse: das Elektron bleibt am
        Atom, aber ein Pfeil von der Bindungsmitte zum Atomzentrum waere nur eine
        halbe Bindungslaenge lang und wuerde zur Schleife entarten. Die Herkunft
        bleibt das Atom, damit die Selbstpruefung greift."""
        x, y = self.atom(idx)
        ax, ay = self.atom(weg_von)
        ux, uy = _norm(x - ax, y - ay)
        return Punkt(x + ux * abstand, y + uy * abstand, ("atom", self.name, idx))

    def aussen(self, i, j=None, abstand=15.0):
        """Ankerpunkt vor einem Atom oder einer Bindung, vom Molekuelschwerpunkt weg
        versetzt. Pfeile zwischen solchen Punkten laufen aussen um das Geruest herum,
        statt quer durch den Ring - besonders wichtig bei konjugierten Systemen, wo
        mehrere Pfeile hintereinander an derselben Struktur haengen."""
        p = self.atom(i) if j is None else self.bindung(i, j)
        herkunft = (("atom", self.name, i) if j is None
                    else ("bindung", self.name, (i, j)))
        cx = sum(q[0] for q in self.koord) / len(self.koord)
        cy = sum(q[1] for q in self.koord) / len(self.koord)
        ux, uy = _norm(p[0] - cx, p[1] - cy)
        return Punkt(p[0] + ux * abstand, p[1] + uy * abstand, herkunft)

    def beschriftung(self, idx):
        """Halbe Breite und Hoehe der Schrift an diesem Atom. Ein Kohlenstoff ist
        nur ein Knick im Linienzug und braucht kaum Platz, 'Adenin' dagegen viel."""
        a = self.mol.GetAtomWithIdx(int(idx))
        if a.HasProp("atomLabel"):
            return (_textbreite(a.GetProp("atomLabel")) / 2.0 + 3.0, 9.0)
        if a.GetSymbol() == "C":
            return (3.0, 3.0)
        n = 1 + (1 if a.GetTotalNumHs() else 0) + (1 if a.GetFormalCharge() else 0)
        return (n * 5.0 + 3.0, 9.0)

    def rand(self):
        xs = [p[0] for p in self.koord]
        ys = [p[1] for p in self.koord]
        return min(xs), min(ys), max(xs), max(ys)

    def idx(self, symbol, n=0):
        """Index des n-ten Atoms mit diesem Elementsymbol - fuer lesbare Skripte."""
        treffer = [a.GetIdx() for a in self.mol.GetAtoms()
                   if a.GetSymbol() == symbol]
        return treffer[n]

    # -------------------------------------------------- SVG
    @staticmethod
    def _inhalt(svg):
        """Nur die Zeichenelemente aus dem RDKit-SVG, ohne Rahmen und Hintergrund."""
        svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        svg = svg.replace("<svg:", "<").replace("</svg:", "</")
        innen = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
        innen = re.sub(r"<rect[^>]*/>", "", innen)          # Hintergrundflaeche
        innen = re.sub(r"\s+class='[^']*'", "", innen)
        innen = innen.replace("#000000", "currentColor").replace("#000", "currentColor")

        def stil(m):
            st = dict(kv.split(":", 1) for kv in m.group(1).split(";") if ":" in kv)
            out = ["fill='%s'" % st.get("fill", "none").strip()]
            if st.get("stroke", "none").strip() != "none":
                out.append("stroke='%s'" % st["stroke"].strip())
                sw = st.get("stroke-width", "").strip().replace("px", "")
                if sw:
                    out.append("stroke-width='%s'" % sw)
            return " ".join(out)

        innen = re.sub(r"style='([^']*)'", stil, innen)
        innen = re.sub(r"(\d+)\.(\d)\d+", lambda m: "%s.%s" % (m.group(1), m.group(2)), innen)
        return re.sub(r"\s*\n\s*", "", innen).strip()

    def svg(self):
        return "<g transform='translate(%.1f,%.1f)'>%s</g>" % (self.ox, self.oy, self.inhalt)


class Zentrum(object):
    """Ein Metallzentrum mit Makrocyclus, wie in der Lehrbuchdarstellung ueblich:
    Porphyrinebene als Balken, das Eisen darin, das Cystein-Thiolat darunter, der
    axiale Ligand als Kette darueber.

    Gebraucht fuer Haem (Porphyrin, Fe) und Corrin (Co).
    Kein SMILES - ein vollstaendig gezeichnetes Porphyrin achtmal um einen Kreis
    waere unlesbar. Entscheidend ist, dass alle acht Zustaende aus demselben
    Bausatz kommen und die Pfeile an benannten Punkten haengen (fe, s, ax, axb).
    """

    SCHRITT = 26.0      # Abstand zweier Atome der axialen Kette
    HALB = 25.0         # halbe Breite der Porphyrinebene

    def __init__(self, tafel, x, y, metall, axial=(), doppelt=False, unten="S&#8722;Cys",
                 radikal=False, name=None, schritt=None, ebene=True):
        """unten: der proximale fuenfte Ligand. Beim P450 ein Cystein-Thiolat,
        bei der Peroxidase und beim Haemoglobin ein Histidin - der Unterschied
        entscheidet ueber die Reaktivitaet und gehoert deshalb ins Bild."""
        self.x, self.y = x, y
        self.name = name or metall
        self._metall = metall
        self._axlab = list(axial)
        # schritt: Abstand Metall-Ligand. Groesser waehlen, wenn an dieser
        # Bindung Elektronenpfeile ansetzen - sonst fehlt ihnen der Platz.
        self.schritt = float(schritt or self.SCHRITT)
        self._ax = [(x, y - self.schritt * (i + 1)) for i in range(len(axial))]
        st = tafel.stuecke

        # Porphyrinebene: zwei Balken mit Luecke fuer das Metallsymbol.
        # ebene=False fuer Metalle ohne Makrocyclus - beim Kupfer der
        # Monooxygenasen waere der Balken schlicht falsch.
        for s in ((-1, 1) if ebene else ()):
            st.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='currentColor' "
                          "stroke-width='2.4' opacity='%s'/>"
                       % (x + s * self.HALB, y, x + s * 15.0, y, ".55" if not radikal else ".9")))
            st.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='currentColor' "
                          "stroke-width='1.6' opacity='.45'/>"
                       % (x + s * self.HALB, y - 5, x + s * self.HALB, y + 5)))
        if radikal:   # Porphyrin-Radikalkation ueber das linke Ende der Ebene gesetzt:
            st.append((3, "<text x='%.1f' y='%.1f' font-size='11' font-weight='700' "
                          "text-anchor='middle' fill='var(--drug)'>&#8226;+</text>"
                       % (x - self.HALB, y - 11)))   # rechts kommen die Pfeile herein

        st.append((3, "<text x='%.1f' y='%.1f' font-size='12.5' font-weight='700' "
                      "text-anchor='middle' fill='var(--warn)'>%s</text>" % (x, y + 4.5, metall)))

        if unten:
            st.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='currentColor' "
                          "stroke-width='1.5'/>" % (x, y + 8, x, y + 20)))
            st.append((3, "<text x='%.1f' y='%.1f' font-size='11' text-anchor='middle' "
                          "fill='var(--cofaktor)' font-weight='700'>%s</text>"
                       % (x, y + 33, unten)))

        vorher = (x, y - 8)
        for i, (lab, px) in enumerate(zip(axial, self._ax)):
            if i == 0 and doppelt:      # Fe(IV)=O
                for d in (-2.2, 2.2):
                    st.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' "
                                  "stroke='currentColor' stroke-width='1.5'/>"
                               % (vorher[0] + d, vorher[1], px[0] + d, px[1] + 9)))
            else:
                st.append((1, "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' "
                              "stroke='currentColor' stroke-width='1.5'/>"
                           % (vorher[0], vorher[1], px[0], px[1] + 9)))
            st.append((3, "<text x='%.1f' y='%.1f' font-size='12.5' font-weight='700' "
                          "text-anchor='middle' fill='var(--enzym)'>%s</text>"
                       % (px[0], px[1] + 4.5, lab)))
            vorher = (px[0], px[1] - 8)

    # -------------------------------------------------- Ankerpunkte
    #
    # Metall und axialer Ligand liegen nur eine halbe Schrittweite auseinander.
    # Ein Pfeil von der Bindungsmitte zum Metall waere dort kuerzer als sein eigener
    # Kopf. Mit winkel/abstand laesst sich der Endpunkt seitlich versetzen: der Pfeil
    # schwingt dann sichtbar heraus und zeigt trotzdem eindeutig auf das Zentrum.
    def fe(self, winkel=None, abstand=0.0):
        if winkel is None:
            return Punkt(self.x, self.y, ("zentrum-fe", self.name, None),
                         rx=_textbreite(self._metall) / 2.0 + 3.0, ry=9.0)
        a = math.radians(winkel)
        return Punkt(self.x + math.cos(a) * abstand, self.y + math.sin(a) * abstand,
                     ("zentrum-fe", self.name, None))

    def s(self):
        return Punkt(self.x, self.y + 22, ("zentrum-thiolat", self.name, None),
                     rx=3.0, ry=3.0)

    def ax(self, i, winkel=None, abstand=0.0):
        p = self._ax[i]
        if winkel is None:
            return Punkt(p[0], p[1], ("zentrum-axial", self.name, i),
                         rx=_textbreite(self._axlab[i]) / 2.0 + 3.0, ry=9.0)
        a = math.radians(winkel)
        return Punkt(p[0] + math.cos(a) * abstand, p[1] + math.sin(a) * abstand,
                     ("zentrum-axial", self.name, i))

    def axb(self, i, j):
        """Mitte der Bindung zwischen zwei axialen Positionen; -1 meint das Eisen."""
        a = (self.x, self.y) if i < 0 else self._ax[i]
        b = (self.x, self.y) if j < 0 else self._ax[j]
        return Punkt((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0,
                     ("zentrum-bindung", self.name, (i, j)))


class Tafel(object):
    """Sammelt Molekuele, Pfeile und Beschriftung und gibt fertiges Inline-SVG aus."""

    def __init__(self, breite, hoehe):
        self.b, self.h = breite, hoehe
        self.mole = []
        self.stuecke = []          # (z, svg) - z steuert die Zeichenreihenfolge
        self.anker = []            # Prueflast: jeder Pfeilendpunkt mit Bezug
        self.schuebe = []          # deklarierte Elektronenverschiebungen
        self.sperren = []          # eigene Beschriftung als Hindernis (Kasten)
        self._geloest = False

    # -------------------------------------------------- Bausteine
    def mol(self, smiles, x, y, **kw):
        m = Molekuel(smiles, x, y, **kw)
        self.mole.append(m)
        return m

    # -------------------------------------------------- Schiebepfeile
    def schub(self, quelle, ziel, elektronen=2, **kw):
        """Eine Elektronenverschiebung anmelden. Geometrie kommt aus dem Solver.

        quelle und ziel sind Paar(m, i), Atom(m, i), Bindung(m, i, j),
        Elektron(m, i) oder ein fester Ort. elektronen=1 ergibt einen Fischhaken.
        kette="a" fasst mehrere Pfeile zu einem Schritt zusammen; die Pruefung
        verlangt dann Kopf an Schwanz.
        """
        s = mech_schub.Schub(quelle, ziel, elektronen, **kw)
        self.schuebe.append(s)
        self.anker.append((s.quelle.herkunft(), s.ziel.herkunft(),
                           "paar" if elektronen == 2 else "fischhaken"))
        self._geloest = False
        return s

    def _tinte(self):
        t = mech_schub.Tinte()
        for m in self.mole:
            for x0, y0, x1, y1, bi in m.strecken:
                t.strecke(x0, y0, x1, y1, ("bindung", m.name, bi))
            for i, (x0, y0, x1, y1) in m.glyphen.items():
                t.kasten(x0, y0, x1, y1, ("glyph", m.name, i))
        for i, (x0, y0, x1, y1) in enumerate(self.sperren):
            t.kasten(x0, y0, x1, y1, ("sperre", None, i))
        return t

    def loesen(self):
        """Alle angemeldeten Pfeile geometrisch aufloesen.

        Erst hier, weil der Solver die vollstaendige Tafel als Hindernislage
        braucht: Beschriftungen, die nach dem Pfeil im Skript stehen, gehoeren
        dazu. Deshalb loest svg() und pruefe() aus, nicht schub() selbst.
        """
        if self._geloest:
            return
        tinte = self._tinte()
        gesetzt = []
        for i, s in enumerate(self.schuebe):
            m = s.quelle.mol() or s.ziel.mol()
            L = m.bindung_px if m is not None else BINDUNG
            vor = None
            if i and s.kette is not None and self.schuebe[i - 1].kette == s.kette:
                vor = self.schuebe[i - 1]
            s.breite = (max(1.4, m.strichbreite * 0.78) if m is not None else 1.6)
            s.loesen(tinte, L, gesetzt, vor)
            gesetzt.append(s.bogen)
            # Ein gezeichnetes Punktpaar ist ab jetzt selbst Hindernis.
            if s.zusatz_q and "paar" in s.zusatz_q:
                px, py, grad = s.zusatz_q["paar"]
                r = mech_schub.PAAR_SPREIZ * L + 2.2
                tinte.kasten(px - r, py - r, px + r, py + r,
                             ("paar", s.quelle.herkunft()[1], i))
                self._punktpaar(px, py, grad, L)
            if s.zusatz_q and "punkt" in s.zusatz_q:
                px, py = s.zusatz_q["punkt"]
                tinte.kasten(px - 2.4, py - 2.4, px + 2.4, py + 2.4,
                             ("punkt", s.quelle.herkunft()[1], i))
                self.stuecke.append((2, "<circle cx='%.1f' cy='%.1f' r='2.0' "
                                        "fill='%s'/>" % (px, py, SIGNAL)))
            for teil in s.svg(L, SIGNAL, s.breite):
                self.stuecke.append((3, teil))
        self._geloest = True

    def _punktpaar(self, x, y, grad, L):
        a = math.radians(grad)
        px, py = -math.sin(a) * mech_schub.PAAR_SPREIZ * L, \
            math.cos(a) * mech_schub.PAAR_SPREIZ * L
        for s in (1, -1):
            self.stuecke.append((2, "<circle cx='%.1f' cy='%.1f' r='1.7' "
                                    "fill='var(--ink-2)'/>"
                                 % (x + px * s, y + py * s)))

    def _punkt(self, ziel):
        """(mol, i) -> Atom, (mol, i, j) -> Bindungsmitte, Punkt -> bereits belegt.
        Liefert Ort, Herkunft und die Ausdehnung der Beschriftung an diesem Ort."""
        if isinstance(ziel, Punkt):
            return (ziel.x, ziel.y), ziel.herkunft, (ziel.rx, ziel.ry)
        if isinstance(ziel, tuple) and len(ziel) == 2 and isinstance(ziel[0], Molekuel):
            return (ziel[0].atom(ziel[1]), ("atom", ziel[0].name, ziel[1]),
                    ziel[0].beschriftung(ziel[1]))
        if isinstance(ziel, tuple) and len(ziel) == 3:
            return (ziel[0].bindung(ziel[1], ziel[2]),
                    ("bindung", ziel[0].name, (ziel[1], ziel[2])), (0.0, 0.0))
        return (float(ziel[0]), float(ziel[1])), ("frei", None, None), (0.0, 0.0)

    def pfeil(self, von, nach, bogen=0.34, typ="paar", seite=1,
              farbe="var(--warn)", gap=GAP, breite=1.7, mindestbogen=17.0, strich=None):
        """Elektronenpfeil. typ='paar' (voller Kopf) oder 'fischhaken' (halber Kopf).

        Bindungsmitte und benachbartes Atom liegen nur eine halbe Bindungslaenge
        auseinander; ohne Mindestbogen und ohne mitschrumpfenden Abstand faellt der
        Pfeil dort in sich zusammen und man sieht nur noch die Spitze."""
        p0, a0, r0 = self._punkt(von)
        p1, a1, r1 = self._punkt(nach)
        self.anker.append((a0, a1, typ))

        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        laenge = math.hypot(dx, dy)
        gap = min(gap, laenge * 0.26)
        hoehe = max(bogen * laenge, mindestbogen)
        nx, ny = -dy / (laenge or 1), dx / (laenge or 1)
        cx = (p0[0] + p1[0]) / 2 + nx * hoehe * seite
        cy = (p0[1] + p1[1]) / 2 + ny * hoehe * seite

        ux, uy = _norm(cx - p0[0], cy - p0[1])
        vx, vy = _norm(p1[0] - cx, p1[1] - cy)
        a = gap + _ellipse(ux, uy, *r0)
        b = gap + _ellipse(vx, vy, *r1)

        # Bei kurzen Pfeilen - Bindungsmitte zum Nachbaratom - waere die Summe
        # beider Verkuerzungen groesser als der Pfeil selbst; er kehrte sich um.
        # Massstab ist die Laenge des Bogens, nicht die der Sehne.
        laenge_bogen = _bogenlaenge(p0, (cx, cy), p1)
        platz = 0.62 * laenge_bogen
        if a + b > platz and a + b > 0:
            f = platz / (a + b)
            a, b = a * f, b * f

        sx, sy = p0[0] + ux * a, p0[1] + uy * a
        ex, ey = p1[0] - vx * b, p1[1] - vy * b

        kopf = "pfk" if typ == "paar" else ("fhl" if seite > 0 else "fhr")
        rest = math.hypot(ex - sx, ey - sy)

        if rest < 14.0:
            # Bindungsmitte und Nachbaratom liegen zu dicht beieinander: eine
            # Bezierkurve waere kuerzer als ihr eigener Pfeilkopf. Stattdessen ein
            # Kreisbogen, der den langen Weg nimmt - die uebliche Schreibweise fuer
            # einen Pfeil, der um ein Atom herumgreift.
            if rest < 9.0:
                mx, my = -uy, ux
                ex, ey = ex + mx * 9.0 * seite, ey + my * 9.0 * seite
                rest = math.hypot(ex - sx, ey - sy)
            r = max(12.0, rest * 0.62)
            sweep = 1 if seite > 0 else 0
            d = "M %.1f %.1f A %.1f %.1f 0 1 %d %.1f %.1f" % (sx, sy, r, r, sweep, ex, ey)
        else:
            d = "M %.1f %.1f Q %.1f %.1f %.1f %.1f" % (sx, sy, cx, cy, ex, ey)

        # gestrichelt = zusammengefasste Delokalisierung, durchgezogen = ein Schritt
        sd = "" if not strich else " stroke-dasharray='%s'" % strich
        self.stuecke.append((3,
            "<path d='%s' fill='none' stroke='%s' stroke-width='%.1f' "
            "stroke-linecap='round'%s marker-end='url(#%s)'/>"
            % (d, farbe, breite, sd, kopf)))
        return (cx, cy)

    def elektronenpaar(self, mol, idx, winkel, abstand=11.0, spreiz=3.6,
                       farbe="var(--ink-2)"):
        """Freies Elektronenpaar als Punktpaar; Winkel in Grad, 0 = rechts."""
        x, y = mol.atom(idx)
        a = math.radians(winkel)
        mx, my = x + math.cos(a) * abstand, y + math.sin(a) * abstand
        px, py = -math.sin(a) * spreiz, math.cos(a) * spreiz
        for s in (1, -1):
            self.stuecke.append((2, "<circle cx='%.1f' cy='%.1f' r='1.7' fill='%s'/>"
                                 % (mx + px * s, my + py * s, farbe)))
        return Punkt(mx, my, ("elektronenpaar", mol.name, idx))

    def zentrum(self, x, y, metall, **kw):
        return Zentrum(self, x, y, metall, **kw)

    def einzelelektron(self, mol, idx, winkel, abstand=11.0, farbe="var(--drug)"):
        """Ein ungepaartes Elektron als einzelner Punkt - Ursprung eines Fischhakens."""
        if isinstance(mol, Punkt):
            x, y, herkunft = mol.x, mol.y, mol.herkunft
        else:
            x, y = mol.atom(idx)
            herkunft = ("einzelelektron", mol.name, idx)
        a = math.radians(winkel)
        mx, my = x + math.cos(a) * abstand, y + math.sin(a) * abstand
        self.stuecke.append((2, "<circle cx='%.1f' cy='%.1f' r='2.0' fill='%s'/>"
                             % (mx, my, farbe)))
        return Punkt(mx, my, herkunft)

    def ringpfeil(self, cx, cy, r, grad0, grad1, farbe="currentColor", breite=1.5):
        """Reaktionspfeil als Kreisbogen - fuer katalytische Zyklen. 0 Grad = oben."""
        def pt(g):
            a = math.radians(g - 90.0)
            return cx + math.cos(a) * r, cy + math.sin(a) * r
        x0, y0 = pt(grad0)
        x1, y1 = pt(grad1)
        gross = 1 if abs(grad1 - grad0) > 180 else 0
        rueck = 1 if grad1 > grad0 else 0
        self.stuecke.append((1,
            "<path d='M %.1f %.1f A %.1f %.1f 0 %d %d %.1f %.1f' fill='none' stroke='%s' "
            "stroke-width='%.1f' marker-end='url(#rxn)'/>"
            % (x0, y0, r, r, gross, rueck, x1, y1, farbe, breite)))

    def paar(self, x, y, winkel, name, spreiz=3.6, farbe="var(--ink-2)"):
        """Freies Elektronenpaar an einem frei gewaehlten Ort - fuer Teilchen, die
        kein SMILES sind, etwa das Cystein-Thiolat am Haem."""
        a = math.radians(winkel)
        px, py = -math.sin(a) * spreiz, math.cos(a) * spreiz
        for s in (1, -1):
            self.stuecke.append((2, "<circle cx='%.1f' cy='%.1f' r='1.7' fill='%s'/>"
                                 % (x + px * s, y + py * s, farbe)))
        return Punkt(x, y, ("elektronenpaar", name, None))

    def marke(self, x, y, name):
        """Ausdruecklich benannter Ankerpunkt fuer Teilchen, die kein SMILES sind
        (Metallcluster, Enzymrest). Die Selbstpruefung listet sie auf, statt sie
        als versehentlich freischwebenden Pfeil zu melden."""
        return Punkt(x, y, ("marke", name, None))

    def ts_klammer(self, x0, y0, x1, y1, farbe="currentColor"):
        """Eckige Klammern um einen Uebergangszustand, mit Doppelkreuz oben rechts."""
        e = 9.0
        for x, s in ((x0, 1), (x1, -1)):
            self.stuecke.append((1,
                "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f' fill='none' "
                "stroke='%s' stroke-width='1.4'/>"
                % (x + e * s, y0, x, y0, x, y1, x + e * s, y1, farbe)))
        self.stuecke.append((1,
            "<text x='%.1f' y='%.1f' font-size='15' font-weight='700' fill='%s'>&#8225;</text>"
            % (x1 + 4, y0 + 12, farbe)))

    # -------------------------------------------------- Beschriftung
    def text(self, x, y, s, size=12.5, anchor="start", farbe="currentColor",
             gewicht=None, mono=False, z=4):
        # Der Pfeil-Solver braucht die Beschriftung als Hindernis. Die Breite ist
        # geschaetzt (halbe Schriftgroesse je Zeichen); anders als bei den
        # Atomsymbolen gibt es hier keine Glyphen, die man ausmessen koennte.
        n = len(re.sub(r"&#?\w+;", "x", s))
        w = n * float(size) * (0.60 if mono else 0.52)
        x0 = x - w / 2.0 if anchor == "middle" else (x - w if anchor == "end" else x)
        self.sperren.append((x0, y - float(size) * 0.76, x0 + w,
                             y + float(size) * 0.22))
        self._geloest = False
        att = ["x='%.1f'" % x, "y='%.1f'" % y, "font-size='%s'" % size,
               "fill='%s'" % farbe]
        if anchor != "start":
            att.append("text-anchor='%s'" % anchor)
        if gewicht:
            att.append("font-weight='%s'" % gewicht)
        if mono:
            att.append("font-family='Consolas, monospace'")
        self.stuecke.append((z, "<text %s>%s</text>" % (" ".join(att), s)))

    def unterschrift(self, mol, *zeilen, **kw):
        """Bildunterschrift mittig unter der tatsaechlichen Ausdehnung des Molekuels.
        Von Hand gesetzte Koordinaten waren die haeufigste Ursache fuer Textkollisionen."""
        x0, y0, x1, y1 = mol.rand()
        cx, y = (x0 + x1) / 2.0, y1 + kw.get("abstand", 28)
        for i, z in enumerate(zeilen):
            self.text(cx, y + i * 15, z, size=kw.get("size", 10.5), anchor="middle",
                      farbe=kw.get("farbe", "var(--ink-3)"), gewicht=kw.get("gewicht"))
        return y + max(0, len(zeilen) - 1) * 15

    def atomnummer(self, mol, idx, text, winkel=90, abstand=13.0, size=9.5,
                   farbe="var(--ink-3)", gewicht=None):
        """Kleine Positionsnummer neben ein Atom - bei langen Ketten unentbehrlich,
        weil ein atomLabel den Kohlenstoff durch Text ersetzen wuerde."""
        x, y = mol.atom(idx)
        a = math.radians(winkel)
        self.text(x + math.cos(a) * abstand, y + math.sin(a) * abstand + 3.5, text,
                  size=size, anchor="middle", farbe=farbe, gewicht=gewicht)

    def ueberschrift(self, mol, zeile, **kw):
        x0, y0, x1, y1 = mol.rand()
        self.text((x0 + x1) / 2.0, y0 - kw.get("abstand", 26), zeile,
                  size=kw.get("size", 12.5), anchor="middle",
                  farbe=kw.get("farbe", "currentColor"), gewicht=kw.get("gewicht", 700))

    def zone(self, y, titel):
        self.stuecke.append((0,
            "<text x='20' y='%.1f' font-size='11' letter-spacing='1.4' font-weight='700' "
            "fill='var(--ink-3)'>%s</text>" % (y, titel)))
        self.stuecke.append((0,
            "<line x1='20' y1='%.1f' x2='%.1f' y2='%.1f' stroke='currentColor' "
            "stroke-width='1' opacity='.25'/>" % (y + 8, self.b - 20, y + 8)))

    def reaktionspfeil(self, x0, y0, x1, y1=None, farbe="currentColor"):
        """Gerader Reaktionspfeil. Ohne y1 waagerecht."""
        # Regel V4: kein Elektronenpfeil ueberquert den Reaktionspfeil.
        yy = y0 if y1 is None else y1
        self.sperren.append((min(x0, x1) - 2, min(y0, yy) - 4,
                             max(x0, x1) + 2, max(y0, yy) + 4))
        self._geloest = False
        self.stuecke.append((1,
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' "
            "stroke-width='1.5' marker-end='url(#rxn)'/>"
            % (x0, y0, x1, y0 if y1 is None else y1, farbe)))

    def ebene(self, x, y, breite=104.0, tiefe=34.0, farbe="var(--warn)", beschriftung=None):
        """Eine Ebene in Schraegsicht als Parallelogramm - fuer die Dunathan-Konformation:
        man sieht erst dann, was 'senkrecht zur Ebene' heisst, wenn die Ebene da ist.
        Gibt den Mittelpunkt zurueck."""
        hb, ht = breite / 2.0, tiefe / 2.0
        self.stuecke.append((0,
            "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='%s' "
            "fill-opacity='.10' stroke='%s' stroke-width='1.1' stroke-opacity='.5'/>"
            % (x - hb, y, x - hb + ht * 1.7, y - ht, x + hb, y,
               x + hb - ht * 1.7, y + ht, farbe, farbe)))
        if beschriftung:
            self.text(x + hb + 6, y + 4, beschriftung, size=9.5, farbe=farbe)
        return (x, y)

    def keil(self, x0, y0, x1, y1, breite=6.0, farbe="currentColor"):
        """Keilbindung zum Betrachter hin - volles Dreieck."""
        dx, dy = x1 - x0, y1 - y0
        nx, ny = _norm(-dy, dx)
        self.stuecke.append((1,
            "<path d='M %.1f %.1f L %.1f %.1f L %.1f %.1f Z' fill='%s'/>"
            % (x0, y0, x1 + nx * breite / 2, y1 + ny * breite / 2,
               x1 - nx * breite / 2, y1 - ny * breite / 2, farbe)))

    def strichkeil(self, x0, y0, x1, y1, breite=6.0, n=5, farbe="currentColor"):
        """Keilbindung vom Betrachter weg - gestrichelter Keil."""
        dx, dy = x1 - x0, y1 - y0
        nx, ny = _norm(-dy, dx)
        for i in range(1, n + 1):
            t = float(i) / n
            b = breite * t / 2.0
            cx, cy = x0 + dx * t, y0 + dy * t
            self.stuecke.append((1,
                "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.4'/>"
                % (cx - nx * b, cy - ny * b, cx + nx * b, cy + ny * b, farbe)))

    def kasten(self, x, y, w, h, fill="var(--surface-2)", stroke="currentColor", r=8):
        self.sperren.append((x, y, x + w, y + h))
        self._geloest = False
        self.stuecke.append((0,
            "<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' rx='%d' fill='%s' "
            "stroke='%s' stroke-width='1.2' opacity='.95'/>" % (x, y, w, h, r, fill, stroke)))

    def linie(self, x0, y0, x1, y1, farbe="currentColor", breite=1.6, strich=None, z=1):
        d = "" if not strich else " stroke-dasharray='%s'" % strich
        self.stuecke.append((z,
            "<line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='%.1f'%s/>"
            % (x0, y0, x1, y1, farbe, breite, d)))

    # -------------------------------------------------- Ausgabe
    DEFS = (
        "<defs>"
        "<marker id='pfk' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6.5' "
        "markerHeight='6.5' orient='auto'>"
        "<path d='M 0 0 L 10 5 L 0 10 z' fill='var(--warn)'/></marker>"
        "<marker id='fhl' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7.5' "
        "markerHeight='7.5' orient='auto'>"
        "<path d='M 0 0 L 10 5 L 2.2 4.2 z' fill='var(--drug)'/></marker>"
        "<marker id='fhr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7.5' "
        "markerHeight='7.5' orient='auto'>"
        "<path d='M 0 10 L 10 5 L 2.2 5.8 z' fill='var(--drug)'/></marker>"
        "<marker id='rxn' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' "
        "markerHeight='7' orient='auto'>"
        "<path d='M 0 0 L 10 5 L 0 10 z' fill='currentColor'/></marker>"
        "</defs>"
    )

    def svg(self, aria):
        self.loesen()
        teile = [m.svg() for m in self.mole]
        teile += [s for _, s in sorted(self.stuecke, key=lambda t: t[0])]
        return (
            "<svg viewBox='0 0 %d %d' role='img' aria-label=\"%s\">%s"
            "<g font-family='Corbel, Segoe UI, system-ui, sans-serif' fill='currentColor'>"
            "%s</g></svg>" % (self.b, self.h, aria, self.DEFS, "".join(teile))
        ).replace("'", '"')

    # -------------------------------------------------- Selbstpruefung
    def pruefe(self):
        """Jeder Pfeil muss an einem Atom, einer Bindung, einem Elektronenpaar oder
        einer ausdruecklich benannten Marke ansetzen und enden. Pfeile, die ueber
        schub() angemeldet sind, werden zusaetzlich gegen den Regelkatalog in
        mech_regeln.py gemessen. Gibt (Fehler, Bericht) zurueck."""
        fehler, bericht = [], []
        for i, (a0, a1, typ) in enumerate(self.anker, 1):
            for rolle, a in (("Start", a0), ("Ziel", a1)):
                if a[0] == "frei":
                    fehler.append("Pfeil %d (%s): %s haengt an einem freien Punkt"
                                  % (i, typ, rolle))
            bericht.append("  %2d %-11s %-34s -> %s"
                           % (i, typ, self._zeige(a0), self._zeige(a1)))
        if self.schuebe:
            self.loesen()
            b = mech_regeln.pruefe_schuebe(self)
            fehler += b.fehler
            bericht = ["", "Gemessen gegen den Regelkatalog "
                           "(L = Bindungslaenge %.0f px):" % self.mole[0].bindung_px]
            bericht += b.zeilen
            for h in b.hinweise:
                bericht.append("  Hinweis: %s" % h)
        return fehler, bericht

    @staticmethod
    def _zeige(a):
        art, name, idx = a
        if art == "marke":
            return "marke[%s]" % name
        if art == "bindung":
            return "%s.bindung%s" % (name, idx)
        return "%s.%s(%s)" % (name, art, idx)


def speichern(tid, svg, tafel=None):
    """Eine fertige Tafel als eigene Datei ablegen: tafeln/<tid>.svg

    Frueher schrieben alle siebzehn Skripte in dieselbe tafeln.json. Sobald
    zwei davon gleichzeitig liefen, ueberschrieb der spaetere den frueheren
    Stand. Eine Datei je Tafel schliesst das aus; site.py liest das ganze
    Verzeichnis.
    """
    import os
    import io as _io
    ordner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tafeln")
    os.makedirs(ordner, exist_ok=True)
    ziel = os.path.join(ordner, "%s.svg" % tid)
    with _io.open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    if tafel is not None:
        print("geschrieben: tafeln/%s.svg  (%d Zeichen, %d Molekuele, %d Pfeile)"
              % (tid, len(svg), len(tafel.mole), len(tafel.anker)))
    else:
        print("geschrieben: tafeln/%s.svg  (%d Zeichen)" % (tid, len(svg)))
