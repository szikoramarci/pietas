"""Az ügyfél kérései és a javítások, körönként (a legújabb elöl).

Ebből készül (generator.py):
  - site/keresek/index.html – „Kérései és a javítások”: mit kért (szó szerint, ahogy a demón beírta),
    mit csináltunk, és hol látja. Értékesítési réteg, élesítéskor törlendő.
  - a változatoldalak tetején a sáv: „Elkészültek a … kéréseinek módosításai” (az új kör után egyszer).
  - site/valtozasok.json – az értesítő (gyorsweb: eszkozok/ertesito/) ebből látja, hogy egy kör élesedett,
    és ha a körnek van `ertesites` része, elküldi az ügyfélnek (másolat Marcellnek). A levél szövegét a PR-ban
    hagyod jóvá: a merge után, az élesítést követően megy ki, körönként egyszer.

Új kör: tedd a lista elejére, új `id`-vel. A kérések forrása a VISSZAJELZES KV (`maskepp` jelzések):
a szöveg szó szerint marad (az ügyfél saját szavai), az időpont helyi idő. Ha egy kérést később bővített,
a bővebb változat marad. Állapot: kesz | var (tőlük várunk valamit) | folyamatban.
"""

DEMO_URL = "https://pietas-temetkezes.pages.dev"
CIMZETT = "miskolcipietas@gmail.com"   # a cég weboldalán közzétett cím

