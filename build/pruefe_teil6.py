# -*- coding: utf-8 -*-
"""Prueft Summenformeln der Teil-6-Cofaktoren."""
import importlib.util

from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

spec = importlib.util.spec_from_file_location("g", "gen_structures.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FORMEL = {
    "thiamin": "C12H17N4OS+", "tpp": "C12H19N4O7P2S+",
    "riboflavin": "C17H20N4O6", "fmn": "C17H21N4O9P",
    "nicotinsaeure": "C6H5NO2", "nicotinamid": "C6H6N2O",
    "pantothensaeure": "C9H17NO5", "coa": "C21H36N7O16P3S",
    "pyridoxin": "C8H11NO3", "pyridoxal": "C8H9NO3",
    "biotin": "C10H16N2O3S", "carboxybiotin": "C11H16N2O5S",
    "dhf": "C19H21N7O6",
    "dehydroascorbat": "C6H6O6", "liponsaeure": "C8H14O2S2",
    "dihydroliponsaeure": "C8H16O2S2",
    "retinol": "C20H30O", "retinal": "C20H28O",
    "tretinoin": "C20H28O2", "isotretinoin": "C20H28O2",
    "tocopherol": "C29H50O2", "phyllochinon": "C31H46O2",
    "vitk_hydrochinon": "C31H48O2", "menadion": "C11H8O2",
    "isoniazid": "C6H7N3O", "warfarin": "C19H16O4",
    "phenprocoumon": "C18H16O3",
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
