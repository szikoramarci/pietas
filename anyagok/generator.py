#!/usr/bin/env python3
"""A Pietas Temetkezés demó három változata, a választó és az ajánlatoldal egy tartalomból.

Használat (a repó gyökeréből):
    python3 anyagok/generator.py site

Minden tény az anyagok/adatok.md-ből jön (a régi weboldal, 2026-11-13). Ami a mi szövegünk és az
ügyfél anyagaiban nincs, azt a HTML-ben „EGYEZTETENDŐ” megjegyzés jelöli; ami hiányzik, az látható
[helyőrző]. Mindhárom változat magáz. Az ügyvezető neve nem kerül az oldalra (SZABALYOK.md).
A logó a régi oldal logójáról vektorosan lekövetve (anyagok/logo/); az eredeti fájl kérendő.
"""
import html
import json
import re
import sys
import pathlib

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
ANYAG = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ANYAG))
from keresek import KOROK, ALLAPOT, DEMO_URL  # noqa: E402

CEG = "Pietas Temetkezés"
CEG_TELJES = "PIETAS Kft. – Teljeskörű temetkezési szolgálat"
NBSP = " "


def tel(szam):
    """06-os belföldi formából tel: link (+36...)."""
    d = re.sub(r"\D", "", szam)
    return "tel:+36" + d[2:] if d.startswith("06") else "tel:+" + d


# A telefonszámok az ügyfél kérése szerint (demó-visszajelzések, 2026-11-17): az ügyeletnél csak a mobil,
# az irodánál a vezetékes és a mobil; a többi (mobil, koszorúrendelés, további számok) nem kerül ki (adatok.md).
UGYELET = "06 20 235 3603"
IRODA = "06 46 431 014"
IRODA_MOBIL = "06 20 368 6533"
UGYELET_SZAMOK = [UGYELET]
IRODA_SZAMOK = [IRODA, IRODA_MOBIL]
EMAIL = "miskolcipietas@gmail.com"
CIM = "3529 Miskolc, Csabai kapu 16."
# A térképlinkek a cég és a temető saját Google-helyére mutatnak (place_id, a Places-keresésből; a szabályaink
# szerint csak ez tárolható), és új lapon nyílnak (az ügyfél kérése, 2026-11-17).
TERKEP = "https://www.google.com/maps/search/?api=1&amp;query=PIETAS+Temetkez%C3%A9s%2C+Miskolc&amp;query_place_id=ChIJN7EtBvWfQEcRqzF3Pll2r_I"
NYITVA = 'hétfőtől péntekig <span class="nowrap">8:30–15:30</span>'
TEMETO = "Hejőcsabai Római Katolikus temető"   # pontos név: Hejőcsabán másik temető is van
TEMETO_CIM = '3508 Miskolc, <span class="nowrap">Csabavezér út 1.</span>'
TEMETO_TERKEP = "https://www.google.com/maps/search/?api=1&amp;query=Hej%C5%91csabai+r%C3%B3mai+katolikus+temet%C5%91&amp;query_place_id=ChIJP3luiCGhQEcRoVPDyzrdZO4"
KULSO = ' target="_blank" rel="noopener"'   # kifelé mutató link: új lapon


def a_tel(szam, cls="tel"):
    return f'<a class="{cls}" href="{tel(szam)}">{szam.replace(" ", NBSP)}</a>'


def a_telek(szamok, elvalaszto=", "):
    return elvalaszto.join(a_tel(s) for s in szamok)


def symbol(nev, azon):
    """A lekövetett logórész SVG-útvonala <symbol>-ként, szoros befoglaló téglalappal."""
    s = (ANYAG / "logo" / f"{nev}.svg").read_text(encoding="utf-8")
    d = re.search(r' d="([^"]+)"', s).group(1)
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", d)]
    xs, ys = nums[0::2], nums[1::2]
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    vb = f"{x0 - 2:.0f} {y0 - 2:.0f} {x1 - x0 + 4:.0f} {y1 - y0 + 4:.0f}"
    return f'<symbol id="{azon}" viewBox="{vb}"><path fill="currentColor" fill-rule="evenodd" d="{d}"/></symbol>', (x1 - x0) / (y1 - y0)


JEL, JEL_ARANY = symbol("logo-jel", "i-jel")
FELIRAT, FELIRAT_ARANY = symbol("logo-pietas", "i-felirat")

IKONOK = """<symbol id="i-tel" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 3.5h3.2l1.6 4.3-2 1.3a12 12 0 0 0 7.1 7.1l1.3-2 4.3 1.6V19a1.8 1.8 0 0 1-1.9 1.8A16.6 16.6 0 0 1 3.2 5.4 1.8 1.8 0 0 1 5 3.5Z"/></symbol>
    <symbol id="i-level" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></g></symbol>
    <symbol id="i-hely" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></g></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16"/></symbol>
    <symbol id="i-ora" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></g></symbol>
    <symbol id="i-mecses" viewBox="0 0 32 40"><path class="lang-kulso" d="M16 2.5c3.2 6.2 8.2 10.6 8.2 17.6a8.2 8.2 0 0 1-16.4 0c0-7 5-11.4 8.2-17.6z"/><path class="lang-belso" d="M16 13.5c1.6 3 4.2 5 4.2 8.6a4.2 4.2 0 0 1-8.4 0c0-3.6 2.6-5.6 4.2-8.6z"/><path class="mecses-tal" d="M4.5 32.5h23c0 4-5 6.5-11.5 6.5s-11.5-2.5-11.5-6.5z"/></symbol>"""

