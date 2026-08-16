// Umschalter fuer die Darstellung: automatisch -> hell -> dunkel -> automatisch.
// Die Wahl liegt im localStorage; das Inline-Skript im <head> setzt sie vor dem
// ersten Anstrich, damit die Seite nicht kurz in der falschen Farbe aufblitzt.
(function () {
  var stufen = [
    ["auto", "Darstellung: automatisch"],
    ["light", "Darstellung: hell"],
    ["dark", "Darstellung: dunkel"]
  ];
  var wurzel = document.documentElement;
  var knopf = document.querySelector("[data-thema]");
  if (!knopf) return;

  function lies() {
    try {
      return localStorage.getItem("thema") || "auto";
    } catch (e) {
      return "auto";
    }
  }

  function zeige(wert) {
    for (var i = 0; i < stufen.length; i++) {
      if (stufen[i][0] === wert) knopf.textContent = stufen[i][1];
    }
  }

  function setze(wert) {
    if (wert === "auto") {
      wurzel.removeAttribute("data-theme");
      try { localStorage.removeItem("thema"); } catch (e) {}
    } else {
      wurzel.setAttribute("data-theme", wert);
      try { localStorage.setItem("thema", wert); } catch (e) {}
    }
    zeige(wert);
  }

  zeige(lies());
  knopf.addEventListener("click", function () {
    var jetzt = lies();
    for (var i = 0; i < stufen.length; i++) {
      if (stufen[i][0] === jetzt) {
        setze(stufen[(i + 1) % stufen.length][0]);
        return;
      }
    }
    setze("light");
  });
})();

// Auf schmalen Schirmen faengt das Inhaltsverzeichnis zugeklappt an.
(function () {
  var knopf = document.querySelector(".railknopf");
  var inhalt = document.getElementById("railinhalt");
  if (!knopf || !inhalt) return;
  knopf.hidden = false;
  var schmal = window.matchMedia("(max-width: 900px)");

  function stelle(zu) {
    inhalt.classList.toggle("zu", zu);
    knopf.setAttribute("aria-expanded", zu ? "false" : "true");
  }

  stelle(schmal.matches);
  schmal.addEventListener("change", function (e) { stelle(e.matches); });
  knopf.addEventListener("click", function () {
    stelle(!inhalt.classList.contains("zu"));
  });
})();
