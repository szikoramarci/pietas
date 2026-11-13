// Cloudflare Pages Functions middleware: PIN-kódos belépés a bemutató oldal elé.
//
// Beállítás (Cloudflare Pages > Settings > Variables and secrets, titkosítva):
//   DEMO_PIN – a belépéshez szükséges kód (pl. 6 számjegy)
// Ha hiányzik, az oldal NEM nyílik meg (zárt alapállapot).
//
// Helyes PIN után egy 30 napos, HttpOnly süti engedi tovább a látogatót.
// A PIN megváltoztatása minden korábbi belépést érvénytelenít.
// Minden válaszra X-Robots-Tag: noindex, nofollow fejléc kerül.

const ROBOTS = "noindex, nofollow";
const SUTI = "demo_belepes";
const BELEPES = "/__belepes";
const encoder = new TextEncoder();

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

  // Belépett látogató
  const suti = sutik(request.headers.get("Cookie"))[SUTI] || "";
  if (egyezik(suti, jel)) {
    const response = await next();
    const res = new Response(response.body, response);
    res.headers.set("X-Robots-Tag", ROBOTS);
    res.headers.set("Cache-Control", "private, no-store");
    return res;
  }

  // Nincs belépve: PIN-oldal (a kérdőív végpontja nem érhető el belépés nélkül)
  if (url.pathname.startsWith("/api/")) {
    return new Response("Belépés szükséges.", { status: 401, headers: { "X-Robots-Tag": ROBOTS } });
  }
  return pinOldal(biztonsagosVissza(url.pathname + url.search), "", 401);
}
