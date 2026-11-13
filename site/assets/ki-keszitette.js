/* ÉRTÉKESÍTÉSI RÉTEG – „Ki készítette?” gomb és ablak (docs/DEMO-RETEG.md).
   A bal alsó sarokban kerek, finoman pulzáló gomb Marcell fotójával és piros értesítés-pöttyel;
   kattintásra egy ablak: bemutatkozás, alatta az ügyfélvélemények.
   Minden demóoldalra (a változatokra és az ajánlatoldalra is) kell. Élesítéskor törlendő.

   Használat: másold a site/assets/ mappába ezt és a ki-keszitette.css fájlt, majd minden oldal <head>-jébe:
     <link rel="stylesheet" href="assets/ki-keszitette.css">          (alkönyvtárban: ../assets/...)
     <script src="assets/ki-keszitette.js" defer></script>
   Demónként csak a lenti BEALLITASOK részt kell átírni. */
(function () {
  "use strict";

  // ---- BEÁLLÍTÁSOK (demónként) -------------------------------------------------------------
  var KEP = "https://webness.hu/assets/";   // Marcell fotója és a véleményírók képei a webness.hu-ról

  // Egy mondat a közös pontról / ismeretségről, ha van – részletek nélkül (docs/SZABALYOK.md).
  // Pl. TudásTárs: "A mostani tudastars.hu-t is én készítettem, 2016 óta dolgozunk együtt."
  var KOZOS_PONT = "";

  // Mind a 16 vélemény, szó szerint a webness.hu/ugyfeleink-velemenye oldalról
  // (forrás: szikoramarci/webness repó, content/ugyfeleink-velemenye.md). Ne írd át, ne rövidítsd.
  // Sorrend: előre a kisvállalkozókhoz legközelebb állók (orvos, tulajdonosok, művész).
  var VELEMENYEK = [
    { nev: "Dr. Békési Diána", szerep: "szájsebész, Nádi-Dental Kft.", kep: "people/bekesi-diana.webp", cim: "Elégedett vagyok",
      szoveg: ["Abszolút elégedett vagyok a munkátokkal. Ha az iskolában lennénk, akkor csillagos ötös osztályzatot adnék. Külön díjazom a rugalmasságotokat és udvariasságotokat. Köszönöm, ahogy hozzám és a weboldalamhoz álltatok az elejétől a végéig és hogy ez nem változott a fizetés után sem."] },
    { nev: "Kocziszky Ádám", szerep: "Controlling & Project Manager, Salzgitter Mannesmann Acélkereskedelmi Kft.", kep: "people/kocziszky-adam.webp", cim: "Együtt gondolkodó partner",
      szoveg: ["2017-ben ajánlásra kerültünk kapcsolatba a Webness-szel. Már az első beszélgetésnél tetszett, hogy odafigyelnek ránk, és olyan megoldást akarnak, amivel elégedettek leszünk. Náluk a technológiai tudás és az üzleti igényeink megértése együtt van jelen. Nem szó szerint azt valósították meg, amit mi megfogalmaztunk, hanem velünk együtt gondolkodtak, így sokszor jobbat kaptunk, mint amit elsőre kértünk! Az átadás után sem tűntek el: azóta is lelkiismeretesen reagálnak minden apró kérésünkre. Bátran ajánlom őket mindenkinek, aki nemcsak kivitelezőt, hanem együtt gondolkodó partnert keres."] },
    { nev: "Papp Gergely", szerep: "tulajdonos, Peaches and Cream, Bedlam Records", kep: "people/papp-gergely.webp", cim: "Évekig számíthattunk rá",
      szoveg: ["2017 óta dolgozunk együtt Marcellel. Ő készítette a Theo Papa ételrendelő oldalát SZÉP-kártyás és bankkártyás fizetéssel és hűségpontokkal, a Peaches and Cream asztalfoglalását, jegyárusítását és webshopját, később pedig a Bedlam Records oldalát is. Az admin felület tökéletesen fel volt építve: a Számlázz.hu-val összekötve egy kattintással elkészült a számla az asztalfoglalásokról, a jegyekről és a merch termékekről. Annyira bevált, hogy amikor később új fejlesztőhöz vittük az oldalt, azt kértük, hogy az admin ugyanígy működjön.",
               "Megbízható, gyors és rugalmas partnernek ismertem meg. Elég volt egy rövid e-mail, és az új árak, klippek, akciók általában egy-két napon belül kint voltak. Amikor 2020-ban, a lezárások alatt sürgősen kellett egy oldal a Peaches támogatói csomagjaihoz, két nap alatt elkészült, és az oldalak átadásakor is segített. Szerettem vele dolgozni, és jókat is beszélgettünk.",
               "Mindenkinek ajánlom, akinek webshop, foglalási vagy online fizetési rendszer kell, és olyan fejlesztőt keres, akire évekig számíthat."] },
    { nev: "Orha József", szerep: "tulajdonos, Orha Művek Kft.", kep: "people/orha-jozsef.webp", cim: "Lelkesek, elhivatottak",
      szoveg: ["Nem futószalagszerűen csináltatok nekem egy weblapot, hanem agyaltatok is a minél jobb megoldásokon. Lelkesek, elhivatottak vagytok, ajánlani foglak másoknak, mert tudom, hogy a legjobbat próbáljátok majd nyújtani nekik is."] },
    { nev: "Koncz Péter", szerep: "online marketing szakember", kep: "people/koncz-peter.webp", cim: "Mindig volt valami plusz",
      szoveg: ["2017 óta dolgozunk együtt Marcellel, többek között a Jánosik, a Hauser és a Bubbles weboldalain. Nem laikusként mondom, hiszen magam is ebben az iparágban dolgozom: minden projekt a megbeszélt határidőre elkészült, olyan szakmai minőségben, amelyben mindig volt valami plusz ahhoz képest, amire számítottam. Szerintem mindenki ezért szeret vele együtt dolgozni."] },
    { nev: "Bakos Gábor", szerep: "szaxofonművész", kep: "people/bakos-gabor.webp", cim: "Ahogy szerettem volna",
      szoveg: ["Gyors munkavégzés, gyors kommunikáció és megbízhatóság. Ez az, amiért szívesen ajánlom a Webness Webügynökséget másoknak is. A szolgáltatás minősége maximális és minden úgy készült el, ahogy szerettem volna. Köszönöm!"] },
    { nev: "Haász Dömötör", szerep: "ügyvezető-tulajdonos, SOLID Agency (korábban a Rézangyal Kft. és a Fundango marketingvezetője)", kep: "people/haasz-domotor.webp", cim: "Nagyok az elvárásaim",
      szoveg: ["Nagyok az elvárásaim: az ár, a minőség, a kommunikáció és a határidők betartása alapvetően fontos minden partnerünknél. Abszolút elégedett vagyok az átadott munkák minőségével és a hozzáállásotokkal is. A konkurenciához képest magasabb áraitok vannak, de szerintem bárki szívesen fizet többet, ha a beígért időpontra elkészülnek a megrendelések. Emiatt is ajánllak titeket mindenkinek, akinek az enyémhez hasonlóan magasak az igényei."] },
    { nev: "Cseppentő Zoltán", szerep: "a FrigyreLépek alapítója és megálmodója", kep: "people/cseppento-zoltan.webp", cim: "Pont így gondoltam én is",
      szoveg: ["2019-ben egy leírással és egy ötlettel kerestem meg Marcit: esküvőszervező portált szerettem volna, ahol a házasulandók és a szolgáltatók egy helyen találkoznak. Ő ebből először egy több mint 50 oldalas specifikációt és drótvázakat készített, aztán lépésről lépésre felépítette a FrigyreLépeket: vendéglista, ülésrendtervező, költségvetés, teendőlista, szolgáltatói profilok, előfizetés és automatikus számlázás. Az oldal 2021 óta élesben működik.",
               "Hét éve dolgozunk együtt, és amit a legtöbbre tartok: pontos, és korrekt a hozzáállása. Előre megmondta, mennyi idővel és költséggel jár egy-egy fejlesztés, és ha valami nem úgy működött, ahogy kellett, gyorsan javította. Sokszor csak annyit tudtam visszaírni: pont így gondoltam én is.",
               "Annak ajánlom, aki nem sablonoldalt, hanem saját logikájú, összetett webes rendszert szeretne, és olyan fejlesztőt keres, aki együtt gondolkodik vele és iránymutatást is ad. Én magam is ajánlottam már őt."] },
    { nev: "Zelerik Attila", szerep: "ügyvezető igazgató, Medor Kft.", kep: "people/zelerik-attila.webp", cim: "Ár/érték arány nagyon jó",
      szoveg: ["A közösen kidolgozott rendszereink megoldása nagyon hatékonyan, rugalmasan történt. A Webness által létrehozott szoftverek kialakításánál teljes mértékben a megrendelő igényei voltak szem előtt tartva. Nagyon pozitív a hozzáállásuk a tesztidőszak letelte utáni problémák megoldásához. Nem utolsó sorban a munkájuk ár/érték aránya nagyon jó."] },
    { nev: "Horváth Oszkár", szerep: "Chief Software Architect, Connectini Telemetria Kft. (korábban az Inteliza, Inc. ügyvezetője)", kep: "people/horvath-oszkar.webp", cim: "Megoldóember",
      szoveg: ["Kevés az olyan cég, amit 3-5 évvel később is ugyanarra a feladatra, ugyanazon a néven el lehet érni - a Webness vezetője nekünk évek óta szállít megoldásokat, és sokadik ügyfélnek tudunk jól teljesíteni azért, mert van megoldóember a háttérben, akire számíthatunk. Technológiailag egyre rugalmasabbak és olyan megoldásokat is hajlandóak megismerni, amikkel nekünk még nem volt tapasztalatunk. A munkához kapcsolódó kommunikáció hatékony. Ha kérdés van, azt egy hónapokig tartó munka esetén is 3x1 óra alatt tisztázzuk, és a végén nem kell minden szőnyeg alá benézni, hogy tényleg van-e ott parketta."] },
    { nev: "Kerülő Tünde", szerep: "ügyvezető, TudásTárs Kft.", kep: "people/kerulo-tunde.webp", cim: "Megbízható, korrekt, stabil",
      szoveg: ["2016 óta dolgozunk együtt Marcellel. Egy egyszerű, ritkán változó, de hosszú távon megbízhatóan működő honlapot szerettünk volna, és pontosan ezt kaptuk: az oldal évekig stabilan működött. Marcell rugalmasan alkalmazkodott a kéréseinkhez, amit szerettünk volna, nagyon rövid időn belül megvalósult, és a nehezebb kérések sem okoztak gondot. Mindig elérhető és válaszkész volt. Nagyon megbízható, korrekt és stabil partnernek ismertük meg, és nekünk ez volt a legfontosabb. Mindenkinek ajánljuk, akinek egy hosszú távon is megbízhatóan működő weboldal és egy elérhető, korrekt partner a fontos."] },
    { nev: "S. Kovács Ádám", szerep: "alapító, SKOVAX Entertainment (korábban a SKA Promotions Kft. ügyvezetője)", kep: "people/kovacs-adam.webp", cim: "Nincs megoldhatatlan",
      szoveg: ["Teljesen elégedettek vagyunk a hozzáállásotokkal, illetve a kiszolgálással is. A fejlesztésekkel teljesen rendben mentek, minden alkalommal a lehető leggyorsabban és megfelelő körültekintéssel álltok a felmerülő feladatokhoz, problémákhoz. Sokadik alkalommal is úgy tűnik, hogy nincs megoldhatatlan feladat számotokra."] },
    { nev: "Bács Levente", szerep: "Head of Art, Republic Group (korábban a Pump City tulajdonosa)", kep: "people/bacs-levente.webp", cim: "Maximális minőség",
      szoveg: ["Ügyfélbarát, megbízható, korrekt, és nem utolsó sorban profi minőség. Szeretek Marcellal és a Webness Webügynökséggel együtt dolgozni, jól működik a kommunikáció, képesek a designerek fejével is gondolkodni, a határidők mindig tartva vannak, problémás kérdésekre is mindig találunk megoldást, mindezek mellet maximális minőség is jellemzi a leadott munkákat."] },
    { nev: "Magyar Péter Medoks", szerep: "co-founder, HEYTHERE", kep: "people/magyar-peter.webp", cim: "Gyors, precíz",
      szoveg: ["Számos projekten dolgoztunk együtt. Megbízható, gyors, precíz és abszolút naprakész az aktuális frontend és backend trendek tekintetében. Az 'ezt nem lehet megoldani' szófordulatot szerencsére nem ismeri. Keressétek bizalommal!"] },
    { nev: "Balla-Seethaler Tamás", szerep: "ügyvezető igazgató, Seethaler Consulting Kft", kep: "people/balla-seethaler-tamas.webp", cim: "Marketing szemlélet",
      szoveg: ["A Webness Webügynökséggel nagyon könnyű együtt dolgozni. Precízek, kreatívak és nem kell mindent a \"szájba rágni\", ami jelentősen megkönnyíti a munkát. Elég megbeszélni az alapokat egy projektnél, a részleteket pedig marketing szemlélettel megoldják, a legjobb módon."] },
    { nev: "Szabados Tímea", szerep: "PR szervező, Régió Terv Kft", kep: "people/szabados-timea.webp", cim: "Szívből ajánlom",
      szoveg: ["A Webness Webügynökség egy igazán jó választás azoknak, akik ügyfélorientált, precíz és rugalmas csapatot keresnek vállalkozásuk informatikai fejlesztéséhez. Vezetője, Szikora Marcell segítőkészsége, megbízhatósága és kompromisszumkereső hozzáállása révén a cég méltó partnerünkké vált. A közös munkánk reméljük szervezeteink számára hosszú távú gyümölcsöző együttműködést jelent. Szívből ajánlom potenciális partnereinek figyelmébe!"] }
  ];
  // A megkeresett céghez köthető személy véleményét itt vedd ki, névvel (pl. TudásTárs-demónál "Kerülő Tünde").
  var KIHAGY = ["Koncz Péter"];  // a megkeresett céghez köthető személy (anyagok/adatok.md)

  // A demó mobilos alsó Hívás/Email sávja: a gomb fölé kerül. Más osztálynév esetén bővítsd.
  var ALSO_SAV = ".hivassav, .also-sav";

  // Marcell közvetlen száma: a demóból nem lehet kimenni, ezért a kapcsolat telefon (és email).
  var MARCELL_TEL = "+36 70 702 1530";
  var EMAIL = "info@webness.hu";
  // -------------------------------------------------------------------------------------------

  // tel: link a megjelenített számból (szóközök, kötőjelek nélkül)
  function telHref(t) { return String(t).replace(/[^0-9+]/g, ""); }

  var LATHATO = VELEMENYEK.filter(function (v) { return KIHAGY.indexOf(v.nev) < 0; });
  var OSSZES_VELEMENY = LATHATO.length;

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  // Egy vélemény HTML-je; a cimSzint a címsor szintje (ablakban h4, oldalon h3).
  function velemenyHtml(v, cimSzint) {
    return "<figure class=\"kk-v\"><" + cimSzint + ">" + esc(v.cim) + "</" + cimSzint + "><blockquote>" +
      v.szoveg.map(function (p, i, t) {
        return "<p>" + (i === 0 ? "„" : "") + esc(p) + (i === t.length - 1 ? "”" : "") + "</p>";
      }).join("") +
      "</blockquote><figcaption><img src=\"" + KEP + v.kep + "\" alt=\"\" width=\"48\" height=\"48\" loading=\"lazy\" decoding=\"async\">" +
      "<span><strong>" + esc(v.nev) + "</strong>" + esc(v.szerep) + "</span></figcaption></figure>";
  }

  var gomb = document.createElement("button");
  gomb.type = "button";
  gomb.className = "kk-lebego";
  gomb.setAttribute("aria-haspopup", "dialog");
  gomb.innerHTML =
    '<img src="' + KEP + 'marcell.jpg" alt="" width="64" height="64">' +
    '<span class="kk-potty" aria-hidden="true"></span>' +
    '<span class="kk-felirat"><strong>Ki készítette?</strong><small>' + OSSZES_VELEMENY + " ügyfél véleménye</small></span>";

  var ablak = document.createElement("dialog");
  ablak.className = "kk-ablak";
  ablak.setAttribute("aria-labelledby", "kk-cim");
  ablak.innerHTML =
    '<div class="kk-belso">' +
      '<div class="kk-fej"><h2 id="kk-cim">Ki készítette?</h2>' +
      '<button type="button" class="kk-zar">Bezárás <span aria-hidden="true">×</span></button></div>' +
      '<div class="kk-rolam">' +
        '<img src="' + KEP + 'marcell.jpg" alt="Szikora Marcell portréja" width="400" height="500" loading="lazy" decoding="async">' +
        "<div>" +
          '<p class="kk-nev"><strong>Szikora Marcell</strong><br>szoftvermérnök, a Webness alapítója, Tiszanagyfaluból</p>' +
          '<div class="kk-hivas"><p class="kk-hivas-cim">Kérdése van? Hívjon most, közvetlenül engem:</p>' +
          '<p class="kk-linkek"><a class="kk-gomb" href="tel:' + telHref(MARCELL_TEL) + '">' + esc(MARCELL_TEL) + "</a>" +
          '<span class="kk-halvany">vagy írjon: <a href="mailto:' + EMAIL + '">' + EMAIL + "</a></span></p></div>" +
          "<p>Több mint 15 éve készítek weboldalakat, webshopokat és egyedi rendszereket, eddig 116-nál is többet adtam át. Az Accenture-nél vezető fejlesztő voltam, ma a WorkFlex nemzetközi startupnál vagyok tech lead.</p>" +
          "<p>Velem közvetlenül dolgoznak: azzal beszélnek, aki megtervezi és megírja az oldalt. Ezt az oldalt előre elkészítettem, hogy ne kelljen elképzelni, milyen lehetne: ki lehet próbálni, mobilon is." + (KOZOS_PONT ? " " + esc(KOZOS_PONT) : "") + "</p>" +
          '<p class="kk-halvany"><strong>Akiknek már dolgoztam:</strong> Salzgitter Mannesmann, D-Link, Miskolci Nemzeti Színház, Jánosik és Társai, Orha Művek.</p>' +
        "</div>" +
      "</div>" +
      '<section class="kk-velemeny-resz" aria-labelledby="kk-velemeny-cim">' +
        '<h3 id="kk-velemeny-cim">Akikkel már dolgoztam</h3>' +
        '<p class="kk-halvany">' + OSSZES_VELEMENY + " ügyfél, az ő szavaikkal, változtatás nélkül, a webness.hu-ról.</p>" +
        '<div class="kk-velemenyek">' +
        LATHATO.map(function (v) { return velemenyHtml(v, "h4"); }).join("") +
        "</div>" +
        '<div class="kk-hivas kk-tovabb"><p class="kk-hivas-cim">Kérdése van? Hívjon most, közvetlenül engem:</p>' +
        '<p class="kk-linkek"><a class="kk-gomb" href="tel:' + telHref(MARCELL_TEL) + '">' + esc(MARCELL_TEL) + "</a>" +
        '<span class="kk-halvany">vagy írjon: <a href="mailto:' + EMAIL + '">' + EMAIL + "</a></span></p></div>" +
      "</section>" +
    "</div>";

  // Az oldalba ágyazott véleménylista (pl. ajánlatoldal): <div data-kk-velemenyek></div>
  Array.prototype.forEach.call(document.querySelectorAll("[data-kk-velemenyek]"), function (hely) {
    hely.classList.add("kk-oldal-velemenyek");
    hely.innerHTML = LATHATO.map(function (v) { return velemenyHtml(v, "h3"); }).join("");
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-kk-szam]"), function (e) { e.textContent = OSSZES_VELEMENY; });

  document.body.appendChild(gomb);
  document.body.appendChild(ablak);

  // A mobilos alsó sáv fölé emeljük a gombot, ha van ilyen sáv és látszik.
  function igazit() {
    var sav = document.querySelector(ALSO_SAV);
    var magas = 0;
    if (sav && getComputedStyle(sav).display !== "none" && getComputedStyle(sav).position === "fixed") {
      magas = sav.getBoundingClientRect().height;
    }
    gomb.style.setProperty("--kk-also", magas ? magas + 10 + "px" : "0px");
  }
  igazit();
  window.addEventListener("resize", igazit);

  gomb.addEventListener("click", function () {
    if (typeof ablak.showModal === "function") ablak.showModal();
    else ablak.setAttribute("open", "");
  });
  ablak.querySelector(".kk-zar").addEventListener("click", function () { ablak.close(); });
  // kattintás az ablakon kívülre (a háttérre) bezárja
  ablak.addEventListener("click", function (e) { if (e.target === ablak) ablak.close(); });
})();
