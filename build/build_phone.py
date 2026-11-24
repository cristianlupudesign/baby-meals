"""Phone wallpapers / camera-roll cards: 1170 x 2532 PNG (390x844 @3x)."""
import os, sys, html, asyncio
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import CONTAINERS, C, CATS, RECIPES, FRESH
from build_print import PREP_SHORT
from playwright.async_api import async_playwright

e = html.escape
OUT = "/mnt/user-data/outputs/phone"
os.makedirs(OUT, exist_ok=True)
F = f"file://{HERE}/fonts"

CSS = f"""
@font-face{{font-family:Fr;src:url({F}/Fraunces-Semi.ttf)}}
@font-face{{font-family:FrR;src:url({F}/Fraunces-Reg.ttf)}}
@font-face{{font-family:In;src:url({F}/Inter-Reg.ttf)}}
@font-face{{font-family:InS;src:url({F}/Inter-Semi.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:390px;height:844px;background:#F6F1EA;color:#1F1B17;font-family:In,sans-serif;overflow:hidden}}
.page{{height:844px;padding:54px 22px 22px;display:flex;flex-direction:column}}
.eyebrow{{font:11px/1 InS;letter-spacing:.16em;color:#B4472F;text-transform:uppercase}}
h1{{font:600 38px/1 Fr;letter-spacing:-.02em;margin:10px 0 6px}}
h1 em{{font:italic 38px/1 FrR;color:#B4472F;display:inline-block;transform:skewX(-12deg)}}
.sub{{font:13.5px/1.4 In;color:#6E645A;margin-bottom:14px}}
.list{{flex:1;display:flex;flex-direction:column;border-top:1.5px solid #1F1B17;border-bottom:1.5px solid #1F1B17}}
.row{{flex:1;display:flex;align-items:center;gap:11px;border-top:1px solid #DDD2C4;min-height:0}}
.row:first-child{{border-top:0}}
.dot{{flex:none;width:26px;height:26px;border-radius:50%;background:var(--c);color:#fff;font:12px/26px InS;text-align:center}}
.name{{flex:none;width:118px;font:600 16px/1.1 Fr}}
.txt{{flex:1;font:13.5px/1.3 In;color:#1F1B17}}
.txt.m{{color:#5E554C;font-size:12.6px}}
.num{{flex:none;width:30px;font:italic 21px/1 FrR;color:var(--c);transform:skewX(-12deg)}}
.meal{{flex:1;min-width:0}}
.meal b{{display:block;font:600 16px/1.1 Fr;margin-bottom:3px}}
.chips{{display:flex;flex-wrap:wrap;gap:4px;align-items:center}}
.chip{{width:17px;height:17px;border-radius:50%;background:var(--c);color:#fff;font:9.5px/17px InS;text-align:center}}
.fresh{{font:11.5px/1 In;color:#6E645A;margin-left:4px}}
.foot{{font:11.5px/1.4 In;color:#6E645A;text-align:center;margin-top:12px}}
.foot b{{white-space:nowrap;font-family:InS;color:#1F1B17;font-weight:normal}}
.key{{display:flex;flex-wrap:wrap;gap:5px 11px;margin-top:8px;font:11px/1 In;color:#6E645A}}
.key span::before{{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--c);margin-right:5px}}
"""
SITE = "cristianlupudesign.github.io/baby-meals"


def page(eyebrow, t1, t2, sub, body, foot):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="page"><div class="eyebrow">{e(eyebrow)}</div><h1>{e(t1)} <em>{e(t2)}</em></h1>
<p class="sub">{sub}</p><div class="list">{body}</div><p class="foot">{foot}</p></div></body></html>"""


def containers():
    rows = "".join(f'<div class="row"><span class="dot" style="--c:{col}">{i}</span>'
                   f'<span class="name">{e(n)}</span><span class="txt">{e(t)}</span></div>'
                   for i, n, col, t, _ in CONTAINERS)
    return page("Freezer Kitchen · 1 of 4", "The 12", "containers",
                "What goes in each one. Freeze in ice cube trays, bag and date.",
                rows, f"Keeps 3 months · <b>{SITE}</b>")


def prep():
    rows = "".join(f'<div class="row"><span class="dot" style="--c:{col}">{i}</span>'
                   f'<span class="name">{e(n)}</span><span class="txt m">{e(PREP_SHORT[i])}</span></div>'
                   for i, n, col, t, _ in CONTAINERS)
    return page("Freezer Kitchen · 2 of 4", "How to", "prep",
                "No salt or sugar. Cook until soft, cool within 1 hour.",
                rows, "Reheat until piping hot · cool before serving · never refreeze")


def meals(part):
    rs = RECIPES[:15] if part == 1 else RECIPES[15:]
    rows = ""
    for r in rs:
        num, name, cat, cons, extras, fresh, _ = r
        col = CATS[cat]
        chips = "".join(f'<span class="chip" style="--c:{C[i][2]}">{i}</span>' for i in cons)
        fr = f'<span class="fresh">+ {e(FRESH[fresh][0].replace("Fresh ", "").lower())}</span>' if fresh else ""
        rows += (f'<div class="row"><span class="num" style="--c:{col}">{num:02d}</span>'
                 f'<div class="meal"><b>{e(name)}</b><div class="chips">{chips}{fr}</div></div></div>')
    rng = "1–15" if part == 1 else "16–30"
    key = '<div class="key">' + "".join(f'<span style="--c:{v}">{e(k)}</span>' for k, v in CATS.items()) + "</div>"
    return page(f"Freezer Kitchen · {2 + part} of 4", "30 meals", rng,
                "Numbers are the containers. 2 cubes each, <span style=\"white-space:nowrap\">heat 5–7 min</span>.",
                rows, f"Full methods: <b>{SITE}</b>")


async def main():
    pages = [("1_Containers", containers()), ("2_How_to_prep", prep()),
             ("3_Meals_1-15", meals(1)), ("4_Meals_16-30", meals(2))]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
        for name, h in pages:
            src = f"/tmp/phone_{name}.html"
            open(src, "w", encoding="utf-8").write(h)
            await pg.goto(f"file://{src}"); await pg.wait_for_timeout(300)
            ov = await pg.evaluate("document.querySelector('.page').scrollHeight")
            await pg.screenshot(path=f"{OUT}/Freezer_Kitchen_{name}.png")
            print(name, "height", ov)
        await b.close()

asyncio.run(main())
