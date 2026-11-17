/* ÉRTÉKESÍTÉSI RÉTEG – időpontfoglaló ablak, docs/DEMO-RETEG.md. Élesítéskor törlendő.

   A demó egyetlen kapcsolatfelvételi lépése: bármely [data-foglalo] elemre kattintva megnyílik egy ablak,
   benne a webness.hu beágyazott időpontfoglalója (iframe). A látogató nem lép ki a demóból: az ablak a demón
   belül nyílik, a foglalóban nincs kifelé mutató link, és nem nyílik új lap.

   Beépítés (minden oldalon, a ki-keszitette.js mellé):
     <link rel="stylesheet" href="assets/foglalo.css">
     <script src="assets/foglalo.js" defer></script>
   Gomb bárhol:  <a class="…" href="#idopont" data-foglalo="ajanlat">Időpontot foglalok</a>
   (a data-foglalo értéke csak a mérésnek szól: honnan nyitották meg)
   Magától hozzáteszi: gombot a felső .bemutato-sav-ba (asztalon a sáv odatapad a lap tetejére), és mobilon
   (900 px alatt) a demó saját Hívás/Email sávja (.also-sav, .hivassav) helyett egy foglalósávot.

   Események: sikeres foglaláskor `webness-foglalva` (window, detail.idopont), és jelzés a VEGPONT-ra. */
(function () {
  "use strict";
  // ---- BEÁLLÍTÁSOK (demónként) -------------------------------------------------------------
  var DEMO_AZONOSITO = "temetkezes-miskolc-pietas";   // a sites/<azonosító> mappa neve; ezzel látszik a foglalásban (?u=)
  var CEGNEV = "Pietas Temetkezés";      // előtöltve a foglalóban. Az üzemeltető neve NEM kerülhet ide.
  var FOGLALO = "https://webness.hu/idopont/beagyazott";
  var VEGPONT = "/api/jelzes";
  // -------------------------------------------------------------------------------------------

  var ORIGIN = new URL(FOGLALO).origin;
  var ablak = null, iframe = null, nyitotta = "";

  function kuld(adat) {
    try {
      fetch(VEGPONT, {
        method: "POST", headers: { "Content-Type": "application/json" }, credentials: "same-origin", keepalive: true,
        body: JSON.stringify(Object.assign({}, adat, { oldal: location.pathname }))
      }).catch(function () {});
    } catch (e) { /* nem baj */ }
  }

  function forras() {
    var q = new URLSearchParams();
    if (DEMO_AZONOSITO && DEMO_AZONOSITO.charAt(0) !== "[") q.set("u", DEMO_AZONOSITO.toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 40));
    if (CEGNEV && CEGNEV.charAt(0) !== "[") q.set("ceg", CEGNEV);
    return FOGLALO + "?" + q.toString();
  }

  function felepit() {
    if (ablak) return;
    ablak = document.createElement("dialog");
    ablak.className = "fg-ablak";
    ablak.setAttribute("aria-label", "Időpontfoglalás");
    ablak.innerHTML =
      '<div class="fg-fej"><span class="fg-cim">Időpontfoglalás</span>' +
      '<button type="button" class="fg-x" aria-label="Bezárás">×</button></div>' +
      '<div class="fg-test"><p class="fg-tolt" aria-live="polite">Időpontok betöltése…</p></div>';
    iframe = document.createElement("iframe");
    iframe.title = "Időpontfoglalás – Szikora Marcell, webness.hu";
    iframe.src = forras();
    iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    iframe.addEventListener("load", function () { var t = ablak.querySelector(".fg-tolt"); if (t) t.remove(); });
    ablak.querySelector(".fg-test").appendChild(iframe);
    document.body.appendChild(ablak);
    ablak.querySelector(".fg-x").addEventListener("click", bezar);
    ablak.addEventListener("click", function (e) { if (e.target === ablak) bezar(); });
    ablak.addEventListener("close", function () { document.documentElement.classList.remove("fg-nyitva"); });
  }

  function megnyit(honnan) {
    felepit();
    nyitotta = honnan || "";
    // ha másik ablak (pl. „Ki készítette?”) van nyitva, az bezárul
    document.querySelectorAll("dialog[open]").forEach(function (d) { if (d !== ablak) d.close(); });
    document.documentElement.classList.add("fg-nyitva");
    if (ablak.showModal) ablak.showModal(); else ablak.setAttribute("open", "");
    ablak.querySelector(".fg-test").scrollTop = 0;
    kuld({ tipus: "foglalo", resz: nyitotta });
  }

  function bezar() { if (ablak && ablak.open) ablak.close(); }

  // Előtöltés: ha a látogató egy foglaló-gomb fölé visz vagy rákoppint, az iframe már töltődik.
  ["pointerover", "focusin", "touchstart"].forEach(function (ev) {
    document.addEventListener(ev, function (e) { if (e.target.closest && e.target.closest("[data-foglalo]")) felepit(); }, { passive: true });
  });
  document.addEventListener("click", function (e) {
    var g = e.target.closest && e.target.closest("[data-foglalo]");
    if (!g) return;
    e.preventDefault();
    megnyit(g.getAttribute("data-foglalo"));
  });

  // Üzenetek a beágyazott foglalótól: magasság, lépésváltás, sikeres foglalás.
  window.addEventListener("message", function (e) {
    if (e.origin !== ORIGIN || !iframe || e.source !== iframe.contentWindow) return;
    var m = e.data || {};
    if (m.forras !== "webness-idopont") return;
    if (m.magassag > 0) iframe.style.height = Math.min(Math.max(m.magassag, 300), 4000) + "px";
    if (m.tipus === "lepes") ablak.querySelector(".fg-test").scrollTop = 0;
    if (m.tipus === "foglalva") {
      kuld({ tipus: "foglalas", resz: nyitotta, idopont: String(m.idopont || "").slice(0, 60) });
      window.dispatchEvent(new CustomEvent("webness-foglalva", { detail: { idopont: m.idopont || "" } }));
    }
  });

  // Fejléc és mobil: a felső bemutató sávba „Időpontot foglalok” gomb (asztalon a sáv a lap tetejére tapad),
  // mobilon a demó saját Hívás/Email sávja helyett egy foglalósáv. A demó HTML-je érintetlen marad:
  // ezt csak a réteg teszi hozzá, élesítéskor a réteggel együtt eltűnik.
  function retegElemek() {
    document.documentElement.classList.add("fg-reteg");
    var sav = document.querySelector(".bemutato-sav");
    if (sav && !sav.querySelector(".fg-sav-gomb")) {
      var g = document.createElement("a");
      g.className = "fg-sav-gomb"; g.href = "#idopont"; g.setAttribute("data-foglalo", "fejlec");
      g.textContent = "Időpontot foglalok";
      sav.appendChild(g);
    }
    if (!document.querySelector(".fg-also")) {
      var a = document.createElement("div");
      a.className = "fg-also";
      a.innerHTML = '<a class="fg-also-gomb" href="#idopont" data-foglalo="also-sav">Időpontot foglalok<span>15 perc, telefonon vagy Google Meeten</span></a>';
      document.body.appendChild(a);
    }
    // a „Ki készítette?” gomb és a „Megjegyeztem” értesítés igazodjon az új sávhoz
    try { window.dispatchEvent(new Event("resize")); } catch (e) {}
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", retegElemek); else retegElemek();

  window.webnessFoglalo = { megnyit: megnyit, bezar: bezar };
})();
