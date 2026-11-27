"""Fridge magnet sheets sized to Cris's magnetic sheets. 8 x 8 cm tiles, big text, no small print.
Sheet A 30x87 cm: recipes 1-30 (3 x 10).
Sheet B 28x67 cm: title, how it works, don't freeze, 12 containers (3 x 5)."""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import BASE, CONTAINERS, C, CATS, RECIPES, FRESH, ingredient_lines
from build_print import fit, qr, wrap, dotnum, INK, PAPER, MUTED, LINE, OUT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm, cm
from reportlab.pdfbase.pdfmetrics import stringWidth

T = 80 * mm          # tile size
PAD = 5 * mm         # inner padding
INSET = 2.4 * mm     # header band inset (keeps colour off the cut line)
HB = 12.5 * mm       # header band height
ROSE = HexColor("#E0A48F")


def base(c, x, y):
    c.setFillColor(PAPER); c.rect(x, y, T, T, fill=1, stroke=0)


def band(c, x, y, col):
    top = y + T
    c.setFillColor(col); c.roundRect(x + INSET, top - INSET - HB, T - 2 * INSET, HB, 2 * mm, fill=1, stroke=0)
    return top - INSET - HB / 2   # centre line of band


def header_num(c, x, y, col, num, name):
    cy = band(c, x, y, col); bx = x + INSET + 3 * mm
    c.setFillColor(white); c.saveState(); c.translate(bx, cy - 6.3); c.skew(0, 12)
    c.setFont("SerifR", 19); c.drawString(0, 0, num); c.restoreState()
    tx = bx + 10.5 * mm; tw = x + T - INSET - 2.5 * mm - tx
    fs = fit(name, 15, tw, "Serif"); c.setFont("Serif", fs); c.drawString(tx, cy - fs * 0.34, name)
    return y + T - INSET - HB - 3.6 * mm


def header_dot(c, x, y, col, n, name):
    cy = band(c, x, y, col); bx = x + INSET + 3 * mm
    c.setFillColor(white); c.circle(bx + 3.3 * mm, cy, 3.3 * mm, fill=1, stroke=0)
    c.setFillColor(col); c.setFont("SansS", 10 if n < 10 else 9); c.drawCentredString(bx + 3.3 * mm, cy - 3.5, str(n))
    tx = bx + 9.4 * mm; tw = x + T - INSET - 2.5 * mm - tx
    fs = fit(name, 15, tw, "Serif"); c.setFillColor(white); c.setFont("Serif", fs); c.drawString(tx, cy - fs * 0.34, name)
    return y + T - INSET - HB - 3.6 * mm


def header_text(c, x, y, col, name):
    cy = band(c, x, y, col); tx = x + INSET + 3.5 * mm
    fs = fit(name, 15, T - 2 * INSET - 7 * mm, "Serif")
    c.setFillColor(white); c.setFont("Serif", fs); c.drawString(tx, cy - fs * 0.34, name)
    return y + T - INSET - HB - 3.6 * mm


def rule(c, x, y):
    c.setStrokeColor(LINE); c.setLineWidth(0.7); c.line(x + PAD, y, x + T - PAD, y)


def numbered(c, x, y, w, steps, col, fs, lead=1.22, measure=False):
    ind = 3.8 * mm
    for k, s in enumerate(steps, 1):
        ls = wrap(s, "Sans", fs, w - ind)
        if not measure:
            c.setFillColor(col); c.setFont("SansS", fs); c.drawString(x, y - fs, str(k))
            c.setFillColor(INK); c.setFont("Sans", fs)
            for j, l in enumerate(ls):
                c.drawString(x + ind, y - fs - j * fs * lead, l)
        y -= len(ls) * fs * lead + fs * 0.5
    return y


FIXED, SEEN = {}, {}


def fit_numbered(c, x, y, w, steps, col, bottom, kind, fs=12.5, minfs=7):
    if kind in FIXED:
        return numbered(c, x, y, w, steps, col, FIXED[kind])
    while fs > minfs and numbered(c, x, y, w, steps, col, fs, measure=True) < bottom:
        fs -= 0.1
    SEEN[kind] = min(SEEN.get(kind, 99), fs)
    return numbered(c, x, y, w, steps, col, fs)


# ---------- recipe ----------
SHORT_FRESH = {
    "rice": "Cook rice for 10–12 min.",
    "pasta": "Cook small pasta for 8–10 min.",
    "mash": "Boil potato for 15 min, mash with a little milk.",
    "mashtop": "Boil potato for 15 min, mash with a little milk.",
    "couscous": "Cover couscous with boiling water for 5 min.",
    "quinoa": "Simmer quinoa for 12–15 min.",
    "oats": "Simmer oats in milk for 3–5 min.",
    "ricemilk": "Simmer cooked rice in milk for 10 min.",
}