SPRITE = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
    {JEL}
    {FELIRAT}
    {IKONOK}
  </svg>"""

ICON = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E'
        '%3Crect width=%2764%27 height=%2764%27 rx=%2714%27 fill=%27%23592131%27/%3E'
        '%3Cpath d=%27M22 54V24a10 10 0 0 1 20 0v30Z%27 fill=%27%23F7F1E8%27/%3E%3C/svg%3E">')

VALTOZATOK = {
    "v1": dict(nev="Mécses", theme="#1C3530", preload="marcellus.woff2",
               rend=["nyito", "teendok", "szolgaltatasok", "ismeros", "rolunk", "velemenyek", "hol", "kapcsolat"],
               leiras="Mélyzöld, nyugodt színek, a nyitóképen mécsesfénnyel a 24 órás ügyelet száma. Nagy, jól olvasható betűk, a telefonszámok mindig kiemelve."),
    "v2": dict(nev="Ív", theme="#592131", preload="sourceserif4.woff2",
               rend=["nyito", "teendok", "szolgaltatasok", "ismeros", "rolunk", "velemenyek", "hol", "kapcsolat"],
               leiras="A mostani arculat felújítva: a logó sírkő-íve, a bordó és a borostyán szín, papírszerű háttér. A nyitóképen külön dobozban az ügyelet és az iroda."),
    "v3": dict(nev="Liliom", theme="#F7F7F4", preload="cormorantgaramond.woff2",
               rend=["nyito", "teendok", "szolgaltatasok", "ismeros", "rolunk", "velemenyek", "hol", "kapcsolat"],
               leiras="Világos, levegős, nagy betűs változat. Már a nyitóképen ott van lépésről lépésre, mi a teendő haláleset után."),
}


# ---- Közös darabok ----
def gombok():
    return f"""<div class="gombok">
            <a class="gomb gomb-fo" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás éjjel-nappal: {UGYELET.replace(" ", NBSP)}</a>
            <a class="gomb gomb-masod" href="mailto:{EMAIL}"><svg aria-hidden="true"><use href="#i-level"/></svg>Email küldése</a>
          </div>"""


TENYEK = f"""<ul class="tenyek">
            <li>1991 óta Miskolcon</li>
            <li>24 órás ügyelet, hétvégén is</li>
            <li>a {TEMETO} üzemeltetője</li>
          </ul>"""

IRODA_SOR = f'<p class="nyito-info">Iroda: {CIM}, {NYITVA}. Telefon: {a_telek(IRODA_SZAMOK, " vagy ")}</p>'


def fej(id_, cim, bev=None):
    b = f'\n        <p class="bevezeto-kicsi">{bev}</p>' if bev else ""
    return f'<h2 id="{id_}-cim">{cim}</h2>{b}'


OTTHON_LEPESEK = f"""<ol class="lepesek">
          <li><h3>Hívja a háziorvost vagy az orvosi ügyeletet</h3><p>Az orvos elvégzi a halottvizsgálatot, kiállítja a bizonyítványt, és engedélyezi az elszállítást.</p></li>
          <li><h3>Hívja ügyeletünket: {a_tel(UGYELET)}</h3><p>A nap bármely órájában. Az orvos előírása szerint az elhunytat halottasházba vagy kórházi patológiára visszük.</p></li>
          <li><h3>Jöjjön be az irodába</h3><p>Hozza magával az iratokat, a listát lent találja. Itt megbeszéljük a temetés részleteit, a többi ügyintézést mi végezzük.</p></li>
        </ol>"""


def ugyelet_tabla(ikon):
    return f"""<aside class="ugyelet-tabla" aria-label="Ügyelet és iroda">
          {ikon}
          <p class="tabla-cimke">24 órás ügyelet</p>
          <p class="tabla-szam">{a_tel(UGYELET)}</p>
          <dl>
            <div><dt>Iroda, {NYITVA}</dt><dd>{a_telek(IRODA_SZAMOK, "<br>")}</dd></div>
            <div><dt>Címünk</dt><dd>{CIM}<br><a href="{TERKEP}"{KULSO}>Térkép és útvonal</a></dd></div>
          </dl>
        </aside>"""


IRATOK = """<ul class="iratok">
              <li>az elhunyt személyi igazolványa és lakcímkártyája</li>
              <li>a halottvizsgálati bizonyítvány</li>
              <li>születési vagy házassági anyakönyvi kivonat, ha megvan; ha nem, segítünk beszerezni</li>
              <li>külföldi elhunytnál az útlevél</li>
            </ul>"""

IRATOK_DOBOZ = f"""<div class="iratok-doboz">
          <h3 class="alcim">Ezeket hozza magával, otthoni és kórházi halálesetnél is</h3>
          {IRATOK}
        </div>"""

# A költség négy része az ügyfél felsorolása szerint (demó-visszajelzés, 2026-11-17).
KOLTSEG_RESZEK = """<ol class="koltseg-reszek">
              <li>a temetkezés: szállítás, szakszemélyzet, ügyintézés, hamvasztás és a kellékek</li>
              <li>a temető díjai: sírhely, sírnyitás, a ravatalozó használata</li>
              <li>a kórháznak fizetendő hűtési díj és halottkiadás</li>
              <li>az egyházi vagy polgári búcsúztató díja</li>
            </ol>"""


# ---- Szakaszok ----
def nyito(v):
    if v == "v1":
        return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret nyito-racs">
        <div class="nyito-szoveg">
          <p class="felcim">Pietas Temetkezés, Miskolc</p>
          <h1 id="nyito-cim">Temetés teljes ügyintézéssel Miskolcon, a Csabai kapu 16. alatt</h1>
          <p class="bevezeto">Átvesszük a temetés minden teendőjét: az elhunyt elszállítását, a hivatalos ügyeket és a búcsúztatás szervezését.</p>
          {TENYEK}
          {gombok()}
        </div>
        {ugyelet_tabla('<svg class="mecses" aria-hidden="true"><use href="#i-mecses"/></svg>')}
      </div>
    </section>"""
    if v == "v2":
        return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret nyito-racs">
        <div class="nyito-szoveg">
          <p class="felcim">Pietas Temetkezés, Miskolc</p>
          <h1 id="nyito-cim">Teljeskörű temetkezési szolgálat Miskolcon, a Csabai kapu 16. alatt</h1>
          <p class="bevezeto">Hamvasztásos és koporsós temetés, koszorú és halottszállítás egy helyen, 1991 óta. Ügyeletünk éjjel is hívható.</p>
          {TENYEK}
          {gombok()}
        </div>
        <!-- A Mécses változat felosztása (az ügyfél kérése, 2026-11-17): jobbra az ügyelet és az iroda. -->
        {ugyelet_tabla('<svg class="tabla-jel" aria-hidden="true"><use href="#i-jel"/></svg>')}
      </div>
    </section>"""
    return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret">
        <p class="felcim">Pietas Temetkezés, Miskolc, Csabai kapu 16. · 1991 óta</p>
        <h1 id="nyito-cim">Haláleset történt? Hívjon minket, éjjel is.</h1>
        <p class="bevezeto">Teljes körű temetkezés Miskolcon, a Csabai kapu 16. szám alatt: a temetés minden ügyintézését átvesszük.</p>
        {gombok()}
        {IRODA_SOR}
        <h2 class="nyito-alcim">Ha otthon hunyt el a szerette, ezt tegye, ebben a sorrendben:</h2>
        {OTTHON_LEPESEK}
      </div>
    </section>"""


def ismeros(v):
    return f"""<section class="szakasz szakasz-alt" id="kerdesek" aria-labelledby="kerdesek-cim">
      <!-- A kérdések a régi oldal saját kérdéseiből és tájékoztatóiból, átfogalmazva (adatok.md). -->
      <div class="keret">
        {fej('kerdesek', 'Amit a családok először kérdeznek')}
        <dl class="kerdesek">
          <div><dt>Otthon hunyt el. Kit hívjak először?</dt><dd>A háziorvost vagy az orvosi ügyeletet. Ha az orvos végzett, hívja ügyeletünket: {a_tel(UGYELET)}.</dd></div>
          <div class="ket-sor"><dt>Mennyibe kerül a temetés?</dt><dd>A költség négy részből áll össze:
            {KOLTSEG_RESZEK}
            Árajánlatot telefonon kérhet: {a_tel(IRODA)}.</dd></div>
          <div><dt>Választhatunk temetőt?</dt><dd>Igen. Miskolcon bármelyik temetkezési szolgáltató bármelyik temetőben temethet.</dd></div>
        </dl>
      </div>
    </section>"""


def teendok(v):
    # Az ügyfél kérése (2026-11-17): a díjmentes elszállításról szóló mondat kimarad, és legyen egyértelmű,
    # hogy az iratok otthoni és kórházi halálesetnél is ugyanazok.
    otthon = "" if v == "v3" else f"""<h3 class="alcim">Ha otthon történt</h3>
        {OTTHON_LEPESEK}"""
    cim = {"v1": "Haláleset után: ezt tegye, ebben a sorrendben",
           "v2": "Mi a teendő haláleset után?",
           "v3": "Kórházban történt? És milyen iratokat hozzon?"}[v]
    return f"""<section class="szakasz" id="teendok" aria-labelledby="teendok-cim">
      <div class="keret">
        {fej('teendok', cim)}
        {otthon}
        <h3 class="alcim">Ha kórházban történt</h3>
        <p>A kórház a halottvizsgálati bizonyítványt állítja ki. Ez néhány napig is tarthat. Addig is jöjjön be az irodába: az időpont kivételével mindent megbeszélhetünk.</p>
        {IRATOK_DOBOZ}
        <p class="halvany">Meghatalmazással bárki intézheti a temetést a temettető helyett.</p>
      </div>
    </section>"""


# Az ügyfél kérése szerint (2026-11-17): urnakiadás és gyászhirdetés nincs (a gyászhirdetés megszűnt),
# koszorút más városba nem szállítanak, kegyeleti szerződés egyéni megbeszélés szerint, külföldről a
# szomszédos országokból szállítanak.
# A négy fő szolgáltatásnak saját aloldala van (hirdetések céloldala, az ügyfél kérése, 2026-11-17): ALOLDALAK.
SZOLG = [
    ("Hamvasztásos temetés", "Teljes ügyintézéssel. Urnát a bemutatótermünkben választhat.", "hamvasztasos-temetes"),
    ("Koporsós temetés", "Teljes ügyintézéssel. Koporsót, sírjelzőt és sírtáblát a bemutatótermünkben választhat.", "koporsos-temetes"),
    ("Halottszállítás", "Belföldön, és a szomszédos országokból is, a szükséges hatósági és konzuli iratokkal.", "halottszallitas"),
    ("Kegyeleti szerződés", "Előre is megállapodhat velünk a temetésről. A részleteket egyéni megbeszélés szerint rögzítjük.", "kegyeleti-szerzodes"),
    ("Koszorú friss virágból", "Csak megrendelésre készül, katalógusból választhat, és díjmentesen kiszállítjuk a temetésre.", None),
]


