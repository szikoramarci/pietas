/* Ajánlatoldal: a mérőszámok beúszása és a betöltés-verseny. JS nélkül is minden a végállapotában látszik. */
(function () {
  "use strict";
  var halk = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("aj-js");

  function figyel(elemek, fn) {
    if (!elemek.length) return;
    if (halk || !("IntersectionObserver" in window)) { elemek.forEach(fn); return; }
    var io = new IntersectionObserver(function (bejegyzesek) {
      bejegyzesek.forEach(function (b) { if (b.isIntersecting) { io.unobserve(b.target); fn(b.target); } });
    }, { threshold: 0.35 });
    elemek.forEach(function (e) { io.observe(e); });
  }

  // Csíkok és gyűrűk: beúszás, amikor láthatóvá válnak.
  figyel([].slice.call(document.querySelectorAll("[data-anim]")), function (e) {
    requestAnimationFrame(function () { e.classList.add("lathato"); });
  });

  // Betöltés-verseny: valós idejű lejátszás a mért értékekkel.
  var mp = function (x) { return x.toFixed(1).replace(".", ",") + " s"; };
  [].forEach.call(document.querySelectorAll("[data-verseny]"), function (v) {
    var telefonok = [
      { el: v.querySelector(".aj-telefon.regi"), cel: parseFloat(v.getAttribute("data-regi")) },
      { el: v.querySelector(".aj-telefon.uj"), cel: parseFloat(v.getAttribute("data-uj")) }
    ];
    var ujra = v.querySelector("[data-ujra]");
    if (halk) return;
    var kezd = 0, fut = false;

    function rajzol(most) {
      var t = (most - kezd) / 1000, mindKesz = true;
      telefonok.forEach(function (p) {
        var kesz = t >= p.cel;
        p.el.classList.toggle("kesz", kesz);
        p.el.querySelector(".aj-ora").textContent = mp(Math.min(t, p.cel));
        p.el.querySelector(".aj-toltes i").style.width = Math.min(t / p.cel, 1) * 100 + "%";
        if (!kesz) mindKesz = false;
      });
      if (mindKesz) { fut = false; ujra.hidden = false; return; }
      requestAnimationFrame(rajzol);
    }
    function indit() {
      if (fut) return;
      fut = true; ujra.hidden = true;
      v.classList.add("fut");
      telefonok.forEach(function (p) { p.el.classList.remove("kesz"); });
      requestAnimationFrame(function (most) { kezd = most; rajzol(most); });
    }
    // Indulás előtti állapot: üres kijelzők, 0,0 s.
    v.classList.add("fut");
    telefonok.forEach(function (p) {
      p.el.querySelector(".aj-ora").textContent = mp(0);
      p.el.querySelector(".aj-toltes i").style.width = "0%";
    });
    ujra.addEventListener("click", indit);
    figyel([v], indit);
  });
})();
