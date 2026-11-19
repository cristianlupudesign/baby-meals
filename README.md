# Freezer Kitchen

Batch-cooking guide for a one-year-old: 12 freezer containers, 30 quick meals.

Live site: https://cristianlupudesign.github.io/baby-meals/

## Links used by the printed QR codes

| Printed item | Link |
|---|---|
| Recipe magnets 1–30 | `#r1` … `#r30` |
| A6 card, front | `#recipes` |
| A6 card, back | `#containers` |
| A4 tracker | site home |

Keep the repo name `baby-meals` and these anchors, or the printed QR codes will stop working.

## Editing

All content lives in `build/data.py`.

```
python build/build_site.py    # rebuilds index.html
python build/build_print.py   # rebuilds the print PDFs (needs reportlab)
```
