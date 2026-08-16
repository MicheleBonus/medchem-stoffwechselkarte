# -*- coding: utf-8 -*-
"""Prueft Summenformeln und CIP-Deskriptoren der Teil-5-Strukturen."""
import importlib.util

from rdkit import Chem
from rdkit.Chem import rdCIPLabeler
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

spec = importlib.util.spec_from_file_location("g", "gen_structures.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FORMEL = {
    "glucose": "C6H12O6", "g6p": "C6H13O9P", "fbp": "C6H14O12P2",
    "pyruvat": "C3H4O3", "lactat": "C3H6O3", "ribose5p": "C5H11O8P",
    "prpp": "C5H13O14P3",
    "imp": "C10H13N4O8P", "amp": "C10H14N5O7P", "gmp": "C10H14N5O8P",
    "atp": "C10H16N5O13P3", "adp": "C10H15N5O10P2", "camp": "C10H12N5O6P",
    "adenosin": "C10H13N5O4", "inosin": "C10H12N4O5",
    "hypoxanthin": "C5H4N4O", "xanthin": "C5H4N4O2", "harnsaeure": "C5H4N4O3",
    "coffein": "C8H10N4O2", "theophyllin": "C7H8N4O2",
    "carbamoylphosphat": "CH4NO5P", "orotat": "C5H4N2O4",
    "ump": "C9H13N2O9P", "dump": "C9H13N2O8P", "dtmp": "C10H15N2O8P",
    "udp_glucuronat": "C15H22N2O18P2", "inositol": "C6H12O6",
    "ip3": "C6H15O15P3", "dag": "C35H68O5",
    "allopurinol": "C5H4N4O", "oxypurinol": "C5H4N4O2",
    "febuxostat": "C16H16N2O3S", "probenecid": "C13H19NO4S",
    "colchicin": "C22H25NO6", "azathioprin": "C9H7N7O2S",
    "mercaptopurin": "C5H4N4S", "aciclovir": "C8H11N5O3",
    "tenofovir": "C9H14N5O4P", "cytarabin": "C9H13N3O5",
    "gemcitabin": "C9H11F2N3O4", "leflunomid": "C12H9F3N2O2",
    "teriflunomid": "C12H9F3N2O2", "metformin": "C4H11N5",
    "empagliflozin": "C23H27ClO7", "glibenclamid": "C23H28ClN3O5S",
    "sitagliptin": "C16H15F6N5O", "clopidogrel": "C16H16ClNO2S",
}

# erwarteter CIP-Deskriptor an mindestens einem Zentrum
CIP = {"lactat": "S", "clopidogrel": "S", "sitagliptin": "R"}

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

print("Summenformeln geprueft: %d, Abweichungen: %d" % (len(FORMEL), fehler))

for k, exp in CIP.items():
    m = Chem.MolFromSmiles(g.MOLS[k][0])
    rdCIPLabeler.AssignCIPLabels(m)
    got = [a.GetPropsAsDict()["_CIPCode"] for a in m.GetAtoms() if a.HasProp("_CIPCode")]
    print(("OK " if exp in got else "!! ") + "%-14s soll=%s ist=%s" % (k, exp, got))
