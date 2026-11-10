# Pietas Temetkezés – weboldal

A miskolci Pietas Temetkezés megújított weboldala. Statikus oldal, függőségek nélkül; Cloudflare Pages szolgálja ki, a `main` ágra küldött minden változás automatikusan élesedik.

## Felépítés

```
src/
  layout.html        közös fejléc, menü, lábléc, mobil hívósáv
  pages/*.html       az egyes oldalak tartalma (a fájl eleji JSON-komment: cím, leírás, útvonal)
  partials/*.html    ismétlődő blokkok, pl. az oldalsó hívódoboz (<!-- include:aside-call -->)
  static/            változtatás nélkül másolódik: CSS, JS, betűk, favicon, _redirects, _headers
scripts/build.mjs    összerakja az oldalakat a dist/ mappába, és elkészíti a sitemap.xml-t
```

## Helyi futtatás

```
npm run build      # → dist/
npm run preview    # build + helyi szerver
```

Node 18 vagy újabb kell, más függőség nincs.

## Cloudflare Pages beállítás

| Beállítás | Érték |
|---|---|
| Production branch | `main` |
| Build command | `node scripts/build.mjs` |
| Build output directory | `dist` |
| Környezeti változó (opcionális) | `SITE_URL` – alapértelmezés: `https://pietas-temetkezes.hu` |

## Tudnivalók

- **Régi címek:** a `src/static/_redirects` a régi WordPress-oldal aloldalait 301-gyel az új oldalakra irányítja, így a Google-találatok és a régi linkek nem vesznek el a domain átállításakor.
- **Betűk:** Marcellus (címek, telefonszámok) és Atkinson Hyperlegible Next (szöveg), saját tárhelyről, SIL Open Font License alatt.
- **Adatvédelem:** az oldal nem használ sütit és külső követőkódot.
- **Kitöltendő:** a `jogi-nyilatkozat` oldalon a hivatalos cégnév, cégjegyzékszám és adószám.
