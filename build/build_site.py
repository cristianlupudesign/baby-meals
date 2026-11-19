import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import CONTAINERS, C, CATS, RECIPES, FRESH, method

e = html.escape
OUT = os.path.join(os.path.dirname(__file__), "..", "index.html")

CSS = r"""
:root{--ink:#1F1B17;--paper:#F6F1EA;--card:#FFFDF9;--muted:#6E645A;--line:#E3D9CC;--accent:#B4472F}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.6 "Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
.serif,h1,h2,h3{font-family:"Fraunces",Georgia,"Times New Roman",serif;font-weight:600;letter-spacing:-.015em}
header.hero{padding:56px 0 36px;border-bottom:1px solid var(--line)}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 14px}
.hero h1{font-size:clamp(44px,10vw,84px);line-height:.95;margin:0 0 18px}
.hero h1 em{font-style:italic;font-weight:400;color:var(--accent)}
.hero p{margin:0;max-width:540px;font-size:19px;color:var(--muted)}
.stats{display:flex;gap:28px;flex-wrap:wrap;margin-top:28px}
.stat{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;font-weight:600}
.stat b{display:block;font:600 34px/1 "Fraunces",Georgia,serif;color:var(--ink);letter-spacing:0;text-transform:none;margin-bottom:4px}
nav{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;gap:22px;overflow-x:auto;padding:14px 16px;scrollbar-width:none}
nav a{flex:none;text-decoration:none;font-weight:600;font-size:14px;color:var(--muted)}
nav a:hover{color:var(--ink)}
section{padding:48px 0 8px;scroll-margin-top:56px}
h2{font-size:clamp(32px,6vw,46px);line-height:1.05;margin:0 0 8px}
.lead{margin:0 0 26px;color:var(--muted);font-size:18px;max-width:560px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;counter-reset:s;padding:0;margin:0;list-style:none;border-top:1px solid var(--line)}
.steps li{padding:16px 14px 16px 0;font-weight:500;border-bottom:1px solid var(--line)}
.steps li::before{counter-increment:s;content:counter(s,decimal-leading-zero);display:block;font:italic 400 28px/1 "Fraunces",Georgia,serif;color:var(--accent);margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--c);border-radius:14px;padding:20px 20px 18px;scroll-margin-top:72px;transition:box-shadow .3s}
.card:target{box-shadow:0 0 0 3px var(--paper),0 0 0 5px var(--c),0 12px 30px rgba(31,27,23,.12)}
.card .top{display:flex;align-items:baseline;gap:12px;margin-bottom:14px}
.num{flex:none;font:italic 400 30px/1 "Fraunces",Georgia,serif;color:var(--c);min-width:34px}
.card h3{margin:0;font-size:24px;line-height:1.1}
.card .tag{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--c);margin-top:4px}
.body h4{margin:16px 0 8px;font-size:11px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);font-weight:600}
.body h4:first-child{margin-top:0}
.body ol{margin:0;padding-left:20px}
.body ol li{margin:5px 0;padding-left:2px}
.body ol li::marker{color:var(--c);font-weight:600}
.contents{font:500 19px/1.35 "Fraunces",Georgia,serif;margin:0 0 4px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:7px;text-decoration:none;font-weight:500;font-size:14px;padding:4px 11px 4px 5px;border-radius:999px;background:color-mix(in srgb,var(--cc) 13%,#fff);color:color-mix(in srgb,var(--cc) 80%,#000)}
.chip i{font-style:normal;display:grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--cc);color:#fff;font-size:11px;font-weight:600}
.chip.plain{background:#EFE8DE;color:var(--ink);padding-left:11px}
.keeps{margin:16px 0 0;padding-top:12px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}
.filters button{font:500 14px/1 "Inter",system-ui,sans-serif;border:1px solid var(--line);background:var(--card);color:var(--ink);padding:9px 14px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
.filters button::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--fc,var(--ink))}
.filters button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.card.hide{display:none}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}
.panel h3{margin:0 0 8px;font-size:24px}
.panel ul{margin:0;padding:0;list-style:none}
.panel li{padding:10px 0;border-top:1px solid var(--line)}
.panel li:first-child{border-top:0}
.panel li b{font-weight:600}
footer{margin-top:56px;border-top:1px solid var(--line);color:var(--muted);padding:24px 0 40px;font-size:14px}
@media print{nav,.filters{display:none}.card{break-inside:avoid}}
"""

JS = r"""
const btns=[...document.querySelectorAll('.filters button')];
const cards=[...document.querySelectorAll('#recipes .card')];
btns.forEach(b=>b.addEventListener('click',()=>{
  btns.forEach(x=>x.setAttribute('aria-pressed',x===b));
  const f=b.dataset.f;
  cards.forEach(c=>c.classList.toggle('hide',f!=='all'&&c.dataset.cat!==f));
}));
function showTarget(instant){
  const t=location.hash&&document.querySelector(location.hash);
  if(!t)return;
  if(t.classList.contains('hide'))btns[0].click();
  t.scrollIntoView({behavior:instant?'instant':'smooth',block:'start'});
}
addEventListener('hashchange',()=>showTarget(false));
const land=()=>showTarget(true);
(document.fonts?document.fonts.ready:Promise.resolve()).then(()=>{land();setTimeout(land,300);});
"""