def szolg_li(c, t, slug, elotag=""):
    tovabb = f'<p class="reszletek"><a href="{elotag}{slug}/">Részletek<span class="rejtett">: {c.lower()}</span> →</a></p>' if slug else ""
    return f"          <li><h3>{c}</h3><p>{t}</p>{tovabb}</li>"


def szolgaltatasok(v):
    cim = {"v1": "Temetés és minden, ami hozzá tartozik",
           "v2": "Szolgáltatásaink egy helyen",
           "v3": "Amiben segítünk"}[v]
    li = "\n".join(szolg_li(c, t, slug) for c, t, slug in SZOLG)
    return f"""<section class="szakasz szakasz-alt" id="szolgaltatasok" aria-labelledby="szolgaltatasok-cim">
      <div class="keret">
        {fej('szolgaltatasok', cim, 'A temetéshez szükséges hivatali ügyeket is mi intézzük.')}
        <ul class="szolg-lista">
{li}
        </ul>
        <div class="temeto">
          <h3>A {TEMETO} üzemeltetője</h3>
          <p>2008 óta mi üzemeltetjük. Sírhely, sírásás és ravatalozó ügyében hozzánk forduljon. Sírkőmunkát a sírkövesnek kell bejelentenie az irodánkban.</p>
          <div class="temeto-racs">
            <div>
              <p><strong>A temető címe:</strong> {TEMETO_CIM}</p>
              <p>Autóval a Segesvári utca felől lehet megközelíteni.</p>
              <p><a class="gomb gomb-masod" href="{TEMETO_TERKEP}"{KULSO}><svg aria-hidden="true"><use href="#i-hely"/></svg>Térkép és útvonal a temetőhöz</a></p>
            </div>
            <table class="nyitva">
              <caption>A temető nyitvatartása</caption>
              <tbody>
                <tr><th scope="row">április 1. – november 1.</th><td>7:00–19:00</td></tr>
                <tr><th scope="row">november 1. – április 1.</th><td>8:00–17:00</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>"""


def rolunk(v):
    cim = {"v1": "1991 óta Miskolcon, egy irodával a Csabai kapuban",
           "v2": "1991 óta Miskolcon",
           "v3": "Miskolc harmadik magán temetkezési vállalkozása, 1991 óta"}[v]
    return f"""<section class="szakasz szakasz-alt" id="rolunk" aria-labelledby="rolunk-cim">
      <div class="keret rolunk-racs">
        <div>
          {fej('rolunk', cim)}
          <p>1991. március 15-én alakultunk, Miskolc harmadik magán temetkezési vállalkozásaként. Egy irodánk van, a Csabai kapu 16.-ban, de a környező és távolabbi településeken is vállalunk teljes körű temetést.</p>
          <p>A gyász napjaiban a fájdalmat nem vehetjük el, de a terheket igen: ezért intézünk el minden ügyet, amit csak lehet.</p>
          <ul class="tenyek-lista">
            <li>Bemutatótermünkben koporsók, urnák, sírjelzők és más kellékek közül választhat.</li>
            <li>2008 óta üzemeltetjük a {TEMETO}t.</li>
            <li>Alapító tagjai vagyunk a Magyar Temetkezési Szolgáltatók Országos Szakegyesületének.</li>
          </ul>
        </div>
        <!-- FOTÓ: a régi oldal „Cégünkről” fotója az irodáról, az emeleti korlát reklámja (Pannónia biztosító)
             nélkül (az ügyfél kérése, 2026-11-17). Reklám nélküli eredeti kérve; ha nincs, retusálva. -->
        <figure class="foto-hely" aria-label="Fotó helye">
          <p>[Ide kerül az iroda fotója a régi oldalról, a korlátról levett reklám nélkül]</p>
        </figure>
      </div>
    </section>"""


def velemenyek(v):
    return f"""<section class="szakasz" id="velemenyek" aria-labelledby="velemenyek-cim">
      <!-- VÉLEMÉNYEK: a cég 12 Google-véleményéből az általuk kiválasztott három (2026-11-17), monogrammal.
           A szöveg szó szerint, tőlük kérve (a Google Térképről nem másolunk, SZABALYOK.md). -->
      <div class="keret">
        {fej('velemenyek', 'Amit a családok írtak rólunk')}
        <div class="velemeny-racs">
          <figure class="velemeny-hely"><blockquote><p>[Az első kiválasztott Google-vélemény szövege: kérjük, küldjék el]</p></blockquote><figcaption>B. K., Google-vélemény</figcaption></figure>
          <figure class="velemeny-hely"><blockquote><p>[A második kiválasztott Google-vélemény szövege: kérjük, küldjék el]</p></blockquote><figcaption>B. B., Google-vélemény</figcaption></figure>
          <figure class="velemeny-hely"><blockquote><p>[A harmadik kiválasztott Google-vélemény szövege: kérjük, küldjék el]</p></blockquote><figcaption>V. A., Google-vélemény</figcaption></figure>
        </div>
      </div>
    </section>"""


def hol(v):
    return f"""<section class="szakasz szakasz-alt" id="hol" aria-labelledby="hol-cim">
      <div class="keret">
        {fej('hol', 'Csabai kapu 16., hétköznap 8:30–15:30')}
        <div class="ketoszlop">
          <div>
            <h3 class="alcim"><svg aria-hidden="true"><use href="#i-ora"/></svg>Nyitvatartás</h3>
            <table class="nyitva">
              <tbody>
                <tr><th scope="row">Iroda, hétfő–péntek</th><td>8:30–15:30</td></tr>
                <tr><th scope="row">Ügyelet</th><td>éjjel-nappal, hétvégén is</td></tr>
              </tbody>
            </table>
          </div>
          <div>
            <h3 class="alcim"><svg aria-hidden="true"><use href="#i-hely"/></svg>Iroda és bemutatóterem</h3>
            <p>{CIM}, földszint</p>
            <p><a class="gomb gomb-masod" href="{TERKEP}"{KULSO}><svg aria-hidden="true"><use href="#i-hely"/></svg>Útvonal a Csabai kapuhoz</a></p>
            <p>Az iroda előtti parkolóban ingyenesen parkolhat.</p>
          </div>
        </div>
      </div>
    </section>"""


def kapcsolat(v):
    return f"""<section class="szakasz kapcsolat" id="kapcsolat" aria-labelledby="kapcsolat-cim">
      <div class="keret">
        {fej('kapcsolat', '24 órás halottszállítási ügyelet', 'Telefonon a leggyorsabb. Árajánlatot munkaidőben az irodai számon adunk.')}
        <p class="kapcs-gomb"><a class="gomb gomb-fo" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás éjjel-nappal: {UGYELET.replace(" ", NBSP)}</a></p>
        <dl class="adatok">
          <div><dt>Ügyelet, 0–24 óra</dt><dd>{a_telek(UGYELET_SZAMOK, "<br>")}</dd></div>
          <div><dt>Iroda, munkaidőben</dt><dd>{a_telek(IRODA_SZAMOK, "<br>")}</dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Cím</dt><dd>{CIM}</dd></div>
        </dl>
      </div>
    </section>"""


SZAKASZOK = dict(nyito=nyito, ismeros=ismeros, teendok=teendok, szolgaltatasok=szolgaltatasok,
                 rolunk=rolunk, velemenyek=velemenyek, hol=hol, kapcsolat=kapcsolat)
MENU = {"teendok": "Teendők", "szolgaltatasok": "Szolgáltatások",
        "rolunk": "Rólunk", "kapcsolat": "Kapcsolat"}


