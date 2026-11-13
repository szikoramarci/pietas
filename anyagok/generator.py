#!/usr/bin/env python3
"""A Pietas Temetkezés demó három változata, a választó és az ajánlatoldal egy tartalomból.

Használat (a repó gyökeréből):
    python3 anyagok/generator.py site

Minden tény az anyagok/adatok.md-ből jön (a régi weboldal, 2026-11-13). Ami a mi szövegünk és az
ügyfél anyagaiban nincs, azt a HTML-ben „EGYEZTETENDŐ” megjegyzés jelöli; ami hiányzik, az látható
[helyőrző]. Mindhárom változat magáz. Az ügyvezető neve nem kerül az oldalra (SZABALYOK.md).
A logó a régi oldal logójáról vektorosan lekövetve (anyagok/logo/); az eredeti fájl kérendő.
"""
import re
import sys
import pathlib

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
ANYAG = pathlib.Path(__file__).resolve().parent

CEG = "Pietas Temetkezés"
CEG_TELJES = "PIETAS Kft. – Teljeskörű temetkezési szolgálat"
NBSP = " "


def tel(szam):
    """06-os belföldi formából tel: link (+36...)."""
    d = re.sub(r"\D", "", szam)
    return "tel:+36" + d[2:] if d.startswith("06") else "tel:+" + d


UGYELET = "06 20 235 3603"
IRODA = "06 46 431 014"
MOBIL = "06 70 947 5490"
KOSZORU = "06 20 523 4394"
TOVABBI = ["06 20 368 6533", "06 70 947 5790"]
EMAIL = "miskolcipietas@gmail.com"
CIM = "3529 Miskolc, Csabai kapu 16."
TERKEP = "https://www.google.com/maps/search/?api=1&amp;query=Miskolc%2C+Csabai+kapu+16."
NYITVA = 'hétfőtől péntekig <span class="nowrap">8:30–16:00</span>'


