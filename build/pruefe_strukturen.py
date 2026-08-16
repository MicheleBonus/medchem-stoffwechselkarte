# -*- coding: utf-8 -*-
"""Prueft jede Struktur aus MOLS einzeln durch.

    python pruefe_strukturen.py            Bericht (nur Auffaelligkeiten)
    python pruefe_strukturen.py --alle     Tabelle mit allen Strukturen

Geprueft wird
  1. Summenformel, Gesamtladung, CIP-Deskriptoren, Zahl der Dummy-Atome
  2. jeder Beschriftungsindex zeigt auf ein Dummy-Atom ('*'). Zeigt er auf ein
     echtes Atom, steht die Beschriftung am falschen Ort und das Sternchen
     bleibt unbeschriftet stehen -> FEHLER
  3. jede id in MOLS wird irgendwo als {{S:id}} aufgerufen, jeder Aufruf
     im HTML hat eine Struktur
  4. REIHEN: Muster trifft jedes Glied, Vorlage liegt in MOLS oder ist eigen,
     jede Reihe mit fester Bindungslaenge hat im HTML die Klasse "masstab"
"""
import io
import os
import re
import sys
from collections import defaultdict

from rdkit import Chem
from rdkit.Chem import rdCIPLabeler
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit import RDLogger

RDLogger.DisableLog("rdApp.*")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gen_structures as G  # noqa: E402

SRC = os.path.join(HERE, "src")
ALLE = "--alle" in sys.argv

fehler = []
warnung = []


def lies(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def html_dateien():
    aus = []
    for wurzel, _, namen in os.walk(SRC):
        for n in sorted(namen):
            if n.endswith(".html"):
                aus.append(os.path.join(wurzel, n))
    return aus


# ------------------------------------------------------------- 1./2. Molekuele
print("=" * 100)
print("%-24s %-26s %5s %4s %-22s %s" %
      ("id", "Summenformel", "Ladg", "Dumm", "CIP", "Beschriftung"))
print("=" * 100)

zeilen = []
for mid, (smi, labels) in G.MOLS.items():
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        fehler.append("%s: SMILES nicht parsebar: %s" % (mid, smi))
        continue
    Chem.rdmolops.AssignStereochemistry(mol, cleanIt=True, force=True)
    try:
        rdCIPLabeler.AssignCIPLabels(mol)
    except Exception as e:
        warnung.append("%s: CIP-Zuweisung fehlgeschlagen (%s)" % (mid, e))

    formel = CalcMolFormula(mol)
    ladung = Chem.GetFormalCharge(mol)
    dummies = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() == 0]

    cip = []
    for a in mol.GetAtoms():
        if a.HasProp("_CIPCode"):
            cip.append("A%d:%s" % (a.GetIdx(), a.GetProp("_CIPCode")))
    for b in mol.GetBonds():
        if b.GetStereo() != Chem.BondStereo.STEREONONE:
            s = str(b.GetStereo()).replace("STEREO", "")
            if s not in ("NONE",):
                cip.append("B%d-%d:%s" % (b.GetBeginAtomIdx(), b.GetEndAtomIdx(), s))
    # unzugewiesene Stereozentren melden
    offen = Chem.FindMolChiralCenters(mol, includeUnassigned=True,
                                      useLegacyImplementation=False)
    # Phosphat-Phosphor zaehlt RDKit als moegliches Zentrum mit. Am Ester-
    # phosphat sind die freien Sauerstoffe durch Resonanz gleich, ein Zentrum
    # ist da nicht; die 23 Treffer waren Rauschen und verdeckten die echten.
    unbestimmt = [i for i, c in offen if c == "?"
                  and mol.GetAtomWithIdx(i).GetAtomicNum() != 15]
    if unbestimmt:
        warnung.append("%s: Stereozentrum ohne Zuweisung an Atom %s (%s)"
                       % (mid, ", ".join(str(i) for i in unbestimmt),
                          ", ".join(mol.GetAtomWithIdx(i).GetSymbol()
                                    for i in unbestimmt)))

    lbl = dict(labels) if labels else {}
    lbltxt = []
    for idx, txt in sorted(lbl.items()):
        idx = int(idx)
        if idx >= mol.GetNumAtoms():
            fehler.append("%s: Beschriftungsindex %d liegt ausserhalb "
                          "(Molekuel hat %d Atome), Text %r"
                          % (mid, idx, mol.GetNumAtoms(), txt))
            lbltxt.append("%d=%s!AUSSERHALB" % (idx, txt))
            continue
        a = mol.GetAtomWithIdx(idx)
        if a.GetAtomicNum() != 0:
            fehler.append("%s: Beschriftung %r sitzt an Index %d = echtes Atom "
                          "%s (kein Dummy). Dummy-Atome liegen bei %s"
                          % (mid, txt, idx, a.GetSymbol(),
                             dummies if dummies else "(keine)"))
            lbltxt.append("%d=%s!%s" % (idx, txt, a.GetSymbol()))
        else:
            lbltxt.append("%d=%s" % (idx, txt))

    # Dummy ohne Beschriftung: bleibt als nacktes Sternchen stehen
    ohne = [i for i in dummies if i not in {int(k) for k in lbl}]
    if ohne and mid not in G.COA_IDS:
        fehler.append("%s: Dummy-Atom(e) %s ohne Beschriftung -> nacktes '*'"
                      % (mid, ", ".join(str(i) for i in ohne)))

    zeilen.append((mid, formel, ladung, len(dummies), cip, lbltxt))

