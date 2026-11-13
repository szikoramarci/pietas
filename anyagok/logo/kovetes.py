import sys, numpy as np, potrace
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(src).convert("L")
def trace(box, name, invert_fill="currentColor", scale=4):
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    a = np.array(c) >= 128
    bm = potrace.Bitmap(a)
    path = bm.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.3)
    d = []
    for curve in path:
        s = curve.start_point
        d.append(f"M{s.x/scale:.1f} {s.y/scale:.1f}")
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{seg.c.x/scale:.1f} {seg.c.y/scale:.1f}L{seg.end_point.x/scale:.1f} {seg.end_point.y/scale:.1f}")
            else:
                d.append(f"C{seg.c1.x/scale:.1f} {seg.c1.y/scale:.1f} {seg.c2.x/scale:.1f} {seg.c2.y/scale:.1f} {seg.end_point.x/scale:.1f} {seg.end_point.y/scale:.1f}")
        d.append("Z")
    w, h = box[2]-box[0], box[3]-box[1]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill="#1a1a1a" fill-rule="evenodd" d="{"".join(d)}"/></svg>'
    open(f"{out}/{name}.svg", "w").write(svg)
    print(name, w, h, len(svg))
trace((1062, 150, 1302, 658), "logo-jel")       # sírkő-ív a gyászoló alakkal
trace((225, 205, 765, 395), "logo-pietas")      # PIETAS felirat (az A sírkő-ív)
trace((820, 262, 1003, 368), "logo-kft")
trace((200, 418, 1030, 600), "logo-alcim")
