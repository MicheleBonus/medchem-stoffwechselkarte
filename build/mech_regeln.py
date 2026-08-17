# -*- coding: utf-8 -*-
"""
Regelkatalog fuer Elektronenpfeile und die Pruefung dagegen.

Quellen
-------
L = Daniel E. Levy, "Arrow Pushing in Organic Chemistry", Wiley 2008.
    Die Masse stammen aus 284 automatisch vermessenen Pfeilen der Schemata sowie
    aus Einzelmessungen an Schema 1.7 bis 1.10, 2.4, 4.1, 4.5, 7.2, 7.12 und 7.16.
B = Reinhard Brueckner, "Reaktionsmechanismen" (reaktionsmechanismen.pdf).

Wo die beiden Zeichenschulen auseinandergehen, steht unten die getroffene
Entscheidung samt Begruendung. Es geht dabei nie um Sachfragen, sondern um
Satzgewohnheiten - amerikanischer ChemDraw-Satz gegen deutschen Springer-Satz.

Katalog
-------
Ursprung
  U1  Der Schwanz liegt nie auf einem Bindungsstrich und nie auf einem Atom-
      symbol; Freiraum zur naechsten fremden Tinte mindestens 0,25 L.        [L,B]
  U2  Ist am Startatom ein freies Paar gezeichnet, setzt der Schwanz am Paar
      an, nicht am Atomzentrum: Abstand zum Paar unter 0,3 L.                [L,B]
  U4  Kommen die Elektronen aus einer Bindung, sitzt der Schwanz seitlich
      daneben, Lot 0,20-0,30 L. Laengslage: L will 0,2-0,6 in Richtung des
      abgebenden Atoms, B will genau die Mitte. Entschieden: |t-0,5| <= 0,10,
      der einzige Bereich, den beide zulassen.                              [L!=B]
  U5  Bei einer Doppelbindung sitzt der Schwanz neben der inneren Linie, auf
      der dem Partner zugewandten Seite.                                     [L,B]
  U8  Nie ein Schwanz am Wasserstoffsymbol. Ein Protonentransfer sind zwei
      Pfeile.                                                                [L,B]

Ziel
  Z1  Neue Sigma-Bindung: die Spitze endet vor dem Atom, ausserhalb des
      Glyphenrechtecks, 0,25-0,50 L vom Atomzentrum.                         [L,B]
  Z2  Neue pi-Bindung: die Spitze endet neben der Mitte der Bindung, die zur
      Doppelbindung wird; |t-0,5| <= 0,15, Lot 0,20-0,30 L.                  [L,B]
  Z3  Heterolyse mit Paar auf ein Atom: L schwingt weit um das Atom herum,
      B setzt die Spitze wie bei Z1 daneben. Entschieden: Z1-Fenster, weil
      der weite Haken bei 21 px Bindungslaenge unlesbar wird. Der bisherige
      Bestand (16-32 px = 0,76-1,52 L) verletzte beide Buecher.             [L!=B]
  Z5  Die Spitze beruehrt weder Schrift noch Bindung; Freiraum mindestens
      0,25 L zu fremder Tinte, 0,11 L zum eigenen Zielglyph.                 [L,B]

Form
  F1  Kreisbogen konstanter Kruemmung, Oeffnungswinkel 90-115 Grad.       [L, B impl.]
  F2  Sagitta/Sehne: L misst 0,20-0,28, B gibt 0,25-0,40 an. Entschieden:
      0,20-0,30, mit 0,233 (100 Grad) als Sollwert.                         [L!=B]
  F3  Kein Wendepunkt. L findet in 284 Pfeilen keine S-Kurve.               [L!=B]
  F4  Sehne: innermolekular 0,75-1,20 L, Ring- und Resonanzpfeil 0,60-0,90 L,
      zwischen zwei Teilchen 1,50-4,00 L.                                    [L,B]
  F5  Schaftbreite gleich der Bindungsstrichbreite, plus/minus 15 Prozent.
      Der Pfeil unterscheidet sich vom Geruest durch Farbe und Kruemmung.    [L,B]
  F7  Farbe: L schwarz wie das Geruest, B eine einzige Signalfarbe fuer alle
      Schiebepfeile. Entschieden: eine Signalfarbe; Paar und Einzelelektron
      unterscheiden sich allein durch die Kopfform, wie in beiden Buechern.  [L!=B]

Kopf
  K1  Voller Kopf gleich Elektronenpaar, halber Kopf gleich einzelnes
      Elektron. Bei einer *Homolyse* treten Fischhaken paarweise auf; eine
      Abstraktion braucht dagegen drei (zwei bilden die neue Bindung, einer
      bleibt am Radikal zurueck). Eine ungerade Gesamtzahl ist deshalb nur
      ein Hinweis, kein Fehler.                                              [L,B]
  K2  Die Barbe des Fischhakens sitzt auf der konvexen Seite des Bogens.     [L]
  K3  Kopflaenge: L misst ueber 284 Pfeile 0,20-0,30 L, B setzt ein festes
      Symbol von 0,53 L. Entschieden: 0,32 L, siehe K4.                     [L!=B]
  K4  Kopfbreite. Die Statistik nennt Breite/Laenge 0,43-0,58, gemessen an
      grossen Pfeilen. An Schema 1.7 (Cope) nachgemessen, wo die Pfeile so
      kurz sind wie unsere: der Kopf ist dort 2,2-2,8 Strichbreiten breit und
      damit fast so breit wie lang. Massgeblich ist deshalb das Verhaeltnis
      zur *Strichbreite*, nicht zur Kopflaenge. Ein Kopf von nur 1,9
      Strichbreiten verschwindet neben dem eigenen Schaft; weil der Schaft
      gekruemmt ist, verdeckt er dabei die innere Barbe, und der Vollpfeil
      sieht aus wie ein Fischhaken. Genau das war der erste Befund am
      fertigen Bild.                                                      [eigene M.]
  K5  Die Kopfachse ist die Tangente am Endpunkt.                            [L]
  K6  Die Spitze liegt genau auf dem Pfadende, kein refX-Ueberstand.      [Ableitung]

Verkettung
  V1  Mehrere Pfeile eines Schrittes haengen Kopf an Schwanz, beruehren sich
      aber nicht: 0,10-0,60 L zwischen Spitze und naechstem Schwanz.         [L,B]

Kollision
  C1  Nulltoleranz: der Pfad einschliesslich Kopf schneidet keine Bindung und
      kein Glyphenrechteck.                                                  [L,B]
  C4  Ist C1 fuer beide Bauchrichtungen unerfuellbar, ist das ein Layout-
      fehler und kein Pfeilfehler. Der Bau bricht ab, statt den Pfeil zu
      verbiegen.                                                        [Ableitung]

Zeichensprache
  N1  Freie Paare werden nur dort gezeichnet, wo sie am Mechanismus
      teilnehmen. Jedes gezeichnete Paar ist Start eines Pfeils.             [L,B]
  N2  Punktpaare, keine Valenzstriche.                                      [L!=B]
  N6  Innerhalb einer Tafel ist die Bindungslaenge konstant. Ein bewusst
      vergroesserter Ausschnitt gehoert in die Bildunterschrift.             [L,B]

Nicht hier geprueft
  V6  Elektronenbilanz gegen die Produktstruktur. Sie verlangt Atommarken in
      jedem SMILES und ist als eigener Schritt vorgesehen.
"""
import math

