# -*- coding: utf-8 -*-
"""
Leitgerueste: feste Referenzlagen fuer wiederkehrende Molekuelkerne.

Warum ueberhaupt ein Register? Ein Mechanismus zeigt dasselbe Geruest in mehreren
Zustaenden nebeneinander. Laesst man RDKit jede Stufe einzeln einnorden, steht der
Ring jedes Mal anders, und der Leser muss vor dem Vergleich erst jedes Bild neu
ausrichten. Gemessen an den fuenf B6-Stufen der Tafel M-01: 95 Grad Spannweite,
davon 70 Grad zwischen vier Stufen mit identischer Drehvorgabe.

Der Ausweg ist nicht besseres Drehen. `zeige=` in mech.py sucht die beste Drehung
gegen den Schwerpunkt *aller* Atome - der wandert mit der Seitenkette - und die
Kostenfunktion ist blind fuer Spiegelung: Original und gespiegelter Konformer
liefern denselben Zielwert bei entgegengesetztem Umlaufsinn.

Stattdessen bekommt jeder wiederkehrende Kern eine ein fuer alle Mal festgelegte
Lage, die hier als Molblock steht, und jede Stufe wird mit
GenerateDepictionMatching2DStructure darauf gelegt. Das haelt Drehung *und*
Haendigkeit fest. Gemessen ueber dieselben fuenf Stufen: 0,00 Grad Spannweite.

Das Register ist bewusst klein zu halten. Ein Kern gehoert hier hinein, wenn er in
mehreren Stufen einer Tafel oder in mehreren Tafeln vorkommt.

Neu erzeugen laesst sich eine Referenz mit

    python mech_kerne.py b6

Das druckt den Molblock samt gemessenen Ringwinkeln; der Molblock wird dann in
KERNE eingetragen. Eingefroren statt bei jedem Lauf gerechnet, damit eine neue
RDKit-Fassung die veroeffentlichten Bilder nicht stillschweigend verschiebt.
"""
import math

from rdkit import Chem
from rdkit.Chem import rdDepictor

rdDepictor.SetPreferCoordGen(True)


class Kern(object):
    """Ein Leitgeruest: Suchmuster, feste Referenzlage, Bauanleitung.

    muster ist bewusst ladungs- und aromatizitaetsagnostisch (~ als Bindung,
    [#7] statt n). Sonst trifft es das protonierte Ringstickstoff-Kation nicht,
    das in fast jeder PLP-Stufe steht, und die Vorlage greift genau dort nicht,
    wo sie gebraucht wird.
    """

    def __init__(self, name, muster, molblock, bau=None, beschreibung=""):
        self.name = name
        self.muster_smarts = muster
        self.molblock = molblock
        self.bau = bau or {}
        self.beschreibung = beschreibung
        self._ref = None
        self._patt = None

    def muster(self):
        if self._patt is None:
            self._patt = Chem.MolFromSmarts(self.muster_smarts)
            if self._patt is None:
                raise ValueError("Kern %s: Muster nicht parsebar" % self.name)
        return self._patt

    def referenz(self):
        if self._ref is None:
            ref = Chem.MolFromMolBlock(self.molblock, sanitize=True)
            if ref is None:
                raise ValueError("Kern %s: Molblock nicht lesbar" % self.name)
            if not ref.GetSubstructMatch(self.muster()):
                raise ValueError("Kern %s: Muster trifft die eigene Referenz nicht"
                                 % self.name)
            self._ref = ref
        return self._ref

    def trifft(self, mol):
        return bool(mol.GetSubstructMatch(self.muster()))

    def lege(self, mol):
        """Das Molekuel auf die Referenzlage legen. Gibt die Trefferliste zurueck."""
        treffer = mol.GetSubstructMatch(self.muster())
        if not treffer:
            raise ValueError("Kern %s trifft dieses Molekuel nicht" % self.name)
        rdDepictor.GenerateDepictionMatching2DStructure(
            mol, self.referenz(), refPatt=self.muster(), acceptFailure=False)
        return treffer


# --------------------------------------------------------------------- Register

