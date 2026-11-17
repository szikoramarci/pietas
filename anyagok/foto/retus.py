"""A Pietas-iroda fotójáról (régi oldal, Cégünkről: wp-content/uploads/2013/01/Kép-024.jpg, 3072×2304, 1600×1200-ra kicsinyítve) a Pannónia-molinó eltávolítása: a korlát rekonstrukciója.
A lécek helye a molinó fölött kilátszó csúcsokból, színek és a rudak sorai a látható bal oldali korlátról,
a párkány és a gerenda a bal oldali sávból; perspektíva: a lécek teteje balról jobbra ~10 px-t süllyed."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = Image.open("iroda-eredeti.jpg").convert("RGB")
a = np.asarray(im).astype(float)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
zold = (G > R + 12) & (G > B + 12)

X0, X1 = 926, 1507                   # a festett sáv
LECEK = [(924, 931), (936, 948), (952, 962), (969, 975), (980, 991), (997, 1008), (1015, 1019), (1026, 1037), (1044, 1054),
         (1059, 1065), (1071, 1082), (1087, 1098), (1104, 1109), (1115, 1125), (1132, 1142), (1144, 1155), (1161, 1171),
         (1177, 1187), (1192, 1197), (1203, 1214), (1220, 1230), (1235, 1241), (1246, 1256), (1262, 1272), (1277, 1282),
         (1288, 1298), (1304, 1313), (1319, 1326), (1329, 1339), (1344, 1354), (1359, 1365), (1369, 1379), (1384, 1394),
         (1399, 1404), (1409, 1419), (1424, 1433), (1438, 1443), (1449, 1458), (1462, 1472), (1476, 1481), (1484, 1495)]
LECALJ = 322
FELSO_RUD, ALSO_RUD = (222, 234), (288, 299)
REF = slice(860, 927)                 # a látható bal oldali korlát

def lejt(yb, x):                      # alap (bal oldali) sor → kimeneti sor az x helyen
    t = (x - 928) / 572
    return yb + 10 * t * (LECALJ - yb) / 114

def alapsor(y, x):                    # kimeneti sor → alap sor
    t = (x - 928) / 572
    k = 10 * t / 114
    return (y - k * LECALJ) / (1 - k)

# színek soronként a referencia-sávból
def soronkent(feltetel):
    out = np.zeros((H, 3))
    for y in range(200, 360):
        m = feltetel[y, REF]
        px = a[y, REF][m]
        out[y] = np.median(px, axis=0) if len(px) > 3 else np.nan
    return out
lecszin = soronkent(zold)
falszin_minta = a[266:287, REF][~zold[266:287, REF]]
falszin_also = a[300:321, REF][~zold[300:321, REF]]
fal_felso, fal_also = np.median(falszin_minta, axis=0), np.median(falszin_also, axis=0)

for y in range(200, 360):            # hiányzó sorok kitöltése a szomszédokból
    if np.isnan(lecszin[y]).any():
        lecszin[y] = lecszin[y - 1]

# maszk: a molinó (sokszög), 2 px ráhagyással
maszk = Image.new("L", (W, H), 0)
ImageDraw.Draw(maszk).polygon([(926, 220), (1503, 228), (1507, 352), (926, 352)], fill=255)
maszk = maszk.filter(ImageFilter.MaxFilter(3))

rng = np.random.default_rng(7)
ki = a.copy()
lec_x = np.zeros(W, dtype=int)        # 0: rés, 1+: léc sorszáma
for i, (p, q) in enumerate(LECEK, 1):
    lec_x[p:q + 1] = i
fenyesseg = 1 + rng.normal(0, 0.035, len(LECEK) + 1)
oszlopzaj = rng.normal(0, 0.03, W)   # a deszkák erezete

# a párkány és a gerenda (sor ≥ LECALJ): soronkénti alapszín a bal oldali sávból, finom, vízszintesen elnyújtott textúrával
# (a sáv puszta ismétlése foltos mintát adott)
csik = a[:, 880:927]
alap = np.median(csik[LECALJ:353], axis=1)
text = rng.normal(0, 4.0, (353 - LECALJ, X1 - X0 + 1, 1))
text = np.asarray(Image.fromarray(np.clip(text[..., 0] * 10 + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(3))).astype(float)
text = (text - 128) / 10
# a bal oldali sáv finom részletei (a nagy foltok nélkül: a sáv mínusz az elmosott változata), tükrözve ismételve
csik_img = Image.fromarray(np.clip(csik, 0, 255).astype(np.uint8))
reszlet = csik - np.asarray(csik_img.filter(ImageFilter.GaussianBlur(5))).astype(float)
for x in range(X0, X1 + 1):
    j = (x - X0) % (2 * csik.shape[1])
    jj = j if j < csik.shape[1] else 2 * csik.shape[1] - 1 - j
    ki[LECALJ:353, x] = alap + text[:, x - X0, None] * 1.2 + reszlet[LECALJ:353, jj] * 0.8

for x in range(X0, X1 + 1):
    for y in range(205, LECALJ + 2):
        yb = alapsor(y, x)
        if yb >= LECALJ:
            continue
        ybi = int(round(yb))
        i = lec_x[x]
        if x > 1495:                  # a korlát vége után: a sarokfal oszlopa
            ki[y, x] = a[y, 1509]
            continue
        if i:
            c = lecszin[ybi] * fenyesseg[i] * (1 + oszlopzaj[x])
            p, q = LECEK[i - 1]
            if x in (p, q):           # a léc széle egy árnyalattal sötétebb
                c = c * 0.86
            ki[y, x] = c
        elif FELSO_RUD[0] <= ybi < FELSO_RUD[1] or ALSO_RUD[0] <= ybi < ALSO_RUD[1]:
            ki[y, x] = lecszin[ybi] * 0.9
        else:
            ki[y, x] = fal_felso if ybi < 287 else fal_also

# szemcse és lágyítás, hogy illeszkedjen a fotóhoz
zaj = rng.normal(0, 2.2, ki.shape)
ki = np.clip(ki + zaj * (np.asarray(maszk)[..., None] / 255), 0, 255)
festett = Image.fromarray(ki.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
lagy_maszk = maszk.filter(ImageFilter.GaussianBlur(1.2))
eredmeny = Image.composite(festett, im, lagy_maszk)
eredmeny.save("iroda-retusalt.png")  # → site/assets/kepek/iroda-1200.webp és -800.webp (80%-os WebP)
eredmeny.crop((820, 180, 1520, 400)).resize((1400, 440), Image.LANCZOS).save("retus-kozel.png")
print("ok")