import numpy as np

import mech_schub as S

# Beim Kreisbogen ist Sagitta/Sehne = tan(theta/4)/2. Gepflegt wird deshalb nur
# das Winkelfenster; das Sagittafenster folgt daraus. F2 verlangt 0,20-0,30, das
# sind 87-123 Grad. Ein zusammengefasster Pfeil ("weit") muss aussen um das
# Geruest greifen und darf weiter ausholen; er ist als solcher gestrichelt
# gezeichnet und in der Bildunterschrift erklaert.
THETA = {"*": (87.0, 123.0)}


def sagitta_fenster(art):
    lo, hi = THETA.get(art, THETA["*"])
    return (math.tan(math.radians(lo) / 4.0) / 2.0,
            math.tan(math.radians(hi) / 4.0) / 2.0)


FENSTER = {
    "kopf_laenge": (0.20, 0.34),
    "kopf_breite": (0.55, 0.95),
    "kopf_strich": (2.4, 3.6),
    "frei": (0.25, None),
    "paar_schwanz": (None, 0.30),
    # gemessen gegen die gezeichnete Linie, siehe _bindungslage
    "bindung_lot": (0.17, 0.34),
    "bindung_t_quelle": (None, 0.10),
    "bindung_t_ziel": (None, 0.15),
    # Z1 nennt 0,25-0,50 L vom Atomzentrum. Das ist an Skelettformeln gemessen,
    # wo das Atom hoechstens ein schmales Symbol traegt. Bei "NH+" oder "Fe(III)"
    # reicht der Glyph allein schon weiter, und die Spitze muss davor bleiben.
    # Massgeblich ist deshalb der Ueberstand ueber den Glyphenrand; der Abstand
    # zum Zentrum wird nur nach unten begrenzt.
    "atom_ziel": (0.25, None),
    "atom_ueberstand": (0.09, 0.46),
    # V1 nennt 0,10-0,60 L. Das ist am Regelfall gemessen, wo die Spitze genau
    # dort landet, wo der naechste Schwanz ansetzt. Treffen sich zwei Pfeile
    # dagegen an einem gemeinsamen *Atom* - der eine endet an der einen Bindung
    # dieses Atoms, der andere beginnt an der anderen -, dann liegen ihre Anker
    # konstruktionsbedingt gut eine Bindungslaenge auseinander, ohne dass der
    # Zusammenhang verlorenginge. Beide Faelle bekommen deshalb ein eigenes
    # Fehlerfenster; das Buchfenster steht daneben und gibt nur einen Hinweis.
    "kette": (0.10, 0.95),
    "kette_atom": (0.10, 1.45),
    "kette_soll": (0.10, 0.60),
}


