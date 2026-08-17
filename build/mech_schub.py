# -*- coding: utf-8 -*-
"""
Schiebepfeile: Anker aus der Chemie, Geometrie aus dem Solver.

Der alte Weg verlangte vier Zahlen je Pfeil - Bogen, Seite, Spalt, Mindestbogen -
und in allen 79 Aufrufen der siebzehn Tafeln waren sie von Hand getippt. Das
konvergiert nicht: jede Lageaenderung eines Molekuels macht alle vier ungueltig.

Hier beschreibt der Aufruf nur noch, welche Elektronen wohin gehen:

    t.schub(Paar(subst, 0),          Atom(intern, 12))       # neue Sigma-Bindung
    t.schub(Bindung(intern, 12, 13), Paar(intern, 13))       # pi-Paar wird freies Paar
    t.schub(Paar(chin, 14),          Bindung(chin, 13, 14))  # neue pi-Bindung

Alles Weitere folgt daraus. Die Kopfform folgt aus der Elektronenzahl, die
Ankerregel aus dem Typenpaar Quelle-Ziel, der Winkel eines freien Elektronenpaars
aus der groessten Winkelluecke der Bindungen am Atom, und Bauchseite, Oeffnungs-
winkel und genaue Ankerlage sucht der Solver aus rund tausend Kandidaten. Findet
er keinen kollisionsfreien, bricht der Bau ab: dann steht ein Molekuel falsch, und
das laesst sich nicht durch Kruemmen des Pfeils heilen.

Drei Dinge machen das ueberhaupt moeglich:

1. RDKit annotiert sein SVG mit class='bond-3 atom-2 atom-4' und class='atom-13'.
   Daraus lassen sich alle Bindungsstrecken und die *exakten* Glyphenrechtecke der
   Atomsymbole lesen. Geschaetzte Textbreiten waren bisher die Ursache der
   groessten Einzelfehler: fuer "NH+" schaetzte die alte Rechnung 36x18 px, in
   Wahrheit sind es 21,1x9,0.
2. Der Bogen ist ein echter Kreisbogen (SVG A-Segment). Die alte quadratische
   Bezierkurve bekam ihren Kontrollpunkt aus den *ungetrimmten* Endpunkten und
   behielt ihn nach dem Trimmen; daher Kruemmungsverhaeltnisse bis 70:1 zwischen
   Scheitel und Ende.
3. Es wird gar nicht mehr getrimmt. Die Anker liefern gleich die sichtbaren
   Endpunkte mitsamt ihren Abstandsregeln; der Bogen verbindet nur noch.

Masse (L = Bindungslaenge der Tafel), belegt aus Levy, "Arrow Pushing in Organic
Chemistry" (284 vermessene Pfeile) und Brueckner, "Reaktionsmechanismen". Wo die
beiden auseinandergehen, steht die Schnittmenge; die Herleitung dazu in
mech_regeln.py.
"""
import math

import numpy as np

# ------------------------------------------------------------------ Masse (x L)
KOPF_LAENGE = 0.27        # Levy 0.20-0.30 L
KOPF_BREITE = 0.80        # Anteil der Kopflaenge, siehe unten
KOPF_KERBE = 0.70         # Hinterkante eingezogen: konkaver Ruecken
# Zur Kopfbreite: die Statistik ueber 284 Pfeile nennt Breite/Laenge 0,43-0,58,
# gemessen an grossen Pfeilen. Fuer unsere kurzen Pfeile ist das zu schlank, und
# zwar aus einem Grund, der sich erst am fertigen Bild zeigt: ein schlanker Kopf
# hat seine beiden Barben fast parallel zum Schaft, und die innere verschwindet
# im gekruemmten Schaft. Uebrig bleibt eine einzige Barbe - der Vollpfeil sieht
# dann aus wie ein Fischhaken, und die wichtigste Unterscheidung der ganzen
# Zeichensprache ist dahin. Der Kopf ist deshalb kompakt (Breite 0,8 der Laenge),
# mindestens 2,6 Strichbreiten breit, und der Schaft endet vor der Kopfbasis,
# damit beide Barben frei stehen. An Schema 1.7 (Cope) nachgemessen ist der Kopf
# dort 2,2-2,8 Strichbreiten breit; das deckt sich.
KOPF_MIN_STRICH = 2.6     # Kopfbreite mindestens so viele Schaftbreiten
KOPF_SCHAFT = 0.74        # Schaft endet an der Kerbe, seine runde Kappe fuellt sie
WINKEL_SOLL = 100.0       # Oeffnungswinkel; entspricht Sagitta/Sehne 0.233
# Fuer einen Kreisbogen ist Sagitta/Sehne = tan(theta/4)/2. Das Fenster 0.20-0.30
# aus F2 entspricht damit 87-123 Grad; die Auswahl bleibt darin, sonst verletzt
# der Solver eine Regel, gegen die er selbst geprueft wird.
WINKEL_WAHL = (88.0, 94.0, 100.0, 107.0, 114.0, 121.0)
# Je Pfeilart ein eigener Winkelsatz, falls einmal noetig. Zur Zeit leer.
# Der Versuch, eine Delokalisierung ueber mehrere Bindungen in *einen* weit
# ausholenden Pfeil zu fassen, ist an der Geometrie gescheitert: aussen um den
# Ring herum muesste er weiter ausgreifen, als er breit ist, und im Ringinneren
# kann er nicht beginnen, weil sein Ursprung ausserhalb des Rings liegt. Eine
# solche Kaskade gehoert als Kette kurzer Pfeile gezeichnet, Kopf an Schwanz.
WINKEL_ART = {}
RAND_FREMD = 0.25         # Mindestabstand zu fremder Tinte
RAND_SOLL = 0.40          # angestrebter Abstand
RAND_ZIEL = 0.11          # Abstand zum eigenen Zielglyph (Spitze steht davor)
RAND_PFEIL = 0.17         # Mindestabstand zweier Pfeile
PAAR_ABSTAND = 0.52       # Mitte des Punktpaars vom Atomzentrum
PAAR_SPREIZ = 0.17        # halber Abstand der beiden Punkte
KETTE_SOLL = 0.30         # Wunschabstand Spitze(i) zu Schwanz(i+1)

