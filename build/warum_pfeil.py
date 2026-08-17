# -*- coding: utf-8 -*-
"""Diagnose: welcher Teil der Tafel blockiert einen Pfeil?

    python warum_pfeil.py tafel_m01.py

Der Solver meldet von sich aus, *warum* er abgelehnt hat und wie oft. Wenn das
nicht reicht, nennt dieses Skript zusaetzlich die vier naechstliegenden
Stoerelemente mit Koordinaten - meist ist es ein Atomsymbol, eine Beschriftung
oder ein Kasten, den man um zwanzig Pixel verschieben muss.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import mech_schub as S

orig = S.Schub.loesen


def wrap(self, tinte, L, gesetzt, vor=None):
    try:
        return orig(self, tinte, L, gesetzt, vor)
    except S.Fehler:
        art = self._art()
        aus = set(self.quelle.ausschluss()) | set(self.ziel.ausschluss())
        qm = self.quelle.mol() or self.ziel.mol()
        zm = self.ziel.mol() or self.quelle.mol()
        pz = S._schwer(self.ziel.kandidaten(S._mitte(qm, self.quelle), L, "ziel"))
        pq = S._schwer(self.quelle.kandidaten(S._mitte(zm, self.ziel), L, "quelle"))
        kq = self.quelle.kandidaten(pz, L, "quelle")
        kz = self.ziel.kandidaten(pq, L, "ziel")
        best = None
        for qx, qy, sq, zq in kq:
            for zx, zy, sz, zz in kz:
                for seite in (1, -1):
                    for th in S.WINKEL_ART.get(art, S.WINKEL_WAHL):
                        try:
                            b = S.Bogen((qx, qy), (zx, zy), th, seite)
                        except ValueError:
                            continue
                        P = b.abtasten(24)
                        alle = np.vstack([P, np.array(S.kopf_polygon(
                            b, L, self.elektronen == 1))])
                        frei = tinte.abstand(alle, aus)
                        if best is None or frei > best[0]:
                            best = (frei, alle, b)
        tinte._bauen()
        frei, alle, b = best
        print(">>> %s -> %s  (Art %s)" % (S._zeige(self.quelle.herkunft()),
                                          S._zeige(self.ziel.herkunft()), art))
        print("    bester Freiraum %.2f L, Sehne %.2f L, theta %.0f"
              % (frei / L, b.sehne / L, b.theta))
        for name, keys, feld, fn in (
                ("Strecke", tinte.s_key, tinte._s, S._pt_seg),
                ("Kasten", tinte.k_key, tinte._k, S._pt_box)):
            m = np.array([k not in aus for k in keys])
            if not m.any():
                continue
            d = fn(alle, feld[m])
            kk = [k for k in keys if k not in aus]
            rang = np.argsort(d.min(0))[:4]
            for i in rang:
                print("    %-8s %-46s %6.1f px  %s"
                      % (name, kk[int(i)], d[:, int(i)].min(),
                         np.round(feld[m][int(i)], 1)))
        raise


S.Schub.loesen = wrap

import runpy
try:
    runpy.run_path(sys.argv[1] if len(sys.argv) > 1 else "tafel_m01.py",
                   run_name="__main__")
except S.Fehler as e:
    print("ABBRUCH:", e)
