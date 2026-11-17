// Cloudflare Pages Functions middleware: PIN-kódos belépés a bemutató oldal elé.
//
// Beállítás (Cloudflare Pages > Settings > Variables and secrets, titkosítva):
//   DEMO_PIN – a belépéshez szükséges kód (pl. 6 számjegy)
// Ha hiányzik, az oldal NEM nyílik meg (zárt alapállapot).
//
// Helyes PIN után egy 30 napos, HttpOnly süti engedi tovább a látogatót.
// A PIN a linkben is megadható: /v1/?pin=123456 (a kód utána lekerül a címről).
// A PIN megváltoztatása minden korábbi belépést érvénytelenít.
// Minden válaszra X-Robots-Tag: noindex, nofollow fejléc kerül.
//
// Nyitott mód (ideiglenes, a tulajdonos döntése, 2026-11-17): DEMO_NYITVA = "1" környezeti változóval
// a PIN-oldal kimarad, bárki beléphet. Ilyenkor is: a botok és a linkelőnézet-készítők 403-at kapnak
// (User-Agent alapján), minden válasz noindex, a robots.txt mindent tilt. Visszakapcsolás: DEMO_NYITVA
// törlése vagy "0", majd újratelepítés (Pages: a változó a következő telepítéstől él).

const ROBOTS = "noindex, nofollow";
const SUTI = "demo_belepes";
const BELEPES = "/__belepes";
const encoder = new TextEncoder();

// Keresők, AI-gyűjtők, SEO-eszközök, linkelőnézet-készítők és parancssori letöltők (a mobilos alkalmazások
// beépített böngészői, pl. Facebook, Instagram, LinkedIn, átmennek). A Google PageSpeed / Lighthouse
// (Chrome-Lighthouse) átengedve, hogy a demó mérhető legyen.
const BOT = /(googlebot|google-inspectiontool|googleother|google-extended|adsbot|mediapartners|apis-google|feedfetcher|bingbot|bingpreview|msnbot|slurp|duckduckbot|duckassistbot|baiduspider|yandex|sogou|exabot|seznambot|petalbot|bytespider|applebot|facebookexternalhit|facebot|meta-externalagent|whatsapp\/|telegrambot|slackbot|discordbot|twitterbot|linkedinbot|pinterestbot|skypeuripreview|embedly|semrush|ahrefs|majestic|mj12bot|dotbot|blexbot|serpstat|dataforseo|gptbot|chatgpt-user|oai-searchbot|claudebot|claude-web|anthropic|perplexity|cohere|ccbot|diffbot|amazonbot|ia_archiver|archive\.org|headlesschrome|phantomjs|python|curl\/|wget|httpclient|okhttp|go-http|java\/|libwww|node-fetch|axios|scrapy|crawler|spider|\bbot\b)/i;
const MERO = /chrome-lighthouse/i;

function bot(request) {
  const ua = request.headers.get("User-Agent") || "";
  if (!ua.trim()) return true;
  return BOT.test(ua) && !MERO.test(ua);
}

function tiltas() {
  return new Response("Ez egy privát bemutató oldal.", {
    status: 403,
    headers: { "Content-Type": "text/plain; charset=utf-8", "X-Robots-Tag": ROBOTS, "Cache-Control": "no-store" },
  });
}

async function atenged(next) {
  const response = await next();
  const res = new Response(response.body, response);
  res.headers.set("X-Robots-Tag", ROBOTS);
  res.headers.set("Cache-Control", "private, no-store");
  return res;
}