B6_MOLBLOCK = """
     RDKit          2D

 11 11  0  0  0  0  0  0  0  0999 V2000
    0.6840   -1.8794    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.3420   -0.9396    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.6428   -0.7660    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
   -0.9848    0.1736    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3420    0.9396    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.6840    1.8794    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.6688    2.0530    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    0.6428    0.7660    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2856    1.5321    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.9848   -0.1736    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.9695   -0.3473    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  2  3  1  0
  3  4  2  0
  4  5  1  0
  5  6  1  0
  6  7  1  0
  5  8  2  0
  8  9  1  0
  8 10  1  0
 10 11  1  0
 10  2  2  0
M  END
"""

KERNE = {
    "b6": Kern(
        name="b6",
        # CH3 ~ C2(1) ~ N1 ~ C6 ~ C5(~CH2~O) ~ C4(~C4') ~ C3 ~1 ~ O3
        muster="[#6]~[#6]1~[#7]~[#6]~[#6](~[#6]~[#8])~[#6](~[#6])~[#6]~1~[#8]",
        molblock=B6_MOLBLOCK,
        bau={"smiles": "Cc1ncc(CO)c(C)c1O", "ring": [1, 2, 3, 4, 7, 9],
             "leit": 7, "folge": 9, "winkel": 50.0},
        beschreibung=(
            "Pyridoxal-Kern. Lehrbuchlage: Ring-Stickstoff unten links, "
            "2-Methyl unten rechts, 3-Oxy rechts, C4 mit dem C4' oben rechts, "
            "5-CH2-O-P oben links. Damit laeuft der Elektronenfluss vom "
            "Substrat oben rechts in den Ring hinunter, also mit der Leserichtung."),
    ),
}


def kern(name):
    if name not in KERNE:
        raise KeyError("Unbekannter Kern %r. Bekannt: %s"
                       % (name, ", ".join(sorted(KERNE))))
    return KERNE[name]


def passender_kern(mol):
    """Der erste Kern des Registers, der dieses Molekuel trifft; sonst None."""
    for k in KERNE.values():
        if k.trifft(mol):
            return k
    return None


# ------------------------------------------------------------------ Neubau

def _bauen(bau):
    """Eine Referenzlage aus SMILES und Zielwinkel erzeugen.

    Der Zielwinkel legt fest, wohin das Leitatom relativ zum Ringschwerpunkt
    zeigt. Zusaetzlich wird der Umlaufsinn festgeklopft: das Folgeatom muss im
    Konformer (y nach oben) 60 Grad *unter* dem Leitatom liegen, damit der Ring
    im fertigen Bild (y nach unten) im Uhrzeigersinn laeuft. Trifft das nicht zu,
    wird gespiegelt. Ohne diesen Schritt haengt die Haendigkeit am Zufall des
    Koordinatengenerators.
    """
    mol = Chem.MolFromSmiles(bau["smiles"])
    rdDepictor.Compute2DCoords(mol)
    k = mol.GetConformer()
    ring = bau["ring"]
    cx = sum(k.GetAtomPosition(i).x for i in ring) / float(len(ring))
    cy = sum(k.GetAtomPosition(i).y for i in ring) / float(len(ring))
    pts = [(k.GetAtomPosition(i).x - cx, k.GetAtomPosition(i).y - cy)
           for i in range(mol.GetNumAtoms())]

    def winkel(i):
        return math.degrees(math.atan2(pts[i][1], pts[i][0]))

    d = (winkel(bau["folge"]) - winkel(bau["leit"]) + 180.0) % 360.0 - 180.0
    if d > 0:
        pts = [(-x, y) for x, y in pts]
    a = math.atan2(pts[bau["leit"]][1], pts[bau["leit"]][0])
    w = math.radians(bau["winkel"]) - a
    c, s = math.cos(w), math.sin(w)
    pts = [(x * c - y * s, x * s + y * c) for x, y in pts]
    for i, (x, y) in enumerate(pts):
        k.SetAtomPosition(i, (x, y, 0.0))
    return mol


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "b6"
    kk = kern(name)
    mol = _bauen(kk.bau)
    k = mol.GetConformer()
    ring = kk.bau["ring"]
    print("Ringwinkel (Konformer, y nach oben):")
    for i in ring:
        p = k.GetAtomPosition(i)
        print("  idx %2d %-2s %7.1f Grad" % (i, mol.GetAtomWithIdx(i).GetSymbol(),
                                             math.degrees(math.atan2(p.y, p.x))))
    print()
    print(Chem.MolToMolBlock(mol))