def marka(v, href="#tartalom"):
    if v == "v2":
        return f"""<a class="marka" href="{href}" aria-label="PIETAS – Teljeskörű temetkezési szolgálat">
        <svg class="marka-ikon" aria-hidden="true"><use href="#i-jel"/></svg>
        <span class="marka-szoveg" aria-hidden="true"><svg class="marka-felirat"><use href="#i-felirat"/></svg><span class="marka-al">Teljeskörű temetkezési szolgálat</span></span>
      </a>"""
    return f"""<a class="marka" href="{href}">
        <svg class="marka-ikon" aria-hidden="true"><use href="#i-jel"/></svg>
        <span class="marka-szoveg"><span class="marka-nev">Pietas</span> <span class="marka-al">Temetkezés, Miskolc</span></span>
      </a>"""


def valtozas_sav(gy):
    """Az új kör után egyszer megjelenő sáv (assets/keresek.js); a „Kérései és a javítások” oldalra visz."""
    kor = KOROK[0]
    return f"""<div class="valtozas-sav" data-kor="{kor['id']}" hidden>
    <p><strong>Elkészültek a {kor['rovid']} kéréseinek módosításai.</strong> <a href="{gy}keresek/">Megnézem, mit és hol javítottunk</a></p>
    <button type="button" class="valtozas-bezar" aria-label="Bezárás">×</button>
  </div>"""


def oldal(v, d, tartalom=None, gy="../", menu_elotag="", title=None, desc=None, marka_href="#tartalom"):
    if tartalom is None:
        tartalom = "\n\n    ".join(SZAKASZOK[s](v) for s in d["rend"])
    title = title or "Pietas Temetkezés, Miskolc – teljes körű temetés, 24 órás ügyelet (bemutató)"
    desc = desc or f"Teljes körű temetkezés Miskolcon 1991 óta: hamvasztásos és koporsós temetés, koszorú, halottszállítás. Iroda: Csabai kapu 16., hétköznap 8:30–15:30. Ügyelet: {UGYELET}."
    nav = "\n".join(f'        <li><a href="{menu_elotag}#{k}">{MENU[k]}</a></li>' for k in d["rend"] if k in MENU)
    return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="{d['theme']}">
  {ICON}
  <link rel="preload" href="{gy}assets/betuk/{d['preload']}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{gy}assets/betuk/betuk.css">
  <link rel="stylesheet" href="{gy}assets/alap.css">
  <link rel="stylesheet" href="{gy}assets/{v}.css">
  <!-- ÉRTÉKESÍTÉSI RÉTEG (élesítéskor törlendő): „Ki készítette?”, időpontfoglaló, „Tetszik ez a rész?”, kérések -->
  <link rel="stylesheet" href="{gy}assets/ki-keszitette.css">
  <script src="{gy}assets/ki-keszitette.js" defer></script>
  <link rel="stylesheet" href="{gy}assets/foglalo.css">
  <script src="{gy}assets/foglalo.js" defer></script>
  <link rel="stylesheet" href="{gy}assets/tetszik.css">
  <script src="{gy}assets/tetszik.js" defer></script>
  <link rel="stylesheet" href="{gy}assets/keresek.css">
  <script src="{gy}assets/keresek.js" defer></script>
  <!-- Cloudflare Web Analytics (sütimentes) – token élesítés előtt:
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "[CLOUDFLARE_TOKEN]"}}'></script>
  -->
</head>
<body class="{v}" data-tz>
  <a class="ugras" href="#tartalom">Ugrás a tartalomra</a>
  {SPRITE}
  <div class="bemutato-sav" role="note">
    <p><strong>Bemutató ajánlat – nem a {CEG} hivatalos weboldala.</strong> Változat: {d['nev']}.</p>
    <p class="sav-linkek"><a href="{gy}">Mindhárom változat</a> <a href="{gy}keresek/">Kérései és a javítások</a> <a href="{gy}ajanlat/">Mit hoz az új oldal, és ki készítette?</a></p>
  </div>
  {valtozas_sav(gy)}

  <header class="fejlec">
    <div class="keret fejlec-sor">
      <!-- LOGÓ: a régi oldal logója vektorosan lekövetve (anyagok/logo/); az eredeti fájl kérendő. -->
      {marka(v, marka_href)}
      <nav class="fomenu" aria-label="Fő menü">
        <ul class="menu-sor">
{nav}
        </ul>
        <!-- Mobilon és tableten: Menü gomb JavaScript nélkül (<details>), a lista a fejléc alá nyílik. -->
        <details class="menu-mobil">
          <summary><svg aria-hidden="true"><use href="#i-menu"/></svg>Menü</summary>
          <ul class="menu-panel">
{nav}
          </ul>
        </details>
      </nav>
      <a class="fejlec-tel" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg><span><span class="fejlec-tel-cimke">Ügyelet 0–24</span> {UGYELET.replace(" ", NBSP)}</span></a>
    </div>
  </header>

  <main id="tartalom">
    {tartalom}
  </main>

  <footer class="lablec">
    <div class="keret lablec-sor">
      <p>© 2026 {CEG_TELJES} · {CIM} fsz. · Cégjegyzékszám: 05-09-001135</p>
      <p>[A cég adatkezelési tájékoztatója: élesítés előtt] · <a href="{gy}adatkezeles/">A bemutató oldal adatkezelése</a></p>
    </div>
  </footer>

  <nav class="also-sav" aria-label="Gyors elérés">
    <a class="gomb gomb-fo" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás 0–24</a>
    <a class="gomb gomb-masod" href="mailto:{EMAIL}"><svg aria-hidden="true"><use href="#i-level"/></svg>Email</a>
  </nav>
