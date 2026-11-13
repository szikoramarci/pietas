/* ÉRTÉKESÍTÉSI RÉTEG – „Tetszik ez a rész?” (kis igenek + saját érvek), docs/DEMO-RETEG.md. Élesítéskor törlendő.

   - Minden szakasz végén: „Tetszik ez a rész? [Tetszik] [Ezt másképp]” – egy koppintás (kis igen).
   - Tetszik után: „Mi tetszik benne?” – kész válaszok vagy saját szavak, egyik sem kötelező (saját érvek).
   - A lap alján összegyűjtjük, ami tetszett, az ő szavaival (visszaidézés), majd a szándékra kérdezünk,
     és igen/talán esetén egy konkrét visszahívási időpontot kérünk.
   - A „Nem” és az „Ezt másképp” ugyanolyan könnyű, mint az igen; semmi nincs előre kiválasztva.
   A jelzések a VEGPONT-ra mennek (functions/api/jelzes.js), és a böngészőben is megmaradnak.

   Beépítés (lásd README.md): a változatoldalak <body> elemére data-tz, és a <head>-be:
     <link rel="stylesheet" href="../assets/tetszik.css">
     <script src="../assets/tetszik.js" defer></script>
   A választó oldalon is töltsd be (data-tz nélkül): a [data-tz-oldal="/v1/"] elemekbe kiírja,
   hány dolgot jelölt meg tetszőnek az adott változatban. */