# (Fenster der Buecher, gibt einen Hinweis), (harte Grenzen, brechen den Bau ab).
# Levy nennt fuer die Sehne ausdruecklich keine Obergrenze; ein Pfeil von einem
# abseits stehenden Reagens zum Substrat wird so lang, wie die Tafel ihn macht.
# Deshalb sind die harten Grenzen weit und dienen nur dazu, einen offensichtlich
# falsch gesetzten Anker abzufangen.
SEHNE = {
    "intra": ((0.75, 1.20), (0.60, 1.90)),
    "ring": ((0.60, 0.90), (0.45, 1.30)),
    "inter": ((1.50, 4.00), (1.20, 8.00)),
    # Der kurze Pfeil um ein gemeinsames Atom herum, siehe Schub._art.
    # Geometrisch kann diese Sehne nicht viel laenger als 1,0 L werden. Nach
    # unten begrenzt sie der Kopf: unter etwa 0,45 L bleibt vom Schaft nichts
    # uebrig, und der Pfeil ist nur noch eine Spitze. Die harte Untergrenze
    # liegt darunter, weil bei einem Bindung-zu-Bindung-Pfeil beide Anker im
    # spitzen Winkel liegen koennen; die Schaftpruefung faengt das ab.
    "zurueck": ((0.50, 0.85), (0.38, 1.10)),
}


