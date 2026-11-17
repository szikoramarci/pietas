#!/usr/bin/env python3
"""Az ajánlatoldal adatai (site/ajanlat/index.html). Generátor és hangnem: a gyorsweb repó
sites/_sablonok/_ajanlat/ (ajanlat.py, README.md); a két repó egymás mellett van (../gyorsweb), vagy GYORSWEB=<útvonal>.
Futtatás: python3 anyagok/ajanlat_oldal.py (a generator.py is meghívja).

Tények: elemzes.md (Chrome, minden aloldal megnyitva, 2026-11-13): egyik telefonszám sem kattintható, a 24 órás ügyelet
száma a kezdőlap szövegének alján; a teendők, iratok, költségek, nyitvatartás és ügyelet öt külön aloldalon; a
nyitvatartás csak a Kapcsolat oldalon. PageSpeed a régi oldalra nincs mérve. Gyászoló családoknak szól: visszafogott
hangnem, kevés „Miért fontos?”, sürgetés nélkül. Képek: site/assets/ajanlat/."""
import os
import pathlib
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
GYORSWEB = pathlib.Path(os.environ.get("GYORSWEB", pathlib.Path(__file__).resolve().parents[2] / "gyorsweb"))
sys.path.insert(0, str(GYORSWEB / "sites" / "_sablonok" / "_ajanlat"))
import ajanlat  # noqa: E402
from ajanlat import stat  # noqa: E402

CFG = {
    "ceg": "Pietas Temetkezés", "domain": "pietas-temetkezes.hu",
    "sav": "Bemutató – nem a PIETAS Kft. hivatalos weboldala.",
    "cim": "Az Önök oldala számokban: most, és az új változatban",
    "title": "Mit hoz az új oldal, és ki készítette",
    "kartyak": [
        {"tipus": "teny", "cim": "A 24 órás ügyelet száma", "most": "a kezdőlap szövegének alján", "uj": "az első képernyőn, egy koppintással"},
        {"tipus": "pont", "cim": "Google hivatalos értékelése", "most": 60, "uj": 100},
        {"tipus": "ido", "cim": "Töltési sebesség", "most": 9.0, "uj": 1.0},
    ],
    "meres": ("Mérés: Google PageSpeed Insights, mobil, 2026. 11. 17., ugyanazon a napon a mostani és az új oldalra. "
              "A tartalmi összevetés böngészőben, minden aloldal megnyitva: 2026. 11. 13."),
    "ut": {
        "cim": "Egy család útja, három lépésben",
        "bevezeto": ("A mostani oldalon megvan minden fontos: a szolgáltatások, a teendők, az iratok és az elérhetőségek. "
                     "Az új változat abban segít, hogy aki most veszítette el valakijét, telefonról is gyorsan elérje Önöket, "
                     "és egy helyen kapjon választ."),
        "lepesek": [
            {"cim": "A család telefonról keresi az ügyeletet",
             "most": {"tipus": "szoveg", "cim": "A kezdőlap szövegében",
                      "sorok": ["„…nyugodtan hívják a 06 46 431 014-es telefonszámot vagy a 06 70 9 475 490-es mobil számot.”",
                                "A számok szövegként, nem egy koppintással hívhatók"],
                      "felirat": "A 24 órás ügyelet száma a kezdőlap szövegének alján és a „Mi a teendőnk?” oldalon van."},
             "uj": {"tipus": "mobil", "kep": "uj-mobil.webp", "alt": "Az új kezdőlap mobilon", "w": 390, "h": 844,
                    "felirat": "<b>Az ügyelet száma az első képernyőn,</b> egy koppintással hívható; mobilon a Hívás gomb mindig látszik."},
             "miert": stat("mobil")},
            {"cim": "A család megnézi, mi a teendő",
             "most": {"tipus": "szoveg", "cim": "Öt külön aloldalon",
                      "sorok": ["Teendők", "Szükséges iratok", "Költségek", "Nyitvatartás", "24 órás ügyelet"],
                      "felirat": "Minden információ megvan, a menü több pontja alatt."},
             "uj": {"tipus": "mobil", "kep": "uj-teendok.webp", "alt": "Az új oldal teendők része mobilon", "w": 780, "h": 1400,
                    "felirat": "<b>Egy oldalon, sorrendben:</b> mi a teendő otthoni és kórházi halálesetnél, milyen iratokat hozzon, miből áll a költség."}},
            {"cim": "A család felkeresi az irodát",
             "most": {"tipus": "szoveg", "cim": "Kapcsolat aloldal",
                      "sorok": ["Cím és nyitvatartás (hétköznap 8:30–16:00)", "A telefonszámok szövegként"],
                      "felirat": "A nyitvatartás csak a Kapcsolat oldalon látszik."},
             "uj": {"tipus": "kivagas", "vilagos": True, "kep": "uj-kapcsolat.webp", "alt": "Az új oldal elérhetőségei", "w": 780, "h": 1100,
                    "felirat": "<b>Cím, útvonal, nyitvatartás és ügyelet egy helyen,</b> minden szám egy koppintással hívható."},
             "miert": stat("ellenoriz")},
        ],
    },
    "tovabbi": {"elemek": ["Az Ív változatban megmarad a logó sírkő-íve és a bordó szín",
                           "Előre kerül: díjmentes elszállítás Miskolcon belül, díjmentes koszorú-kiszállítás, urnakiadás",
                           "„Amit a családok először kérdeznek”: rövid válaszok", "A temetés költségének tételei egy helyen",
                           "Évszámokkal: 1991 óta, a hejőcsabai temető 2008 óta", "Mobilon nagyítható betűk",
                           "Hely a családok véleményének és saját fotóknak"]},
    "valtozatok": {"kartyak": [
        ("Mécses", "Mélyzöld, nyugodt színek, a nyitóképen mécsesfénnyel a 24 órás ügyelet száma. Nagy, jól olvasható betűk.", "v1"),
        ("Ív", "A mostani arculat felújítva: a logó sírkő-íve, a bordó és a borostyán szín, papírszerű háttér.", "v2"),
        ("Liliom", "Világos, levegős, nagy betűs változat; már a nyitóképen ott van lépésről lépésre, mi a teendő.", "v3"),
    ]},
    "gyik": [
        ("Mit kell nekünk csinálni?", "Szinte semmit: a tartalom a mostani weboldalukról van. Egy rövid hívásban átnézzük, mi tetszik, és kérek néhány dolgot: az eredeti logót, pár fotót az irodáról, és hogy mely adatok változtak."),
        ("Mi lesz a mostani oldallal és a címmel?", "A pietas-temetkezes.hu cím marad, csak az új oldal kerül mögé. A régi aloldalak címeit átirányítjuk, így a Google-találatok sem vesznek el."),
        ("Kell-e ehhez WordPress-t frissítgetni?", "Nem. Az új oldalon nincs bővítmény és admin-felület, így nincs mit frissítgetni, és a feltörés esélye is jóval kisebb."),
        ("Mibe kerül?", "Ezt a hívásban, a kívánságaik alapján beszéljük meg, és írásban is elküldöm. Ha nem kérik, a bemutatót töröljük."),
    ],
}


def main():
    ajanlat.general(SITE, CFG)


if __name__ == "__main__":
    main()