</body>
</html>
"""


# ---- Szolgáltatás-aloldalak (a hirdetések céloldalai, az ügyfél kérése, 2026-11-17) ----
# Tények: adatok.md (a régi oldal szolgáltatásoldalai és az ügyfél javításai). Ami nincs meg, az látható
# [helyőrző] és EGYEZTETENDŐ megjegyzés: a hívásban pontosítjuk. Ár nincs; a költség az ügyfél négy pontja szerint.
ALOLDALAK = {
    "hamvasztasos-temetes": dict(
        nev="Hamvasztásos temetés",
        cim="Hamvasztásos temetés Miskolcon, teljes ügyintézéssel",
        bev="Az első hívástól a búcsúztatásig mindent elintézünk: az elhunyt elszállítását, a hivatalos ügyeket, a hamvasztást és a temetés megszervezését. Ügyeletünk éjjel-nappal hívható.",
        desc=f"Hamvasztásos temetés teljes ügyintézéssel Miskolcon, 1991 óta. Iroda: Csabai kapu 16., hétköznap 8:30–15:30. Ügyelet éjjel-nappal: {UGYELET}.",
        mit=["Elszállítjuk az elhunytat a haláleset helyéről, majd a hamvasztóüzembe.",
             "Intézzük a temetéshez szükséges hivatalos ügyeket.",
             "A bemutatótermünkben urnát és a hozzá tartozó kellékeket választhat.",
             "Megszervezzük a búcsúztatást a választott temetőben, egyházi vagy polgári szertartással.",
             "Koszorút friss virágból, megrendelésre készítünk, és díjmentesen kiszállítjuk a temetésre."],
        mit_utan="Miskolcon bármelyik temetkezési szolgáltató bármelyik temetőben temethet, így a temetőt Ön választja meg.",
        helyorzo="[Egyeztetendő: mit tartalmaz pontosan a hamvasztásos temetés, és mennyi idő alatt készül el a hamvasztás.]",
        lepesek=[("Hívja ügyeletünket", f"Ha az orvos elvégezte a halottvizsgálatot, hívjon minket a nap bármely órájában: {a_tel(UGYELET)}. Az elhunytat az orvos előírása szerint halottasházba vagy kórházi patológiára visszük."),
                 ("Jöjjön be az irodába", "Hozza magával az iratokat, a listát lent találja. Megbeszéljük a búcsúztatás idejét és helyét, és kiválasztja az urnát."),
                 ("A többit mi intézzük", "A hivatalos ügyeket, a hamvasztást és a búcsúztatás szervezését átvesszük. Ha közben kérdése van, munkaidőben az irodában, éjjel az ügyeleten elér minket.")],
        koltseg=True, koltseg_megj="", iratok=True,
        gyik=[("Választhatunk temetőt?", "Igen. Miskolcon bármelyik temetkezési szolgáltató bármelyik temetőben temethet."),
              ("Mennyibe kerül?", f"A végösszeg a választott kellékeken, a temető díjain és a búcsúztatáson múlik, ezért pontos árat tételesen tudunk mondani. Árajánlatot munkaidőben telefonon kérhet: {a_tel(IRODA)}."),
              ("Kórházban hunyt el. Mikor jöhetek be?", "Már a halottvizsgálati bizonyítvány előtt is: az időpont kivételével mindent megbeszélhetünk az irodában.")],
    ),
    "koporsos-temetes": dict(
        nev="Koporsós temetés",
        cim="Koporsós temetés Miskolcon, teljes ügyintézéssel",
        bev="Átvesszük a temetés minden teendőjét: az elhunyt elszállítását, a hivatalos ügyeket és a búcsúztatás szervezését. Koporsót, sírjelzőt és sírtáblát a bemutatótermünkben választhat.",
        desc=f"Koporsós temetés teljes ügyintézéssel Miskolcon, 1991 óta. Bemutatóterem a Csabai kapu 16. alatt. Ügyelet éjjel-nappal: {UGYELET}.",
        mit=["Elszállítjuk az elhunytat a haláleset helyéről, majd a temetés helyére.",
             "Intézzük a temetéshez szükséges hivatalos ügyeket.",
             "A bemutatótermünkben koporsót, sírjelzőt vagy fejfát és sírtáblát választhat.",
             "Megszervezzük a búcsúztatást a választott temetőben, egyházi vagy polgári szertartással.",
             "Koszorút friss virágból, megrendelésre készítünk, és díjmentesen kiszállítjuk a temetésre."],
        mit_utan=f"A {TEMETO}t mi üzemeltetjük: ott a sírhely, a sírásás és a ravatalozó ügyében is közvetlenül nálunk intézkedhet.",
        helyorzo="[Egyeztetendő: mit tartalmaz pontosan a koporsós temetés.]",
        lepesek=[("Hívja ügyeletünket", f"Ha az orvos elvégezte a halottvizsgálatot, hívjon minket a nap bármely órájában: {a_tel(UGYELET)}. Az elhunytat az orvos előírása szerint halottasházba vagy kórházi patológiára visszük."),
                 ("Jöjjön be az irodába", "Hozza magával az iratokat, a listát lent találja. Megbeszéljük a búcsúztatás idejét és helyét, és kiválasztja a koporsót és a sírjelzőt."),
                 ("A többit mi intézzük", "A hivatalos ügyeket és a búcsúztatás szervezését átvesszük. Ha közben kérdése van, munkaidőben az irodában, éjjel az ügyeleten elér minket.")],
        koltseg=True, koltseg_megj="Koporsós temetésnél a sírásás díja jóval magasabb, mint urnás temetésnél.", iratok=True,
        gyik=[("Választhatunk temetőt?", "Igen. Miskolcon bármelyik temetkezési szolgáltató bármelyik temetőben temethet."),
              ("Mennyibe kerül?", f"A végösszeg a választott kellékeken, a temető díjain és a búcsúztatáson múlik, ezért pontos árat tételesen tudunk mondani. Árajánlatot munkaidőben telefonon kérhet: {a_tel(IRODA)}."),
              ("Hol választhatok koporsót?", f"A bemutatótermünkben, az irodában: {CIM}, {NYITVA}.")],
    ),
    "halottszallitas": dict(
        nev="Halottszállítás",
        cim="Halottszállítás éjjel-nappal, belföldön és a szomszédos országokból",
        bev="Ügyeletünk a nap bármely órájában hívható, hétvégén is. Elszállítjuk az elhunytat a haláleset helyéről, és ha kell, a szomszédos országokból is hazahozzuk.",
        desc=f"Halottszállítás Miskolcon és környékén, a szomszédos országokból is. Ügyelet éjjel-nappal: {UGYELET}.",
        mit=["Elszállítjuk az elhunytat a haláleset helyéről halottasházba vagy kórházi patológiára, az orvos előírása szerint.",
             "Onnan a temetés helyére vagy a hamvasztóüzembe szállítjuk.",
             "Miskolcon kívül, a környező és távolabbi településekről is."],
        mit_utan="",
        extra="""<h3 class="alcim">A szomszédos országokból</h3>
        <p>Ha szerette külföldön hunyt el, a szomszédos országokból hazaszállítjuk. Ehhez hatósági és konzuli iratok kellenek, például konzuli engedély, hatósági orvosi tanúsítvány és a temető befogadó nyilatkozata: ezek beszerzésében segítünk.</p>""",
        helyorzo="[Egyeztetendő: mely országokból, mennyi idő alatt, és mely iratokat intézik Önök.]",
        lepesek=[("Hívjon minket", f"Éjjel-nappal: {a_tel(UGYELET)}. Mondja el, hol történt a haláleset."),
                 ("Megbeszéljük a részleteket", "Hova, mikor, és milyen iratok kellenek. Külföldi halálesetnél végigvesszük, mit kell beszerezni."),
                 ("Elszállítjuk", "Az elhunytat a szükséges iratokkal, méltósággal szállítjuk a megbeszélt helyre.")],
        koltseg=False, iratok=False,
        gyik=[("Éjjel is hívhatom?", "Igen, ügyeletünk a nap bármely órájában, hétvégén is hívható."),
              ("Mennyibe kerül a szállítás?", f"Árajánlatot munkaidőben telefonon kérhet: {a_tel(IRODA)}."),
              ("A temetést is Önök intézhetik?", "Igen, hamvasztásos és koporsós temetést is vállalunk, teljes ügyintézéssel.")],
    ),
    "kegyeleti-szerzodes": dict(
        nev="Kegyeleti szerződés",
        cim="Kegyeleti szerződés: a temetés előre, egyéni megbeszélés szerint",
        bev="Ha szeretné előre elrendezni a saját vagy egy szerette temetését, kegyeleti szerződést köthet velünk. A részleteket személyesen, egyéni megbeszélés szerint rögzítjük.",
        desc="Kegyeleti szerződés Miskolcon: a temetés részletei előre, egyéni megbeszélés szerint. Iroda: Csabai kapu 16., hétköznap 8:30–15:30.",
        mit_cim="Mit rögzíthet előre?",
        mit=["a temetés módját: hamvasztásos vagy koporsós temetés",
             "a koporsó vagy az urna típusát",
             "a koszorúkat",
             "a búcsúztatást"],
        mit_utan="Így a családnak a gyász napjaiban már nem kell ezekről döntenie.",
        helyorzo="[Egyeztetendő: a fizetés módja és a szerződés további részletei.]",
        lepesek=[("Hívjon, vagy jöjjön be", f"Munkaidőben, {NYITVA}: {a_tel(IRODA)}."),
                 ("Megbeszéljük, mit szeretne", "A temetés módját, a kellékeket és a búcsúztatást, ahogy Önnek fontos."),
                 ("Írásban rögzítjük", "A megbeszélteket szerződésbe foglaljuk.")],
        koltseg=False, iratok=False, fo_tel=IRODA,
        gyik=[("Mennyibe kerül?", "A megbeszélt tételek alapján, egyénileg mondjuk meg."),
              ("Hol köthetem meg?", f"Az irodánkban: {CIM}, {NYITVA}.")],
    ),
}
IKON = {"v1": '<svg class="mecses" aria-hidden="true"><use href="#i-mecses"/></svg>',
        "v2": '<svg class="tabla-jel" aria-hidden="true"><use href="#i-jel"/></svg>',
        "v3": '<svg class="tabla-jel" aria-hidden="true"><use href="#i-jel"/></svg>'}


def aloldal(v, slug):
    a = ALOLDALAK[slug]
    if a.get("fo_tel"):
        gomb = f"""<div class="gombok">
            <a class="gomb gomb-fo" href="{tel(a['fo_tel'])}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás munkaidőben: {a['fo_tel'].replace(" ", NBSP)}</a>
            <a class="gomb gomb-masod" href="mailto:{EMAIL}"><svg aria-hidden="true"><use href="#i-level"/></svg>Email küldése</a>
          </div>"""
    else:
        gomb = gombok()
    mit = "\n".join(f"          <li>{m}</li>" for m in a["mit"])
    mit_utan = f'\n        <p>{a["mit_utan"]}</p>' if a.get("mit_utan") else ""
    lepesek = "\n".join(f"          <li><h3>{c}</h3><p>{t}</p></li>" for c, t in a["lepesek"])
    gyik = "\n".join(f"          <div><dt>{k}</dt><dd>{v_}</dd></div>" for k, v_ in a["gyik"])
    tobbi = "\n".join(f'          <li><a href="../{s}/">{ALOLDALAK[s]["nev"]}</a></li>' for s in ALOLDALAK if s != slug)
    reszek = [f"""<section class="nyito aloldal-nyito" aria-labelledby="nyito-cim">
      <div class="keret nyito-racs">
        <div class="nyito-szoveg">
          <nav class="morzsa" aria-label="Hol jár"><a href="../">Főoldal</a> › <a href="../#szolgaltatasok">Szolgáltatások</a> › <span aria-current="page">{a['nev']}</span></nav>
          <h1 id="nyito-cim">{a['cim']}</h1>
          <p class="bevezeto">{a['bev']}</p>
          {gomb}
        </div>
        {ugyelet_tabla(IKON[v])}
      </div>
    </section>""",
              f"""<section class="szakasz szakasz-alt" id="mit" aria-labelledby="mit-cim">
      <div class="keret">
        {fej('mit', a.get('mit_cim', 'Mit intézünk el Ön helyett?'))}
        <ul class="pipa-lista">
{mit}
        </ul>{mit_utan}
        {a.get('extra', '')}
        <!-- EGYEZTETENDŐ: a részletek a hívásban. -->
        <p class="helyorzo">{a['helyorzo']}</p>
      </div>
    </section>""",
              f"""<section class="szakasz" id="menete" aria-labelledby="menete-cim">
      <div class="keret">
        {fej('menete', 'Így zajlik')}
        <ol class="lepesek">
{lepesek}
        </ol>
      </div>
    </section>"""]
    if a.get("koltseg"):
        megj = f'\n        <p>{a["koltseg_megj"]}</p>' if a.get("koltseg_megj") else ""
        reszek.append(f"""<section class="szakasz szakasz-alt" id="koltseg" aria-labelledby="koltseg-cim">
      <div class="keret">
        {fej('koltseg', 'Miből áll a költség?', 'A végösszeg a választott kellékeken, a temető díjain és a búcsúztatáson múlik. Négy részből áll össze:')}
        {KOLTSEG_RESZEK}{megj}
        <p>Pontos árat tételesen tudunk mondani. Árajánlatot munkaidőben telefonon kérhet: {a_tel(IRODA)}.</p>
      </div>
    </section>""")
    if a.get("iratok"):
        reszek.append(f"""<section class="szakasz" id="iratok" aria-labelledby="iratok-cim">
      <div class="keret">
        {fej('iratok', 'Ezeket hozza magával', 'Otthoni és kórházi halálesetnél is ugyanazok.')}
        <div class="iratok-doboz">
          {IRATOK}
        </div>
        <p class="halvany">Meghatalmazással bárki intézheti a temetést a temettető helyett.</p>
      </div>
    </section>""")
    reszek.append(f"""<section class="szakasz szakasz-alt" id="kerdesek" aria-labelledby="kerdesek-cim">
      <div class="keret">
        {fej('kerdesek', 'Gyakori kérdések')}
        <dl class="kerdesek">
{gyik}
        </dl>
        <h3 class="alcim">További szolgáltatásaink</h3>
        <ul class="tovabbi-szolg">
{tobbi}
          <li><a href="../#szolgaltatasok">Minden szolgáltatás</a></li>
        </ul>
      </div>
    </section>""")
    reszek.append(kapcsolat(v))
    return "\n\n    ".join(reszek)


# ---- „Kérései és a javítások” (értékesítési réteg) és az értesítő adatai ----
HONAP = ["január", "február", "március", "április", "május", "június", "július", "augusztus", "szeptember",
         "október", "november", "december"]


def ido_szoveg(ido):
    datum, ora = ido.split(" ")
    _, h, n = datum.split("-")
    return f"{HONAP[int(h) - 1][:3]}. {int(n)}., {ora}"


def oldal_neve(utvonal):
    reszek = [r for r in utvonal.split("/") if r]
    nev = VALTOZATOK[reszek[0]]["nev"] + " változat" if reszek and reszek[0] in VALTOZATOK else "Választó"
    if len(reszek) > 1 and reszek[1] in ALOLDALAK:
        nev += ", " + ALOLDALAK[reszek[1]]["nev"]
    return nev


def keresek_oldal():
    esc = html.escape
    osszes = [k for kor in KOROK for k in kor["keresek"]]
    db = {a: sum(1 for k in osszes if k["allapot"] == a) for a in ALLAPOT}
    osszesito = f"Összesen {len(osszes)} kérés: {db['kesz']} kész" + (f", {db['var']} Önökre vár" if db["var"] else "") + (f", {db['folyamatban']} folyamatban" if db["folyamatban"] else "") + "."
    korok = []
    for kor in KOROK:
        li = []
        for k in kor["keresek"]:
            hol = ", ".join(f'<a href="..{u}">{esc(c)}</a>' for u, c in k["hol"]) or "a szakasz kikerült"
            szoveg = "<br>".join(esc(sor) for sor in k["szoveg"].split("\n"))
            li.append(f"""        <li class="keres keres-{k['allapot']}">
          <p class="keres-meta"><span class="allapot">{ALLAPOT[k['allapot']]}</span> {ido_szoveg(k['ido'])} · {oldal_neve(k['oldal'])} · „{esc(k['resz'])}”</p>
          <blockquote class="keres-szoveg"><p>{szoveg}</p></blockquote>
          <p class="keres-mit"><strong>Mit csináltunk:</strong> {esc(k['mit'])}</p>
          <p class="keres-hol"><strong>Hol látja:</strong> {hol}</p>
        </li>""")
        korok.append(f"""    <section class="kor" id="kor-{kor['id']}" aria-labelledby="kor-{kor['id']}-cim">
      <h2 id="kor-{kor['id']}-cim">{kor['cim']}</h2>
      <ol class="keres-lista">
{chr(10).join(li)}
      </ol>
    </section>""")
    return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Kérései és a javítások – Pietas Temetkezés (bemutató)</title>
  <meta name="description" content="Amit a Pietas Temetkezés a bemutató oldalon kért, és amit javítottunk.">
  {ICON}
  <link rel="stylesheet" href="../assets/valaszto.css">
  <!-- ÉRTÉKESÍTÉSI RÉTEG (élesítéskor törlendő): az ügyfél kérései és a javítások (anyagok/keresek.py) -->
  <link rel="stylesheet" href="../assets/keresek.css">
  <script src="../assets/keresek.js" defer></script>
  <link rel="stylesheet" href="../assets/ki-keszitette.css">
  <script src="../assets/ki-keszitette.js" defer></script>
  <link rel="stylesheet" href="../assets/foglalo.css">
  <script src="../assets/foglalo.js" defer></script>
</head>
<body class="keresek-oldal" data-kor-latta="{KOROK[0]['id']}">
  <div class="bemutato-sav" role="note"><p><strong>Bemutató – nem a {CEG} hivatalos weboldala.</strong> <a href="../">Vissza a három változathoz</a></p></div>
  <main class="keret">
    <h1>Kérései és a javítások</h1>
    <p class="bevezeto">Itt követheti, mit kért a bemutató oldalon, mit csináltunk, és hol látja. Szó szerint idézzük, amit a szakaszok alatt az „Ezt másképp” gombbal írt. A legújabb van felül.</p>
    <p class="osszesito">{osszesito}</p>
{chr(10).join(korok)}
    <p class="tovabb-kerdes">Ha valamit még másképp szeretne, a változatokban a szakaszok alatt továbbra is jelezheti: ide kerül, és itt látja, mikor készült el.</p>
  </main>
  <footer class="lablec-egyszeru"><p>Bemutató a {CEG} részére · webness.hu · <a href="../adatkezeles/">Adatkezelési tájékoztató</a></p></footer>
</body>
</html>
"""


