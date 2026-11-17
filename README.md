# Pietas Temetkezés – bemutató weboldal (demó)

Privát, PIN-kóddal védett bemutató oldal a miskolci PIETAS Kft. részére, a gyorsweb-folyamat szerint
(`szikoramarci/gyorsweb`: `CLAUDE.md`, `docs/SZABALYOK.md`, `docs/DEMO-RETEG.md`, `docs/DIZAJN.md`).
Nem indexelt, csak a tulajdonossal osztjuk meg. Ha nem kérik, 2–4 hét után töröljük.

## Felépítés

```
site/                     ← a Cloudflare Pages gyökere (a functions/ miatt ennek kell lennie)
  index.html              ← választó: három változat előnézeti képpel
  v1/ v2/ v3/             ← Mécses, Ív, Liliom (generált), mindegyikben 4 szolgáltatás-aloldal (a hirdetések céloldala)
  keresek/                ← „Kérései és a javítások”: mit kért az ügyfél, mit csináltunk, hol látja (réteg)
  valtozasok.json         ← a javítási körök; az értesítő ebből látja az élesedést (PIN nélkül elérhető)
  ajanlat/                ← mit hoz az új oldal, ki készítette (anyagok/ajanlat_oldal.py, sablon: gyorsweb _sablonok/_ajanlat)
  adatkezeles/            ← a bemutató oldal adatkezelési tájékoztatója (réteg)
  assets/                 ← alap.css + v1–v3.css, betűk (saját tárhelyről), réteg JS/CSS
  valaszto/               ← előnézeti képek (elonezet.py)
  functions/_middleware.js  ← PIN-kódos belépés (DEMO_PIN); nyitott mód: DEMO_NYITVA=1 (botok kizárva)
  functions/api/jelzes.js   ← „Tetszik ez a rész?” és időpontfoglaló jelzések → VISSZAJELZES KV
anyagok/
  adatok.md               ← tényadatok forrással, nyitott kérdések
  generator.py            ← a változatok, az aloldalak, a választó és a kérések oldala egy tartalomból
  keresek.py              ← az ügyfél kérései körönként (szó szerint), állapot, mit és hol javítottunk,
                             és a kör értesítő levele az ügyfélnek (a PR-ban hagyod jóvá)
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
| `ERTESITO_URL` | opcionális webhook (foglalás, záró válasz, „Ezt másképp”) |

## Élesítéskor (ha az ügyfél kéri)

A választott változat lesz a gyökér; a réteg törlendő: `ajanlat/`, `adatkezeles/`, `valaszto/`,
`keresek/`, `valtozasok.json`, `functions/`, `assets/ki-keszitette.*`, `assets/foglalo.*`, `assets/tetszik.*`, `assets/keresek.*`, a bemutató sáv, a `noindex`, a `robots.txt`
tiltása. A régi WordPress-címek 301-es átirányítása ekkor kerül be (`_redirects`).

## Javítási körök (ügyfél-kérések)

1. Az új „Ezt másképp” jelzések a `VISSZAJELZES` KV-ban; az értesítő 30 perc csend után összefoglalót küld róluk.
2. Új kör az `anyagok/keresek.py` elejére (szó szerint a kérések, állapot, mit és hol), és ha az ügyfélnek levél
   is menjen, az `ertesites` rész. Generálás, ág, PR.
3. A PR jóváhagyása (merge) után a Pages élesít; az értesítő a `valtozasok.json`-ból látja az új kört, és elküldi
   a levelet az ügyfélnek (másolat az info@webness.hu-ra), körönként egyszer. A demón a „Kérései és a javítások”
   sáv egyszer megjelenik.
