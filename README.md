# Pietas Temetkezés – bemutató weboldal (demó)

Privát, PIN-kóddal védett bemutató oldal a miskolci PIETAS Kft. részére, a gyorsweb-folyamat szerint
(`szikoramarci/gyorsweb`: `CLAUDE.md`, `docs/SZABALYOK.md`, `docs/DEMO-RETEG.md`, `docs/DIZAJN.md`).
Nem indexelt, csak a tulajdonossal osztjuk meg. Ha nem kérik, 2–4 hét után töröljük.

## Felépítés

```
site/                     ← a Cloudflare Pages gyökere (a functions/ miatt ennek kell lennie)
  index.html              ← választó: három változat előnézeti képpel
  v1/ v2/ v3/             ← Mécses, Ív, Liliom (generált)
  ajanlat/                ← miért készült, mit találtunk, ki készítette (értékesítési réteg)
  adatkezeles/            ← a bemutató oldal adatkezelési tájékoztatója (réteg)
  assets/                 ← alap.css + v1–v3.css, betűk (saját tárhelyről), réteg JS/CSS
  valaszto/               ← előnézeti képek (elonezet.py)
  functions/_middleware.js  ← PIN-kódos belépés (DEMO_PIN)
  functions/api/jelzes.js   ← „Tetszik ez a rész?” jelzések → VISSZAJELZES KV
anyagok/
  adatok.md               ← tényadatok forrással, nyitott kérdések
  generator.py            ← a változatok, a választó és az ajánlatoldal egy tartalomból
  logo/                   ← a régi logó vektorosan lekövetve (az eredeti kérendő)
  regi-oldal/, kepernyokepek/, lighthouse.txt
elemzes.md                ← a régi oldal elemzése, ingyenes tipp, Lighthouse
```

## Módosítás

```sh
python3 anyagok/generator.py site                     # oldalak újragenerálása
# minden változat-módosítás után az előnézeti képek (a gyorsweb repóból):
CHROME_PATH=/usr/bin/google-chrome python3 sites/_sablonok/_valaszto/elonezet.py ../pietas/site v1 v2 v3
python3 sites/_sablonok/_dizajn/kontraszt.py ../pietas/site/assets/v1.css
```

## Cloudflare Pages (`pietas-temetkezes` projekt)

| Beállítás | Érték |
|---|---|
| Production branch | `main` (minden push élesít) |
| Root directory | `site` |
| Build command / output | nincs |
| `DEMO_PIN` | titkosított környezeti változó, 6 számjegy |
| `VISSZAJELZES` | KV-kötés a jelzésekhez |
| `ERTESITO_URL` | opcionális webhook a hívásigényekhez |

## Élesítéskor (ha az ügyfél kéri)

A választott változat lesz a gyökér; a réteg törlendő: `ajanlat/`, `adatkezeles/`, `valaszto/`,
`functions/`, `assets/ki-keszitette.*`, `assets/tetszik.*`, a bemutató sáv, a `noindex`, a `robots.txt`
tiltása. A régi WordPress-címek 301-es átirányítása ekkor kerül be (`_redirects`).