def valtozasok_json():
    """Az értesítő (gyorsweb: eszkozok/ertesito/) ebből látja, melyik kör élesedett."""
    korok = []
    for kor in KOROK:
        k = kor["keresek"]
        korok.append({"id": kor["id"], "cim": kor["cim"], "keresek": len(k),
                      "kesz": sum(1 for x in k if x["allapot"] == "kesz"),
                      "var": sum(1 for x in k if x["allapot"] == "var"),
                      "ertesites": kor["ertesites"]})
    return json.dumps({"ceg": "temetkezes-miskolc-pietas", "nev": CEG, "url": DEMO_URL,
                       "keresek_oldal": DEMO_URL + "/keresek/", "korok": korok}, ensure_ascii=False, indent=1)


# ---- Választó és ajánlatoldal: ugyanazok a kártyák ----
def kartyak(elotag="", cim_tag="h2"):
    out = []
    for i, (v, d) in enumerate(VALTOZATOK.items(), 1):
        out.append(f"""      <li class="valtozat">
        <div class="elonezet">
          <img class="asztali" src="{elotag}valaszto/{v}-asztali.webp" alt="" width="720" height="450">
          <img class="mobil" src="{elotag}valaszto/{v}-mobil.webp" alt="" width="195" height="422">
        </div>
        <div class="test">
          <p class="szam">{i}. változat</p>
          <{cim_tag} class="kartya-cim">{d['nev']}</{cim_tag}>
          <p class="leir">{d['leiras']}</p>
          <p class="tz-szam" data-tz-oldal="/{v}/" hidden></p>
          <a class="megnez" href="{elotag}{v}/">Megnézem a {d['nev']} változatot</a>
        </div>
      </li>""")
    return "\n".join(out)