def _gemeinsame_atome(a, b):
    """Atome, die der Zielanker von a und der Quellanker von b teilen."""
    def atome(anker):
        if isinstance(anker, S.Bindung):
            return {(anker.m.name, anker.i), (anker.m.name, anker.j)}
        if isinstance(anker, (S.Atom, S.Paar, S.Elektron)):
            return {(anker.m.name, anker.idx)}
        return set()
    return atome(a.ziel) & atome(b.quelle)


def _im(wert, fenster):
    lo, hi = fenster
    if lo is not None and wert < lo - 1e-9:
        return False
    if hi is not None and wert > hi + 1e-9:
        return False
    return True


def _fmt(fenster):
    lo, hi = fenster
    if lo is None:
        return "< %.2f" % hi
    if hi is None:
        return "> %.2f" % lo
    return "%.2f-%.2f" % (lo, hi)


class Befund(object):
    def __init__(self):
        self.fehler = []
        self.hinweise = []
        self.zeilen = []


def pruefe_schuebe(tafel):
    """Jeden geloesten Schub gegen den Katalog messen.

    Gibt (Fehler, Hinweise, Berichtszeilen) zurueck. Fehler brechen den Bau ab;
    Hinweise sind Abweichungen innerhalb der weicheren Grenzen des Solvers.
    """
    b = Befund()
    if not tafel.schuebe:
        return b

    laengen = sorted({round(m.bindung_px, 2) for m in tafel.mole})
    if len(laengen) > 1:
        b.hinweise.append(
            "N6: die Tafel mischt %s px Bindungslaenge. Das ist zulaessig, wenn "
            "ein Ausschnitt vergroessert ist und die Unterschrift es sagt."
            % ", ".join("%g" % x for x in laengen))

    for L, strich in sorted({(s.L, round(s.breite, 2)) for s in tafel.schuebe}):
        hl, hw = S.kopf_masse(L, strich)
        if not _im(hl / L, FENSTER["kopf_laenge"]):
            b.fehler.append("K3: Kopflaenge %.2f L ausserhalb %s"
                            % (hl / L, _fmt(FENSTER["kopf_laenge"])))
        if not _im(hw / hl, FENSTER["kopf_breite"]):
            b.fehler.append("K4: Kopfbreite/Kopflaenge %.2f ausserhalb %s"
                            % (hw / hl, _fmt(FENSTER["kopf_breite"])))
        if not _im(hw / strich, FENSTER["kopf_strich"]):
            b.fehler.append("K4: Kopfbreite %.2f Strichbreiten, gefordert %s. "
                            "Darunter ist der Vollpfeil nicht mehr von einem "
                            "Fischhaken zu unterscheiden."
                            % (hw / strich, _fmt(FENSTER["kopf_strich"])))
        weit = max(S.kopf_masse(s.L, s.breite, s.bogen.r)[1]
                   for s in tafel.schuebe if s.L == L)
        for i, sch in enumerate(tafel.schuebe, 1):
            if sch.L != L or sch.elektronen == 1:
                continue
            hl2, hw2 = S.kopf_masse(sch.L, sch.breite, sch.bogen.r)
            zu = S.kopf_eng(hl2, hw2, sch.bogen.r, sch.breite)
            if zu > 0.0:
                b.fehler.append(
                    "Pfeil %d K4: der Bogen ist so eng (r = %.1f px), dass der "
                    "Schaft die innere Barbe um %.1f px ueberdeckt. Der "
                    "Vollpfeil sieht damit aus wie ein Fischhaken."
                    % (i, sch.bogen.r, zu))
        b.zeilen.append("  Kopf bei L=%.0f px: %.1f px lang (%.2f L), %.1f bis "
                        "%.1f px breit (%.2f bis %.2f Strichbreiten), Schaft %.2f px"
                        % (L, hl, hl / L, hw, weit, hw / strich, weit / strich,
                           strich))

    b.zeilen.append("  Nr Elek Art    Sehne/L  theta  Sag/Sehne  Frei/L  Anker")
    haken = 0
    for i, sch in enumerate(tafel.schuebe, 1):
        bo = sch.bogen
        L = sch.L
        frei = sch.frei / L
        sag = bo.sagitta / bo.sehne
        art = sch.mass["art"]
        b.zeilen.append(
            "  %2d %4d %-6s %7.2f %6.0f %10.3f %7.2f  %s -> %s"
            % (i, sch.elektronen, art, bo.sehne / L, bo.theta, sag, frei,
               S._zeige(sch.quelle.herkunft()), S._zeige(sch.ziel.herkunft())))

        wo = "Pfeil %d (%s -> %s)" % (i, S._zeige(sch.quelle.herkunft()),
                                      S._zeige(sch.ziel.herkunft()))
        if sch.elektronen == 1:
            haken += 1
        if not _im(frei, FENSTER["frei"]):
            b.fehler.append("%s C1: Freiraum %.2f L, gefordert %s"
                            % (wo, frei, _fmt(FENSTER["frei"])))
        if not _im(sag, sagitta_fenster(art)):
            b.fehler.append("%s F2: Sagitta/Sehne %.3f, gefordert %s"
                            % (wo, sag, _fmt(sagitta_fenster(art))))
        if not _im(bo.theta, THETA.get(art, THETA["*"])):
            b.fehler.append("%s F1: Oeffnungswinkel %.0f Grad, gefordert %s"
                            % (wo, bo.theta, _fmt(THETA.get(art, THETA["*"]))))
        buch = S.SEHNE[art][0]
        if not _im(bo.sehne / L, buch):
            b.hinweise.append("%s F4: Sehne %.2f L, Buchfenster %s fuer '%s'"
                              % (wo, bo.sehne / L, _fmt(buch), art))

        _anker_regeln(b, wo, sch, L)

    if haken % 2:
        b.hinweise.append(
            "K1: %d Fischhaken, also eine ungerade Zahl. Bei einer Homolyse "
            "gehoeren sie paarweise; eine Abstraktion ist dagegen mit drei "
            "Haken richtig (zwei bilden die neue Bindung, einer bleibt am "
            "Radikal). Zaehlen Sie nach." % haken)

    for i in range(1, len(tafel.schuebe)):
        a, c = tafel.schuebe[i - 1], tafel.schuebe[i]
        if c.kette is None or c.kette != a.kette:
            continue
        d = math.hypot(a.bogen.punkt(1.0)[0] - c.bogen.p0[0],
                       a.bogen.punkt(1.0)[1] - c.bogen.p0[1]) / c.L
        streng = FENSTER["kette_atom" if _gemeinsame_atome(a, c) else "kette"]
        if not _im(d, streng):
            b.fehler.append("V1: Pfeil %d endet %.2f L vom Schwanz des Pfeils %d, "
                            "gefordert %s" % (i, d, i + 1, _fmt(streng)))
        elif not _im(d, FENSTER["kette_soll"]):
            b.hinweise.append("V1: Pfeil %d endet %.2f L vom Schwanz des Pfeils "
                              "%d; das Buchfenster ist %s."
                              % (i, d, i + 1, _fmt(FENSTER["kette_soll"])))
    return b


