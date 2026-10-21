/* Publications index — client-side filter, no dependencies */
(function () {
  "use strict";

  var input = document.getElementById("pubSearch");
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".filter-btn"));
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-work-card]"));
  var counter = document.getElementById("pubCount");
  var empty = document.getElementById("pubEmpty");
  var activeType = "all";

  function normalise(s) {
    return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  function apply() {
    var q = normalise(input ? input.value : "");
    var shown = 0;

    cards.forEach(function (card) {
      var haystack = normalise(card.getAttribute("data-search"));
      var typeOk = activeType === "all" || card.getAttribute("data-type") === activeType;
      var queryOk = !q || haystack.indexOf(q) !== -1;
      var visible = typeOk && queryOk;
      card.style.display = visible ? "" : "none";
      if (visible) shown++;
    });

    if (counter) {
      counter.textContent = shown + (shown === 1 ? " work" : " works") +
        (activeType === "all" ? "" : " in this category");
    }
    if (empty) empty.style.display = shown ? "none" : "";
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) { b.classList.remove("active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      activeType = btn.getAttribute("data-filter");
      apply();
    });
  });

  if (input) {
    input.addEventListener("input", apply);
    input.addEventListener("search", apply);
  }

  /* Deep link: /publications/?type=thesis */
  var params = new URLSearchParams(window.location.search);
  var wanted = params.get("type");
  if (wanted) {
    var match = buttons.filter(function (b) { return b.getAttribute("data-filter") === wanted; })[0];
    if (match) match.click();
  }

  apply();
})();
