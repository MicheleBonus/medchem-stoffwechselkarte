# -*- coding: utf-8 -*-
"""Prueft Summenformeln der Teil-8-Strukturen."""
import importlib.util

from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

spec = importlib.util.spec_from_file_location("g", "gen_structures.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FORMEL = {
    "gssg": "C20H32N6O12S2", "selenocystein": "C3H7NO2Se",
    "ebselen": "C13H9NOSe", "dimethylfumarat": "C6H8O4",
    "monomethylfumarat": "C5H6O4", "doxorubicin": "C27H29NO11",
    "nitrofurantoin": "C8H6N4O5", "metronidazol": "C6H9N3O3",
    "artemisinin": "C15H22O5", "methylenblau": "C16H18N3S+",
    "hydroxycarbamid": "CH4N2O2", "deferipron": "C7H9NO2",
}

fehler = 0
for k, f in FORMEL.items():
    smi = g.MOLS.get(k, (None,))[0]
    if smi is None:
        print("!! %-20s fehlt in MOLS" % k); fehler += 1; continue
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print("!! %-20s SMILES nicht parsebar" % k); fehler += 1; continue
    got = CalcMolFormula(m)
    if got != f:
        print("!! %-20s %-18s soll %s" % (k, got, f)); fehler += 1

print("Geprueft: %d, Abweichungen: %d" % (len(FORMEL), fehler))
