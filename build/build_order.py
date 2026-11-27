"""Turn a customer's order code into a print-and-cut PDF of 8 x 8 cm magnets.

    python build/build_order.py FK.R01.R09.G8-2-4-6p...

Output: Freezer_Kitchen_Order_<n>magnets_<date>.pdf, 3 magnets across (30 cm wide),
as many rows as the order needs, with the order code printed in the margin."""
import os, sys, datetime, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate import parse_code
import build_magnet_sheets as M
from reportlab.lib.units import cm, mm
from reportlab.pdfbase.pdfmetrics import stringWidth


def build(code, out_dir=M.OUT):
    items = parse_code(code)
    if not 10 <= len(items) <= 60:
        raise SystemExit(f"Order has {len(items)} magnets; must be 10–60.")
    tiles = [(lambda r: (lambda c, x, y: M.recipe_tile(c, x, y, r)))(r) for r in items]
    cols = 3; rows = -(-len(tiles) // cols)
    W = 30 * cm; H = 18 * mm + rows * M.T + 22 * mm
    stamp = datetime.date.today().strftime("%Y-%m-%d")
    path = os.path.join(out_dir, f"Freezer_Kitchen_Order_{len(items)}magnets_{stamp}.pdf")
    name = f"ORDER {stamp}"
    M.FIXED.clear(); M.SEEN.clear()
    M.sheet(tempfile.mktemp(suffix=".pdf"), W, H, cols, rows, tiles, name)   # measuring pass
    M.FIXED.update(M.SEEN)
    M.sheet(path, W, H, cols, rows, tiles, name, footer=f"Order code: {code}")
    return path, items


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    path, items = build(sys.argv[1])
    print(path)
    for i, r in enumerate(items, 1):
        print(f"{i:2d}. {r[1]}")
