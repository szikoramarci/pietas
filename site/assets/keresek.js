/* ÉRTÉKESÍTÉSI RÉTEG – „Kérései és a javítások”: az új kör után egyszer megjelenő sáv. Élesítéskor törlendő.
   A sáv (.valtozas-sav[data-kor]) addig látszik, amíg a látogató meg nem nyitja a kérések oldalát, vagy be nem
   zárja. Hogy melyik kört látta, a böngészőjében marad (localStorage); a kérések oldala (body[data-kor-latta])
   magától „látottnak” jelöli a legújabbat. Adatok: anyagok/keresek.py. */
(() => {
  const KULCS = "keresek:latott";
  const olvas = () => { try { return localStorage.getItem(KULCS) || ""; } catch { return ""; } };
  const ment = (id) => { try { localStorage.setItem(KULCS, id); } catch { /* privát mód */ } };
  const latta = document.body.dataset.korLatta;
  if (latta) { ment(latta); return; }
  const sav = document.querySelector(".valtozas-sav[data-kor]");
  if (!sav) return;
  const id = sav.dataset.kor;
  if (olvas() === id) return;
  sav.hidden = false;
  const bezar = sav.querySelector(".valtozas-bezar");
  if (bezar) bezar.addEventListener("click", () => { ment(id); sav.hidden = true; });
  const link = sav.querySelector("a");
  if (link) link.addEventListener("click", () => ment(id));
})();