def _anker_regeln(b, wo, sch, L):
    q, z = sch.quelle, sch.ziel
    p0, p1 = sch.bogen.p0, sch.bogen.punkt(1.0)

    if isinstance(q, S.Paar) and sch.zusatz_q and "paar" in sch.zusatz_q:
        px, py, _ = sch.zusatz_q["paar"]
        d = math.hypot(p0[0] - px, p0[1] - py) / L
        if not _im(d, FENSTER["paar_schwanz"]):
            b.fehler.append("%s U2: Schwanz %.2f L vom Paar, gefordert %s"
                            % (wo, d, _fmt(FENSTER["paar_schwanz"])))
    if isinstance(q, S.Bindung):
        t, lot = _bindungslage(q, p0)
        if not _im(lot / L, FENSTER["bindung_lot"]):
            b.fehler.append("%s U4: Schwanz %.2f L neben der Bindung, gefordert %s"
                            % (wo, lot / L, _fmt(FENSTER["bindung_lot"])))
        if not _im(abs(t - 0.5), FENSTER["bindung_t_quelle"]):
            b.fehler.append("%s U4: Schwanz bei t=%.2f der Bindung, gefordert "
                            "|t-0,5| %s" % (wo, t, _fmt(FENSTER["bindung_t_quelle"])))
    if isinstance(q, S.Atom):
        h = q.m.mol.GetAtomWithIdx(q.idx)
        if h.GetSymbol() == "H":
            b.fehler.append("%s U8: kein Pfeilschwanz am Wasserstoff." % wo)

    if isinstance(z, (S.Atom, S.Paar, S.Elektron)):
        cx, cy = z.m.atom(z.idx)
        d = math.hypot(p1[0] - cx, p1[1] - cy)
        regel = "Z1" if isinstance(z, S.Atom) else "Z3"
        if not _im(d / L, FENSTER["atom_ziel"]):
            b.fehler.append("%s %s: Spitze %.2f L vom Atomzentrum, gefordert %s"
                            % (wo, regel, d / L, _fmt(FENSTER["atom_ziel"])))
        grad = math.degrees(math.atan2(p1[1] - cy, p1[0] - cx))
        ueber = (d - S._glyph_reichweite(z.m, z.idx, grad)) / L
        if not _im(ueber, FENSTER["atom_ueberstand"]):
            b.fehler.append("%s %s: Spitze %.2f L vor dem Atomsymbol, gefordert %s"
                            % (wo, regel, ueber, _fmt(FENSTER["atom_ueberstand"])))
        box = z.m.glyphen.get(z.idx)
        if box and box[0] <= p1[0] <= box[2] and box[1] <= p1[1] <= box[3]:
            b.fehler.append("%s Z5: die Spitze steht im Atomsymbol." % wo)
    if isinstance(z, S.Bindung):
        t, lot = _bindungslage(z, p1)
        if not _im(lot / L, FENSTER["bindung_lot"]):
            b.fehler.append("%s Z2: Spitze %.2f L neben der Bindung, gefordert %s"
                            % (wo, lot / L, _fmt(FENSTER["bindung_lot"])))
        if not _im(abs(t - 0.5), FENSTER["bindung_t_ziel"]):
            b.fehler.append("%s Z2: Spitze bei t=%.2f der Bindung, gefordert "
                            "|t-0,5| %s" % (wo, t, _fmt(FENSTER["bindung_t_ziel"])))


def _bindungslage(anker, p):
    """Laengslage t und Lotabstand eines Ankerpunktes an seiner Bindung.

    Der Lotabstand wird gegen die *gezeichnete* Linie gemessen, nicht gegen die
    Verbindungslinie der Atommittelpunkte. Bei einer Doppelbindung liegt die
    zweite Linie einseitig versetzt; U5 verlangt den Schwanz neben der inneren
    Linie, und das ist nur an der Tinte messbar.
    """
    (ax, ay), (bx, by) = anker.m.atom(anker.i), anker.m.atom(anker.j)
    dx, dy = bx - ax, by - ay
    laenge = math.hypot(dx, dy) or 1.0
    ux, uy = dx / laenge, dy / laenge
    t = ((p[0] - ax) * ux + (p[1] - ay) * uy) / laenge
    b = anker.m.mol.GetBondBetweenAtoms(anker.i, anker.j)
    eigen = [s[:4] for s in anker.m.strecken if b is not None and s[4] == b.GetIdx()]
    if eigen:
        lot = float(S._pt_seg(np.array([[p[0], p[1]]]),
                              np.array(eigen, dtype=float)).min())
    else:
        lot = abs(-(p[0] - ax) * uy + (p[1] - ay) * ux)
    return t, lot
