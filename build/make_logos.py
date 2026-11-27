"""Freezer Kitchen logo files as pure SVG outlines (no font needed to display)."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, "fonts")
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
INK, PAPER, TOMATO, ROSE = "#1F1B17", "#F6F1EA", "#B4472F", "#E0A48F"
CELLS = ["#7A9A6E", "#C98A3D", "#4E6577", "#A0673F", "#7D5A7B"]

fonts = {k: TTFont(os.path.join(FD, f)) for k, f in [("semi", "Fraunces-Semi.ttf"), ("ital", "Fraunces-Italic.ttf")]}

def text_path(txt, key, size, x, y):
    f = fonts[key]; gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    s = size / upm; d = []; cx = x
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is None: continue
        pen = SVGPathPen(gs); tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[g].draw(tp); d.append(pen.getCommands()); cx += gs[g].width * s
    return " ".join(d), cx

def tray(ox, oy, k, tray_fill, hole_fill):
    """Mark drawn in a 120 x 120 box at (ox, oy), scale k."""
    r = lambda x, y, w, h, rx, fill, rot=None: (f'<rect x="{ox+x*k:.2f}" y="{oy+y*k:.2f}" width="{w*k:.2f}" height="{h*k:.2f}" rx="{rx*k:.2f}" fill="{fill}"'
        + (f' transform="rotate({rot} {ox+(x+w/2)*k:.2f} {oy+(y+h/2)*k:.2f})"' if rot else "") + "/>")
    out = [r(10, 34, 100, 74, 16, tray_fill)]
    pos = [(19, 43), (48, 43), (77, 43), (19, 75), (48, 75), (77, 75)]
    cols = [CELLS[0], CELLS[1], None, CELLS[2], CELLS[3], CELLS[4]]
    for (x, y), c in zip(pos, cols):
        out.append(r(x, y, 24, 24, 6, c or hole_fill))
    out.append(r(80, 6, 25, 25, 6, TOMATO, rot=14))      # the popped cube
    return "".join(out)

def svg(w, h, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'

def wordmark(x, y, size, ink, ital_col):
    a, ax = text_path("Freezer", "semi", size, x, y)
    b, bx = text_path("Kitchen", "ital", size, ax + size * 0.24, y)
    return f'<path d="{a}" fill="{ink}"/><path d="{b}" fill="{ital_col}"/>', bx

files = {}
files["freezer-kitchen-mark.svg"] = svg(120, 120, tray(0, 0, 1, INK, "#4A423B"), "Freezer Kitchen mark")
wm, end = wordmark(4, 74, 80, INK, TOMATO)
files["freezer-kitchen-wordmark.svg"] = svg(end + 8, 96, wm, "Freezer Kitchen")
# horizontal lockup: mark + wordmark
wm2, end2 = wordmark(150, 92, 64, INK, TOMATO)
files["freezer-kitchen-lockup.svg"] = svg(end2 + 10, 132, tray(6, 6, 1.0, INK, "#4A423B") + wm2, "Freezer Kitchen")
# reversed lockup on ink
wm3, end3 = wordmark(150, 92, 64, PAPER, ROSE)
body = f'<rect width="{end3 + 26:.0f}" height="132" fill="{INK}"/>' + tray(6, 6, 1.0, PAPER, "#D9CFC2") + wm3
files["freezer-kitchen-lockup-reversed.svg"] = svg(end3 + 26, 132, body, "Freezer Kitchen")
# app icon / profile picture
files["freezer-kitchen-app-icon.svg"] = svg(512, 512, f'<rect width="512" height="512" rx="112" fill="{PAPER}"/>' + tray(76, 90, 3.0, INK, "#4A423B"), "Freezer Kitchen")
for n, s in files.items():
    open(os.path.join(OUT, n), "w").write(s); print(n, len(s))