def a_tel(szam, cls="tel"):
    return f'<a class="{cls}" href="{tel(szam)}">{szam.replace(" ", NBSP)}</a>'


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
               rend=["nyito", "ismeros", "teendok", "szolgaltatasok", "koltsegek", "rolunk", "velemenyek", "hol", "kapcsolat"],
               leiras="Mélyzöld, nyugodt színek, a nyitóképen mécsesfénnyel a 24 órás ügyelet száma. Nagy, jól olvasható betűk, a telefonszámok mindig kiemelve."),
    "v2": dict(nev="Ív", theme="#592131", preload="sourceserif4.woff2",
               rend=["nyito", "szolgaltatasok", "teendok", "ismeros", "rolunk", "koltsegek", "velemenyek", "hol", "kapcsolat"],
               leiras="A mostani arculat felújítva: a logó sírkő-íve, a bordó és a borostyán szín, papírszerű háttér. A szolgáltatások kerülnek előre."),
    "v3": dict(nev="Liliom", theme="#F7F7F4", preload="cormorantgaramond.woff2",
               rend=["nyito", "teendok", "ismeros", "szolgaltatasok", "koltsegek", "rolunk", "velemenyek", "hol", "kapcsolat"],
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
            <li>a hejőcsabai temető üzemeltetője</li>
          </ul>"""

IRODA_SOR = f'<p class="nyito-info">Iroda: {CIM}, {NYITVA}, {a_tel(IRODA)}</p>'


def fej(id_, cim, bev=None):
    b = f'\n        <p class="bevezeto-kicsi">{bev}</p>' if bev else ""
    return f'<h2 id="{id_}-cim">{cim}</h2>{b}'


OTTHON_LEPESEK = f"""<ol class="lepesek">
          <li><h3>Hívja a háziorvost vagy az orvosi ügyeletet</h3><p>Az orvos elvégzi a halottvizsgálatot, kiállítja a bizonyítványt, és engedélyezi az elszállítást.</p></li>
          <li><h3>Hívja ügyeletünket: {a_tel(UGYELET)}</h3><p>A nap bármely órájában. Az orvos előírása szerint az elhunytat halottasházba vagy kórházi patológiára visszük.</p></li>
          <li><h3>Jöjjön be az irodába</h3><p>Hozza a halottvizsgálati bizonyítványt. Itt megbeszéljük a temetés részleteit, a többi ügyintézést mi végezzük.</p></li>
        </ol>"""


# ---- Szakaszok ----
def nyito(v):
    if v == "v1":
        return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret nyito-racs">
        <div class="nyito-szoveg">
          <p class="felcim">Pietas Temetkezés, Miskolc</p>
          <h1 id="nyito-cim">Temetés teljes ügyintézéssel, Miskolcon 1991 óta</h1>
          <p class="bevezeto">Átvesszük a temetés minden teendőjét: az elhunyt elszállítását, a hivatalos ügyeket, a gyászhirdetést és a búcsúztatás szervezését.</p>
          {TENYEK}
          {gombok()}
        </div>
        <aside class="ugyelet-tabla" aria-label="Ügyelet és iroda">
          <svg class="mecses" aria-hidden="true"><use href="#i-mecses"/></svg>
          <p class="tabla-cimke">24 órás ügyelet</p>
          <p class="tabla-szam">{a_tel(UGYELET)}</p>
          <dl>
            <div><dt>Iroda, {NYITVA}</dt><dd>{a_tel(IRODA)}</dd></div>
            <div><dt>Címünk</dt><dd>{CIM}</dd></div>
          </dl>
        </aside>
      </div>
    </section>"""
    if v == "v2":
        return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret nyito-racs">
        <div class="nyito-szoveg">
          <p class="felcim">Pietas Temetkezés, Miskolc</p>
          <h1 id="nyito-cim">Teljeskörű temetkezési szolgálat Miskolcon, 1991 óta</h1>
          <p class="bevezeto">Hamvasztásos és koporsós temetés, gyászhirdetés, koszorú és halottszállítás egy helyen, a Csabai kapuban. Ügyeletünk éjjel is hívható.</p>
          {gombok()}
          {IRODA_SOR}
        </div>
        <div class="nyito-jel">
          <svg class="nagy-jel" aria-hidden="true"><use href="#i-jel"/></svg>
          {TENYEK}
        </div>
      </div>
    </section>"""
    return f"""<section class="nyito" aria-labelledby="nyito-cim">
      <div class="keret">
        <p class="felcim">Pietas Temetkezés, Miskolc, 1991 óta</p>
        <h1 id="nyito-cim">Haláleset történt? Hívjon minket, éjjel is.</h1>
        <p class="bevezeto">Teljes körű temetkezés Miskolcon: a temetés minden ügyintézését átvesszük.</p>
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
          <div><dt>Mennyibe kerül a temetés?</dt><dd>A választott kellékeken és a temető díjain múlik. Árajánlatot telefonon kérhet: {a_tel(IRODA)}. <a href="#koltsegek">Miből áll a költség?</a></dd></div>
          <div><dt>Választhatunk temetőt?</dt><dd>Igen. Miskolcon bármelyik temetkezési szolgáltató bármelyik temetőben temethet.</dd></div>
          <div><dt>Hazavihetjük az urnát?</dt><dd>Igen, ez az urnakiadás. Jóval kevesebbe kerül, mert nincs temetés, temetői és búcsúztatási díj.</dd></div>
        </dl>
      </div>
    </section>"""


def teendok(v):
    otthon = "" if v == "v3" else f"""<h3 class="alcim">Ha otthon történt</h3>
        {OTTHON_LEPESEK}
        <p class="kiemelt-sor">Ha a temetést is ránk bízza, Miskolcon belül az elszállítás díjmentes.</p>"""
    cim = {"v1": "Haláleset után: ezt tegye, ebben a sorrendben",
           "v2": "Mi a teendő haláleset után?",
           "v3": "Kórházban történt? És milyen iratokat hozzon?"}[v]
    v3_dij = '<p class="kiemelt-sor">Ha a temetést is ránk bízza, Miskolcon belül az elszállítás díjmentes.</p>' if v == "v3" else ""
    return f"""<section class="szakasz" id="teendok" aria-labelledby="teendok-cim">
      <div class="keret">
        {fej('teendok', cim)}
        {otthon}{v3_dij}
        <div class="ketoszlop">
          <div>
            <h3 class="alcim">Ha kórházban történt</h3>
            <p>A halottvizsgálati bizonyítványt és a haláleset bejelentéséről szóló jegyzőkönyvet a kórház adja át. Ez néhány napig is tarthat.</p>
            <p>Addig is jöjjön be az irodába: az időpont kivételével mindent megbeszélhetünk.</p>
          </div>
          <div>
            <h3 class="alcim">Ezeket hozza magával</h3>
            <ul class="iratok">
              <li>az elhunyt személyi igazolványa és lakcímkártyája</li>
              <li>a halottvizsgálati bizonyítvány</li>
              <li>születési vagy házassági anyakönyvi kivonat, ha megvan; ha nem, segítünk beszerezni</li>
              <li>külföldi elhunytnál az útlevél</li>
            </ul>
            <p class="halvany">A statisztikai lapot otthoni halálesetnél az irodában töltjük ki.</p>
          </div>
        </div>
        <!-- EGYEZTETENDŐ: a régi kezdőlap járványügyi szövegéből; marad-e. -->
        <p class="halvany">Ha Ön beteg, meghatalmazottja is megrendelheti a temetést.</p>
      </div>
    </section>"""


SZOLG = [
    ("Hamvasztásos temetés", "Teljes ügyintézéssel. Ha az urnát otthon helyeznék el, urnakiadást intézünk."),
    ("Koporsós temetés", "Teljes ügyintézéssel. Koporsót, sírjelzőt és sírtáblát a bemutatótermünkben választhat."),
    ("Gyászhirdetés az Észak-Magyarországban", "Irodánkból adjuk fel, azonnali visszaigazolással: gyászhirdetés, köszönetnyilvánítás, megemlékezés."),
    ("Koszorú friss virágból", f"Csak megrendelésre készül, katalógusból választhat, és díjmentesen kiszállítjuk a temetésre. Más városba is küldhet: {a_tel(KOSZORU)}."),
    ("Kegyeleti szerződés", "Előre rögzítheti a temetés módját, a koporsót vagy urnát, a hirdetés szövegét és a búcsúztatást. Fizethet egy összegben vagy két részletben."),
    ("Halottszállítás", "Belföldön, és Európa szinte minden országából vagy országába, a szükséges hatósági és konzuli iratokkal."),
]


def szolgaltatasok(v):
    cim = {"v1": "Temetés és minden, ami hozzá tartozik",
           "v2": "Szolgáltatásaink egy helyen",
           "v3": "Amiben segítünk"}[v]
    li = "\n".join(f'          <li><h3>{c}</h3><p>{t}</p></li>' for c, t in SZOLG)
    return f"""<section class="szakasz szakasz-alt" id="szolgaltatasok" aria-labelledby="szolgaltatasok-cim">
      <div class="keret">
        {fej('szolgaltatasok', cim, 'A temetéshez szükséges hivatali ügyeket is mi intézzük.')}
        <ul class="szolg-lista">
{li}
        </ul>
        <div class="temeto">
          <h3>A Hejőcsabai Római Katolikus Temető üzemeltetője</h3>
          <p>2008 óta mi üzemeltetjük. Sírhely, sírásás és ravatalozó ügyében hozzánk forduljon. Sírkőmunkát a sírkövesnek kell bejelentenie az irodánkban, a családnak elég telefonon szólnia.</p>
          <!-- EGYEZTETENDŐ: a temető címe és nyitvatartása. -->
          <p class="helyorzo">[A temető címe és nyitvatartása: egyeztetendő]</p>
        </div>
      </div>
    </section>"""


HIRDETES = [("2/25", 10160), ("2/50", 15240), ("2/75", 22860), ("2/100", 30480), ("2/125", 37500), ("2/150", 45720)]


def ft(n):
    return f"{n:,}".replace(",", NBSP) + f"{NBSP}Ft"


def koltsegek(v):
    sorok = "\n".join(
        f'              <tr{" class=\"ajanlott\"" if m == "2/50" else ""}><th scope="row">{m}</th><td>{ft(a)}</td></tr>' for m, a in HIRDETES)
    return f"""<section class="szakasz" id="koltsegek" aria-labelledby="koltsegek-cim">
      <div class="keret">
        {fej('koltsegek', 'Mennyibe kerül? Ebből áll össze a számla', f'A végösszeg a választott kellékeken múlik, ezért pontos árat csak tételesen tudunk mondani. Árajánlatot telefonon kérhet: {a_tel(IRODA)}.')}
        <div class="ketoszlop">
          <div>
            <h3 class="alcim">A temetkezési számla</h3>
            <ul>
              <li>a szolgáltatás díja</li>
              <li>a választott termékek: koporsó vagy urna, sírjelző vagy fejfa, sírtábla, urnánál urnaterítő és keszon</li>
            </ul>
            <h3 class="alcim">Amivel még számolni kell</h3>
            <ul>
              <li>a temető díjai (ravatalozó, sírásás); koporsós temetésnél a sírásás jóval drágább</li>
              <li>kórházi díjak (öltöztetés, hűtés)</li>
              <li>virág és búcsúztatás</li>
            </ul>
            <p>Urnakiadásnál a költség jóval kisebb, mert nincs temetés.</p>
            <!-- EGYEZTETENDŐ: ha vállalják, tájékoztató „-tól” árak. Marcell a hívásban kérdezzen rá. -->
            <p class="helyorzo">[Tájékoztató ár: hamvasztásos temetés …-tól, koporsós temetés …-tól – egyeztetendő]</p>
          </div>
          <div>
            <h3 class="alcim">Gyászhirdetés az Észak-Magyarországban</h3>
            <!-- EGYEZTETENDŐ: az árak a régi weboldalról, dátum nélkül; aktuálisak-e. -->
            <table class="arak">
              <caption class="halvany">Méret és ár</caption>
              <tbody>
{sorok}
              </tbody>
            </table>
            <p class="halvany">Gyászhirdetéshez a 2/50-es méretet javasoljuk: belefér egy jelkép és egy rövid idézet. Köszönetnyilvánításhoz a 2/25 elég.</p>
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
            <li>2008 óta üzemeltetjük a Miskolc-Hejőcsabai Római Katolikus Temetőt.</li>
            <li>Alapító tagjai vagyunk a Magyar Temetkezési Szolgáltatók Országos Szakegyesületének.</li>
          </ul>
        </div>
        <figure class="foto-hely" aria-label="Fotó helye">
          <p>[Ide kerül egy fotó az irodáról vagy a bemutatóteremről]</p>
        </figure>
      </div>
    </section>"""


def velemenyek(v):
    return f"""<section class="szakasz" id="velemenyek" aria-labelledby="velemenyek-cim">
      <!-- VÉLEMÉNYEK: csak valós, hozzájárulással közölt vélemény kerülhet ide (Fttv.). Most helyőrzők. -->
      <div class="keret">
        {fej('velemenyek', 'Amit a családok írtak rólunk')}
        <div class="velemeny-racs">
          <figure class="velemeny-hely"><blockquote><p>[Ide kerül egy család véleménye, az írója hozzájárulásával.]</p></blockquote><figcaption>[Név vagy monogram]</figcaption></figure>
          <figure class="velemeny-hely"><blockquote><p>[Ide kerül egy második vélemény, az írója hozzájárulásával.]</p></blockquote><figcaption>[Név vagy monogram]</figcaption></figure>
          <figure class="velemeny-hely"><blockquote><p>[Ide kerül egy harmadik vélemény, az írója hozzájárulásával.]</p></blockquote><figcaption>[Név vagy monogram]</figcaption></figure>
        </div>
      </div>
    </section>"""


def hol(v):
    return f"""<section class="szakasz szakasz-alt" id="hol" aria-labelledby="hol-cim">
      <div class="keret">
        {fej('hol', 'Csabai kapu 16., hétköznap 8:30–16:00')}
        <div class="ketoszlop">
          <div>
            <h3 class="alcim"><svg aria-hidden="true"><use href="#i-ora"/></svg>Nyitvatartás</h3>
            <table class="nyitva">
              <tbody>
                <tr><th scope="row">Iroda, hétfő–péntek</th><td>8:30–16:00</td></tr>
                <tr><th scope="row">Ügyelet</th><td>éjjel-nappal, hétvégén is</td></tr>
              </tbody>
            </table>
            <p class="halvany">Emailt a nap bármely szakában írhat.</p>
          </div>
          <div>
            <h3 class="alcim"><svg aria-hidden="true"><use href="#i-hely"/></svg>Iroda és bemutatóterem</h3>
            <p>{CIM}, földszint</p>
            <p><a class="gomb gomb-masod" href="{TERKEP}"><svg aria-hidden="true"><use href="#i-hely"/></svg>Útvonal a Csabai kapuhoz</a></p>
            <p class="helyorzo">[Parkolás a közelben: egyeztetendő]</p>
          </div>
        </div>
      </div>
    </section>"""


def kapcsolat(v):
    tovabbi = ", ".join(a_tel(s) for s in TOVABBI)
    return f"""<section class="szakasz kapcsolat" id="kapcsolat" aria-labelledby="kapcsolat-cim">
      <div class="keret">
        {fej('kapcsolat', 'Hívjon, éjjel is felvesszük', 'Telefonon a leggyorsabb. Árajánlatot munkaidőben az irodai számon adunk.')}
        <p class="kapcs-gomb"><a class="gomb gomb-fo" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás éjjel-nappal: {UGYELET.replace(" ", NBSP)}</a></p>
        <dl class="adatok">
          <div><dt>Ügyelet, 0–24 óra</dt><dd>{a_tel(UGYELET)}</dd></div>
          <div><dt>Iroda, munkaidőben</dt><dd>{a_tel(IRODA)}</dd></div>
          <div><dt>Mobil</dt><dd>{a_tel(MOBIL)}</dd></div>
          <div><dt>Koszorúrendelés</dt><dd>{a_tel(KOSZORU)}</dd></div>
          <div><dt>További számok, munkaidőben</dt><dd>{tovabbi}</dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Cím</dt><dd>{CIM}</dd></div>
        </dl>
      </div>
    </section>"""


SZAKASZOK = dict(nyito=nyito, ismeros=ismeros, teendok=teendok, szolgaltatasok=szolgaltatasok,
                 koltsegek=koltsegek, rolunk=rolunk, velemenyek=velemenyek, hol=hol, kapcsolat=kapcsolat)
MENU = {"teendok": "Teendők", "szolgaltatasok": "Szolgáltatások", "koltsegek": "Költségek",
        "rolunk": "Rólunk", "kapcsolat": "Kapcsolat"}


def marka(v):
    if v == "v2":
        return f"""<a class="marka" href="#tartalom" aria-label="PIETAS – Teljeskörű temetkezési szolgálat">
        <svg class="marka-ikon" aria-hidden="true"><use href="#i-jel"/></svg>
        <span class="marka-szoveg" aria-hidden="true"><svg class="marka-felirat"><use href="#i-felirat"/></svg><span class="marka-al">Teljeskörű temetkezési szolgálat</span></span>
      </a>"""
    return f"""<a class="marka" href="#tartalom">
        <svg class="marka-ikon" aria-hidden="true"><use href="#i-jel"/></svg>
        <span class="marka-szoveg"><span class="marka-nev">Pietas</span> <span class="marka-al">Temetkezés, Miskolc</span></span>
      </a>"""


def oldal(v, d):
    tartalom = "\n\n    ".join(SZAKASZOK[s](v) for s in d["rend"])
    nav = "\n".join(f'        <li><a href="#{k if k != "koltsegek" else "koltsegek"}">{MENU[k]}</a></li>' for k in d["rend"] if k in MENU)
    return f"""<!doctype html>
<html lang="hu">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>Pietas Temetkezés, Miskolc – teljes körű temetés, 24 órás ügyelet (bemutató)</title>
  <meta name="description" content="Teljes körű temetkezés Miskolcon 1991 óta: hamvasztásos és koporsós temetés, gyászhirdetés, koszorú, halottszállítás. Iroda: Csabai kapu 16., hétköznap 8:30–16:00. Ügyelet: {UGYELET}.">
  <meta name="theme-color" content="{d['theme']}">
  {ICON}
  <link rel="preload" href="../assets/betuk/{d['preload']}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../assets/betuk/betuk.css">
  <link rel="stylesheet" href="../assets/alap.css">
  <link rel="stylesheet" href="../assets/{v}.css">
  <!-- ÉRTÉKESÍTÉSI RÉTEG (élesítéskor törlendő): „Ki készítette?” és „Tetszik ez a rész?” -->
  <link rel="stylesheet" href="../assets/ki-keszitette.css">
  <script src="../assets/ki-keszitette.js" defer></script>
  <link rel="stylesheet" href="../assets/tetszik.css">
  <script src="../assets/tetszik.js" defer></script>
  <!-- Cloudflare Web Analytics (sütimentes) – token élesítés előtt:
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "[CLOUDFLARE_TOKEN]"}}'></script>
  -->