async function hash(text) {
  const d = await crypto.subtle.digest("SHA-256", encoder.encode(text));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Időzítés-független összehasonlítás azonos hosszú hex-szövegekre.
function egyezik(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function sutik(header) {
  const ki = {};
  for (const resz of (header || "").split(";")) {
    const i = resz.indexOf("=");
    if (i > 0) ki[resz.slice(0, i).trim()] = resz.slice(i + 1).trim();
  }
  return ki;
}

// Csak saját oldalon belüli visszairányítás.
function biztonsagosVissza(v) {
  return typeof v === "string" && v.startsWith("/") && !v.startsWith("//") && !v.startsWith(BELEPES) ? v : "/";
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function pinOldal(vissza, hiba, status = 401) {
  const html = `<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Bemutató oldal – belépés</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#eef6f9;color:#1d2430;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:1.25rem}
  main{background:#fff;border:1px solid #d6e2e8;border-radius:16px;padding:2rem 1.75rem;width:min(100%,24rem);box-shadow:0 18px 40px -24px rgba(16,40,60,.35)}
  h1{font-size:1.35rem;margin:0 0 .5rem}
  p{margin:0 0 1.25rem;color:#4b5866;line-height:1.5}
  label{display:block;font-weight:600;margin-bottom:.4rem}
  input{width:100%;font:600 1.6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.35em;text-align:center;padding:.7rem;border:2px solid #c3d2da;border-radius:12px}
  input:focus{outline:3px solid #0e7aa6;outline-offset:2px;border-color:#0e7aa6}
  button{margin-top:1rem;width:100%;min-height:3rem;border:0;border-radius:12px;background:#0e7aa6;color:#fff;font:600 1.05rem system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;cursor:pointer}
  button:hover{background:#0a5f82}
  .hiba{color:#a1262b;font-weight:600;margin:.75rem 0 0}
  small{display:block;margin-top:1.25rem;color:#4b5866}
</style>
</head>
<body>
<main>
  <h1>Bemutató oldal</h1>
  <p>Ezt az oldalt személyesen Önnek készítettük. Adja meg a levélben kapott PIN-kódot.</p>
  <form method="post" action="${BELEPES}">
    <input type="hidden" name="vissza" value="${esc(vissza)}">
    <label for="pin">PIN-kód</label>
    <input id="pin" name="pin" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]*" maxlength="12" required autofocus>
    ${hiba ? `<p class="hiba" role="alert">${esc(hiba)}</p>` : ""}
    <button type="submit">Belépés</button>
  </form>
  <small>Készítette: Szikora Marcell, webness.hu</small>
</main>
</body>
</html>`;
  return new Response(html, {
    status,
    headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store", "X-Robots-Tag": ROBOTS },
  });
}

export async function onRequest({ request, env, next }) {
  const url0 = new URL(request.url);

  // Az értesítő (gyorsweb: eszkozok/ertesito/) ebből látja, hogy egy javítási kör élesedett: PIN nélkül is
  // elérhető (csak ez a fájl; a kérések listáját és az ügyfélnek szóló levél szövegét tartalmazza).
  if (url0.pathname === "/valtozasok.json" && request.method === "GET") return atenged(next);

  // Nyitott mód: PIN nélkül, de botok nélkül és indexelés nélkül.
  if (env.DEMO_NYITVA === "1") {
    if (url0.pathname === "/robots.txt") return atenged(next);
    if (bot(request)) return tiltas();
    if (url0.pathname === BELEPES) return Response.redirect(new URL("/", url0).toString(), 303);
    if (url0.searchParams.has("pin") && request.method === "GET") {
      url0.searchParams.delete("pin");
      return new Response(null, { status: 303, headers: { Location: biztonsagosVissza(url0.pathname + url0.search), "Cache-Control": "no-store", "X-Robots-Tag": ROBOTS } });
    }
    return atenged(next);
  }

  const pin = env.DEMO_PIN;
  if (!pin) {
    return new Response("A bemutató oldal még nincs beállítva.", {
      status: 503,
      headers: { "Content-Type": "text/plain; charset=utf-8", "X-Robots-Tag": ROBOTS },
    });
  }

  const url = new URL(request.url);
  const jel = await hash("gyorsweb-demo:" + pin);

  // PIN beküldése
  if (url.pathname === BELEPES) {
    if (request.method !== "POST") return Response.redirect(new URL("/", url).toString(), 303);
    let beirt = "", vissza = "/";
    try {
      const f = await request.formData();
      beirt = String(f.get("pin") || "").replace(/\s/g, "");
      vissza = biztonsagosVissza(String(f.get("vissza") || "/"));
    } catch {}
    if (beirt && egyezik(await hash("gyorsweb-demo:" + beirt), jel)) {
      return new Response(null, {
        status: 303,
        headers: {
          Location: vissza,
          "Set-Cookie": `${SUTI}=${jel}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`,
          "Cache-Control": "no-store",
          "X-Robots-Tag": ROBOTS,
        },
      });
    }
    await new Promise((r) => setTimeout(r, 800)); // lassítja a próbálgatást
    return pinOldal(vissza, "Ez a kód nem jó. Próbálja újra.");
  }

  const suti = sutik(request.headers.get("Cookie"))[SUTI] || "";

  // PIN a linkben (pl. /v1/?pin=123456), hogy ne kelljen beírni: helyes kódnál süti, és
  // átirányítás ugyanoda a kód nélkül, így a PIN nem marad a címsorban.
  const linkPin = url.searchParams.get("pin");
  if (linkPin !== null && request.method === "GET") {
    url.searchParams.delete("pin");
    const cel = biztonsagosVissza(url.pathname + url.search);
    const fejlec = { Location: cel, "Cache-Control": "no-store", "X-Robots-Tag": ROBOTS };
    if (egyezik(suti, jel)) return new Response(null, { status: 303, headers: fejlec });
    if (egyezik(await hash("gyorsweb-demo:" + linkPin.replace(/\s/g, "")), jel)) {
      fejlec["Set-Cookie"] = `${SUTI}=${jel}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`;
      return new Response(null, { status: 303, headers: fejlec });
    }
    await new Promise((r) => setTimeout(r, 800)); // lassítja a próbálgatást
    return pinOldal(cel, "A linkben lévő kód nem jó. Írja be a kapott PIN-kódot.");
  }

  // Belépett látogató
  if (egyezik(suti, jel)) return atenged(next);

  // Nincs belépve: PIN-oldal (a kérdőív végpontja nem érhető el belépés nélkül)
  if (url.pathname.startsWith("/api/")) {
    return new Response("Belépés szükséges.", { status: 401, headers: { "X-Robots-Tag": ROBOTS } });
  }
  return pinOldal(biztonsagosVissza(url.pathname + url.search), "", 401);
}