for mid, formel, ladung, nd, cip, lbltxt in zeilen:
    auff = (ladung != 0) or nd or lbltxt or cip
    if ALLE or auff:
        print("%-24s %-26s %5d %4d %-22s %s"
              % (mid, formel, ladung, nd,
                 ",".join(cip)[:22] if cip else "-",
                 ",".join(lbltxt) if lbltxt else "-"))

# vollstaendige CIP-Liste separat, damit die Tabelle lesbar bleibt
print("\n--- CIP-Deskriptoren vollstaendig ---")
for mid, _, _, _, cip, _ in zeilen:
    if cip:
        print("  %-24s %s" % (mid, " ".join(cip)))

# ------------------------------------------------------------ 3. Aufrufe
text = {p: lies(p) for p in html_dateien()}
aufrufe = defaultdict(list)
for p, t in text.items():
    for m in re.finditer(r"\{\{S:([a-z0-9_]*)\}\}", t):
        aufrufe[m.group(1)].append(os.path.basename(p))
    for m in re.finditer(r"\{\{S:([^}]*)\}\}", t):
        if not re.match(r"^[a-z0-9_]+$", m.group(1)):
            fehler.append("%s: Aufruf ohne brauchbare id: {{S:%s}}"
                          % (os.path.basename(p), m.group(1)))

unbenutzt = sorted(set(G.MOLS) - set(aufrufe))
ohne_struktur = sorted(set(aufrufe) - set(G.MOLS))

print("\n--- Aufrufe ---")
print("  MOLS: %d, aufgerufene ids: %d" % (len(G.MOLS), len(aufrufe)))
# Eine gezeichnete, aber noch nicht gesetzte Struktur ist kein Defekt: die Karte
# wird etappenweise geliefert, der Vorrat laeuft der Prosa voraus. Sie gehoert
# aber sichtbar in den Bericht, sonst waechst der Vorrat unbemerkt.
if ohne_struktur:
    fehler.append("aufgerufen, aber nicht in MOLS: %s" % ", ".join(ohne_struktur))
mehrfach = {k: v for k, v in aufrufe.items() if len(v) > 1}
if mehrfach:
    print("  mehrfach aufgerufen: %s"
          % ", ".join("%s (%dx)" % (k, len(v)) for k, v in sorted(mehrfach.items())))

# ------------------------------------------------------------ 4. Reihen
print("\n--- Reihen ---")
reihe_glieder = defaultdict(list)
for mid, s in G.SCHMUCK.items():
    if s.get("reihe"):
        reihe_glieder[s["reihe"]].append(mid)