def chip_c(i):
    _, n, col, _, _ = C[i]
    return f'<a class="chip" href="#c{i}" style="--cc:{col}"><i>{i}</i>{e(n)}</a>'


def container_card(c):
    i, n, col, contents, prep = c
    li = "".join(f"<li>{e(s)}</li>" for s in prep)
    return f"""<article class="card" id="c{i}" style="--c:{col}">
<div class="top"><span class="num">{i:02d}</span><div><h3>{e(n)}</h3><div class="tag">Container</div></div></div>
<div class="body"><h4>Inside</h4><p class="contents">{e(contents)}</p><h4>How to prep</h4><ol>{li}</ol>
<p class="keeps">Cool within 1 hour · ice cube trays · bag, label &amp; date · keeps 3 months</p></div></article>"""


def recipe_card(r):
    num, name, cat, cons, extras, fresh, finish = r
    col = CATS[cat]
    chips = "".join(chip_c(i) for i in cons)
    chips += "".join(f'<span class="chip plain">{e(x)}</span>' for x in extras)
    if fresh:
        chips += f'<span class="chip plain">{e(FRESH[fresh][0])}</span>'
    li = "".join(f"<li>{e(s)}</li>" for s in method(r))
    return f"""<article class="card" id="r{num}" data-cat="{e(cat)}" style="--c:{col}">
<div class="top"><span class="num">{num:02d}</span><div><h3>{e(name)}</h3><div class="tag">{e(cat)} · 5–15 min</div></div></div>
<div class="body"><h4>You need</h4><div class="chips">{chips}</div><h4>Method</h4><ol>{li}</ol></div></article>"""


filters = '<button data-f="all" aria-pressed="true">All 30</button>' + "".join(
    f'<button data-f="{e(k)}" aria-pressed="false" style="--fc:{v}">{e(k)}</button>' for k, v in CATS.items())

page = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Freezer Kitchen · 12 containers, 30 baby meals</title>
<meta name="description" content="Batch-cook 12 freezer containers and mix them into 30 quick meals for a one-year-old.">
<meta name="theme-color" content="#F6F1EA">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231F1B17'/%3E%3Crect x='14' y='14' width='16' height='16' rx='3' fill='%23C98A3D'/%3E%3Crect x='34' y='14' width='16' height='16' rx='3' fill='%23B4472F'/%3E%3Crect x='14' y='34' width='16' height='16' rx='3' fill='%237A9A6E'/%3E%3Crect x='34' y='34' width='16' height='16' rx='3' fill='%234E6577'/%3E%3C/svg%3E">
<style>{CSS}</style></head><body>
<header class="hero"><div class="wrap">
<p class="eyebrow">Batch cooking · 12 months+</p>
<h1>Freezer <em>Kitchen</em></h1>
<p>Cook 12 freezer containers once. Mix the cubes into 30 meals for your one-year-old in 5–15 minutes.</p>
<div class="stats"><div class="stat"><b>12</b>containers</div><div class="stat"><b>30</b>meals</div><div class="stat"><b>3</b>months frozen</div></div>
</div></header>
<nav><div class="wrap"><a href="#how">How it works</a><a href="#containers">Containers</a><a href="#recipes">Recipes</a><a href="#safety">Safety</a></div></nav>
<main class="wrap">
<section id="how"><h2>How it works</h2><p class="lead">No salt, no sugar. Everything cooked until soft.</p>
<ol class="steps"><li>Cook each container's mix</li><li>Cool it within 1 hour</li><li>Freeze in ice cube trays</li><li>Bag, label and date the cubes</li><li>Mix about 2 cubes of each, heat until piping hot</li><li>Cool and serve</li></ol></section>
<section id="containers"><h2>The 12 containers</h2><p class="lead">What goes in each one and how to prep it.</p>
<div class="grid">{''.join(container_card(c) for c in CONTAINERS)}</div></section>
<section id="recipes"><h2>30 meals</h2><p class="lead">Tap a container to see how it's made.</p>
<div class="filters">{filters}</div>
<div class="grid">{''.join(recipe_card(r) for r in RECIPES)}</div></section>
<section id="safety"><h2>Safety</h2><p class="lead">The few rules that matter.</p><div class="two">
<div class="panel"><h3>Don't freeze</h3><ul>
<li><b>Cooked egg</b> goes rubbery. Make it fresh.</li>
<li><b>Cucumber, lettuce, raw tomato</b> go mushy. Serve fresh.</li>
<li><b>Potato chunks</b> go grainy. Freeze as mash.</li>
<li><b>Yoghurt and soft cheese</b> separate. Add fresh after heating.</li></ul></div>
<div class="panel"><h3>Stay safe</h3><ul>
<li><b>Reheat</b> until piping hot, then cool before serving.</li>
<li><b>Never refreeze</b> food that has thawed.</li>
<li><b>Rice:</b> cool within 1 hour, reheat only once.</li>
<li><b>No honey</b> before age 1, <b>no whole nuts</b>.</li>
<li><b>Quarter</b> grapes and cherry tomatoes.</li>
<li><b>No added salt or sugar.</b> Use no-salt tinned beans.</li></ul></div>
</div></section>
</main>
<footer><div class="wrap">Freezer Kitchen · batch-cooking guide for ages 12 months and up. Check with your health visitor about allergies.</div></footer>
<script>{JS}</script></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("written", os.path.abspath(OUT))
