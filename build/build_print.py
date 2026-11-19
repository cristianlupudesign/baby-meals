import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import BASE, CONTAINERS, C, CATS, RECIPES, ingredient_lines
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

FD = os.path.join(HERE, "fonts")
for n, f in [("Serif", "Fraunces-Semi.ttf"), ("SerifR", "Fraunces-Reg.ttf"),
             ("Sans", "Inter-Reg.ttf"), ("SansS", "Inter-Semi.ttf"), ("SansB", "Inter-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))

OUT = "/mnt/user-data/outputs"
os.makedirs(OUT, exist_ok=True)
INK = HexColor("#1F1B17"); PAPER = HexColor("#F6F1EA"); MUTED = HexColor("#6E645A")
LINE = HexColor("#DDD2C4"); ACC = HexColor("#B4472F")


def fit(t, fs, w, font="Sans"):
    while stringWidth(t, font, fs) > w and fs > 4:
        fs -= 0.25
    return fs


def spaced(c, x, y, t, font, fs, track, color, align="l"):
    """Letter-spaced small caps style label."""
    w = stringWidth(t, font, fs) + track * (len(t) - 1)
    if align == "r":
        x -= w
    to = c.beginText(x, y); to.setFont(font, fs); to.setCharSpace(track); to.setFillColor(color)
    to.textOut(t); to.setCharSpace(0); c.drawText(to)
    return w


def qr(c, url, x, y, size, bg=white):
    w = QrCodeWidget(url, barLevel="M", barBorder=0, barFillColor=INK, barStrokeColor=INK)
    b = w.getBounds(); bw, bh = b[2] - b[0], b[3] - b[1]
    pad = size * 0.07
    c.setFillColor(bg); c.roundRect(x, y, size, size, size * 0.06, fill=1, stroke=0)
    s = size - 2 * pad
    d = Drawing(s, s, transform=[s / bw, 0, 0, s / bh, 0, 0]); d.add(w)
    renderPDF.draw(d, c, x + pad, y + pad)


def wrap2(name, font, fs, w):
    words = name.split()
    if stringWidth(name, font, fs) <= w or len(words) == 1:
        return [name]
    best = None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        m = max(stringWidth(a, font, fs), stringWidth(b, font, fs))
        if best is None or m < best[0]:
            best = (m, [a, b])
    return best[1]


def dotnum(c, x, y, r, n, col, fs=None):
    c.setFillColor(col); c.circle(x, y, r, fill=1, stroke=0)
    fs = fs or r * 1.05
    c.setFillColor(white); c.setFont("SansS", fs); c.drawCentredString(x, y - fs * 0.36, str(n))


def heart(c, hx, hy, hs, col, lw=0.9):
    p = c.beginPath()
    p.moveTo(hx, hy - hs * 1.15)
    p.curveTo(hx - hs * 2.1, hy + hs * 0.2, hx - hs * 0.9, hy + hs * 1.6, hx, hy + hs * 0.55)
    p.curveTo(hx + hs * 0.9, hy + hs * 1.6, hx + hs * 2.1, hy + hs * 0.2, hx, hy - hs * 1.15)
    c.setStrokeColor(col); c.setLineWidth(lw); c.drawPath(p, stroke=1, fill=0)


# ---------------- MAGNETS: 3 sheets, 11.5 x 7.5 in, 10 per sheet ----------------
def magnets():
    SW, SH = 11.5 * inch, 7.5 * inch
    cols, rows = 5, 2
    cw, ch = 2.2 * inch, 3.4 * inch
    mx, my = (SW - cols * cw) / 2, (SH - rows * ch) / 2
    f = f"{OUT}/Freezer_Kitchen_Magnets_PrintCut.pdf"
    c = canvas.Canvas(f, pagesize=(SW, SH)); c.setTitle("Freezer Kitchen magnets")
    N = len(RECIPES) // 10
    pad = 12
    for s in range(N):
        for k in range(10):
            r = RECIPES[s * 10 + k]; num, name, cat = r[0], r[1], r[2]
            col = HexColor(CATS[cat])
            x = mx + (k % cols) * cw; top = SH - my - (k // cols) * ch; bot = top - ch
            c.setFillColor(PAPER); c.rect(x, bot, cw, ch, fill=1, stroke=0)
            c.setFillColor(col); c.rect(x, top - 7, cw, 7, fill=1, stroke=0)
            # number + category
            c.setFillColor(col); c.setFont("SerifR", 24)
            # italic look: Fraunces Reg upright; skew for italic feel
            c.saveState(); c.translate(x + pad, top - 36); c.skew(0, 12)
            c.drawString(0, 0, f"{num:02d}"); c.restoreState()
            spaced(c, x + cw - pad, top - 32, cat.upper(), "SansS", 6.3, 1.1, col, align="r")
            # name
            tw = cw - 2 * pad; fs = 18
            lines = wrap2(name, "Serif", fs, tw)
            fs = min(fs, min(fit(l, fs, tw, "Serif") for l in lines))
            c.setFillColor(INK); c.setFont("Serif", fs); ty = top - 42 - fs
            for l in lines:
                c.drawString(x + pad, ty, l); ty -= fs * 1.08
            ry = ty + fs * 1.08 - 9
            c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(x + pad, ry, x + cw - pad, ry)
            # footer: QR
            qs = 0.78 * inch; qx = x + cw - pad - qs + 3; qy = bot + pad - 3
            qr(c, f"{BASE}#r{num}", qx, qy, qs)
            fy = qy + qs + 8
            c.setStrokeColor(LINE); c.line(x + pad, fy, x + cw - pad, fy)
            spaced(c, x + pad, qy + qs - 12, "SCAN FOR", "SansS", 6, 1, MUTED)
            c.setFillColor(INK); c.setFont("Serif", 13)
            c.drawString(x + pad, qy + qs - 28, "the method")
            c.setFillColor(MUTED); c.setFont("Sans", 6.6)
            c.drawString(x + pad, qy + 11, "2 cubes of each")
            c.drawString(x + pad, qy + 2, "heat 5–7 min")
            # ingredients
            items = ingredient_lines(r)
            area_top = ry - 6; area_bot = fy + 6
            step = min(19, (area_top - area_bot) / len(items))
            ifs = min(10.5, min(fit(t, 10.5, cw - 2 * pad - 18) for t, _ in items))
            for j, (t, cc) in enumerate(items):
                cy = area_top - step * (j + 0.5)
                if cc:
                    cid = next(cn[0] for cn in CONTAINERS if cn[1] == t)
                    dotnum(c, x + pad + 6, cy, 6, cid, HexColor(cc), fs=6.4)
                    c.setFillColor(INK); c.setFont("SansS", ifs)
                else:
                    c.setStrokeColor(MUTED); c.setLineWidth(0.8); c.circle(x + pad + 6, cy, 2.4, fill=0, stroke=1)
                    c.setFillColor(MUTED); c.setFont("Sans", ifs)
                c.drawString(x + pad + 17, cy - ifs * 0.36, t)
        # cut guides
        c.setStrokeColor(INK); c.setLineWidth(0.5); c.setDash(4, 3)
        for a in range(cols + 1):
            X = mx + a * cw; c.line(X, 0, X, my - 2); c.line(X, SH - my + 2, X, SH)
        for b in range(rows + 1):
            Y = my + b * ch; c.line(0, Y, mx - 2, Y); c.line(SW - mx + 2, Y, SW, Y)
        c.setDash(); c.setStrokeColor(LINE); c.setLineWidth(0.4)
        for a in range(1, cols):
            X = mx + a * cw; c.line(X, my, X, SH - my)
        c.line(mx, my + ch, SW - mx, my + ch)
        c.setFillColor(INK); c.setFont("SansS", 8.5)
        c.drawString(mx, my - 14, f"SHEET {s+1} OF {N}   ·   Recipes {s*10+1}–{s*10+10}   ·   10 magnets   ·   2.2 × 3.4 in each   ·   Print at 100% (no scaling)")
        c.showPage()
    c.save(); return f


# ---------------- A6 CARD: double-sided ----------------
PREP_SHORT = {
    1: "Steam 5–6 min until soft. Chop small or mash lightly.",
    2: "Peel, dice, boil 15 min. Mash or chop small.",
    3: "Roast at 200 °C for 40 min. Scoop out and mash.",
    4: "Wilt 2–3 min in a splash of water. Squeeze, chop fine.",
    5: "Soften peppers and courgette 8–10 min. Add corn, mash.",
    6: "Soften onion and garlic, add tomatoes, simmer 20 min, blend.",
    7: "Boil cauli soft. Make a cheese sauce, blend together.",
    8: "Poach thighs about 20 min until cooked. Shred fine.",
    9: "Brown in a dry pan until no pink. Break up small, drain.",
    10: "Cook like the beef. Stir in red sauce to keep moist.",
    11: "Simmer lentils 15–20 min. Add rinsed beans, mash.",
    12: "Stew apple and pear 10 min. Add mango and berries, mash.",
}


def wrap(t, font, fs, w):
    words = t.split(); lines = [""]
    for wd in words:
        trial = (lines[-1] + " " + wd).strip()
        if stringWidth(trial, font, fs) <= w:
            lines[-1] = trial
        else:
            lines.append(wd)
    return lines


def a6():
    W, H = 105 * mm, 148 * mm
    f = f"{OUT}/Freezer_Kitchen_A6_Card.pdf"
    c = canvas.Canvas(f, pagesize=(W, H)); c.setTitle("Freezer Kitchen A6 card")
    m = 6 * mm

    def side(t1, t2, url, scan, text_for, foot):
        c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
        qs = 17 * mm; qy = H - m - qs
        qr(c, url, W - m - qs, qy, qs)
        spaced(c, m, H - m - 6, "FREEZER KITCHEN", "SansS", 6, 1.3, ACC)
        c.setFillColor(INK); c.setFont("Serif", 21); c.drawString(m, H - m - 25, t1)
        c.setFillColor(ACC); c.saveState(); c.translate(m + stringWidth(t1 + " ", "Serif", 21), H - m - 25)
        c.skew(0, 12); c.setFont("SerifR", 21); c.drawString(0, 0, t2); c.restoreState()
        c.setFillColor(MUTED); c.setFont("Sans", 6.4)
        c.drawRightString(W - m - qs - 2.5 * mm, qy + 3, scan)
        top = qy - 3.5 * mm; bot = 11 * mm; n = 12; rh = (top - bot) / n
        c.setStrokeColor(INK); c.setLineWidth(0.9); c.line(m, top, W - m, top)
        split = 31 * mm
        for i, (cid, name, col, contents, _) in enumerate(CONTAINERS):
            y = top - i * rh; cy = y - rh / 2
            dotnum(c, m + 2.6 * mm, cy, 2.6 * mm, cid, HexColor(col), fs=7)
            nm_w = split - 9.5 * mm
            fs = fit(name, 10, nm_w, "Serif")
            c.setFillColor(INK); c.setFont("Serif", fs); c.drawString(m + 6.6 * mm, cy - fs * 0.34, name)
            t = text_for(cid); iw = W - 2 * m - split - 1 * mm
            fs = 7.4; ls = wrap(t, "Sans", fs, iw)
            while len(ls) > 2:
                fs -= 0.2; ls = wrap(t, "Sans", fs, iw)
            c.setFillColor(INK if text_for is contents_of else MUTED)
            c.setFont("Sans" if text_for is not contents_of else "SansS", fs)
            lh = fs * 1.22; yy = cy + (len(ls) - 1) * lh / 2 - fs * 0.34
            for j, l in enumerate(ls):
                c.drawString(m + split + 1 * mm, yy - j * lh, l)
            if i < n - 1:
                c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(m, y - rh, W - m, y - rh)
        c.setStrokeColor(INK); c.setLineWidth(0.9); c.line(m, bot, W - m, bot)
        c.setFillColor(MUTED); c.setFont("Sans", 6.3)
        c.drawCentredString(W / 2, bot - 5.5 * mm, foot)

    def contents_of(cid):
        return C[cid][3]

    side("The 12", "containers", f"{BASE}#recipes", "Scan for 30 meals →", contents_of,
         "Cool within 1 hour · freeze in cubes · bag and date · keeps 3 months")
    c.showPage()
    side("How to", "prep", f"{BASE}#containers", "Scan for the full guide →", lambda cid: PREP_SHORT[cid],
         "No salt or sugar · reheat until piping hot · cool · never refreeze")
    c.showPage(); c.save(); return f


# ---------------- A4 FREEZER TRACKER ----------------
def tracker():
    W, H = 210 * mm, 297 * mm
    f = f"{OUT}/Freezer_Kitchen_Tracker_A4.pdf"
    c = canvas.Canvas(f, pagesize=(W, H)); c.setTitle("Freezer Kitchen tracker")
    m = 13 * mm
    c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
    # header
    qs = 23 * mm; qx = W - m - qs; qy = H - m - qs
    qr(c, BASE, qx, qy, qs, bg=white)
    spaced(c, m, H - m - 7, "BATCH COOKING · 12 MONTHS+", "SansS", 7, 1.5, ACC)
    c.setFillColor(INK); c.setFont("Serif", 36); c.drawString(m, H - m - 40, "Freezer")
    c.setFillColor(ACC); c.saveState(); c.translate(m + stringWidth("Freezer ", "Serif", 36), H - m - 40)
    c.skew(0, 12); c.setFont("SerifR", 36); c.drawString(0, 0, "Kitchen"); c.restoreState()
    c.setFillColor(MUTED); c.setFont("Sans", 9)
    c.drawString(m, H - m - 55, "Tick a box for every bag in the freezer and wipe it off when you use one.")
    c.drawRightString(qx - 3 * mm, qy + qs - 10, "Recipes, methods")
    c.drawRightString(qx - 3 * mm, qy + qs - 21, "and prep guide →")

    def boxes(x, cy, n, s=3.9 * mm, gap=1.5 * mm, col=INK):
        c.setStrokeColor(col); c.setLineWidth(0.8)
        for k in range(n):
            c.roundRect(x + k * (s + gap), cy - s / 2, s, s, 0.7 * mm, fill=0, stroke=1)
        return x + n * (s + gap)

    def section(y, title, right=None):
        c.setFillColor(INK); c.setFont("Serif", 15); c.drawString(m, y, title)
        if right:
            spaced(c, W - m, y + 1, right, "SansS", 6.2, 1.2, MUTED, align="r")
        c.setStrokeColor(INK); c.setLineWidth(1); c.line(m, y - 4 * mm, W - m, y - 4 * mm)
        return y - 4 * mm

    y = section(H - m - 82, "My 12 containers", "BAGS IN THE FREEZER          FROZEN ON")
    rh = 8.4 * mm
    bx0 = W - m - 64 * mm
    for i, (cid, name, col, contents, _) in enumerate(CONTAINERS):
        top = y - i * rh; cy = top - rh / 2; colr = HexColor(col)
        dotnum(c, m + 3 * mm, cy, 3 * mm, cid, colr, fs=8)
        c.setFillColor(INK); c.setFont("Serif", 11.5); c.drawString(m + 8 * mm, cy - 3.9, name)
        c.setFillColor(MUTED); c.setFont("Sans", fit(contents, 8.4, bx0 - (m + 45 * mm) - 4 * mm))
        c.drawString(m + 45 * mm, cy - 2.9, contents)
        boxes(bx0, cy, 6, col=colr)
        c.setStrokeColor(LINE); c.setLineWidth(0.7)
        c.line(W - m - 22 * mm, cy - 2.6 * mm, W - m, cy - 2.6 * mm)
        if i < 11:
            c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(m, top - rh, W - m, top - rh)
    y = y - 12 * rh - 9 * mm
    y = section(y, "30 meals", "TICK WHEN MADE  ·  HEART THE FAVOURITES")
    colw = (W - 2 * m - 8 * mm) / 2; mrh = 6.75 * mm
    for idx, r in enumerate(RECIPES):
        col_i = 0 if idx < 15 else 1; row = idx % 15
        x = m + col_i * (colw + 8 * mm); top = y - row * mrh; cy = top - mrh / 2
        colr = HexColor(CATS[r[2]])
        c.setFillColor(colr); c.saveState(); c.translate(x, cy - 3.4); c.skew(0, 12)
        c.setFont("SerifR", 10.5); c.drawString(0, 0, f"{r[0]:02d}"); c.restoreState()
        c.setFillColor(INK); c.setFont("SansS", fit(r[1], 8.8, colw - 44 * mm, "SansS"))
        c.drawString(x + 7.5 * mm, cy - 3.1, r[1])
        bx = boxes(x + colw - 31 * mm, cy, 4, s=3.6 * mm, gap=1.3 * mm, col=colr)
        heart(c, bx + 2.6 * mm, cy, 1.45 * mm, colr)
        if row < 14:
            c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(x, top - mrh, x + colw, top - mrh)
    # key + footer
    ky = y - 15 * mrh - 7 * mm
    kx = m
    for cat, col in CATS.items():
        c.setFillColor(HexColor(col)); c.circle(kx + 1.4 * mm, ky + 1.1 * mm, 1.4 * mm, fill=1, stroke=0)
        c.setFillColor(MUTED); c.setFont("Sans", 7.6); c.drawString(kx + 4 * mm, ky, cat)
        kx += 4 * mm + stringWidth(cat, "Sans", 7.6) + 6 * mm
    c.setStrokeColor(INK); c.setLineWidth(1); c.line(m, m + 6 * mm, W - m, m + 6 * mm)
    c.setFillColor(MUTED); c.setFont("Sans", 7.4)
    c.drawString(m, m + 1.5 * mm, "Reheat until piping hot, then cool  ·  Never refreeze  ·  Rice: reheat once  ·  No honey under 1  ·  No whole nuts  ·  No added salt or sugar")
    c.showPage(); c.save(); return f


if __name__ == "__main__":
    for fn in (magnets, a6, tracker):
        print(fn())