VELEMENY_RESZ = """<section class="valaszto-velemenyek" aria-labelledby="vel-cim">
      <h2 id="vel-cim">Akiknek már készítettem weboldalt</h2>
      <p class="halvany"><span data-kk-szam>16</span> ügyfél, az ő szavaikkal, változtatás nélkül, ahogy a webness.hu-n is olvashatók.</p>
      <div data-kk-velemenyek></div>
      <p class="vel-hivas">Kérdése van? Beszéljük meg 15 percben: <a href="#idopont" data-foglalo="valaszto">Időpontot foglalok</a></p>
    </section>"""


def valaszto():
    return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Pietas Temetkezés – három változat az új weboldalra (bemutató)</title>
  <meta name="description" content="Három változat a Pietas Temetkezés weboldalára.">
  {ICON}
  <link rel="stylesheet" href="assets/valaszto.css">
  <!-- ÉRTÉKESÍTÉSI RÉTEG (élesítéskor törlendő) -->
  <link rel="stylesheet" href="assets/ki-keszitette.css">
  <script src="assets/ki-keszitette.js" defer></script>
  <link rel="stylesheet" href="assets/foglalo.css">
  <script src="assets/foglalo.js" defer></script>
  <script src="assets/tetszik.js" defer></script>
  <link rel="stylesheet" href="assets/keresek.css">
  <script src="assets/keresek.js" defer></script>
</head>
<body>
  <div class="bemutato-sav" role="note"><p><strong>Bemutató ajánlat – nem a {CEG} hivatalos weboldala.</strong> Csak Ön látja. <a href="keresek/">Kérései és a javítások</a></p></div>
  {valtozas_sav("")}
  <main class="keret">
    <h1>Három változat a {CEG} weboldalára</h1>
    <p class="bevezeto">A tartalom mindháromban ugyanaz: a 24 órás ügyelet egy érintéssel hívható száma, a teendők haláleset után, a szükséges iratok, hogy miből áll a költség, és az iroda nyitvatartása. A különbség az arculat és a hangsúly. Nézze meg mindhármat, és jelölje meg, mi tetszik.</p>

    <!-- Változatkártyák: sites/_sablonok/_valaszto/ (gyorsweb; képek: elonezet.py) -->
    <ul class="valtozatok">
{kartyak()}
    </ul>
    <p class="tovabb"><a href="ajanlat/">Mit hoz az új oldal, és ki készítette?</a></p>

    {VELEMENY_RESZ}
  </main>