KOROK = [
    dict(
        id="2026-11-17-du",
        cim="November 17., délután",
        rovid="november 17-i délutáni",
        ertesites=dict(
            cimzett=CIMZETT,
            targy="Pietas bemutató oldal: elkészültek a kért módosítások",
            szoveg=f"""Jó napot kívánok!

Átvezettem a bemutató oldalon a november 17-én délután kért módosításokat. Hogy mit kértek, mit hogyan javítottam, és hol látják, egy helyen összegyűjtöttem:
{DEMO_URL}/keresek/

A legfontosabbak:
– a főcímben már szerepel a cím (Miskolc, Csabai kapu 16.), alatta jönnek a teendők, utána a szolgáltatások, a Mécses-féle felosztással;
– a négy fő szolgáltatásnak saját aloldala lett, ide lehet majd a hirdetésekből érkezőket vezetni;
– az ügyeletnél csak a 06 20 235 3603 szerepel, a térkép a cég Google-helyét mutatja, és új lapon nyílik.

A Rólunk részbe bekerült az irodáról készült fotó a régi oldalról; a korlátról eltüntettem a Pannónia-molinót.

Egy dologhoz kérném a segítségüket: a három kiválasztott Google-vélemény szövegét küldjék el, kérem, hogy szó szerint tehessük ki.

Ha valamit másképp szeretnének, a szakaszok alatt továbbra is jelezhetik, vagy egyszerűen válaszoljanak erre a levélre.

Üdvözlettel:
Szikora Marcell
webness.hu""",
        ),
        keresek=[
            dict(ido="2026-11-17 12:22", oldal="/v2/", resz="Nyitókép",
                 szoveg="Hamvasztásos és koporsós temetés, koszorú és halottszállítás egy helyen, a Csabai kapuban. Ügyeletünk éjjel is hívható.  Ezt javítani kellene szerintem hogy Miskolcon a Csabai kapu 16 szám alatt, már a főcímben is legyen egyértelmű. Illetve ez alatt a szekció alatt kellene helyet kapnia, hogy mi a teendő ha valaki otthon hunyt el, illetve kórházban. Azt kövesse a Szolgáltatásaink 1 helyen rész.\n\nIlletve a mécses verzióban látható felosztás is jobban tetszik, ahogy a szövegek vannak.",
                 allapot="kesz",
                 mit="A főcímben már ott van: Miskolcon, a Csabai kapu 16. alatt. A nyitókép alatt jönnek a teendők (otthon és kórházban), utána a szolgáltatások, mindhárom változatban. Az Ív nyitóképe a Mécses felosztását követi: balra a szöveg, jobbra külön dobozban az ügyelet száma, az iroda nyitvatartása, számai és címe.",
                 hol=[("/v2/#nyito-cim", "Nyitókép"), ("/v2/#teendok", "Teendők")]),
            dict(ido="2026-11-17 11:32", oldal="/v2/", resz="Mi a teendő haláleset után?",
                 szoveg="Ezt a részt vegyük ki: Ha a temetést is ránk bízza, Miskolcon belül az elszállítás díjmentes. Illetve ebben a felosztásban nem egyértelmű szerintem hogy otthoni illetve kórházi halálozásnál is ugyanazok a dokumentumok kellenek. Otthoninál olyan mintha csak a halottvizsgálatit kellene vinni. Utalni kell rá hogy az Ezeket hozza magával rész vonatkozik mindkettőre.",
                 allapot="kesz",
                 mit="A díjmentes elszállításról szóló mondat kikerült. Az iratok listája külön dobozba került, ezzel a címmel: „Ezeket hozza magával, otthoni és kórházi halálesetnél is”. Az otthoni lépéseknél is erre a listára utalunk.",
                 hol=[("/v2/#teendok", "Teendők")]),
            dict(ido="2026-11-17 12:12", oldal="/v2/", resz="24 órás halottszállítási ügyelet",
                 szoveg="Ügyeletnél vegyük ki akkor az irodai telefonszámot. legyen csak a 06202353603",
                 allapot="kesz",
                 mit="Az ügyeletnél csak a 06 20 235 3603 szerepel.",
                 hol=[("/v2/#kapcsolat", "Kapcsolat")]),
            dict(ido="2026-11-17 11:36", oldal="/v2/", resz="Csabai kapu 16., hétköznap 8:30–15:30",
                 szoveg="Külön ablakban nyíljanak meg a linkek. Itt is és az oldal egyéb részén is. Illetve azt hogy Emailt a nap bármely szakában írhat. ezt töröljük. Illetve jó lenne hogyha a Googleben a cég konkrét pontja jelenne meg és nem csak a címre letett egyéb pont.",
                 allapot="kesz",
                 mit="A térképlinkek új lapon nyílnak, és a cég saját Google-helyét mutatják (a temetőnél a temetőét). Az „Emailt a nap bármely szakában írhat” mondat kikerült.",
                 hol=[("/v2/#hol", "Iroda és nyitvatartás"), ("/v2/#szolgaltatasok", "A temető")]),
            dict(ido="2026-11-17 11:38", oldal="/v2/", resz="Szolgáltatásaink egy helyen",
                 szoveg="Itt az a bajom, hogy akarok majd Google Ads és egyéb hirdetéseket futtatni, most ha 1 mondtatot írunk egy hamvasztásos temetésről mindenféle info nélkül, akkor a hirdetésből hova hozzam be a látogatót és én őt mivel fogom meggyőzni? Illetve a kifelé mutató link itt is külön ablakban nyíljon meg.",
                 allapot="kesz",
                 mit="A négy fő szolgáltatásnak saját aloldala lett, ide lehet a hirdetésekből érkezőket vezetni. Mindegyiken szerepel, mit intézünk el, hogyan zajlik, miből áll a költség, néhány gyakori kérdés és a hívásgomb. A szaggatott keretes helyekre a részleteket a hívásban egyeztetjük. A kifelé mutató linkek új lapon nyílnak.",
                 hol=[("/v2/hamvasztasos-temetes/", "Hamvasztásos temetés"), ("/v2/koporsos-temetes/", "Koporsós temetés"),
                      ("/v2/halottszallitas/", "Halottszállítás"), ("/v2/kegyeleti-szerzodes/", "Kegyeleti szerződés")]),
            dict(ido="2026-11-17 11:35", oldal="/v2/", resz="Amit a családok írtak rólunk",
                 szoveg="Itt a céghez kapcsolódó 12 db Google vélemények közül jelenjen meg az alábbi: Kornélia Bésán, Beatrixw Bíró, Andrea Varga, Lehet monogramm is megjelenítésben.",
                 allapot="var",
                 mit="A három helyet monogrammal előkészítettük. Kérjük, küldjék el a három vélemény szövegét, és szó szerint kitesszük.",
                 hol=[("/v2/#velemenyek", "Vélemények")]),
            dict(ido="2026-11-17 11:33", oldal="/v2/", resz="1991 óta Miskolcon",
                 szoveg="Az eredeti pietas weboldalon a cégünkről menüpontban van egy fotó kívülről az irodáról. Az emeleti korláton lévő hirdetést le kéne róla szedni (Pannónia biztosító) és akkor az mehet is ide.",
                 allapot="kesz",
                 mit="A régi oldal „Cégünkről” fotója került ide. A korlátról eltüntettük a Pannónia-molinót, és a korlátot a kilátszó lécek alapján rajzoltuk újra.",
                 hol=[("/v2/#rolunk", "Rólunk")]),
        ],
    ),
    dict(
        id="2026-11-17-de",
        cim="November 13. és 17., délelőtt",
        rovid="november 13-i és 17-i délelőtti",
        ertesites=None,   # a kör már élesben volt, mielőtt az értesítő elkészült
        keresek=[
            dict(ido="2026-11-13 11:32", oldal="/v2/", resz="Nyitókép",
                 szoveg="A gyaszhirdetés megszűnt ki kellene venni,a nyitvatartas 15:30-ig\nAz irodai 203686533 mobiszamot is feltüntetni a temető pontos nevet mert van masik temető is hejőcsaban Hejőcsabai Római Katolikus temető",
                 allapot="kesz",
                 mit="A gyászhirdetés mindenhonnan kikerült. Az iroda nyitvatartása 8:30–15:30. Az irodai mobilszám (06 20 368 6533) a nyitóképen és a kapcsolatnál is szerepel. A temető mindenhol a pontos nevén áll: Hejőcsabai Római Katolikus temető.",
                 hol=[("/v2/#nyito-cim", "Nyitókép")]),
            dict(ido="2026-11-17 09:38", oldal="/v2/", resz="Szolgáltatásaink egy helyen",
                 szoveg="Szolgaltatas az urnakiadást kiveni gyaszhirdetés megszűnt,viragot mas varosba nem szállítunk. Kegyeleti szerződés van rá lehetőség egyéni megbeszélés szerint\nA temető címe Hejőcsabai Római Katolikus temető 3508 Miskolc Csabavezér út 1. Terkepet kene hozza mellekelni hogy autóval a Segesvári utca felől lehet megközelíteni. Nyitvatartás: április 1 es nov.1 között 7-19ig\nNov.i és apr 1 között 8-17 ig.\nKülföldi halottszállitas szomszedos orszagokból.\nA sirköves reszből kihúzni hogy eleg a csaladnak telefonálni.",
                 allapot="kesz",
                 mit="Az urnakiadás és a gyászhirdetés kikerült. A koszorúnál nincs más városba szállítás. A kegyeleti szerződés egyéni megbeszélés szerint szerepel. A temetőnél ott a cím, a nyitvatartás, a Segesvári utcai megközelítés és a térkép. A halottszállítás a szomszédos országokból szól, a sírköves mondat kikerült.",
                 hol=[("/v2/#szolgaltatasok", "Szolgáltatások és a temető")]),
            dict(ido="2026-11-17 09:42", oldal="/v2/", resz="Mi a teendő haláleset után?",
                 szoveg="A kórhaz csak a halottvizsgalati bizonyítvanyt állítja ki.\nA statisztikai lap kitölteset húzzuk ki.\nA meghatalmazással bárki in tezheti nem csak akkor ha beteg a temettető",
                 allapot="kesz",
                 mit="Kórházi halálesetnél csak a halottvizsgálati bizonyítvány szerepel. A statisztikai lap kikerült. Meghatalmazással bárki intézheti a temetést.",
                 hol=[("/v2/#teendok", "Teendők")]),
            dict(ido="2026-11-17 09:49", oldal="/v2/", resz="Amit a családok először kérdeznek",
                 szoveg="A költsegek 1. A temetkezes (szállitasi díjak,szakszemélyzet,\nügyintézes,hamvasztas dijja ,kellekek)\n2. Temető díjai sírhelyel kapcsolatos,sírnyitás,ravatalozóhasználat.\n3.Kórhaz fele fizetendő hűtésidíj halottkiadás\n4. Búcsúztató egyházi vagy polgari díja\nAz urna hazavitelt ne reszletezzük",
                 allapot="kesz",
                 mit="A „Mennyibe kerül a temetés?” válasza az Önök négy pontja szerint szól. Az urna hazaviteléről szóló kérdés kikerült.",
                 hol=[("/v2/#kerdesek", "Gyakori kérdések")]),
            dict(ido="2026-11-17 09:52", oldal="/v2/", resz="Mennyibe kerül? Ebből áll össze a számla",
                 szoveg="Ezt az egészet kihagyám",
                 allapot="kesz",
                 mit="A szakasz kikerült, a menüből is.",
                 hol=[]),
            dict(ido="2026-11-17 09:53", oldal="/v2/", resz="Csabai kapu 16., hétköznap 8:30–16:00",
                 szoveg="Nyitvatartas 15:30 ig. Parkolás ingyenes az iroda előtt kialakított parkolóban",
                 allapot="kesz",
                 mit="Az iroda nyitvatartása 8:30–15:30, és szerepel az ingyenes parkoló az iroda előtt.",
                 hol=[("/v2/#hol", "Iroda és nyitvatartás")]),
            dict(ido="2026-11-17 10:08", oldal="/v2/", resz="Hívjon, éjjel is felvesszük",
                 szoveg="A hívjon ejjel i felvesszük helyett 24 óras haluttszállitasi ügyeletA telefon szamokat így kéne, Ügyelet:0646 431 014\n20 2353603\nIroda:46 431 014\n20 3686533 a többit nem kell feltüntetni",
                 allapot="kesz",
                 mit="A cím: „24 órás halottszállítási ügyelet”. Csak az ügyelet és az iroda számai maradtak, a többi kikerült. (Délután az ügyeletnél az irodai számot is kivettük, lásd fent.)",
                 hol=[("/v2/#kapcsolat", "Kapcsolat")]),
        ],
    ),
]

ALLAPOT = {"kesz": "Kész", "var": "Önökre vár", "folyamatban": "Folyamatban"}
