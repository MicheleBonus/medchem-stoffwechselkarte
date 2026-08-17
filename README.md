# Stoffwechselkarte der Signalmoleküle

Nachhilfeunterlage in Pharmazeutischer und Medizinischer Chemie für das
2. Staatsexamen Pharmazie. Sie ordnet die körpereigenen Signalstoffe nach ihrer
biosynthetischen Herkunft statt nach Organsystemen und verzeichnet an jedem
Syntheseschritt Enzym, Cofaktor, Regulation und die dort angreifenden Arzneistoffe.

**Website:** https://michelebonus.github.io/medchem-stoffwechselkarte/

## Inhalt

| Seite | Was darin steht |
|---|---|
| `index.html` | Einstieg, drei Wege in die Unterlage |
| `fahrplan.html` | Lernfahrplan: vier Blöcke, 26 Pflichtpositionen, zwölf Prüfergespräche, zwei Zeitpläne |
| `teil0.html` … `teil9.html` | Die Stoffwechselwege, von der C₂-Einheit bis zu den Redoxsystemen |
| `mechanismen.html` | Übersicht der siebzehn Mechanismus-Tafeln |
| `m01.html` … `m17.html` | Je eine Tafel, mit Elektronenpfeilen ausgeführt |

Quellen: Steinhilber/Schubert-Zsilavecz/Roth, *Medizinische Chemie*;
Müller/Prinz/Lehr, *Pharmazeutische und Medizinische Chemie*;
Berg/Tymoczko/Stryer, *Biochemie*.

## Aufbau des Projekts

Die HTML-Dateien in `docs/` werden **erzeugt und nicht von Hand bearbeitet.**
Wer eine Seite ändern will, ändert die Quelle in `build/` und baut neu.

```
build/
  site.py              baut docs/ aus allen Quellen; prüft Anker, Tags, Platzhalter
  shot_site.py         rendert alle Seiten headless und prüft Layout und Verweise
  gen_structures.py    SMILES -> structures.json (rund 300 Strukturformeln)
  mech.py              Zeichensprache für Mechanismus-Tafeln
  mech_kerne.py        Leitgerüste: feste Referenzlage wiederkehrender Molekülkerne
  mech_schub.py        Elektronenpfeile: Anker aus der Chemie, Geometrie aus dem Solver
  mech_regeln.py       Regelkatalog für Elektronenpfeile und die Prüfung dagegen
  tafel_m01.py … m17   je eine Tafel -> tafeln/mNN.svg
  vorschau.py          eine Tafel einzeln ansehen und prüfen
  vorschau_reihe.py    eine Gruppe von Strukturformeln nebeneinander ansehen
  src/                 Teil 0 bis 9 und die Rahmentexte der Tafeln
  src_plan/            der Lernfahrplan
  geruest/             Stylesheet, Navigation, Startseite, Themenumschalter
docs/                  die fertige Website (GitHub Pages liest hier)
```

## Bauen

Voraussetzungen: Python 3.12, `rdkit`, `playwright` (mit `playwright install chromium`).

```sh
cd build
python gen_structures.py       # nur nötig, wenn sich eine Strukturformel ändert
python tafel_m01.py            # nur nötig, wenn sich eine Tafel ändert
python site.py                 # baut docs/
python shot_site.py            # prüft alle Seiten in hell und dunkel
```

`site.py` bricht ab, wenn eine Struktur oder Tafel fehlt, ein Anker ins Leere
zeigt, eine ID doppelt vergeben ist, ein Platzhalter stehen bleibt oder ein
HTML-Tag im inline-SVG steht. `shot_site.py` bricht ab, wenn eine Seite waagerecht
überläuft, ein SVG keine Höhe hat, Beschriftungen einander überdecken, eine Linie
durch eine Beschriftung läuft oder ein Verweis auf eine fehlende Datei oder einen
fehlenden Anker zeigt.

### Verweise zwischen den Seiten

In den Quellen steht jeder interne Verweis als `href="#anker"`, unabhängig davon,
auf welcher Seite der Anker liegt. `site.py` sammelt alle Anker ein, ermittelt die
Zielseite und schreibt den Verweis um. Wer Inhalte zwischen Dateien verschiebt,
muss deshalb nichts an den Verweisen ändern.

### Elektronenpfeile

Ein Pfeil wird als Chemie angemeldet, nicht als Geometrie:

```python
t.schub(Paar(subst, 0),          Atom(intern, 12))       # neue σ-Bindung
t.schub(Bindung(intern, 12, 13), Paar(intern, 13))       # π-Paar wird freies Paar
```

Kopfform, Farbe, Bauchseite, Öffnungswinkel und die genaue Ankerlage folgen daraus.
Ein Solver sucht unter rund tausend Kandidaten den Bogen, der keine Bindung, kein
Atomsymbol und keinen anderen Pfeil schneidet; als Hindernisse dienen die exakten
Bindungsstrecken und Glyphenrechtecke, die RDKit in seinem SVG mit annotiert.
Findet er keinen, bricht der Bau ab und nennt den Grund — das ist dann ein
Layoutfehler und keiner, den man wegkrümmt. `mech_regeln.py` misst jeden fertigen
Pfeil gegen einen Katalog aus Levy, *Arrow Pushing in Organic Chemistry*, und
Brückner, *Reaktionsmechanismen*, und druckt die Maße beim Bauen aus.

Wiederkehrende Molekülkerne bekommen in `mech_kerne.py` eine ein für alle Mal
festgelegte Lage (`t.mol(..., kern="b6")`). Damit steht derselbe Kern in jeder
Stufe einer Tafel gleich, gedreht und gespiegelt.

### Strukturformeln

Alle Strukturformeln entstehen aus SMILES über RDKit; Stereodeskriptoren werden
nach CIP automatisch annotiert. Verwandte Strukturen, die nebeneinanderstehen,
gehören in eine **Reihe** (`REIHEN` in `gen_structures.py`): sie teilen dann Lage
und Bindungslänge, damit der Unterschied zwischen ihnen ins Auge fällt und nicht
die verschiedene Ausrichtung. Farbige Hinterlegungen (`SCHMUCK`) zeigen, welcher
Molekülteil in einem Schritt hinzukommt, welcher abgeht und wo die Reaktion
stattfindet.

## Lizenz

Der Text und die Grafiken stehen unter [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de).
Die Skripte in `build/` stehen unter der MIT-Lizenz. Die Lehrbücher, auf die sich
die Unterlage stützt, sind nicht Teil dieses Repositorys.