def short_method(r):
    num, name, cat, cons, extras, fresh, finish = r
    st = []
    if fresh in SHORT_FRESH:
        st.append(SHORT_FRESH[fresh])
    if fresh == "mashtop":
        finish = "Top with the mash."
    pin = [e.lower() for e in extras if "pinch" in e.lower()]
    if cat == "Sweet":
        st.append("Heat 2 cubes of fruit mix until piping hot" + (f", with a {pin[0]}." if pin else "."))
        if num == 29:
            finish = "Cool, then swirl into the yoghurt."
    else:
        sp = f" and a {pin[0]}" if pin else ""
        st.append(f"Heat 2 cubes of each with a splash of water{sp}, covered, 5–7 min until piping hot.")
    st.append(finish)
    return st


def recipe_tile(c, x, y, r):
    num, name, cat, cons, extras, fresh, finish = r
    col = HexColor(CATS[cat])
    base(c, x, y)
    yb = header_num(c, x, y, col, f"{num:02d}", name)
    lx = x + PAD; w = T - 2 * PAD
    items = [(t, cc) for t, cc in ingredient_lines(r) if not t.lower().startswith("pinch")]
    rows = (len(items) + 1) // 2; rh = 6.4 * mm; cw = w / 2
    for k, (t, cc) in enumerate(items):
        ix = lx + (k // rows) * cw; iy = yb - (k % rows) * rh - rh / 2
        t = t.replace("Fresh ", "").capitalize() if not cc else t
        if cc:
            cid = next(cn[0] for cn in CONTAINERS if cn[1] == ingredient_name(t, cc))
            dotnum(c, ix + 2.4 * mm, iy, 2.4 * mm, cid, HexColor(cc), fs=7.4)
            c.setFillColor(INK); fnt = "SansS"
        else:
            c.setStrokeColor(INK); c.setLineWidth(0.9); c.circle(ix + 2.4 * mm, iy, 1.2 * mm, fill=0, stroke=1)
            c.setFillColor(INK); fnt = "Sans"
        fs = fit(t, 10.5, cw - 6.6 * mm, fnt); c.setFont(fnt, fs); c.drawString(ix + 6.2 * mm, iy - fs * 0.36, t)
    yb -= rows * rh + 1.6 * mm
    rule(c, x, yb); yb -= 2.6 * mm
    fit_numbered(c, lx, yb, w, short_method(r), col, y + PAD - 1 * mm, "recipe")


def ingredient_name(t, cc):
    return t


# ---------- container ----------
def container_tile(c, x, y, cont):
    cid, name, col, contents, prep = cont
    colr = HexColor(col)
    base(c, x, y)
    yb = header_dot(c, x, y, colr, cid, name)
    lx = x + PAD; w = T - 2 * PAD
    fs = 14; ls = wrap(contents, "Serif", fs, w)
    while len(ls) > 2:
        fs -= 0.5; ls = wrap(contents, "Serif", fs, w)
    c.setFillColor(INK); c.setFont("Serif", fs)
    for j, l in enumerate(ls):
        c.drawString(lx, yb - fs - j * fs * 1.15, l)
    yb -= len(ls) * fs * 1.15 + 2.6 * mm
    rule(c, x, yb); yb -= 2.6 * mm
    fit_numbered(c, lx, yb, w, prep, colr, y + PAD - 1 * mm, "container")


# ---------- info ----------
def title_tile(c, x, y):
    c.setFillColor(INK); c.rect(x, y, T, T, fill=1, stroke=0)
    lx = x + PAD; top = y + T - PAD
    c.setFillColor(PAPER); c.setFont("Serif", 26); c.drawString(lx, top - 24, "Freezer")
    c.setFillColor(ROSE); c.saveState(); c.translate(lx, top - 50); c.skew(0, 12)
    c.setFont("SerifR", 26); c.drawString(0, 0, "Kitchen"); c.restoreState()
    c.setFillColor(PAPER); c.setFont("Sans", 10.5)
    c.drawString(lx, top - 70, "12 containers · 30 meals")
    qs = 34 * mm; qr(c, BASE, x + T - PAD - qs, y + PAD, qs)
    c.setFillColor(ROSE); c.setFont("SansS", 10.5)
    c.drawString(lx, y + PAD + qs - 12, "Scan for")
    c.drawString(lx, y + PAD + qs - 25, "every recipe")
    c.drawString(lx, y + PAD + qs - 38, "and method")


def how_tile(c, x, y):
    base(c, x, y)
    yb = header_text(c, x, y, INK, "How it works")
    steps = ["Cook each container, no salt or sugar.",
             "Cool within 1 hour, freeze in cubes, bag and date.",
             "Numbers on a meal = the containers to use.",
             "Heat until piping hot, then cool before serving.",
             "Never refreeze. Keeps 3 months."]
    fit_numbered(c, x + PAD, yb - 1 * mm, T - 2 * PAD, steps, HexColor("#B4472F"), y + PAD - 1 * mm, "how", fs=12)


def dontfreeze_tile(c, x, y):
    base(c, x, y)
    yb = header_text(c, x, y, HexColor("#4E6577"), "Don't freeze")
    items = [("Cooked egg", "make fresh"), ("Cucumber, lettuce, raw tomato", "serve fresh"),
             ("Potato chunks", "freeze as mash"), ("Yoghurt", "add after heating"),
             ("Rice, pasta, oats", "cook fresh")]
    lx = x + PAD; w = T - 2 * PAD; n = len(items); rh = (yb - (y + PAD)) / n
    for k, (a, b) in enumerate(items):
        top = yb - k * rh; cy = top - rh / 2
        fa = fit(a, 11, w - 4.4 * mm, "SansS")
        c.setFillColor(HexColor("#4E6577")); c.circle(lx + 1.2 * mm, cy + 5.5, 1.2 * mm, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("SansS", fa); c.drawString(lx + 4.4 * mm, cy + 1.6, a)
        c.setFillColor(MUTED); c.setFont("Sans", 9.6); c.drawString(lx + 4.4 * mm, cy - 9.6, b)
        if k < n - 1:
            c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(lx, top - rh, lx + w, top - rh)


# ---------- sheet ----------
def sheet(path, W, H, cols, rows, tiles, name):
    c = canvas.Canvas(path, pagesize=(W, H)); c.setTitle(f"Freezer Kitchen magnets · {name}")
    gw, gh = cols * T, rows * T
    mx, my = (W - gw) / 2, 18 * mm        # grid pinned near the top so spare sheet stays in one piece
    gy0 = H - my - gh
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    for i, fn in enumerate(tiles):
        x = mx + (i % cols) * T; y = H - my - (i // cols + 1) * T
        fn(c, x, y)
    c.setStrokeColor(HexColor("#9A8F84")); c.setLineWidth(0.25)
    for a in range(cols + 1):
        X = mx + a * T; c.line(X, gy0, X, H - my)
    for b in range(rows + 1):
        Y = gy0 + b * T; c.line(mx, Y, W - mx, Y)
    c.setStrokeColor(INK); c.setLineWidth(0.5)
    for a in range(cols + 1):
        X = mx + a * T; c.line(X, H - my + 1.5 * mm, X, H); c.line(X, gy0 - 1.5 * mm, X, max(0, gy0 - 12 * mm))
    for b in range(rows + 1):
        Y = gy0 + b * T; c.line(0, Y, mx - 1.5 * mm, Y); c.line(W - mx + 1.5 * mm, Y, W, Y)
    lab = f"{name}  ·  {W/cm:.0f} × {H/cm:.0f} cm sheet  ·  {len(tiles)} magnets, 8 × 8 cm  ·  print at 100%"
    ly = H - my + 6 * mm; lw = stringWidth(lab, "SansS", 7.5) + 6 * mm
    c.setFillColor(white); c.rect(W / 2 - lw / 2, ly - 2 * mm, lw, 6 * mm, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("SansS", 7.5); c.drawCentredString(W / 2, ly, lab)
    if gy0 > 30 * mm:
        c.setFillColor(MUTED); c.setFont("Sans", 9)
        c.drawCentredString(W / 2, gy0 - 20 * mm, f"Spare magnetic sheet below this line: about {W/cm:.0f} × {(gy0 - 12*mm)/cm:.0f} cm")
        c.setStrokeColor(MUTED); c.setDash(3, 3); c.line(0, gy0 - 12 * mm, W, gy0 - 12 * mm); c.setDash()
    c.showPage(); c.save()
    return path


def main():
    R = {r[0]: r for r in RECIPES}
    rt = lambda n: (lambda c, x, y: recipe_tile(c, x, y, R[n]))
    ct = lambda i: (lambda c, x, y: container_tile(c, x, y, C[i]))
    a_tiles = [rt(n) for n in range(1, 31)]
    b_tiles = [title_tile, how_tile, dontfreeze_tile] + [ct(i) for i in range(1, 13)]
    jobs = [(f"{OUT}/Freezer_Kitchen_Magnets_Sheet_A_30x87cm.pdf", 30 * cm, 87 * cm, 3, 10, a_tiles, "SHEET A OF 2 · RECIPES 1–30"),
            (f"{OUT}/Freezer_Kitchen_Magnets_Sheet_B_28x67cm.pdf", 28 * cm, 67 * cm, 3, 5, b_tiles, "SHEET B OF 2 · CONTAINERS & GUIDES")]
    for j in jobs:                                    # measuring pass
        sheet(tempfile.mktemp(suffix=".pdf"), *j[1:])
    FIXED.update(SEEN); print("uniform sizes", {k: round(v, 1) for k, v in FIXED.items()})
    for j in jobs:
        print(sheet(*j))


if __name__ == "__main__":
    main()