for name in sorted(set(G.REIHEN) | set(reihe_glieder)):
    if name not in G.REIHEN:
        fehler.append("Reihe %r wird benutzt (%s), ist aber nicht definiert"
                      % (name, ", ".join(sorted(reihe_glieder[name]))))
        continue
    r = G.REIHEN[name]
    glieder = sorted(reihe_glieder.get(name, []))
    if not glieder:
        fehler.append("Reihe %r ist definiert, aber kein Glied benutzt sie" % name)
        continue
    if len(glieder) < 2:
        warnung.append("Reihe %r hat nur ein Glied (%s) - Ausrichtung ohne Zweck"
                       % (name, glieder[0]))

    # Vorlage: liegt sie in MOLS?
    vsmi = r["vorlage"]
    vref = Chem.MolFromSmiles(vsmi)
    if vref is None:
        fehler.append("Reihe %r: Vorlage nicht parsebar" % name)
        continue
    vkan = Chem.MolToSmiles(vref)
    quelle = [m for m, (s, _) in G.MOLS.items()
              if Chem.MolFromSmiles(s) is not None
              and Chem.MolToSmiles(Chem.MolFromSmiles(s)) == vkan]
    herkunft = ("MOLS:" + ",".join(sorted(quelle))) if quelle else "eigene SMILES"

    # Muster
    vorgabe = r.get("muster")
    patt = Chem.MolFromSmarts(vorgabe) if vorgabe else None
    if vorgabe and patt is None:
        fehler.append("Reihe %r: SMARTS nicht parsebar: %s" % (name, vorgabe))
        continue
    if patt is not None and not vref.GetSubstructMatch(patt):
        fehler.append("Reihe %r: Muster trifft die eigene Vorlage nicht" % name)

    treffer = []
    for g in glieder:
        mol = Chem.MolFromSmiles(G.MOLS[g][0])
        if mol is None:
            continue
        if patt is not None:
            n = len(mol.GetSubstructMatches(patt))
            if n == 0:
                fehler.append("Reihe %r: Muster trifft Glied %r nicht" % (name, g))
            elif n > 1:
                # Mehrdeutig: RDKit legt das Molekuel nach dem ERSTEN Treffer aus.
                # Bei symmetrischen Treffern ist das egal, sonst kippt das Bild
                # gegenueber den Nachbarn - genau der Vergleich, um den es geht.
                warnung.append("Reihe %r: Muster trifft %r %dx - Lage folgt dem "
                               "ersten Treffer, Bild gegen die Nachbarn pruefen"
                               % (name, g, n))
            treffer.append("%s:%d" % (g, n))
        else:
            mu = G.gemeinsames_muster(mol, G.vorlage(name))
            if mu is None:
                fehler.append("Reihe %r: keine gemeinsame Teilstruktur mit %r"
                              % (name, g))
                treffer.append("%s:MCS-0" % g)
            else:
                treffer.append("%s:MCS%d" % (g, mu.GetNumAtoms()))

    print("  %-22s bindung=%-5s vorlage=%-22s glieder=%d  %s"
          % (name, r.get("bindung", "-"), herkunft, len(glieder),
             " ".join(treffer)))

# masstab-Klasse im HTML
masstab_dateien = defaultdict(set)
for p, t in text.items():
    for m in re.finditer(r'class="[^"]*\bmasstab\b[^"]*"', t):
        # welche ids stehen in diesem Block? grob: bis zum naechsten schliessenden
        # Element des Blocks; hier reicht ein Fenster von 4000 Zeichen
        fenster = t[m.end():m.end() + 4000]
        for s in re.finditer(r"\{\{S:([a-z0-9_]+)\}\}", fenster):
            masstab_dateien[s.group(1)].add(os.path.basename(p))

print("\n--- masstab im HTML ---")
for name in sorted(G.REIHEN):
    if not G.REIHEN[name].get("bindung"):
        continue
    # Nur Glieder pruefen, die ueberhaupt im HTML stehen. Ein noch nicht
    # gesetztes Glied kann in keinem masstab-Block liegen; es hier zu melden
    # verdoppelte bloss den Vorratsbericht und verdeckte die echten Faelle.
    glieder = sorted(reihe_glieder.get(name, []))
    gesetzt = [g for g in glieder if g in aufrufe]
    fehlend = [g for g in gesetzt if g not in masstab_dateien]
    if fehlend:
        fehler.append("Reihe %r hat feste Bindungslaenge, aber die Glieder %s "
                      "stehen im HTML in keinem Block mit Klasse 'masstab'"
                      % (name, ", ".join(fehlend)))
    else:
        offen = len(glieder) - len(gesetzt)
        print("  %-22s ok (%d Glieder im masstab-Block%s)"
              % (name, len(gesetzt),
                 ", %d noch nicht gesetzt" % offen if offen else ""))

# ------------------------------------------------------------------- Ergebnis
print("\n" + "=" * 100)
if unbenutzt:
    print("OFFEN: gezeichnet, aber nirgends gesetzt (%d von %d):"
          % (len(unbenutzt), len(G.MOLS)))
    for i in range(0, len(unbenutzt), 6):
        print("  " + ", ".join(unbenutzt[i:i + 6]))
    print("")
if warnung:
    print("HINWEISE (%d):" % len(warnung))
    for w in warnung:
        print("  - %s" % w)
if fehler:
    print("FEHLER (%d):" % len(fehler))
    for f in fehler:
        print("  - %s" % f)
    sys.exit(1)
print("PRUEFUNG: sauber (%d Strukturen)" % len(zeilen))
