# PIETAS Kft. (Pietas Temetkezés) – oldalelemzés (2026. 11. 13.)

URL: https://pietas-temetkezes.hu/ (WordPress, „Blessing” sablon)
PageSpeed mobil: [Marcell méri: pagespeed.web.dev, mobil] / asztali: [ ]
Ellenőrzés: Chrome, asztali nézet, minden aloldal megnyitva; képernyőképek: `anyagok/regi-oldal/`.

## A 3 legfontosabb probléma

1. **Telefonról nem lehet egy érintéssel hívni, és az éjszakai szám el van dugva.** Az oldalon egyetlen telefonszám sem kattintható (a kezdőlapon és a Kapcsolat oldalon sincs `tel:` link). A 24 órás ügyelet száma (+36 20 235 3603) csak a kezdőlap szövegének alján és a „Mi a teendőnk?” aloldal közepén áll. Aki éjjel, telefonról keres segítséget, annak ki kell írnia a számot, vagy tovább keres. Ráadásul az oldal letiltja a nagyítást mobilon (`maximum-scale=1`), így az idősebb hozzátartozók a kis betűt sem tudják felnagyítani.
2. **Elavult és üres részek rontják a bizalmat.** A kezdőlapon még a járvány idejéből maradt kérés áll („csak egy hozzátartozó tartózkodhat az irodában”). A temetőüzemeltetés oldal szerint „közel 2 éve” üzemeltetik a hejőcsabai temetőt (valójában 2008 óta), a Cégünkről oldal „közel 30 évről” ír (1991 óta ez 35 év). A „Szórásos” oldal üres, csak egy 2013-as dátum van rajta, a Kapcsolat oldalon a térkép helye üres, a Hírekben egyetlen régi bejegyzés van.
3. **Aki most veszítette el valakijét, nem kap egy helyen választ.** A teendők, a szükséges iratok, a költségek, a nyitvatartás és az ügyelet öt külön aloldalon van, a kezdőlap csak egy felsorolás. A nyitvatartás (hétköznap 8:30–16:00) csak a Kapcsolat oldalon látszik. Fontos előnyök el vannak rejtve: hogy Miskolcon belül díjmentes az elszállítás, ha a temetést is ők intézik, hogy a koszorút díjmentesen kiszállítják, és hogy az urnát haza is lehet vinni.

## Ingyenes tipp (az oldaltól függetlenül, azonnal javítandó)

**Idegen reklámlink a gyászhirdetés-oldalon.** Az „Észak gyászhirdetés” aloldal utolsó bekezdésébe valaki egy oda nem illő mondatot és linket tett: egy „virtuális barátnő” szolgáltatásra mutat (cloneher.com). Ezt olvassák a gyászhirdetést feladni készülő családok. Ez feltört WordPressre vagy illetéktelen hozzáférésre utalhat. Javaslat: a mondat törlése, az admin-jelszavak cseréje, a WordPress és a bővítmények frissítése. (Ellenőrizve: 2026. 11. 13., a link a cikk szövegében, `rel` nélkül.)

## Apróbb hibák

- Három oldalon a telefonszám hibásan áll: „+36 06 46 431 014” (a kettőzött előhívóval a szám így nem hívható).
- A logó képének nincs alternatív szövege (`alt=""`), a képernyőolvasó nem mondja ki a cég nevét.
- A süti-sáv „Elfogadom” gombot kér, miközben a jogi nyilatkozat szerint az oldal csak munkamenet-sütit használ.
- A Kapcsolat oldalon az „Irodáink” többes szám, de egy iroda van; a „Mi a teendőnk?” oldal is „valamelyik irodánkat” írja.
- A mobil szám kétféleképpen szerepel („+36 70 9 475 490” és „06 70 9 475 490”), ami könnyen elírható.
- Az oldalsávban 2013-as naptár és egy „Oldalak” lista ismétli a menüt.
- Nincs `meta description`, a Google maga választ részletet a találathoz.

## Mit nyer az új oldallal

- Az első képernyőn: ki, hol, 1991 óta, és egy érintéssel hívható 24 órás ügyelet; mobilon a Hívás gomb mindig látszik.
- Egy oldalon, sorrendben: mi a teendő otthoni és kórházi halálesetnél, milyen iratokat hozzon, miből áll a költség, mikor van nyitva az iroda.
- A rejtett előnyök előre kerülnek: díjmentes elszállítás Miskolcon belül, díjmentes koszorú-kiszállítás, urnakiadás, gyászhirdetés az irodából.
- Gyors, sütimentes oldal WordPress-frissítések és feltörési kockázat nélkül.

## Demó Lighthouse (mobil)

Lighthouse 12, mobil, helyi szerver (2026. 11. 13.):

| Oldal | Teljesítmény | Akadálymentesség | Bevált gyakorlatok | LCP |
|---|---|---|---|---|
| v1 Mécses | 99 | 100 | 100 | 1,8 s |
| v2 Ív | 99 | 100 | 100 | 2,0 s |
| v3 Liliom | 99 | 100 | 100 | 2,0 s |
| választó | 100 | 100 | 100 | 1,8 s |
| ajánlatoldal | 100 | 100 | 100 | 1,8 s |
| adatkezelési tájékoztató | 100 | 100 | 100 | 0,6 s |

SEO a `noindex` miatt nem mérve (várt). Kontraszt (kontraszt.py): mindhárom változat minden párosa AA felett.