(() => {
  // ---- BEÁLLÍTÁSOK (demónként) -------------------------------------------------------------
  const ZARO_KERDES = "El tudja képzelni, hogy ez legyen az Ön oldala a mostani helyett?";
  const TEL = "+36 46 431 014";      // a cég nyilvános irodai száma (weboldal, Kapcsolat), előtöltve, javítható
  const ADATKEZELES = "/adatkezeles/";              // a demón belüli tájékoztató (sablon: _reteg/adatkezeles/)
  const MARCELL_TEL = "+36 70 702 1530";      // Marcell közvetlen száma
  const OKOK = ["Áttekinthető", "Nyugodt, méltó hangulat", "Hasznos tartalom", "Mobilon is kényelmes"];
  const VEGPONT = "/api/jelzes";
  // A hívás kérése fölött: Marcell fotója és egy rövid, szó szerinti vélemény (a megkeresett céghez nem köthető).
  const KERES_KEP = "https://webness.hu/assets/marcell.jpg";
  const KERES_VELEMENY = ["Bátran ajánlom őket mindenkinek, aki nemcsak kivitelezőt, hanem együtt gondolkodó partnert keres.",
                          "Kocziszky Ádám, Salzgitter Mannesmann"];
  // A demó mobilos alsó Hívás/Email sávja: a bejelentés fölé kerül. Más osztálynév esetén bővítsd.
  const ALSO_SAV = ".hivassav, .also-sav";
  // A szakaszon belül ebbe a tárolóba kerül a sáv (ha nincs, magába a szakaszba).
  const TAROLO = ".keret, .wrap, .container, .nyito__szoveg";
  // -------------------------------------------------------------------------------------------

  const ELOTAG = "tz:";
  const olvas = (oldal) => { try { return JSON.parse(localStorage.getItem(ELOTAG + oldal)) || { reszek: {} }; } catch { return { reszek: {} }; } };
  const ment = (oldal, allapot) => { try { localStorage.setItem(ELOTAG + oldal, JSON.stringify(allapot)); } catch { /* privát mód */ } };
  const kuld = (adat) => {
    try {
      fetch(VEGPONT, {
        method: "POST", headers: { "Content-Type": "application/json" }, credentials: "same-origin", keepalive: true,
        body: JSON.stringify({ ...adat, oldal: location.pathname }),
      });
    } catch { /* a jelzés elveszhet, az oldal ettől működik */ }
  };
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const tetszettDb = (allapot) => Object.values(allapot.reszek || {}).filter((r) => r.tetszik).length;

  // Választó oldal: a kártyákra kiírjuk, hány dolog tetszett az adott változatban.
  document.querySelectorAll("[data-tz-oldal]").forEach((el) => {
    const n = tetszettDb(olvas(el.dataset.tzOldal));
    if (n) { el.textContent = `${n} dolgot jelölt meg tetszőnek ebben a változatban`; el.hidden = false; }
  });

  if (!document.body.hasAttribute("data-tz")) return;
  const main = document.querySelector("main");
  if (!main) return;

  const OLDAL = location.pathname;
  const allapot = olvas(OLDAL);
  allapot.reszek = allapot.reszek || {};

  const SZIV = '<svg class="tz-sziv" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-7.5-10.3A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.6c0 5.7-7.5 10.3-7.5 10.3Z"/></svg>';

  // Bejelentés (képernyőolvasónak is), a mobilos alsó sáv fölött
  const hir = document.createElement("div");
  hir.className = "tz-hir";
  hir.setAttribute("role", "status");
  hir.setAttribute("aria-live", "polite");
  document.body.appendChild(hir);
  const igazit = () => {
    const sav = document.querySelector(ALSO_SAV);
    const lathato = sav && getComputedStyle(sav).display !== "none" && getComputedStyle(sav).position === "fixed";
    hir.style.setProperty("--tz-also", lathato ? sav.getBoundingClientRect().height + "px" : "0px");
  };
  igazit();
  window.addEventListener("resize", igazit);
  let hirIdo;
  const bejelent = (szoveg) => {
    hir.textContent = szoveg;
    hir.classList.add("tz-hir--latszik");
    clearTimeout(hirIdo);
    hirIdo = setTimeout(() => hir.classList.remove("tz-hir--latszik"), 4500);
  };

  // ---- Szakaszonkénti sáv -------------------------------------------------------------------
  const szakaszok = [...main.querySelectorAll(":scope > section")];
  szakaszok.forEach((sec, i) => {
    const h = sec.querySelector("h1, h2");
    const cim = sec.dataset.tzCim || (i === 0 ? "Nyitókép" : (h ? h.textContent.replace(/\s+/g, " ").trim() : `${i + 1}. rész`));
    const cel = sec.querySelector(TAROLO) || sec;
    const azon = `tz-${i}`;
    const sor = document.createElement("div");
    sor.className = "tz-sor";
    sor.innerHTML = `
      <div class="tz-gombok" role="group" aria-label="Visszajelzés erről a részről: ${esc(cim)}">
        <span class="tz-kerdes">Tetszik ez a rész?</span>
        <button type="button" class="tz-tetszik" aria-pressed="false" aria-controls="${azon}">${SZIV}<span>Tetszik</span></button>
        <button type="button" class="tz-maskepp" aria-expanded="false" aria-controls="${azon}">Ezt másképp</button>
      </div>
      <div class="tz-panel" id="${azon}" hidden></div>
      <p class="tz-allapot"></p>`;
    cel.appendChild(sor);

    const gTetszik = sor.querySelector(".tz-tetszik");
    const gMaskepp = sor.querySelector(".tz-maskepp");
    const panel = sor.querySelector(".tz-panel");
    const allapotSor = sor.querySelector(".tz-allapot");
    const r = () => (allapot.reszek[cim] = allapot.reszek[cim] || { tetszik: false, okok: [], sajat: "", maskepp: "" });

    const frissit = () => {
      const x = allapot.reszek[cim];
      gTetszik.setAttribute("aria-pressed", String(!!(x && x.tetszik)));
      let t = "";
      if (x && x.tetszik) {
        const okok = [...(x.okok || [])];
        if (x.sajat) okok.push(`„${x.sajat}”`);
        t = okok.length ? `Tetszik: ${okok.join(", ")}` : "";
      }
      if (x && x.maskepp) t += (t ? "; " : "") + `Másképp: „${x.maskepp}”`;
      allapotSor.textContent = t;
    };

    const bezar = () => {
      panel.hidden = true;
      panel.innerHTML = "";
      gMaskepp.setAttribute("aria-expanded", "false");
    };

    const miert = () => {
      const x = r();
      panel.innerHTML = `
        <p class="tz-p-cim">Köszönöm! Mi tetszik benne? <span>(nem kötelező)</span></p>
        <div class="tz-okok">${OKOK.map((o) => `<button type="button" class="tz-ok" aria-pressed="${x.okok.includes(o)}">${esc(o)}</button>`).join("")}</div>
        <label class="tz-p-cimke" for="${azon}-s">Vagy a saját szavaival:</label>
        <div class="tz-p-sor">
          <input id="${azon}-s" type="text" maxlength="200" value="${esc(x.sajat || "")}">
          <button type="button" class="tz-kesz">Kész</button>
        </div>`;
      panel.hidden = false;
      panel.querySelectorAll(".tz-ok").forEach((b) => b.addEventListener("click", () => {
        b.setAttribute("aria-pressed", String(b.getAttribute("aria-pressed") !== "true"));
      }));
      panel.querySelector(".tz-kesz").addEventListener("click", () => {
        x.okok = [...panel.querySelectorAll('.tz-ok[aria-pressed="true"]')].map((b) => b.textContent);
        x.sajat = panel.querySelector("input").value.trim().slice(0, 200);
        ment(OLDAL, allapot);
        kuld({ tipus: "miert", resz: cim, okok: x.okok, sajat: x.sajat });
        bezar(); frissit(); osszegez();
        gTetszik.focus();
      });
      panel.querySelector(".tz-ok").focus();
    };

    gTetszik.addEventListener("click", () => {
      const x = r();
      x.tetszik = !x.tetszik;
      ment(OLDAL, allapot);
      kuld({ tipus: x.tetszik ? "tetszik" : "visszavonta", resz: cim });
      if (x.tetszik) {
        const elso = tetszettDb(allapot) === 1;
        miert();
        if (elso) bejelent("Megjegyeztem. A lap alján összegyűjtöm, ami tetszett.");
      } else {
        bezar();
      }
      frissit(); osszegez();
    });

    gMaskepp.addEventListener("click", () => {
      if (gMaskepp.getAttribute("aria-expanded") === "true") { bezar(); return; }
      const x = r();
      panel.innerHTML = `
        <label class="tz-p-cim" for="${azon}-m">Mit csinálna másképp ebben a részben?</label>
        <textarea id="${azon}-m" rows="3" maxlength="1000">${esc(x.maskepp || "")}</textarea>
        <button type="button" class="tz-kesz">Elküldöm</button>`;
      panel.hidden = false;
      gMaskepp.setAttribute("aria-expanded", "true");
      panel.querySelector(".tz-kesz").addEventListener("click", () => {
        x.maskepp = panel.querySelector("textarea").value.trim().slice(0, 1000);
        ment(OLDAL, allapot);
        if (x.maskepp) kuld({ tipus: "maskepp", resz: cim, szoveg: x.maskepp });
        bezar(); frissit(); osszegez();
        if (x.maskepp) bejelent("Köszönöm, átnézem, és ha tudom, átírom.");
        gMaskepp.focus();
      });
      panel.querySelector("textarea").focus();
    });

    sor.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) { bezar(); gTetszik.focus(); } });
    frissit();
  });

  // ---- Összegzés a lap alján ----------------------------------------------------------------
  const ossz = document.createElement("section");
  ossz.className = "tz-osszegzes";
  ossz.setAttribute("aria-labelledby", "tz-o-cim");
  ossz.innerHTML = `
    <div class="tz-o-belso">
      <h2 id="tz-o-cim">Ami Önnek tetszett ezen a változaton</h2>
      <div class="tz-o-lista"></div>
      <div class="tz-zaro">
        <p class="tz-zaro-kerdes" id="tz-zaro-kerdes">${esc(ZARO_KERDES)}</p>
        <div class="tz-valaszok" role="group" aria-labelledby="tz-zaro-kerdes">
          <button type="button" data-v="igen">Igen</button>
          <button type="button" data-v="talan">Talán, van kérdésem</button>
          <button type="button" data-v="meg-nem">Még nem</button>
        </div>
        <div class="tz-zaro-panel" aria-live="polite"></div>
      </div>
    </div>`;
  main.after(ossz);

  const lista = ossz.querySelector(".tz-o-lista");
  function osszegez() {
    const tetszett = Object.entries(allapot.reszek).filter(([, x]) => x.tetszik);
    const maskepp = Object.entries(allapot.reszek).filter(([, x]) => x.maskepp);
    if (!tetszett.length && !maskepp.length) {
      lista.innerHTML = '<p class="tz-o-ures">Ha valami tetszik, jelölje meg a szakaszok alatti <strong>Tetszik</strong> gombbal. Itt összegyűjtöm, és erre építek tovább.</p>';
      return;
    }
    const sor = ([cim, x]) => {
      const okok = [...(x.okok || [])].map(esc);
      if (x.sajat) okok.push(`<q>${esc(x.sajat)}</q>`);
      return `<li>${SZIV}<span><strong>${esc(cim)}</strong>${okok.length ? `: ${okok.join(", ")}` : ""}</span></li>`;
    };
    lista.innerHTML =
      (tetszett.length ? `<ul class="tz-o-tetszett">${tetszett.map(sor).join("")}</ul>` : "") +
      (maskepp.length ? `<p class="tz-o-alcim">Amin változtatna:</p><ul class="tz-o-maskepp">${maskepp.map(([cim, x]) => `<li><strong>${esc(cim)}</strong>: <q>${esc(x.maskepp)}</q></li>`).join("")}</ul>` : "") +
      (tetszett.length ? '<p class="tz-o-meg">Köszönöm! Ezekre építek a következő körben.</p>' : "");
  }
  osszegez();

  // Záró kérdés (szándékra kérdezés) és konkrét következő lépés
  const zaroPanel = ossz.querySelector(".tz-zaro-panel");
  const valaszGombok = ossz.querySelectorAll(".tz-valaszok button");

  const napNev = (d) => ["vasárnap", "hétfőn", "kedden", "szerdán", "csütörtökön", "pénteken", "szombaton"][d.getDay()];
  const kovetkezoMunkanap = () => {
    const d = new Date(); d.setDate(d.getDate() + 1);
    while (d.getDay() === 0 || d.getDay() === 6) d.setDate(d.getDate() + 1);
    const holnap = new Date(); holnap.setDate(holnap.getDate() + 1);
    return d.toDateString() === holnap.toDateString() ? "holnap" : napNev(d);
  };
  const nagy = (t) => t[0].toUpperCase() + t.slice(1);

  valaszGombok.forEach((b) => b.addEventListener("click", () => {
    valaszGombok.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    allapot.zaro = b.dataset.v;
    ment(OLDAL, allapot);
    kuld({ tipus: "zaro", valasz: b.dataset.v });

    if (b.dataset.v === "meg-nem") {
      zaroPanel.innerHTML = `<p>Rendben, köszönöm! Ha kérdése lesz, hívjon: <a href="tel:${esc(MARCELL_TEL.replace(/[^0-9+]/g, ""))}">${esc(MARCELL_TEL)}</a>, vagy írjon: <a href="mailto:info@webness.hu">info@webness.hu</a>. A többi változatot <a href="../">itt találja</a>.</p>`;
      return;
    }
    const nap = kovetkezoMunkanap();
    zaroPanel.innerHTML = `
      <div class="tz-ki"><img src="${esc(KERES_KEP)}" alt="" width="48" height="48" loading="lazy">
        <p><strong>Szikora Marcell</strong>, webness.hu<q>${esc(KERES_VELEMENY[0])}</q><span>${esc(KERES_VELEMENY[1])}</span></p></div>
      <p class="tz-zaro-cim">${b.dataset.v === "igen" ? "Örülök!" : "Szívesen válaszolok."} Felhívhatom 10 percre, hogy átbeszéljük, mit tenne még bele?</p>
      <label for="tz-tel">Telefonszám</label>
      <input id="tz-tel" type="tel" autocomplete="tel" value="${esc(TEL.startsWith("[") ? "" : TEL)}">
      <p class="tz-zaro-cimke" id="tz-ido-cim">Mikor hívhatom?</p>
      <div class="tz-valaszok tz-idopontok" role="group" aria-labelledby="tz-ido-cim">
        <button type="button" data-ido="${nap} délelőtt" aria-pressed="false">${nagy(nap)} délelőtt</button>
        <button type="button" data-ido="${nap} délután" aria-pressed="false">${nagy(nap)} délután</button>
        <button type="button" data-ido="másik nap" aria-pressed="false">Másik nap</button>
      </div>
      <button type="button" class="tz-kerem">Kérem a hívást</button>
      <p class="tz-apro">A számot csak a visszahíváshoz használom. <a href="${ADATKEZELES}">Adatkezelési tájékoztató</a><br>Inkább most beszélne? Hívjon: <a href="tel:${esc(MARCELL_TEL.replace(/[^0-9+]/g, ""))}">${esc(MARCELL_TEL)}</a>, vagy írjon: <a href="mailto:info@webness.hu">info@webness.hu</a></p>`;
    let ido = "";
    zaroPanel.querySelectorAll("[data-ido]").forEach((g) => g.addEventListener("click", () => {
      ido = g.dataset.ido;
      zaroPanel.querySelectorAll("[data-ido]").forEach((x) => x.setAttribute("aria-pressed", String(x === g)));
    }));
    zaroPanel.querySelector(".tz-kerem").addEventListener("click", () => {
      const tel = zaroPanel.querySelector("#tz-tel").value.trim();
      if (tel.replace(/\D/g, "").length < 8) {
        if (!zaroPanel.querySelector(".tz-hiba")) zaroPanel.querySelector(".tz-kerem").insertAdjacentHTML("afterend", '<p class="tz-hiba" role="alert">Adjon meg egy telefonszámot, amelyen elérhetem.</p>');
        return;
      }
      kuld({ tipus: "hivas", telefon: tel.slice(0, 40), idopont: ido || "mindegy", valasz: allapot.zaro });
      zaroPanel.innerHTML = `<p class="tz-zaro-cim">Köszönöm! ${ido && ido !== "másik nap" ? esc(nagy(ido)) + " hívom" : "Hamarosan hívom"} a ${esc(tel)} számon.</p>`;
    });
  }));
})();