</body>
</html>
"""


def ajanlat():
    return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Weboldal a Pietas Temetkezés részére – miért készült, és ki készítette (bemutató)</title>
  <meta name="description" content="Miért készült weboldal-bemutató a Pietas Temetkezés részére, mit találtunk, és ki készítette.">
  {ICON}
  <link rel="stylesheet" href="../assets/valaszto.css">
  <link rel="stylesheet" href="../assets/ajanlat.css">
  <!-- ÉRTÉKESÍTÉSI RÉTEG (élesítéskor törlendő) -->
  <link rel="stylesheet" href="../assets/ki-keszitette.css">
  <script src="../assets/ki-keszitette.js" defer></script>
  <link rel="stylesheet" href="../assets/foglalo.css">
  <script src="../assets/foglalo.js" defer></script>
  <script src="../assets/tetszik.js" defer></script>
  <!-- Cloudflare Web Analytics (sütimentes) – token élesítés előtt:
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "[CLOUDFLARE_TOKEN]"}}'></script>
  -->
</head>
<body>
  <a class="ugras" href="#tartalom">Ugrás a tartalomra</a>
  <div class="bemutato-sav" role="note">
    <p><strong>Bemutató – nem a {CEG} hivatalos weboldala.</strong> <a href="../">Vissza a három változathoz</a></p>
  </div>

  <main id="tartalom">
    <section class="keret nyit">
      <h1>Miért készült ez az oldal, és ki készítette?</h1>
      <!-- KÖZÖS PONT: egy mondat, részletek nélkül (SZABALYOK.md). Marcell döntse el, van-e ismeretség (lásd adatok.md, „Nyitott kérdések”). -->
      <p>Szikora Marcell vagyok, weboldalakat készítek (webness.hu). Tiszanagyfaluban lakom, itt a környéken.</p>
      <p>A mostani weboldalukon a fontos tudnivalók több aloldalon vannak, és a telefonszámok mobilon nem hívhatók egy érintéssel. A nyilvános anyagaikból elkészítettem három változatot, hogy ne kelljen elképzelni, milyen lehetne: ki lehet próbálni, telefonon is.</p>
      <p class="alairas">Szikora Marcell<br><small>webness.hu</small></p>
    </section>

    <section class="sav-vilagos">
      <div class="keret">
        <h2>Mit találtunk?</h2>
        <p class="halvany">Három dolog, ami azokat érinti, akik most keresnek temetkezési szolgáltatót Miskolcon. Ellenőrizve: 2026. november 13.</p>

        <ol class="problemak">
          <li>
            <h3>Telefonról nem lehet egy érintéssel hívni</h3>
            <dl>
              <div><dt>Most</dt><dd>Egyik telefonszám sem kattintható. A 24 órás ügyelet száma a kezdőlap szövegének alján és egy aloldal közepén áll. Az oldal mobilon a nagyítást is letiltja.</dd></div>
              <div class="uj"><dt>Az új oldalon</dt><dd>Az első képernyőn ott a „Hívás éjjel-nappal” gomb, és telefonon görgetés közben is mindig látszik. Minden szám egy érintéssel hívható.</dd></div>
            </dl>
          </li>
          <li>
            <h3>Elavult és üres részek</h3>
            <dl>
              <div><dt>Most</dt><dd>A kezdőlapon még a járvány idejéből maradt kérés áll. A temető üzemeltetéséről „közel 2 éve” olvasható, pedig 2008 óta tart. A „Szórásos” oldal üres, a Kapcsolat oldalon a térkép helye üres.</dd></div>
              <div class="uj"><dt>Az új oldalon</dt><dd>Friss, ellenőrzött tények: 1991 óta, 2008 óta a {TEMETO}, a temető címe és nyitvatartása, útvonal az irodához és a temetőhöz.</dd></div>
            </dl>
          </li>
          <li>
            <h3>Aki most veszítette el valakijét, nem kap egy helyen választ</h3>
            <dl>
              <div><dt>Most</dt><dd>A teendők, az iratok, a költségek és a nyitvatartás öt külön aloldalon vannak. A díjmentes elszállítás és koszorú-kiszállítás alig látszik.</dd></div>
              <div class="uj"><dt>Az új oldalon</dt><dd>Egy oldalon, sorrendben: kit hívjon, mit hozzon, miből áll a költség, mikor van nyitva az iroda. Az előnyök jól látható helyen.</dd></div>
            </dl>
          </li>
        </ol>

        <div class="tipp">
          <h3>Ingyenes tipp, az oldaltól függetlenül</h3>
          <p>Az „Észak gyászhirdetés” aloldal utolsó bekezdésébe valaki egy oda nem illő mondatot és reklámlinket tett, egy „virtuális barátnő” szolgáltatásra. Ezt látja minden család, aki erre az aloldalra jut. Feltört WordPressre vagy illetéktelen hozzáférésre utalhat. Mivel a gyászhirdetést már nem vállalják, az aloldal egészében törölhető; emellett érdemes az admin-jelszavakat lecserélni, és a WordPresst a bővítményekkel együtt frissíteni. Szívesen megmutatom, hol van.</p>
        </div>

        <h3>Amit még beletettem</h3>
        <ul class="apro">
          <li>„Amit a családok először kérdeznek”: rövid válaszok a leggyakoribb kérdésekre, a mostani oldal tájékoztatóiból.</li>
          <li>A temetés költségének tételei egy helyen, a gyakori kérdések között.</li>
          <li>Hely a családok véleményének és néhány saját fotónak: ezeket a hívásban pontosítjuk.</li>
          <li>A logót vektorosan újrarajzoltam, hogy minden méretben éles legyen. Az eredeti fájl jobb lenne.</li>
        </ul>
        <!-- MÉRÉS: PageSpeed (régi oldal, Marcell méri) és Lighthouse (új oldal), mobil – elemzes.md. -->
        <p class="meres">Az új oldal mindhárom változata a Google Lighthouse mérésén mobilon: [LIGHTHOUSE_EREDMENY].</p>
      </div>
    </section>

    <section class="keret">
      <h2>Három változat</h2>
      <p class="halvany">A tartalom ugyanaz, az arculat és a hangsúly más. Mindegyik változatban részenként jelezheti, mi tetszik és min változtatna; a lap alján összegyűjtjük, és ott időpontot is foglalhat egy rövid beszélgetésre.</p>
      <ul class="valtozatok">
{kartyak('../', 'h3')}
      </ul>
    </section>

    <section class="sav-vilagos" aria-labelledby="gyik-cim">
      <div class="keret">
        <h2 id="gyik-cim">Gyakori kérdések</h2>
        <dl class="gyik">
          <dt>Mit kell nekünk csinálni?</dt>
          <dd>Szinte semmit: a tartalom a mostani weboldalukról van. Egy rövid hívásban átnézzük, mi tetszik, és kérek néhány dolgot: az eredeti logót, pár fotót az irodáról, és hogy mely adatok változtak.</dd>
          <dt>Mi lesz a mostani oldallal és a címmel?</dt>
          <dd>A pietas-temetkezes.hu cím marad, csak az új oldal kerül mögé. A régi aloldalak címeit átirányítjuk, így a Google-találatok sem vesznek el.</dd>
          <dt>Kell-e ehhez WordPress-t frissítgetni?</dt>
          <dd>Nem. Az új oldalon nincs bővítmény és admin-felület, így nincs mit frissítgetni, és a feltörés esélye is jóval kisebb.</dd>
          <dt>Mibe kerül?</dt>
          <dd>Ezt a hívásban, a kívánságaik alapján beszéljük meg, és írásban is elküldöm. Ha nem kérik, a bemutatót töröljük.</dd>
        </dl>
      </div>
    </section>

    <section class="keret ki" id="ki" aria-labelledby="ki-cim">
      <img class="portre" src="https://webness.hu/assets/marcell.jpg" alt="Szikora Marcell portréja" width="800" height="1000" loading="lazy">
      <div>
        <h2 id="ki-cim">Ki készítette?</h2>
        <p>Szikora Marcell vagyok, szoftvermérnök, a Webness alapítója. Gyerekkorom óta programozom: több mint 15 év alatt 116+ weboldalt, webshopot és üzleti rendszert adtam át. Az Accenture-nél vezető fejlesztő voltam, ma a WorkFlex nemzetközi startupnál vagyok tech lead.</p>
        <p>Kis családi vállalkozásoknak és nagy cégeknek is dolgozom, például a Salzgitter Mannesmann, a D-Link, a Miskolci Nemzeti Színház, a Jánosik és Társai és az Orha Művek számára. Velem közvetlenül dolgoznak: azzal beszélnek, aki a megoldást megtervezi és megírja.</p>
      </div>
    </section>

    <section class="sav-vilagos" aria-labelledby="vel-cim">
      <div class="keret">
        <h2 id="vel-cim">Akikkel már dolgoztam</h2>
        <p class="halvany"><span data-kk-szam>16</span> ügyfél, az ő szavaikkal, változtatás nélkül, ahogy a webness.hu-n is olvashatók.</p>
        <div data-kk-velemenyek></div>
      </div>
    </section>

    <section class="keret zaro hivas-resz" aria-labelledby="hivas-cim">
      <h2 id="hivas-cim">Kérdése van? Beszéljük meg 15 percben</h2>
      <p class="halvany">Azzal beszél, aki az oldalt megtervezte és megírta. Telefonon hívom, vagy Google Meeten beszélünk, ahogy Önnek kényelmesebb.</p>
      <p class="hivas-sor"><a class="gomb gomb-fo hivas-gomb" href="#idopont" data-foglalo="ajanlat">Időpontot foglalok</a></p>
      <p><a href="../">Vissza a három változathoz</a></p>
    </section>
  </main>

  <footer class="lablec">
    <div class="keret">
      <p>Bemutató a {CEG} részére · webness.hu · <a href="../adatkezeles/">Adatkezelési tájékoztató</a></p>
    </div>
  </footer>
</body>
</html>
"""


if __name__ == "__main__":
    for v, d in VALTOZATOK.items():
        (SITE / v).mkdir(parents=True, exist_ok=True)
        (SITE / v / "index.html").write_text(oldal(v, d), encoding="utf-8")
        for slug, a in ALOLDALAK.items():
            (SITE / v / slug).mkdir(exist_ok=True)
            (SITE / v / slug / "index.html").write_text(
                oldal(v, d, tartalom=aloldal(v, slug), gy="../../", menu_elotag="../", marka_href="../",
                      title=f"{a['nev']} Miskolcon – Pietas Temetkezés (bemutató)", desc=a["desc"]), encoding="utf-8")
    (SITE / "keresek").mkdir(exist_ok=True)
    (SITE / "keresek" / "index.html").write_text(keresek_oldal(), encoding="utf-8")
    (SITE / "valtozasok.json").write_text(valtozasok_json(), encoding="utf-8")
    (SITE / "index.html").write_text(valaszto(), encoding="utf-8")
    import ajanlat_oldal  # az ajánlatoldal: anyagok/ajanlat_oldal.py (sablon: gyorsweb sites/_sablonok/_ajanlat/)
    ajanlat_oldal.main()
    print("ok")