</head>
<body class="{v}" data-tz>
  <a class="ugras" href="#tartalom">Ugrás a tartalomra</a>
  {SPRITE}
  <div class="bemutato-sav" role="note">
    <p><strong>Bemutató ajánlat – nem a {CEG} hivatalos weboldala.</strong> Változat: {d['nev']}.</p>
    <p class="sav-linkek"><a href="../">Mindhárom változat</a> <a href="../ajanlat/">Miért készült, és ki készítette?</a></p>
  </div>

  <header class="fejlec">
    <div class="keret fejlec-sor">
      <!-- LOGÓ: a régi oldal logója vektorosan lekövetve (anyagok/logo/); az eredeti fájl kérendő. -->
      {marka(v)}
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
      <p>[A cég adatkezelési tájékoztatója: élesítés előtt] · <a href="../adatkezeles/">A bemutató oldal adatkezelése</a></p>
    </div>
  </footer>

  <nav class="also-sav" aria-label="Gyors elérés">
    <a class="gomb gomb-fo" href="{tel(UGYELET)}"><svg aria-hidden="true"><use href="#i-tel"/></svg>Hívás 0–24</a>
    <a class="gomb gomb-masod" href="mailto:{EMAIL}"><svg aria-hidden="true"><use href="#i-level"/></svg>Email</a>
  </nav>
