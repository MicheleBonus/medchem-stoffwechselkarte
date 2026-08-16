# -*- coding: utf-8 -*-
"""Prueft Summenformeln der Teil-7-Strukturen."""
import importlib.util

from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

spec = importlib.util.spec_from_file_location("g", "gen_structures.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FORMEL = {
    "captopril": "C9H15NO3S", "enalapril": "C20H28N2O5",
    "enalaprilat": "C18H24N2O5", "lisinopril": "C21H31N3O5",
    "losartan": "C22H23ClN6O", "valsartan": "C24H29N5O3",
    "sacubitril": "C24H29NO5",
    "morphin": "C17H19NO3", "naloxon": "C19H21NO4",
    "gla": "C6H9NO6", "vitk_epoxid": "C31H46O3",
    "tranexamsaeure": "C8H15NO2", "rivaroxaban": "C19H18ClN3O5S",
}

fehler = 0
for k, f in FORMEL.items():
    smi = g.MOLS.get(k, (None,))[0]
    if smi is None:
        print("!! %-18s fehlt in MOLS" % k); fehler += 1; continue
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print("!! %-18s SMILES nicht parsebar" % k); fehler += 1; continue
    got = CalcMolFormula(m)
    if got != f:
        print("!! %-18s %-18s soll %s" % (k, got, f)); fehler += 1

print("Geprueft: %d, Abweichungen: %d" % (len(FORMEL), fehler))
