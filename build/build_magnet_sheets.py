"""Fridge magnet sheets sized to Cris's magnetic sheets.
Sheet A 30x87 cm: recipes 1-27.  Sheet B 28x67 cm: recipes 28-30, 12 containers, info + wipe-clean tiles.
All tiles 90 x 90 mm on a shared grid, so every cut runs edge to edge."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import BASE, CONTAINERS, C, CATS, RECIPES, FRESH, ingredient_lines
from build_print import (fit, spaced, qr, wrap, dotnum, INK, PAPER, MUTED, LINE, ACC, OUT)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm, cm
from reportlab.pdfbase.pdfmetrics import stringWidth

T = 90 * mm          # tile size
PAD = 6 * mm         # inner padding
INSET = 2.6 * mm     # header band inset (keeps colour away from the cut line)
HB = 14 * mm         # header band height


# ---------- shared tile pieces ----------
def base(c, x, y):
    c.setFillColor(PAPER); c.rect(x, y, T, T, fill=1, stroke=0)


def header(c, x, y, col, big, label, name, big_is_num=True):
    top = y + T
    c.setFillColor(col); c.roundRect(x + INSET, top - INSET - HB, T - 2 * INSET, HB, 2 * mm, fill=1, stroke=0)
    bx = x + INSET + 3.2 * mm; cy = top - INSET - HB / 2
    if big_is_num:
        c.setFillColor(white); c.saveState(); c.translate(bx, cy - 6); c.skew(0, 12)
        c.setFont("SerifR", 19); c.drawString(0, 0, big); c.restoreState()
        tx = bx + 11 * mm
    else:
        c.setFillColor(white); c.circle(bx + 3.2 * mm, cy, 3.2 * mm, fill=1, stroke=0)
        c.setFillColor(col); c.setFont("SansS", 9 if len(big) < 2 else 8)
        c.drawCentredString(bx + 3.2 * mm, cy - 3.1, big)
        tx = bx + 8.8 * mm
    tw = x + T - INSET - 3 * mm - tx
    spaced(c, tx, cy + 6.6, label.upper(), "SansS", 5.6, 1.0, HexColor("#FFFFFF"))
    fs = fit(name, 13.5, tw, "Serif")
    c.setFillColor(white); c.setFont("Serif", fs); c.drawString(tx, cy - 8.2, name)
    return top - INSET - HB - 4.2 * mm   # y where body starts


def label(c, x, y, t, col=MUTED):
    spaced(c, x, y, t, "SansS", 5.6, 1.1, col)


def numbered(c, x, y, w, steps, col, fs, lead=1.25, measure=False):
    """Numbered list; returns y after the list."""
    ind = 3.6 * mm
    for k, s in enumerate(steps, 1):
        ls = wrap(s, "Sans", fs, w - ind)
        if not measure:
            c.setFillColor(col); c.setFont("SansS", fs); c.drawString(x, y - fs, f"{k}")
            c.setFillColor(INK); c.setFont("Sans", fs)
            for j, l in enumerate(ls):
                c.drawString(x + ind, y - fs - j * fs * lead, l)
        y -= len(ls) * fs * lead + fs * 0.45
    return y


FIXED = {}      # kind -> uniform font size, filled by a measuring pass
SEEN = {}


def fit_numbered(c, x, y, w, steps, col, bottom, fs=8.2, minfs=6.4, kind=None):
    if kind and kind in FIXED:
        return numbered(c, x, y, w, steps, col, FIXED[kind])
    while fs > minfs and numbered(c, x, y, w, steps, col, fs, measure=True) < bottom:
        fs -= 0.2
    if kind:
        SEEN[kind] = min(SEEN.get(kind, 99), fs)
    return numbered(c, x, y, w, steps, col, fs)


# ---------- recipe tile ----------
def short_method(r):
    num, name, cat, cons, extras, fresh, finish = r
    st = []
    if fresh and FRESH[fresh][1]:
        st.append(FRESH[fresh][1])
    if cat == "Sweet":
        st.append("Heat 2 cubes of fruit mix until piping hot.")
        if num == 29:
            finish = "Let it cool, then swirl into the yoghurt."
    else:
        pin = [e.lower() for e in extras if "pinch" in e.lower()]
        sp = f" and a {pin[0]}" if pin else ""
        st.append(f"Heat 2 cubes of each in a covered pan with a splash of water{sp} "
                  "for 5–7 min, stirring, until piping hot.")
    if cat == "Sweet" and any("pinch" in e.lower() for e in extras):
        st.append("Stir in a pinch of cinnamon.")
    st.append(finish)
    if num != 29:
        st.append("Let it cool before serving.")
    return st


def recipe_tile(c, x, y, r):
    num, name, cat, cons, extras, fresh, finish = r
    col = HexColor(CATS[cat])
    base(c, x, y)
    yb = header(c, x, y, col, f"{num:02d}", cat, name)
    lx = x + PAD; w = T - 2 * PAD
    label(c, lx, yb - 4, "YOU NEED"); yb -= 7.5
    items = ingredient_lines(r)
    rows = (len(items) + 1) // 2; rh = 6 * mm; cw = w / 2
    for k, (t, cc) in enumerate(items):
        ix = lx + (k // rows) * cw; iy = yb - (k % rows) * rh - rh / 2
        if cc:
            cid = next(cn[0] for cn in CONTAINERS if cn[1] == t)
            dotnum(c, ix + 2.2 * mm, iy, 2.2 * mm, cid, HexColor(cc), fs=6.6)
            c.setFillColor(INK); fnt = "SansS"
        else:
            c.setStrokeColor(MUTED); c.setLineWidth(0.7); c.circle(ix + 2 * mm, iy, 0.9 * mm, fill=0, stroke=1)
            c.setFillColor(MUTED); fnt = "Sans"
        fs = fit(t, 9.8, cw - 6.6 * mm, fnt); c.setFont(fnt, fs); c.drawString(ix + 5.8 * mm, iy - fs * 0.36, t)
    yb -= rows * rh + 3.2 * mm
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(lx, yb + 1.4 * mm, lx + w, yb + 1.4 * mm)
    label(c, lx, yb - 4, "METHOD"); yb -= 8
    fit_numbered(c, lx, yb, w, short_method(r), col, y + PAD - 1 * mm, fs=10.4, kind='recipe')


# ---------- container tile ----------
def container_tile(c, x, y, cont):
    cid, name, col, contents, prep = cont
    colr = HexColor(col)
    base(c, x, y)
    yb = header(c, x, y, colr, str(cid), "Container", name, big_is_num=False)
    lx = x + PAD; w = T - 2 * PAD
    label(c, lx, yb - 4, "INSIDE"); yb -= 8
    fs = 14; ls = wrap(contents, "Serif", fs, w)
    while len(ls) > 2:
        fs -= 0.5; ls = wrap(contents, "Serif", fs, w)
    c.setFillColor(INK); c.setFont("Serif", fs)
    for j, l in enumerate(ls):
        c.drawString(lx, yb - fs - j * fs * 1.15, l)
    yb -= len(ls) * fs * 1.15 + 3.5 * mm
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(lx, yb + 1.4 * mm, lx + w, yb + 1.4 * mm)
    label(c, lx, yb - 4, "HOW TO PREP"); yb -= 8
    foot_y = y + PAD - 0.5 * mm
    fit_numbered(c, lx, yb, w, prep, colr, foot_y + 9 * mm, fs=12, kind='container')
    c.setStrokeColor(LINE); c.line(lx, foot_y + 6 * mm, lx + w, foot_y + 6 * mm)
    c.setFillColor(MUTED); c.setFont("Sans", 7.2)
    c.drawString(lx, foot_y + 2.3 * mm, "Cool within 1 hour · freeze in cubes")
    c.drawString(lx, foot_y - 0.6 * mm, "Bag, label and date · keeps 3 months")


# ---------- info tiles ----------
def title_tile(c, x, y):
    c.setFillColor(INK); c.rect(x, y, T, T, fill=1, stroke=0)
    lx = x + PAD; top = y + T - PAD
    spaced(c, lx, top - 6, "BATCH COOKING · 12 MONTHS+", "SansS", 5.6, 1.1, HexColor("#E0A48F"))
    c.setFillColor(PAPER); c.setFont("Serif", 22); c.drawString(lx, top - 27, "Freezer")
    c.setFillColor(HexColor("#E0A48F")); c.saveState(); c.translate(lx, top - 48); c.skew(0, 12)
    c.setFont("SerifR", 22); c.drawString(0, 0, "Kitchen"); c.restoreState()
    qs = 21 * mm; qr(c, BASE, x + T - PAD - qs, top - qs, qs)
    steps = ["Cook each container's mix, no salt or sugar.", "Cool it within 1 hour.",
             "Freeze in ice cube trays, then bag and date.", "Pick a meal magnet.",
             "Heat 2 cubes of each until piping hot.", "Cool and serve."]
    yy = top - 66
    c.setStrokeColor(HexColor("#4A423B")); c.setLineWidth(0.6); c.line(lx, yy + 3, x + T - PAD, yy + 3)
    step_h = (yy - (y + PAD + 5 * mm)) / len(steps)
    for k, s in enumerate(steps, 1):
        fs = fit(s, 9.6, T - 2 * PAD - 5 * mm)
        cy = yy - step_h * (k - 0.5)
        c.setFillColor(HexColor("#E0A48F")); c.setFont("SansS", fs); c.drawString(lx, cy - fs * 0.36, str(k))
        c.setFillColor(PAPER); c.setFont("Sans", fs); c.drawString(lx + 4.6 * mm, cy - fs * 0.36, s)
        if k < len(steps):
            c.setStrokeColor(HexColor("#3A332D")); c.line(lx, cy - step_h / 2, x + T - PAD, cy - step_h / 2)
    c.setFillColor(HexColor("#B8AEA3")); c.setFont("Sans", 7)
    c.drawString(lx, y + PAD - 1 * mm, "Full guide: cristianlupudesign.github.io/baby-meals")


def list_tile(c, x, y, col, lab, title, items):
    base(c, x, y)
    yb = header(c, x, y, col, "", lab, title, big_is_num=True)
    lx = x + PAD; w = T - 2 * PAD
    yb -= 1 * mm
    bottom = y + PAD
    n = len(items); rh = (yb - bottom) / n
    for k, (b, t) in enumerate(items):
        top = yb - k * rh
        fs = 8.2; txt = (b + " " + t).strip()
        ls = wrap(txt, "Sans", fs, w - 4 * mm)
        while len(ls) * fs * 1.22 > rh - 2 and fs > 6.5:
            fs -= 0.2; ls = wrap(txt, "Sans", fs, w - 4 * mm)
        cy = top - rh / 2; ty = cy + (len(ls) - 1) * fs * 1.22 / 2 - fs * 0.36
        c.setFillColor(col); c.circle(lx + 1 * mm, cy, 1 * mm, fill=1, stroke=0)
        # bold lead word(s)
        for j, l in enumerate(ls):
            xx = lx + 4 * mm
            if j == 0 and b and l.startswith(b):
                c.setFillColor(INK); c.setFont("SansS", fs); c.drawString(xx, ty, b)
                xx += stringWidth(b + " ", "SansS", fs); l = l[len(b):].lstrip()
            c.setFillColor(INK); c.setFont("Sans", fs); c.drawString(xx, ty - j * fs * 1.22, l)
        if k < n - 1:
            c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(lx, top - rh, lx + w, top - rh)


def header_plain(c, x, y, col, lab, title):
    """Header band without a big number (shift text left)."""
    top = y + T
    c.setFillColor(col); c.roundRect(x + INSET, top - INSET - HB, T - 2 * INSET, HB, 2 * mm, fill=1, stroke=0)
    tx = x + INSET + 4 * mm; cy = top - INSET - HB / 2
    spaced(c, tx, cy + 6.6, lab.upper(), "SansS", 5.6, 1.0, white)
    c.setFillColor(white); c.setFont("Serif", fit(title, 13.5, T - 2 * INSET - 8 * mm, "Serif")); c.drawString(tx, cy - 8.2, title)
    return top - INSET - HB - 4.2 * mm


def safety_tile(c, x, y):
    items = [("Reheat", "until piping hot all the way through, then cool before serving."),
             ("Never refreeze", "food that has thawed."),
             ("Rice:", "cool within 1 hour, reheat only once."),
             ("No honey", "before age 1. No whole nuts."),
             ("Quarter", "grapes and cherry tomatoes."),
             ("No added", "salt or sugar. Use no-salt tinned beans.")]
    _list(c, x, y, HexColor("#B4472F"), "Read me", "Stay safe", items)


def dontfreeze_tile(c, x, y):
    items = [("Cooked egg", "goes rubbery. Make it fresh."),
             ("Cucumber, lettuce, raw tomato", "go mushy. Serve fresh."),
             ("Potato chunks", "go grainy. Freeze as mash."),
             ("Yoghurt, soft cheese", "separate. Add fresh after heating."),
             ("Rice, pasta, couscous, oats", "cook fresh each time.")]
    _list(c, x, y, HexColor("#4E6577"), "Keep out of the freezer", "Don't freeze", items)


def _list(c, x, y, col, lab, title, items):
    base(c, x, y)
    yb = header_plain(c, x, y, col, lab, title) - 1 * mm
    lx = x + PAD; w = T - 2 * PAD; bottom = y + PAD
    n = len(items); rh = (yb - bottom) / n
    for k, (b, t) in enumerate(items):
        top = yb - k * rh; cy = top - rh / 2; fs = 9.6
        full = f"{b} {t}"
        ls = wrap(full, "Sans", fs, w - 4 * mm)
        while len(ls) * fs * 1.22 > rh - 2 and fs > 6.5:
            fs -= 0.2; ls = wrap(full, "Sans", fs, w - 4 * mm)
        lh = fs * 1.22; ty = cy + (len(ls) - 1) * lh / 2 - fs * 0.36
        c.setFillColor(col); c.circle(lx + 1 * mm, cy, 1 * mm, fill=1, stroke=0)
        remaining_bold = b
        for j, l in enumerate(ls):
            xx = lx + 4 * mm; yy = ty - j * lh
            words = l.split(" "); bold_part = []
            while words and remaining_bold and remaining_bold.startswith(words[0]):
                bold_part.append(words.pop(0)); remaining_bold = remaining_bold[len(bold_part[-1]):].lstrip()
            if bold_part:
                bt = " ".join(bold_part); c.setFillColor(INK); c.setFont("SansS", fs); c.drawString(xx, yy, bt)
                xx += stringWidth(bt + " ", "SansS", fs)
            c.setFillColor(INK); c.setFont("Sans", fs); c.drawString(xx, yy, " ".join(words))
        if k < n - 1:
            c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(lx, top - rh, lx + w, top - rh)


# ---------- wipe-clean tiles ----------
def stock_tile(c, x, y):
    base(c, x, y)
    yb = header_plain(c, x, y, INK, "Wipe-clean · tick a box per bag", "Freezer stock") - 0.5 * mm
    lx = x + PAD; w = T - 2 * PAD; rh = (yb - (y + PAD - 1 * mm)) / 12
    s = 3.1 * mm; g = 1.1 * mm
    for k, (cid, name, col, _, _) in enumerate(CONTAINERS):
        cy = yb - k * rh - rh / 2; colr = HexColor(col)
        dotnum(c, lx + 1.9 * mm, cy, 1.9 * mm, cid, colr, fs=5.6)
        c.setFillColor(INK); c.setFont("SansS", fit(name, 8.6, 30 * mm, "SansS")); c.drawString(lx + 5 * mm, cy - 3, name)
        bx = lx + w - 6 * (s + g) + g
        c.setStrokeColor(colr); c.setLineWidth(0.7)
        for j in range(6):
            c.roundRect(bx + j * (s + g), cy - s / 2, s, s, 0.6 * mm, fill=0, stroke=1)


def week_tile(c, x, y):
    base(c, x, y)
    yb = header_plain(c, x, y, HexColor("#5E7F5E"), "Wipe-clean · write the meal number", "This week") - 0.5 * mm
    lx = x + PAD; w = T - 2 * PAD
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hx = [lx + 9 * mm, lx + 9 * mm + (w - 9 * mm) / 3, lx + 9 * mm + 2 * (w - 9 * mm) / 3]
    c.setFillColor(MUTED); c.setFont("SansS", 5.8)
    for t, xx in zip(["BREAKFAST", "LUNCH", "DINNER"], hx):
        c.drawString(xx, yb - 5, t)
    yb -= 8; rh = (yb - (y + PAD)) / 7
    for k, d in enumerate(days):
        top = yb - k * rh; cy = top - rh / 2
        c.setFillColor(INK); c.setFont("Serif", 9.5); c.drawString(lx, cy - 3.2, d)
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        for xx in hx:
            c.line(xx, cy - 3.5, xx + (w - 9 * mm) / 3 - 2.5 * mm, cy - 3.5)


def shop_tile(c, x, y):
    base(c, x, y)
    yb = header_plain(c, x, y, HexColor("#C98A3D"), "Wipe-clean", "To buy & to cook") - 1 * mm
    lx = x + PAD; w = T - 2 * PAD; cwid = (w - 4 * mm) / 2
    c.setFillColor(MUTED); c.setFont("SansS", 5.8)
    c.drawString(lx, yb - 5, "TO BUY"); c.drawString(lx + cwid + 4 * mm, yb - 5, "TO COOK")
    yb -= 8; n = 10; rh = (yb - (y + PAD)) / n
    for col_i in range(2):
        xx = lx + col_i * (cwid + 4 * mm)
        for k in range(n):
            cy = yb - k * rh - rh / 2
            c.setStrokeColor(HexColor("#C98A3D")); c.setLineWidth(0.7)
            c.roundRect(xx, cy - 1.4 * mm, 2.8 * mm, 2.8 * mm, 0.5 * mm, fill=0, stroke=1)
            c.setStrokeColor(LINE); c.line(xx + 4.4 * mm, cy - 1.4 * mm, xx + cwid, cy - 1.4 * mm)


# ---------- sheet ----------
def sheet(path, W, H, cols, rows, tiles, name):
    c = canvas.Canvas(path, pagesize=(W, H)); c.setTitle(f"Freezer Kitchen magnets · {name}")
    gw, gh = cols * T, rows * T
    mx, my = (W - gw) / 2, (H - gh) / 2
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    for i, fn in enumerate(tiles):
        col_i, row = i % cols, i // cols
        x = mx + col_i * T; y = H - my - (row + 1) * T
        fn(c, x, y)
    # cut lines: hairline through the grid + marks into the margin
    c.setStrokeColor(HexColor("#9A8F84")); c.setLineWidth(0.25)
    for a in range(cols + 1):
        X = mx + a * T; c.line(X, my, X, H - my)
    for b in range(rows + 1):
        Y = my + b * T; c.line(mx, Y, W - mx, Y)
    c.setStrokeColor(INK); c.setLineWidth(0.5)
    for a in range(cols + 1):
        X = mx + a * T; c.line(X, 0, X, my - 1.5 * mm); c.line(X, H - my + 1.5 * mm, X, H)
    for b in range(rows + 1):
        Y = my + b * T; c.line(0, Y, mx - 1.5 * mm, Y); c.line(W - mx + 1.5 * mm, Y, W, Y)
    lab = f"{name}  ·  {W/cm:.0f} × {H/cm:.0f} cm magnetic sheet  ·  {len(tiles)} magnets, 9 × 9 cm  ·  print at 100%"
    ly = H - my + 4 * mm if my > 9 * mm else 2 * mm
    lw = stringWidth(lab, "SansS", 7.5) + 6 * mm
    c.setFillColor(white); c.rect(W / 2 - lw / 2, ly - 2 * mm, lw, 6 * mm, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("SansS", 7.5)
    c.drawCentredString(W / 2, ly, lab)
    c.showPage(); c.save()
    return path


def main():
    R = {r[0]: r for r in RECIPES}
    rt = lambda n: (lambda c, x, y: recipe_tile(c, x, y, R[n]))
    ct = lambda i: (lambda c, x, y: container_tile(c, x, y, C[i]))
    a_tiles = [rt(n) for n in range(1, 28)]
    b_tiles = ([title_tile, safety_tile, dontfreeze_tile]
               + [ct(i) for i in range(1, 13)]
               + [rt(28), rt(29), rt(30)]
               + [stock_tile, week_tile, shop_tile])
    import tempfile
    for _ in range(1):   # measuring pass: find the size that fits every tile of each kind
        sheet(tempfile.mktemp(suffix=".pdf"), 30 * cm, 87 * cm, 3, 9, a_tiles, "m")
        sheet(tempfile.mktemp(suffix=".pdf"), 28 * cm, 67 * cm, 3, 7, b_tiles, "m")
    FIXED.update(SEEN); print("uniform sizes", FIXED)
    pa = sheet(f"{OUT}/Freezer_Kitchen_Magnets_Sheet_A_30x87cm.pdf", 30 * cm, 87 * cm, 3, 9, a_tiles, "SHEET A OF 2 · RECIPES 1–27")
    pb = sheet(f"{OUT}/Freezer_Kitchen_Magnets_Sheet_B_28x67cm.pdf", 28 * cm, 67 * cm, 3, 7, b_tiles, "SHEET B OF 2 · CONTAINERS, RECIPES 28–30, GUIDES")
    print(pa); print(pb)


if __name__ == "__main__":
    main()