</body>
</html>
"""


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
      <p class="vel-hivas">Kérdése van? Hívjon most, közvetlenül engem: <a href="tel:+36707021530">+36 70 702 1530</a></p>
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
  <script src="assets/tetszik.js" defer></script>
</head>
<body>
  <div class="bemutato-sav" role="note"><p><strong>Bemutató ajánlat – nem a {CEG} hivatalos weboldala.</strong> Csak Ön látja.</p></div>
  <main class="keret">
    <h1>Három változat a {CEG} weboldalára</h1>
    <p class="bevezeto">A tartalom mindháromban ugyanaz: a 24 órás ügyelet egy érintéssel hívható száma, a teendők haláleset után, a szükséges iratok, a költségek és az iroda nyitvatartása. A különbség az arculat és a hangsúly. Nézze meg mindhármat, és jelölje meg, mi tetszik.</p>

    <!-- Változatkártyák: sites/_sablonok/_valaszto/ (gyorsweb; képek: elonezet.py) -->
    <ul class="valtozatok">
{kartyak()}
    </ul>
    <p class="tovabb"><a href="ajanlat/">Miért készült, és ki készítette?</a></p>

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
              <div class="uj"><dt>Az új oldalon</dt><dd>Friss, ellenőrzött tények: 1991 óta, 2008 óta a hejőcsabai temető, nyitvatartás és útvonal a Csabai kapuhoz.</dd></div>
            </dl>
          </li>
          <li>
            <h3>Aki most veszítette el valakijét, nem kap egy helyen választ</h3>
            <dl>
              <div><dt>Most</dt><dd>A teendők, az iratok, a költségek és a nyitvatartás öt külön aloldalon vannak. A díjmentes elszállítás és koszorú-kiszállítás, és az urnakiadás alig látszik.</dd></div>
              <div class="uj"><dt>Az új oldalon</dt><dd>Egy oldalon, sorrendben: kit hívjon, mit hozzon, miből áll a költség, mikor van nyitva az iroda. Az előnyök jól látható helyen.</dd></div>
            </dl>
          </li>
        </ol>

        <div class="tipp">
          <h3>Ingyenes tipp, az oldaltól függetlenül</h3>
          <p>Az „Észak gyászhirdetés” aloldal utolsó bekezdésébe valaki egy oda nem illő mondatot és reklámlinket tett, egy „virtuális barátnő” szolgáltatásra. Ezt olvassák a gyászhirdetést feladni készülő családok. Feltört WordPressre vagy illetéktelen hozzáférésre utalhat: érdemes a mondatot törölni, az admin-jelszavakat lecserélni, és a WordPresst a bővítményekkel együtt frissíteni. Szívesen megmutatom, hol van.</p>
        </div>

        <h3>Amit még beletettem</h3>
        <ul class="apro">
          <li>„Amit a családok először kérdeznek”: rövid válaszok a leggyakoribb kérdésekre, a mostani oldal tájékoztatóiból.</li>
          <li>A gyászhirdetés árai táblázatban, a javasolt mérettel; a temetés költségeinek tételei egy helyen.</li>
          <li>Hely a családok véleményének, a tájékoztató áraknak és néhány saját fotónak: ezeket a hívásban pontosítjuk.</li>
          <li>A logót vektorosan újrarajzoltam, hogy minden méretben éles legyen. Az eredeti fájl jobb lenne.</li>
        </ul>
        <!-- MÉRÉS: PageSpeed (régi oldal, Marcell méri) és Lighthouse (új oldal), mobil – elemzes.md. -->
        <p class="meres">Az új oldal mindhárom változata a Google Lighthouse mérésén mobilon: [LIGHTHOUSE_EREDMENY].</p>
      </div>
    </section>

    <section class="keret">
      <h2>Három változat</h2>
      <p class="halvany">A tartalom ugyanaz, az arculat és a hangsúly más. Mindegyik változatban részenként jelezheti, mi tetszik és min változtatna; a lap alján összegyűjtjük, és ott kérheti a visszahívást is.</p>
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
      <h2 id="hivas-cim">Kérdése van? Hívjon most, közvetlenül engem</h2>
      <p class="halvany">Azzal beszél, aki az oldalt megtervezte és megírta.</p>
      <p class="hivas-sor"><a class="gomb gomb-fo hivas-gomb" href="tel:+36707021530">+36 70 702 1530</a> <span class="halvany">vagy írjon: <a href="mailto:info@webness.hu">info@webness.hu</a></span></p>
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
    (SITE / "index.html").write_text(valaszto(), encoding="utf-8")
    lh_f = ANYAG / "lighthouse.txt"
    lh = lh_f.read_text(encoding="utf-8").strip() if lh_f.exists() else "[mérés folyamatban]"
    (SITE / "ajanlat").mkdir(exist_ok=True)
    (SITE / "ajanlat" / "index.html").write_text(ajanlat().replace("[LIGHTHOUSE_EREDMENY]", lh), encoding="utf-8")
    print("ok")
