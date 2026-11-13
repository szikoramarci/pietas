// ÉRTÉKESÍTÉSI RÉTEG – a „Tetszik ez a rész?” jelzések fogadása (assets/tetszik.js). Élesítéskor törlendő.
// A _middleware.js PIN-kódos védelme ide is vonatkozik.
//
// Beállítások (Cloudflare Pages > Settings):
//   VISSZAJELZES  – KV namespace binding: a jelzések tárolása (egy jelzés = egy bejegyzés)
//   ERTESITO_URL  – opcionális webhook (pl. ntfy, Slack, Telegram-bot): azonnali értesítés Marcellnek
//                   hívásigényről, a záró kérdés válaszáról és az „Ezt másképp” szövegekről
// Ha egyik sincs beállítva, a jelzés csak a Functions naplóban jelenik meg.

const CEG = "temetkezes-miskolc-pietas";
const TIPUSOK = new Set(["tetszik", "visszavonta", "miert", "maskepp", "zaro", "hivas"]);
const ERTESIT = new Set(["hivas", "zaro", "maskepp"]);
const szoveg = (v, max) => String(v ?? "").trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  let be;
  try {
    be = await request.json();
  } catch {
    return new Response(null, { status: 400 });
  }
  const tipus = szoveg(be.tipus, 20);
  if (!TIPUSOK.has(tipus)) return new Response(null, { status: 400 });

  const jelzes = {
    ido: new Date().toISOString(),
    ceg: CEG,
    tipus,
    oldal: szoveg(be.oldal, 100),
    resz: szoveg(be.resz, 120),
    okok: Array.isArray(be.okok) ? be.okok.slice(0, 8).map((o) => szoveg(o, 60)) : [],
    sajat: szoveg(be.sajat, 200),
    szoveg: szoveg(be.szoveg, 1000),
    valasz: szoveg(be.valasz, 20),
    telefon: szoveg(be.telefon, 40),
    idopont: szoveg(be.idopont, 40),
  };
  for (const k of Object.keys(jelzes)) {
    if (jelzes[k] === "" || (Array.isArray(jelzes[k]) && !jelzes[k].length)) delete jelzes[k];
  }
  console.log("jelzes", JSON.stringify(jelzes));

  const feladatok = [];
  if (env.VISSZAJELZES) {
    feladatok.push(env.VISSZAJELZES.put(`jelzes:${CEG}:${jelzes.ido}:${crypto.randomUUID().slice(0, 8)}`, JSON.stringify(jelzes), {
      metadata: { tipus, oldal: jelzes.oldal || "", resz: jelzes.resz || "" },
    }));
  }
  if (env.ERTESITO_URL && ERTESIT.has(tipus)) {
    const sor = [
      `${CEG} demó: ${tipus}`,
      jelzes.oldal && `oldal: ${jelzes.oldal}`,
      jelzes.resz && `rész: ${jelzes.resz}`,
      jelzes.valasz && `válasz: ${jelzes.valasz}`,
      jelzes.szoveg && `szöveg: ${jelzes.szoveg}`,
      jelzes.telefon && `tel: ${jelzes.telefon}`,
      jelzes.idopont && `időpont: ${jelzes.idopont}`,
    ].filter(Boolean).join(" | ");
    feladatok.push(fetch(env.ERTESITO_URL, { method: "POST", body: sor }).catch(() => {}));
  }
  await Promise.allSettled(feladatok);
  return new Response(null, { status: 204 });
}

export function onRequestGet() {
  return new Response("Csak POST", { status: 405, headers: { Allow: "POST" } });
}