def _e(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def _winkel_diff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


# ------------------------------------------------------------------- Tintenkarte
class Tinte(object):
    """Wo im Bild schon Farbe liegt: Bindungsstrecken, Glyphenrechtecke, Texte.

    Jedes Stueck traegt einen Schluessel, damit ein Pfeil seine eigene
    Quellbindung und seinen eigenen Zielglyph vom Abstandstest ausnehmen kann -
    an denen gelten eigene, engere Regeln.
    """

    def __init__(self):
        self.strecken, self.s_key = [], []
        self.kaesten, self.k_key = [], []
        self._s = self._k = None
        self._k_hart = np.zeros(0, dtype=bool)

    def strecke(self, x0, y0, x1, y1, key):
        self.strecken.append((x0, y0, x1, y1))
        self.s_key.append(key)
        self._s = None

    def kasten(self, x0, y0, x1, y1, key):
        self.kaesten.append((x0, y0, x1, y1))
        self.k_key.append(key)
        self._k = None

    def abstand(self, P, ausser=()):
        """Kleinster Abstand der Punktwolke P zu aller Tinte ausser den genannten."""
        return self._mess(P, lambda k: k not in ausser)

    def abstand_nur(self, P, keys):
        """Kleinster Abstand zu genau den genannten Stuecken."""
        return self._mess(P, lambda k: k in keys)

    def kreuzt(self, P):
        """Kreuzt der Polygonzug irgendeine gezeichnete Linie oder Beschriftung?

        Ohne Ausnahmen. Auch die eigene Quellbindung und der eigene Zielglyph
        zaehlen: nahe duerfen sie sein, durchquert werden nie.
        """
        self._bauen()
        if _kreuzt_strecken(P, self._s):
            return True
        return bool(len(self._k)) and _in_box(P, self._k[self._k_hart])

    def _bauen(self):
        if self._s is None:
            self._s = (np.array(self.strecken, dtype=float).reshape(-1, 4)
                       if self.strecken else np.zeros((0, 4)))
        if self._k is None:
            self._k = (np.array(self.kaesten, dtype=float).reshape(-1, 4)
                       if self.kaesten else np.zeros((0, 4)))
            # Glyphen und Beschriftungen darf kein Bogen durchqueren. Punktpaare
            # und Einzelelektronen stehen dagegen als kleine Marken im Weg, an
            # denen ein Pfeil ansetzt; fuer die gilt nur der Abstandstest.
            self._k_hart = np.array([k[0] in ("glyph", "sperre")
                                     for k in self.k_key], dtype=bool)

    def _mess(self, P, nimm):
        self._bauen()
        best = 1e9
        if len(self.strecken):
            m = np.array([nimm(k) for k in self.s_key])
            if m.any():
                best = min(best, float(_pt_seg(P, self._s[m]).min()))
        if len(self.kaesten):
            m = np.array([nimm(k) for k in self.k_key])
            if m.any():
                best = min(best, float(_pt_box(P, self._k[m]).min()))
        return best


def _pt_seg(P, S):
    a, b = S[:, 0:2], S[:, 2:4]
    ab = b - a
    l2 = np.maximum((ab ** 2).sum(1), 1e-12)
    ap = P[:, None, :] - a[None, :, :]
    t = np.clip((ap * ab[None, :, :]).sum(2) / l2[None, :], 0.0, 1.0)
    diff = ap - t[:, :, None] * ab[None, :, :]
    return np.sqrt((diff ** 2).sum(2))


def _pt_box(P, B):
    dx = np.maximum(np.maximum(B[None, :, 0] - P[:, None, 0],
                               P[:, None, 0] - B[None, :, 2]), 0.0)
    dy = np.maximum(np.maximum(B[None, :, 1] - P[:, None, 1],
                               P[:, None, 1] - B[None, :, 3]), 0.0)
    return np.hypot(dx, dy)


def _kreuzt_strecken(P, S):
    """Kreuzt der Polygonzug P eine der Strecken S? Echter Schnitt, kein Abstand.

    Der Abstandstest allein genuegt nicht. An seiner eigenen Quellbindung darf ein
    Pfeil nahe sein - dort gilt ein Lotabstand von 0,22 L, weniger als der
    Mindestabstand zu fremder Tinte -, und deshalb ist diese Bindung vom
    Abstandstest ausgenommen. Durch sie hindurchlaufen darf er trotzdem nie. Genau
    das ist in fuenf Tafeln passiert und von der Pruefung nicht bemerkt worden.
    Ein Schnitttest braucht keine Ausnahmen: Kreuzen ist immer falsch.
    """
    if len(P) < 2 or not len(S):
        return False
    a, b = P[:-1], P[1:]
    c, d = S[:, 0:2], S[:, 2:4]
    r = (b - a)[:, None, :]
    s = (d - c)[None, :, :]
    qp = c[None, :, :] - a[:, None, :]
    rxs = r[:, :, 0] * s[:, :, 1] - r[:, :, 1] * s[:, :, 0]
    mit = np.abs(rxs) > 1e-12
    if not mit.any():
        return False
    sicher = np.where(mit, rxs, 1.0)
    t = (qp[:, :, 0] * s[:, :, 1] - qp[:, :, 1] * s[:, :, 0]) / sicher
    u = (qp[:, :, 0] * r[:, :, 1] - qp[:, :, 1] * r[:, :, 0]) / sicher
    return bool((mit & (t > 1e-9) & (t < 1 - 1e-9)
                 & (u > 1e-9) & (u < 1 - 1e-9)).any())


def _in_box(P, B):
    """Liegt ein Punkt aus P im Inneren eines Rechtecks aus B?

    Fuer den Zielglyph: die Spitze steht nach Z1 davor, also ausserhalb. Kommt
    trotzdem ein Stueck des Bogens im Rechteck zu liegen, laeuft er durch das
    Atomsymbol.
    """
    if not len(P) or not len(B):
        return False
    return bool(((P[:, None, 0] > B[None, :, 0] + 0.4)
                 & (P[:, None, 0] < B[None, :, 2] - 0.4)
                 & (P[:, None, 1] > B[None, :, 1] + 0.4)
                 & (P[:, None, 1] < B[None, :, 3] - 0.4)).any())


# ------------------------------------------------------------------------ Anker
class Anker(object):
    """Ein chemisch benannter Endpunkt. Liefert Kandidatenlagen, keine Koordinate.

    kandidaten() gibt Tupel (x, y, strafe, zusatz) zurueck. 'zusatz' traegt, was
    beim Zeichnen noch gebraucht wird - etwa der Winkel, unter dem ein freies
    Elektronenpaar gesetzt werden soll.
    """

    rolle_beschreibung = ""

    def herkunft(self):
        raise NotImplementedError

    def ausschluss(self):
        return ()

    def mol(self):
        return None

    def kandidaten(self, partner, L, rolle):
        raise NotImplementedError


def _freie_richtungen(m, idx, partner, n=6, L=21.0, seite="auto"):
    """Richtungen, in die am Atom kein Substituent steht, beste zuerst.

    Ein freies Elektronenpaar und die Spitze eines Pfeils gehoeren in dieselbe
    Luecke, in der ein Chemiker sie zeichnen wuerde: in den groessten Winkel-
    bereich zwischen den vorhandenen Bindungen, und dort moeglichst auf der Seite
    des Reaktionspartners.

    Ein Atomsymbol steht dem im Weg. RDKit setzt die Wasserstoffe eines Labels
    waagerecht neben das Element, "H2N" reicht dadurch nach links weiter als eine
    halbe Bindungslaenge. Ein Paar in diese Richtung stuende weit ausserhalb des
    Molekuels und saehe aus, als gehoere es zu nichts. Deshalb werden Richtungen
    bestraft, in denen der Glyph weit reicht: das Paar rueckt dann nach oben oder
    unten, wo die Schrift schmal ist.
    """
    x, y = m.atom(idx)
    nach = [math.degrees(math.atan2(m.atom(a.GetIdx())[1] - y,
                                    m.atom(a.GetIdx())[0] - x))
            for a in m.mol.GetAtomWithIdx(int(idx)).GetNeighbors()
            if a.GetIdx() < len(m.koord)]
    ziel = math.degrees(math.atan2(partner[1] - y, partner[0] - x))
    if not nach:
        kand = [(ziel, 0.0)]
    else:
        nach = sorted(a % 360.0 for a in nach)
        kand = []
        for i, a in enumerate(nach):
            b = nach[(i + 1) % len(nach)] + (360.0 if i + 1 == len(nach) else 0.0)
            luecke = b - a
            if luecke < 62.0:
                continue
            mitte = (a + b) / 2.0
            kand.append((mitte, luecke))
            # Eine weite Luecke wird abgetastet statt nur halbiert. Das ist noetig,
            # weil die brauchbare Richtung nicht die geometrische Mitte sein muss:
            # an einem Stickstoff mit der Beschriftung "HN+" reicht der Glyph nach
            # links weit hinaus, nach unten kaum - und genau dort muss die Spitze
            # hin, wenn sie das Wort nicht durchqueren soll.
            if luecke > 150.0:
                innen0, innen1 = a + 40.0, b - 40.0
                n_ab = max(2, int((innen1 - innen0) // 42))
                for k in range(n_ab + 1):
                    kand.append((innen0 + (innen1 - innen0) * k / float(n_ab),
                                 luecke))
        if not kand:
            kand = [(ziel, 90.0)]
    # Nach Naehe zum Partner sortieren; enge Luecken und breite Glyphen bestraft,
    # und Richtungen, die ins Molekuel hineinzeigen, ebenfalls. Der letzte Punkt
    # ist noetig, weil der Partner eines weit ausgreifenden Pfeils auf der
    # *anderen* Seite des Geruests liegen kann: dann zeigt die partnernaechste
    # Luecke mitten durch den Ring, und der Pfeil haette dort nie Platz.
    cx, cy = _bezugsmitte(m, idx, seite)
    nach_innen = math.degrees(math.atan2(cy - y, cx - x))
    out = []
    for a, luecke in kand:
        innen = math.cos(math.radians(_winkel_diff(a, nach_innen)))
        if seite == "innen":
            innen = -innen
        strafe = (_winkel_diff(a, ziel) / 45.0
                  + max(0.0, 110.0 - luecke) / 40.0
                  + max(0.0, _glyph_reichweite(m, idx, a) / L - 0.22) * 3.0
                  + max(0.0, innen) ** 2 * (0.0 if seite == "egal" else 1.6))
        out.append((a % 360.0, strafe))
    out.sort(key=lambda t: t[1])
    # Aehnliche Richtungen zusammenfassen, damit die Auswahl breit bleibt: sonst
    # belegen fuenf Varianten derselben Luecke alle Plaetze und die eine
    # brauchbare Richtung auf der anderen Seite faellt heraus.
    entfernt = []
    for a, s in out:
        if all(_winkel_diff(a, b) > 32.0 for b, _ in entfernt):
            entfernt.append((a, s))
        if len(entfernt) >= n:
            break
    return entfernt


def _bezugsmitte(m, idx, seite):
    """Wohin 'innen' zeigt.

    Fuer die Aussenwahl ist der Schwerpunkt aller Atome der richtige Bezug. Fuer
    'innen' waere er falsch: bei einem Substituenten am Ring zoege er den Pfeil
    zur Seitenkette statt in den Ring. Massgeblich ist dann der Mittelpunkt des
    Rings, an dem das Atom haengt.
    """
    if seite == "innen":
        ri = m.mol.GetRingInfo()
        nachbarn = {idx} | {a.GetIdx() for a
                            in m.mol.GetAtomWithIdx(int(idx)).GetNeighbors()}
        for ring in ri.AtomRings():
            if nachbarn & set(ring):
                pts = [m.atom(i) for i in ring if i < len(m.koord)]
                if pts:
                    return (sum(p[0] for p in pts) / len(pts),
                            sum(p[1] for p in pts) / len(pts))
    return (sum(p[0] for p in m.koord) / len(m.koord),
            sum(p[1] for p in m.koord) / len(m.koord))


def _glyph_reichweite(m, idx, richtung_grad):
    """Wie weit das Atomsymbol vom Atomzentrum aus in diese Richtung reicht.

    Gemessen als Austrittspunkt des Strahls aus dem Glyphenrechteck, nicht als
    Projektion der Ecken. Der Unterschied ist gross: bei "H2N" reicht das
    Rechteck weit nach links, und die Eckprojektion meldete deshalb auch nach
    oben einen grossen Wert. Ein freies Paar wurde dadurch senkrecht nach oben
    weggeschoben, obwohl dort nur die Oberkante der Schrift liegt.
    """
    box = m.glyphen.get(int(idx))
    if not box:
        return 0.0
    x, y = m.atom(idx)
    a = math.radians(richtung_grad)
    ux, uy = math.cos(a), math.sin(a)
    ts = []
    if abs(ux) > 1e-9:
        for bx in (box[0], box[2]):
            t = (bx - x) / ux
            if t > 0 and box[1] - 1e-6 <= y + uy * t <= box[3] + 1e-6:
                ts.append(t)
    if abs(uy) > 1e-9:
        for by in (box[1], box[3]):
            t = (by - y) / uy
            if t > 0 and box[0] - 1e-6 <= x + ux * t <= box[2] + 1e-6:
                ts.append(t)
    return max(ts) if ts else 0.0


class Paar(Anker):
    """Ein freies Elektronenpaar am Atom.

    Als Quelle wird das Punktpaar mitgezeichnet und ist Pfeilursprung; als Ziel
    steht es fuer das Paar, das bei einer Heterolyse am Atom zurueckbleibt - dort
    wird nichts gezeichnet, weil die Produktstruktur daneben steht.
    """

    def __init__(self, mol, idx):
        self.m, self.idx = mol, int(idx)

    def herkunft(self):
        return ("elektronenpaar", self.m.name, self.idx)

    def mol(self):
        return self.m

    def ausschluss(self):
        return (("glyph", self.m.name, self.idx),)

    def kandidaten(self, partner, L, rolle):
        out = []
        for grad, strafe in _freie_richtungen(self.m, self.idx, partner, L=L):
            a = math.radians(grad)
            ux, uy = math.cos(a), math.sin(a)
            x, y = self.m.atom(self.idx)
            # Die Spreizung setzt die beiden Punkte quer zur Richtung. Wird nur
            # ihre Mitte aus dem Glyphenrechteck geschoben, rutscht einer der
            # beiden wieder hinein und verschmilzt mit dem Buchstaben. Deshalb
            # wird die Reichweite auch fuer die beiden ausgelenkten Richtungen
            # gemessen.
            quer = math.degrees(math.atan(PAAR_SPREIZ / max(PAAR_ABSTAND, 0.01)))
            weite = max(_glyph_reichweite(self.m, self.idx, grad + dd)
                        for dd in (-quer, 0.0, quer))
            r = max(PAAR_ABSTAND * L, weite + 0.20 * L)
            px, py = x + ux * r, y + uy * r
            if rolle == "quelle":
                tx, ty = _e(partner[0] - px, partner[1] - py)
                for weg in (0.06, 0.15, 0.25):
                    out.append((px + tx * weg * L, py + ty * weg * L,
                                strafe + weg * 1.2, {"paar": (px, py, grad)}))
            else:
                for d in (0.30, 0.37, 0.45):
                    rr = max(d * L, _glyph_reichweite(self.m, self.idx, grad)
                             + RAND_ZIEL * L)
                    out.append((x + ux * rr, y + uy * rr,
                                strafe + abs(rr / L - 0.37) * 2.0, {}))
        return out


class Atom(Anker):
    """Ein Atom als Ziel einer neuen Sigma-Bindung, oder als geladene Quelle.

    seite= bestimmt, auf welcher Seite des Atoms der Pfeil ansetzt bzw. endet:
    "auto" waehlt die Luecke, die vom Molekuel wegzeigt, "innen" die zum
    Molekuelinneren hin. "innen" braucht ein Pfeil, der die Delokalisierung
    durch einen Ring zeigt; ohne die Angabe schoebe ihn die Automatik nach
    aussen, wo er um das halbe Molekuel herumgreifen muesste.
    """

    def __init__(self, mol, idx, seite="auto"):
        self.m, self.idx = mol, int(idx)
        self.seite = seite

    def herkunft(self):
        return ("atom", self.m.name, self.idx)

    def mol(self):
        return self.m

    def ausschluss(self):
        return (("glyph", self.m.name, self.idx),)

    def kandidaten(self, partner, L, rolle):
        x, y = self.m.atom(self.idx)
        # Als Ziel steht die Spitze dicht vor dem Atom (Z1). Als Quelle - ein
        # geladenes Atom ohne gezeichnetes Paar, U3 - darf der Schwanz weiter
        # weg beginnen: an einem Atom mit zwei Substituenten liegt die
        # Winkelhalbierende sonst noch zwischen deren Bindungsstrichen.
        weiten = (0.29, 0.36, 0.44) if rolle == "ziel" else (0.33, 0.42, 0.52)
        out = []
        for grad, strafe in _freie_richtungen(self.m, self.idx, partner, L=L,
                                              seite=self.seite):
            a = math.radians(grad)
            ux, uy = math.cos(a), math.sin(a)
            for d in weiten:
                r = max(d * L,
                        _glyph_reichweite(self.m, self.idx, grad) + RAND_ZIEL * L)
                out.append((x + ux * r, y + uy * r,
                            strafe + abs(r / L - weiten[1]) * 2.0, {}))
        return out


class Elektron(Anker):
    """Ein einzelnes Elektron - Ursprung eines Fischhakens."""

    def __init__(self, mol, idx):
        self.m, self.idx = mol, int(idx)

    def herkunft(self):
        return ("einzelelektron", self.m.name, self.idx)

    def mol(self):
        return self.m

    def ausschluss(self):
        return (("glyph", self.m.name, self.idx),)

    def kandidaten(self, partner, L, rolle):
        out = []
        for grad, strafe in _freie_richtungen(self.m, self.idx, partner, L=L):
            a = math.radians(grad)
            ux, uy = math.cos(a), math.sin(a)
            x, y = self.m.atom(self.idx)
            r = max(PAAR_ABSTAND * L,
                    _glyph_reichweite(self.m, self.idx, grad) + 0.30 * L)
            px, py = x + ux * r, y + uy * r
            if rolle == "quelle":
                tx, ty = _e(partner[0] - px, partner[1] - py)
                for weg in (0.06, 0.18):
                    out.append((px + tx * weg * L, py + ty * weg * L,
                                strafe + weg, {"punkt": (px, py)}))
            else:
                for d in (0.30, 0.40):
                    out.append((x + ux * d * L, y + uy * d * L, strafe, {}))
        return out


class Bindung(Anker):
    """Eine Bindung: als Quelle das Paar, das sie traegt; als Ziel die Bindung,
    die neu entsteht. In beiden Rollen sitzt der Anker seitlich neben der Linie,
    nie darauf."""

    def __init__(self, mol, i, j):
        self.m, self.i, self.j = mol, int(i), int(j)

    def herkunft(self):
        return ("bindung", self.m.name, (self.i, self.j))

    def mol(self):
        return self.m

    def ausschluss(self):
        b = self.m.mol.GetBondBetweenAtoms(self.i, self.j)
        return (("bindung", self.m.name, b.GetIdx()),) if b else ()

    def kandidaten(self, partner, L, rolle):
        (ax, ay), (bx, by) = self.m.atom(self.i), self.m.atom(self.j)
        ux, uy = _e(bx - ax, by - ay)
        nx, ny = -uy, ux
        laenge = math.hypot(bx - ax, by - ay)
        # Fenster nach U4/U5 bzw. Z2: laengs um die Mitte, quer 0.20-0.30 L
        ts = (0.42, 0.50, 0.58) if rolle == "quelle" else (0.40, 0.50, 0.60)
        # Die eigene Bindungstinte: bei einer Doppelbindung liegt die zweite
        # Linie um etwa 0,15 L seitlich versetzt, und zwar nur auf einer Seite.
        # Der Lotabstand wird deshalb nicht von der Verbindungslinie der
        # Atommittelpunkte gemessen, sondern vom tatsaechlich gezeichneten
        # Strich. Regel U5 will den Schwanz neben der inneren Linie, nicht auf ihr.
        b = self.m.mol.GetBondBetweenAtoms(self.i, self.j)
        eigen = np.array([s[:4] for s in self.m.strecken
                          if b is not None and s[4] == b.GetIdx()]) \
            if self.m.strecken else np.zeros((0, 4))
        out = []
        for t in ts:
            px, py = ax + ux * laenge * t, ay + uy * laenge * t
            for lot in (0.22, 0.28):
                for s in (1, -1):
                    qx = px + nx * lot * L * s
                    qy = py + ny * lot * L * s
                    if len(eigen):
                        for _ in range(6):
                            d = float(_pt_seg(np.array([[qx, qy]]), eigen).min())
                            if d >= 0.20 * L:
                                break
                            qx += nx * s * 0.04 * L
                            qy += ny * s * 0.04 * L
                    nah = math.hypot(partner[0] - qx, partner[1] - qy)
                    out.append((qx, qy, abs(t - 0.5) * 6.0 + nah / (14.0 * L),
                                {"t": t, "lot": lot}))
        out.sort(key=lambda k: k[2])
        return out[:12]


class Fest(Anker):
    """Ein ausdruecklich benannter Ort - fuer Teilchen ohne SMILES.

    Das sind die Anker der Bausteine: Metallzentrum, axialer Ligand, Thiolat,
    frei gesetzte Elektronenpaare, benannte Marken. Sie kennen keine
    Nachbarschaft, aus der sich eine freie Richtung ableiten liesse; deshalb
    wird ein Faecher um die Richtung zum Partner angeboten und der Solver
    waehlt daraus. Frueher gab es nur drei Lagen genau auf der Verbindungslinie,
    und die Sehnenstrafe zog den Anker dabei systematisch vom Ort weg - die
    Spitze landete dann bis zu 1,4 Bindungslaengen neben dem Atom, das sie
    treffen sollte.
    """

    def __init__(self, x, y, name, art="marke", rx=0.0, ry=0.0):
        self.x, self.y, self.name, self.art = float(x), float(y), name, art
        self.rx, self.ry = rx, ry

    def herkunft(self):
        return (self.art, self.name, None)

    def kandidaten(self, partner, L, rolle):
        grund = math.degrees(math.atan2(partner[1] - self.y, partner[0] - self.x))
        r = max(self.rx, self.ry)
        out = []
        for ab in (0.0, -34.0, 34.0, -66.0, 66.0, -98.0, 98.0):
            a = math.radians(grund + ab)
            ux, uy = math.cos(a), math.sin(a)
            for weg in (0.16, 0.28, 0.42):
                d = r + weg * L
                out.append((self.x + ux * d, self.y + uy * d,
                            abs(ab) / 55.0 + abs(weg - 0.28) * 2.0, {}))
        return out


def anker_aus(ziel):
    """Alte Schreibweisen mitnehmen: (mol, i), (mol, i, j), Punkt, (x, y)."""
    if isinstance(ziel, Anker):
        return ziel
    if hasattr(ziel, "herkunft") and hasattr(ziel, "x"):        # mech.Punkt
        return Fest(ziel.x, ziel.y, ziel.herkunft[1] or "punkt",
                    art=ziel.herkunft[0], rx=getattr(ziel, "rx", 0.0),
                    ry=getattr(ziel, "ry", 0.0))
    if isinstance(ziel, tuple) and len(ziel) == 3 and hasattr(ziel[0], "atom"):
        return Bindung(ziel[0], ziel[1], ziel[2])
    if isinstance(ziel, tuple) and len(ziel) == 2 and hasattr(ziel[0], "atom"):
        return Atom(ziel[0], ziel[1])
    raise TypeError("Kein Anker: %r" % (ziel,))


# ------------------------------------------------------------------- Kreisbogen
class Bogen(object):
    """Kreisbogen fester Kruemmung zwischen zwei Punkten.

    Beschrieben ueber Sehne und Oeffnungswinkel theta. Sagitta/Sehne ist dann
    tan(theta/4)/2 - bei theta=100 Grad also 0.233, mitten im Fenster beider
    Buecher. Konstante Kruemmung ist der Punkt: bei der frueheren Parabel zeigte
    der tangential gesetzte Kopf flacher ins Ziel, als der Bogen es versprach.
    """

    def __init__(self, p0, p1, theta, seite):
        self.p0, self.p1, self.theta, self.seite = p0, p1, float(theta), seite
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        self.sehne = math.hypot(dx, dy)
        if self.sehne < 1e-6:
            raise ValueError("Bogen ohne Laenge")
        t = math.radians(self.theta)
        self.r = self.sehne / (2.0 * math.sin(t / 2.0))
        ux, uy = dx / self.sehne, dy / self.sehne
        nx, ny = -uy, ux
        h = self.r * math.cos(t / 2.0)
        mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
        self.c = (mx - nx * h * seite, my - ny * h * seite)
        self.sagitta = self.r - h
        self.scheitel = (mx + nx * self.sagitta * seite,
                         my + ny * self.sagitta * seite)
        a0 = math.atan2(p0[1] - self.c[1], p0[0] - self.c[0])
        a1 = math.atan2(p1[1] - self.c[1], p1[0] - self.c[0])
        d = (a1 - a0) % (2 * math.pi)
        if d > math.pi:
            d -= 2 * math.pi
        self.a0, self.spanne = a0, d
        self.sweep = 1 if d > 0 else 0

    def punkt(self, s):
        a = self.a0 + self.spanne * s
        return (self.c[0] + math.cos(a) * self.r,
                self.c[1] + math.sin(a) * self.r)

    def tangente(self, s):
        a = self.a0 + self.spanne * s
        v = (-math.sin(a), math.cos(a)) if self.spanne > 0 else (math.sin(a), -math.cos(a))
        return v

    def abtasten(self, n=26):
        return np.array([self.punkt(i / float(n - 1)) for i in range(n)])

    def zurueck(self, laenge):
        """Anteil s, um den man vom Ende her um 'laenge' zurueckgeht."""
        bogenlaenge = abs(self.spanne) * self.r
        return max(0.0, 1.0 - laenge / bogenlaenge) if bogenlaenge else 1.0

    def pfad(self, bis=1.0):
        p = self.punkt(bis)
        gross = 1 if abs(self.spanne * bis) > math.pi else 0
        return "M %.1f %.1f A %.1f %.1f 0 %d %d %.1f %.1f" % (
            self.p0[0], self.p0[1], self.r, self.r, gross, self.sweep, p[0], p[1])


def kopf_masse(L, strich, r=None):
    """Kopflaenge und Kopfbreite in Pixeln.

    r ist der Bogenradius. Bei einem engen Bogen weicht der Schaft auf dem Weg
    zur Spitze um r*(1-cos(hl/r)), also etwa hl^2/(2r), zur Bogenmitte hin ab -
    genau dorthin, wo die innere Barbe sitzt. Ist der Kopf dann nicht breit genug, verschwindet sie im
    Schaft, und der Vollpfeil sieht aus wie ein Fischhaken. Gemessen an einem
    Fall mit r = 8,2 px: Abweichung 1,98 px, halbe Kopfbreite 2,25 px, halbe
    Schaftbreite 0,7 px - die Barbe lag 0,43 px innerhalb des Schaftes. Der Kopf
    waechst deshalb mit der Kruemmung mit.
    """
    hl = KOPF_LAENGE * L
    hw = max(KOPF_BREITE * hl, KOPF_MIN_STRICH * strich)
    if r:
        # gedeckelt: ein Kopf, der breiter waere als lang, ist ein Faecher und
        # kein Pfeilkopf. Wo der Deckel nicht reicht, ist der Bogen zu eng - das
        # bestraft die Bewertung, statt es durch die Kopfform zu kaschieren.
        hw = max(hw, min(hl * hl / float(r) + 1.7 * strich, 1.35 * hl))
    return hl, hw


def kopf_eng(hl, hw, r, strich):
    """Wie weit die innere Barbe im Schaft verschwindet, in Pixeln.

    Positiv heisst: der Schaft deckt sie zu, und der Vollpfeil beginnt wie ein
    Fischhaken auszusehen.
    """
    if not r:
        return -1.0
    weicht = r * (1.0 - math.cos(min(hl / float(r), math.pi)))
    return (weicht + 0.5 * strich) - hw / 2.0


def kopf_polygon(bogen, L, halb=False, strich=1.6):
    """Pfeilkopf als Polygon in Nutzerkoordinaten.

    Nicht als marker-end: dort fehlte markerUnits, der SVG-Default ist
    strokeWidth, und die Kopflaenge wurde dadurch mit der Strichbreite
    multipliziert - 11,05 px statt der zulaessigen 5,9 bei 21 px Bindung. refX
    schob die Spitze zusaetzlich ueber den berechneten Endpunkt hinaus.
    """
    hl, hw = kopf_masse(L, strich, bogen.r)
    spitze = bogen.punkt(1.0)
    ux, uy = bogen.tangente(1.0)
    nx, ny = -uy, ux
    ruecken = (spitze[0] - ux * hl, spitze[1] - uy * hl)
    kerbe = (spitze[0] - ux * hl * KOPF_KERBE, spitze[1] - uy * hl * KOPF_KERBE)
    if not halb:
        pts = [spitze,
               (ruecken[0] + nx * hw / 2.0, ruecken[1] + ny * hw / 2.0),
               kerbe,
               (ruecken[0] - nx * hw / 2.0, ruecken[1] - ny * hw / 2.0)]
    else:
        # Fischhaken: die Barbe auf der konvexen Seite des Bogens
        s = 1.0 if ((spitze[0] - bogen.c[0]) * nx
                    + (spitze[1] - bogen.c[1]) * ny) > 0 else -1.0
        pts = [spitze,
               (ruecken[0] + nx * hw * s, ruecken[1] + ny * hw * s),
               kerbe]
    return pts


# ----------------------------------------------------------------------- Solver
class Schub(object):
    """Eine Elektronenverschiebung, solange sie noch keine Geometrie hat."""

    def __init__(self, quelle, ziel, elektronen=2, art=None, kette=None,
                 strich=None, notiz=None):
        self.quelle = anker_aus(quelle)
        self.ziel = anker_aus(ziel)
        self.elektronen = int(elektronen)
        self.art = art
        self.kette = kette
        self.strich = strich
        self.notiz = notiz
        self.bogen = None
        self.zusatz_q = self.zusatz_z = None
        self.mass = {}
        self.L = 21.0
        self.breite = 1.6      # Schaftbreite in px, von der Tafel gesetzt
        self._letzte_art = "intra"
        self.frei = 0.0

    # ------------------------------------------------------------------
    def _art(self):
        if self.art:
            return self.art
        mq, mz = self.quelle.mol(), self.ziel.mol()
        if mq is None or mz is None or mq is not mz:
            return "inter"
        idx = []
        for a in (self.quelle, self.ziel):
            idx += ([a.i, a.j] if isinstance(a, Bindung) else [a.idx])
        # Der kurze Pfeil um ein gemeinsames Atom herum. Zwei Faelle, dieselbe
        # Geometrie: aus einer Bindung auf eines ihrer eigenen Atome (jede
        # Heterolyse), und aus einer Bindung in die Nachbarbindung am selben Atom
        # (jede Verschiebung, jeder Radikalschritt). Es ist das haeufigste Motiv
        # der Sammlung und hat die kuerzeste Sehne: Anfang und Ende liegen eine
        # halbe Bindungslaenge auseinander, quer dazu je 0,2 L versetzt. Im
        # Fenster fuer gewoehnliche innermolekulare Pfeile (ab 0,60 L) fiel es
        # regelmaessig durch, und der Pfeil blieb ungezeichnet - obwohl reichlich
        # kreuzungsfreie Boegen zur Verfuegung standen. Neun Tafeln hatten
        # dadurch unvollstaendige Pfeilsaetze.
        def atome(a):
            return {a.i, a.j} if isinstance(a, Bindung) else {a.idx}

        gemeinsam = atome(self.quelle) & atome(self.ziel)
        if gemeinsam and not (isinstance(self.quelle, Bindung)
                              and isinstance(self.ziel, Bindung)
                              and atome(self.quelle) == atome(self.ziel)):
            return "zurueck"
        ri = mq.mol.GetRingInfo()
        for ring in ri.AtomRings():
            if all(i in ring for i in idx):
                return "ring"
        return "intra"

    def loesen(self, tinte, L, gesetzt, vorgaenger=None):
        art = self._art()
        self._letzte_art = art
        (f0, f1), (h0, h1) = SEHNE[art]
        aus = set(self.quelle.ausschluss()) | set(self.ziel.ausschluss())

        qm = self.quelle.mol() or self.ziel.mol()
        zp = self.ziel.mol() or self.quelle.mol()
        grob_q = self.quelle.kandidaten(_mitte(zp, self.ziel), L, "quelle")
        grob_z = self.ziel.kandidaten(_mitte(qm, self.quelle), L, "ziel")
        # zweiter Durchgang, jetzt mit dem tatsaechlichen Partnerschwerpunkt
        pz = _schwer(grob_z)
        pq = _schwer(grob_q)
        kand_q = self.quelle.kandidaten(pz, L, "quelle")
        kand_z = self.ziel.kandidaten(pq, L, "ziel")

        vorspitze = None
        if vorgaenger is not None and vorgaenger.bogen is not None:
            vorspitze = vorgaenger.bogen.punkt(1.0)
        paare = []
        for qx, qy, sq, zq in kand_q:
            for zx, zy, sz, zz in kand_z:
                d = math.hypot(zx - qx, zy - qy) / L
                if not (h0 <= d <= h1):
                    continue
                mitte = (f0 + f1) / 2.0
                wert = sq + sz + abs(d - mitte) * 1.1
                if vorspitze is not None:
                    # Kopf an Schwanz: der Schwanz dieses Pfeils gehoert dicht an
                    # die Spitze des vorigen, sonst zerfaellt der Schritt in
                    # Einzelpfeile, die der Leser nicht zusammenliest.
                    k = math.hypot(vorspitze[0] - qx, vorspitze[1] - qy) / L
                    wert += abs(k - KETTE_SOLL) * 3.0
                paare.append((wert, (qx, qy), (zx, zy), zq, zz, d))
        if not paare:
            raise Fehler(self, "Sehnenlaenge liegt ausserhalb %.2f-%.2f L (Typ %s). "
                               "Das ist ein Layoutfehler: die Molekuele stehen zu "
                               "weit auseinander oder zu dicht beieinander." % (h0, h1, art))
        paare.sort(key=lambda t: t[0])

        winkel = WINKEL_ART.get(art, WINKEL_WAHL)
        self._soll = WINKEL_SOLL if art not in WINKEL_ART else winkel[len(winkel) // 2]

        def suchen(auswahl):
            gut, weit = None, []
            for grund, p0, p1, zq, zz, d in auswahl:
                for seite in (1, -1):
                    for theta in winkel:
                        try:
                            b = Bogen(p0, p1, theta, seite)
                        except ValueError:
                            continue
                        wert, frei, warum = self._bewerten(
                            b, tinte, aus, gesetzt, L, d, f0, f1, vorgaenger)
                        weit.append(frei)
                        if wert is None:
                            self._abgelehnt[warum] = self._abgelehnt.get(warum, 0) + 1
                            continue
                        if gut is None or wert + grund < gut[0]:
                            gut = (wert + grund, b, zq, zz, d, art, frei)
            return gut, weit

        # Erst die aussichtsreichsten Ankerpaare, dann notfalls alle. Die
        # Vorauswahl bewertet nur die Anker, nicht den Bogen; wo es eng ist,
        # sind die vorn liegenden Paare manchmal genau die, deren Boegen dann
        # doch irgendwo anstossen.
        self._abgelehnt = {}
        best, eng = suchen(paare[:60])
        if best is None and len(paare) > 60:
            best, eng2 = suchen(paare[60:])
            eng += eng2
        if best is None:
            warum = sorted(self._abgelehnt.items(), key=lambda kv: -kv[1])
            raise Fehler(self, "kein zulaessiger Bogen unter %d Kandidaten. "
                               "Abgelehnt wegen: %s. Bester Freiraum zu fremder "
                               "Tinte %.2f L. Das ist ein Layoutfehler: an dieser "
                               "Stelle ist kein Platz fuer den Pfeil."
                         % (sum(self._abgelehnt.values()),
                            ", ".join("%s (%dx)" % (k, n) for k, n in warum),
                            (max(eng) / L) if eng else 0.0))
        _, self.bogen, self.zusatz_q, self.zusatz_z, d, art, self.frei = best
        self.L = L
        self.mass = {"art": art, "sehne": d, "theta": self.bogen.theta,
                     "sagitta": self.bogen.sagitta / self.bogen.sehne}
        return self.bogen

    def _bewerten(self, b, tinte, aus, gesetzt, L, d, f0, f1, vorgaenger):
        P = b.abtasten(24)
        kopf = np.array(kopf_polygon(b, L, self.elektronen == 1, self.breite))
        alle = np.vstack([P, kopf])
        # Kreuzen ist immer falsch, auch an der eigenen Quellbindung und am
        # eigenen Zielglyph. Der Abstandstest darunter nimmt beide aus, weil dort
        # die engeren Ankerregeln U4 und Z1 gelten, die kleinere Abstaende
        # verlangen als der Mindestabstand zu fremder Tinte. Frueher stand hier
        # statt des Schnitttests eine Abstandsheuristik auf der Bogenmitte; ein
        # Schnitt dicht am Schwanz fiel dadurch hindurch, und fuenf Tafeln
        # lieferten Pfeile, die sichtbar durch eine Bindung liefen.
        # Der Schaft muss sichtbar bleiben. Sonst entartet der Pfeil zur blossen
        # Spitze, und man sieht nicht mehr, woher die Elektronen kommen.
        hl, hw = kopf_masse(L, self.breite, b.r)
        schaft = abs(b.spanne) * b.r - hl * KOPF_SCHAFT
        if schaft < 0.85 * hl:
            return None, 0.0, "kein Platz fuer den Schaft neben dem Kopf"
        zug = np.vstack([P, kopf, kopf[:1]])
        if tinte.kreuzt(zug):
            return None, 0.0, "kreuzt eine Bindung oder ein Atomsymbol"
        frei = tinte.abstand(alle, aus)
        if frei < RAND_FREMD * L:
            return None, frei, "zu nah an fremder Tinte"
        for vb in gesetzt:
            strecken = _als_strecken(vb)
            if _kreuzt_strecken(zug, strecken):
                return None, 0.0, "kreuzt einen anderen Pfeil"
            nah = float(_pt_seg(alle, strecken).min())
            if nah < RAND_PFEIL * L:
                return None, min(frei, nah), "zu nah an einem anderen Pfeil"
            frei = min(frei, nah)
        wert = abs(b.theta - getattr(self, "_soll", WINKEL_SOLL)) / 9.0
        wert += max(0.0, RAND_SOLL * L - frei) / (0.10 * L)
        # Enge Boegen meiden: dort deckt der Schaft die innere Barbe zu.
        wert += max(0.0, kopf_eng(hl, hw, b.r, self.breite)) * 3.0
        if d < f0:
            wert += (f0 - d) * 5.0
        if d > f1:
            wert += (d - f1) * 5.0
        # Zeigt der Kopf auf sein Ziel? Die Bewertung kannte die Kopfrichtung
        # nicht, und bei sonst gleichwertigen Lagen waehlte der Solver ebenso
        # gern die Seite, auf der der Kopf am Ziel vorbeizeigt. Der Leser sieht
        # aber genau das: wohin die Spitze weist. Beim Rueckhaken weicht die
        # Tangente konstruktionsbedingt um bis zu theta/2 ab, dort wird milder
        # gewichtet.
        ziel = self._zielort()
        if ziel is not None:
            ux, uy = b.tangente(1.0)
            sp = b.punkt(1.0)
            zx, zy = _e(ziel[0] - sp[0], ziel[1] - sp[1])
            ab = math.degrees(math.acos(max(-1.0, min(1.0, ux * zx + uy * zy))))
            wert += (ab / 30.0) ** 2 * (0.5 if self._letzte_art == "zurueck" else 1.5)
        if vorgaenger is not None and vorgaenger.bogen is not None:
            v = vorgaenger.bogen.punkt(1.0)
            k = math.hypot(v[0] - b.p0[0], v[1] - b.p0[1]) / L
            wert += abs(k - KETTE_SOLL) * 2.2
        return wert, frei, None

    def _zielort(self):
        """Der Ort, auf den die Spitze zeigen soll: Atomzentrum bzw. Bindungsmitte."""
        z = self.ziel
        if isinstance(z, Bindung):
            (ax, ay), (bx, by) = z.m.atom(z.i), z.m.atom(z.j)
            return ((ax + bx) / 2.0, (ay + by) / 2.0)
        if isinstance(z, (Atom, Paar, Elektron)):
            return z.m.atom(z.idx)
        if isinstance(z, Fest):
            return (z.x, z.y)
        return None

    # ------------------------------------------------------------------ Ausgabe
    def svg(self, L, farbe, breite):
        b = self.bogen
        hl, _ = kopf_masse(L, breite, b.r)
        # Der Schaft endet genau an der Kerbe des Kopfes; seine runde Endkappe
        # fuellt sie aus. Endete er frueher, klaffte eine Luecke, endete er
        # spaeter, stuende er ueber die Barben hinaus.
        bis = b.zurueck(hl * KOPF_SCHAFT)
        sd = "" if not self.strich else " stroke-dasharray='%s'" % self.strich
        pts = " ".join("%.1f,%.1f" % p for p in
                       kopf_polygon(b, L, self.elektronen == 1, breite))
        return ["<path d='%s' fill='none' stroke='%s' stroke-width='%.2f' "
                "stroke-linecap='round'%s/>" % (b.pfad(bis), farbe, breite, sd),
                "<polygon points='%s' fill='%s'/>" % (pts, farbe)]


class Fehler(Exception):
    def __init__(self, schub, text):
        self.schub = schub
        q = _zeige(schub.quelle.herkunft())
        z = _zeige(schub.ziel.herkunft())
        Exception.__init__(self, "Pfeil %s -> %s: %s" % (q, z, text))


def _zeige(a):
    art, name, idx = a
    if idx is None:
        return "%s[%s]" % (art, name)
    return "%s.%s%s" % (name, art, ("(%s)" % (idx,)) if not isinstance(idx, tuple)
                        else str(idx))


def _mitte(m, anker):
    if m is not None and hasattr(m, "koord") and m.koord:
        return (sum(p[0] for p in m.koord) / len(m.koord),
                sum(p[1] for p in m.koord) / len(m.koord))
    if isinstance(anker, Fest):
        return (anker.x, anker.y)
    return (0.0, 0.0)


def _schwer(kand):
    return (sum(k[0] for k in kand) / len(kand),
            sum(k[1] for k in kand) / len(kand))


def _als_strecken(b):
    P = b.abtasten(20)
    return np.hstack([P[:-1], P[1:]])
