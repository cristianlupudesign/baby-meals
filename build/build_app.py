"""Builds app/index.html: pick your frozen containers -> recipes -> order custom magnets (min 10)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import CONTAINERS, CATS, RECIPES, FRESH, method

OUT = os.path.join(HERE, "..", "app", "index.html")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

DATA = {
    "containers": [{"id": i, "name": n, "col": col, "contents": t} for i, n, col, t, _ in CONTAINERS],
    "recipes": [{"n": r[0], "name": r[1], "cat": r[2], "cons": r[3], "extras": r[4],
                 "fresh": FRESH[r[5]][0] if r[5] else None, "method": method(r)} for r in RECIPES],
    "cats": CATS,
    "freshStep": {k: FRESH[k][1] for k in ("rice", "pasta", "mash", "couscous", "quinoa")},
}

CSS = r"""
:root{--ink:#1F1B17;--paper:#F6F1EA;--card:#FFFDF9;--muted:#6E645A;--line:#E3D9CC;--accent:#B4472F}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.55 "Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding-bottom:96px}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
h1,h2,h3,.serif{font-family:"Fraunces",Georgia,serif;font-weight:600;letter-spacing:-.015em}
.top{display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-bottom:1px solid var(--line)}
.top a{text-decoration:none;font-weight:600;font-size:14px;color:var(--muted)}
.brand{font:600 18px/1 "Fraunces",Georgia,serif;color:var(--ink)!important}
.brand em{font-style:italic;font-weight:400;color:var(--accent)}
.hero{padding:34px 0 10px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
.hero h1{font-size:clamp(34px,8vw,58px);line-height:1;margin:0 0 12px}
.hero h1 em{font-style:italic;font-weight:400;color:var(--accent)}
.hero p{margin:0;color:var(--muted);font-size:17px;max-width:560px}
.step{display:flex;align-items:baseline;gap:10px;margin:30px 0 14px}
.step b{font:italic 400 26px/1 "Fraunces",Georgia,serif;color:var(--accent)}
.step h2{margin:0;font-size:26px}
.tools{display:flex;gap:8px;margin:0 0 12px}
.btn-s{font:500 14px/1 "Inter",sans-serif;border:1px solid var(--line);background:var(--card);color:var(--ink);padding:9px 14px;border-radius:999px;cursor:pointer}
.picker{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.pick{display:flex;gap:10px;align-items:flex-start;text-align:left;background:var(--card);border:1.5px solid var(--line);border-radius:14px;padding:12px;cursor:pointer;font:inherit;color:inherit;transition:border-color .15s,background .15s}
.pick .d{flex:none;display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:color-mix(in srgb,var(--c) 14%,#fff);color:var(--c);font-weight:600;font-size:13px;transition:all .15s}
.pick b{display:block;font:600 16px/1.2 "Fraunces",Georgia,serif}
.pick small{display:block;color:var(--muted);font-size:12.5px;line-height:1.3;margin-top:2px}
.pick[aria-pressed=true]{border-color:var(--c);background:color-mix(in srgb,var(--c) 8%,var(--card))}
.pick[aria-pressed=true] .d{background:var(--c);color:#fff}
.empty{background:var(--card);border:1px dashed var(--line);border-radius:14px;padding:22px;color:var(--muted);text-align:center}
.group h3{font-size:22px;margin:22px 0 4px}
.group p.note{margin:0 0 12px;color:var(--muted);font-size:14.5px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--c);border-radius:14px;padding:16px 16px 14px;display:flex;flex-direction:column}
.card.dim{opacity:.72}
.card .t{display:flex;gap:10px;align-items:baseline}
.card .n{font:italic 400 24px/1 "Fraunces",Georgia,serif;color:var(--c);min-width:28px}
.card h4{margin:0;font:600 20px/1.15 "Fraunces",Georgia,serif}
.tag{font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--c);margin:4px 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:500;padding:3px 10px 3px 4px;border-radius:999px;background:color-mix(in srgb,var(--cc) 13%,#fff);color:color-mix(in srgb,var(--cc) 80%,#000)}
.chip i{font-style:normal;display:grid;place-items:center;width:19px;height:19px;border-radius:50%;background:var(--cc);color:#fff;font-size:10.5px;font-weight:600}
.chip.plain{background:#EFE8DE;color:var(--ink);padding-left:10px}
.chip.miss{background:#fff;border:1px dashed var(--cc);color:var(--cc)}
details{margin:2px 0 12px}
summary{cursor:pointer;font-weight:600;font-size:14px;color:var(--muted)}
details ol{margin:8px 0 0;padding-left:20px;font-size:14.5px}
details li{margin:3px 0}
.row{display:flex;gap:8px;align-items:center;margin-top:auto}
select{font:500 14px "Inter",sans-serif;border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:#fff;color:var(--ink)}
.add{flex:1;font:600 14.5px/1 "Inter",sans-serif;border:1.5px solid var(--ink);background:var(--card);color:var(--ink);padding:11px 12px;border-radius:12px;cursor:pointer}
.add[aria-pressed=true]{background:var(--ink);color:var(--paper)}
.more{margin:14px 0 0}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:20;background:var(--ink);color:var(--paper);padding:12px 0 calc(12px + env(safe-area-inset-bottom))}
.bar .wrap{display:flex;align-items:center;gap:14px}
.bar .info{flex:1;min-width:0}
.bar b{font:600 18px/1.1 "Fraunces",Georgia,serif;display:block}
.bar small{color:#CFC6BC;font-size:13px}
.meter{height:4px;background:#3A332D;border-radius:4px;margin-top:6px;overflow:hidden}
.meter i{display:block;height:100%;background:#E0A48F;width:0;transition:width .25s}
.go{flex:none;font:600 15px/1 "Inter",sans-serif;border:0;background:var(--paper);color:var(--ink);padding:13px 16px;border-radius:12px;cursor:pointer}
.go:disabled{opacity:.45;cursor:not-allowed}
.sheet{position:fixed;inset:0;z-index:30;background:rgba(31,27,23,.5);display:none;align-items:flex-end;justify-content:center}
.sheet.open{display:flex}
.panel{background:var(--paper);width:100%;max-width:760px;max-height:92vh;overflow:auto;border-radius:18px 18px 0 0;padding:20px 16px 28px}
.panel header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel h2{margin:0;font-size:28px}
.x{border:0;background:transparent;font-size:28px;line-height:1;cursor:pointer;color:var(--muted)}
.mags{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0}
.mag{position:relative;aspect-ratio:1;background:#F6F1EA;border:1px solid var(--line);border-radius:6px;padding:6px;box-shadow:0 2px 6px rgba(31,27,23,.08);display:flex;flex-direction:column}
.mag .hb{background:var(--c);color:#fff;border-radius:4px;padding:6px 7px;display:flex;gap:6px;align-items:baseline}
.mag .hb i{font:italic 400 15px/1 "Fraunces",Georgia,serif}
.mag .hb span{font:600 12.5px/1.1 "Fraunces",Georgia,serif}
.mag ul{list-style:none;margin:7px 2px 0;padding:0;font-size:11px;line-height:1.5}
.mag li::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--dc,#1F1B17);margin-right:5px;vertical-align:1px}
.mag li.fr::before{border:1px solid #6E645A;background:transparent}
.mag .rm{position:absolute;top:-8px;right:-8px;width:26px;height:26px;border-radius:50%;border:0;background:var(--ink);color:#fff;font-size:16px;line-height:26px;cursor:pointer}
.sum{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);padding-top:12px;font-size:15px}
.sum b{font:600 26px/1 "Fraunces",Georgia,serif}
.code{font:600 13px/1.4 ui-monospace,Menlo,Consolas,monospace;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;word-break:break-all;margin:10px 0}
.cta{width:100%;font:600 16px/1 "Inter",sans-serif;border:0;background:var(--accent);color:#fff;padding:16px;border-radius:14px;cursor:pointer;margin-top:12px}
.fine{color:var(--muted);font-size:13.5px;margin:10px 0 0}
.toast{position:fixed;left:50%;bottom:110px;transform:translateX(-50%);background:var(--ink);color:var(--paper);padding:10px 16px;border-radius:999px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none;z-index:40}
.toast.on{opacity:1}
"""

JS = r"""
// ---- Shop settings: fill these in once the Shopify product exists ----
const SHOP = {
  domain: "",          // e.g. "speedarmy.co.uk" or "your-store.myshopify.com"
  variantId: "",       // variant ID of the "Custom recipe magnet" product
  email: "",           // fallback: where order codes are emailed if Shopify isn't set
  price: 2.50,         // price per magnet, in pounds (display only; Shopify charges the real price)
  min: 10, max: 60
};
const D = JSON.parse(document.getElementById('data').textContent);
const CON = Object.fromEntries(D.containers.map(c => [c.id, c]));
const PROTEIN = {8:"Chicken",9:"Beef",10:"Turkey",11:"Bean"};
const PROT_CAT = {8:"Chicken",9:"Beef",10:"Turkey",11:"Beans & lentils"};
const VEG_SHORT = {1:"Green Veg",2:"Roots",3:"Squash",4:"Spinach",5:"Sweetcorn"};
const SAUCE_WORD = {6:"Tomato",7:"Cheesy"};
const CARB = {r:"rice",p:"pasta",m:"mash",c:"couscous",q:"quinoa",n:null};
const CARB_LABEL = {r:"Rice",p:"Pasta",m:"Mash",c:"Couscous",q:"Quinoa",n:"No carb"};
const FINISH = {rice:"Stir through the rice.",pasta:"Toss with the pasta.",mash:"Serve with the mash.",couscous:"Stir through the couscous.",quinoa:"Stir through the quinoa.",null:"Mash a little if it's chunky."};
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

const store = {
  get(k, d){ try{ const v = localStorage.getItem('fk_'+k); return v ? JSON.parse(v) : d; }catch(e){ return d; } },
  set(k, v){ try{ localStorage.setItem('fk_'+k, JSON.stringify(v)); }catch(e){} }
};
let picked = new Set(store.get('picked', []));
let basket = store.get('basket', []);        // [{key, name, cat, cons, carb}]
let carbChoice = {};                          // generated combo -> carb letter
let showAllGen = false;

function split(cons){
  return { p: cons.find(c => c in PROTEIN) ?? null,
           v: cons.filter(c => c in VEG_SHORT),
           s: cons.find(c => c in SAUCE_WORD) ?? null };
}
function genName(cons){
  const {p, v, s} = split(cons);
  const pre = s ? SAUCE_WORD[s] + " " : "";
  const vs = v.map(x => VEG_SHORT[x]).join(" & ");
  if (p) return v.length > 1 ? `${pre}${PROTEIN[p]}, ${vs}` : `${pre}${PROTEIN[p]} & ${vs}`;
  return `${pre}${vs}`;
}
function defaultCarb(cons){
  if (cons.includes(6)) return 'p';
  if (cons.includes(7)) return 'm';
  if (cons.includes(3)) return 'c';
  return 'r';
}
function genMethod(cons, carbL){
  const carb = CARB[carbL], st = [];
  if (carb) st.push(D.freshStep[carb]);
  const names = cons.map(i => CON[i].name.toLowerCase());
  const list = names.length === 1 ? names[0] : names.slice(0,-1).join(', ') + ' and ' + names.at(-1);
  st.push(`Put 2 cubes each of ${list} in a pan with a splash of water.`);
  st.push('Cover and heat for 5–7 minutes, stirring, until piping hot all the way through.');
  st.push(FINISH[carb]);
  st.push('Let it cool before serving.');
  return st;
}
const setKey = a => [...a].sort((x,y)=>x-y).join('-');
const CURATED_SETS = new Set(D.recipes.map(r => setKey(r.cons)));

function generate(){
  const sel = [...picked];
  const prots = sel.filter(c => c in PROTEIN);
  const vegs = sel.filter(c => c in VEG_SHORT).sort((a,b)=>a-b);
  const sauces = sel.filter(c => c in SAUCE_WORD);
  const vegSets = [];
  if (vegs.length >= 2) for (let i=0;i<vegs.length;i++) for (let j=i+1;j<vegs.length;j++) vegSets.push([vegs[i],vegs[j]]);
  else if (vegs.length === 1) vegSets.push([vegs[0]]);
  const out = [], seen = new Set();
  const bases = prots.length ? prots : (sauces.includes(7) ? [null] : []);
  for (const p of bases) for (const vs of vegSets) for (const s of [...sauces, null]) {
    if (p === null && s !== 7) continue;
    const cons = [p, ...vs, s].filter(x => x !== null);
    const k = setKey(cons);
    if (CURATED_SETS.has(k) || seen.has(k)) continue;
    seen.add(k);
    out.push({cons, name: genName(cons), cat: PROT_CAT[p] || 'Veggie'});
  }
  return out;
}

function chipsHTML(cons, missing=[]){
  return cons.map(i => `<span class="chip${missing.includes(i)?' miss':''}" style="--cc:${CON[i].col}"><i>${i}</i>${esc(CON[i].name)}</span>`).join('');
}
function inBasket(key){ return basket.some(b => b.key === key); }

function curatedCard(r, missing=[]){
  const key = 'R' + String(r.n).padStart(2,'0'), col = D.cats[r.cat];
  const extra = [...r.extras, r.fresh].filter(Boolean).map(x => `<span class="chip plain">${esc(x)}</span>`).join('');
  const miss = missing.length ? `<p class="fine" style="margin:0 0 10px">Add <b>${esc(CON[missing[0]].name)}</b> to your freezer for this one.</p>` : '';
  return `<article class="card${missing.length?' dim':''}" style="--c:${col}">
    <div class="t"><span class="n">${String(r.n).padStart(2,'0')}</span><div><h4>${esc(r.name)}</h4></div></div>
    <div class="tag">${esc(r.cat)}</div>
    <div class="chips">${chipsHTML(r.cons, missing)}${extra}</div>${miss}
    <details><summary>Method</summary><ol>${r.method.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></details>
    <div class="row"><button class="add" data-add="${key}" aria-pressed="${inBasket(key)}">${inBasket(key)?'✓ Magnet added':'+ Add as a magnet'}</button></div>
  </article>`;
}
function genCard(g){
  const k = setKey(g.cons), carbL = carbChoice[k] || defaultCarb(g.cons);
  const key = 'G' + g.cons.join('-') + carbL, col = D.cats[g.cat];
  const opts = Object.entries(CARB_LABEL).map(([l,t]) => `<option value="${l}"${l===carbL?' selected':''}>${t}</option>`).join('');
  return `<article class="card" style="--c:${col}">
    <div class="t"><span class="n">✦</span><div><h4>${esc(g.name)}</h4></div></div>
    <div class="tag">${esc(g.cat)} · new combination</div>
    <div class="chips">${chipsHTML(g.cons)}${CARB[carbL]?`<span class="chip plain">Fresh ${CARB[carbL]}</span>`:''}</div>
    <details><summary>Method</summary><ol>${genMethod(g.cons, carbL).map(s=>`<li>${esc(s)}</li>`).join('')}</ol></details>
    <div class="row"><select data-carb="${k}" aria-label="Serve with">${opts}</select>
    <button class="add" data-add="${key}" aria-pressed="${inBasket(key)}">${inBasket(key)?'✓ Added':'+ Magnet'}</button></div>
  </article>`;
}

function renderPicker(){
  $('#picker').innerHTML = D.containers.map(c => `<button class="pick" style="--c:${c.col}" data-pick="${c.id}" aria-pressed="${picked.has(c.id)}">
    <span class="d">${c.id}</span><span><b>${esc(c.name)}</b><small>${esc(c.contents)}</small></span></button>`).join('');
}
function renderResults(){
  const box = $('#results');
  if (!picked.size){ box.innerHTML = '<div class="empty">Tap the containers you have in the freezer and your meals appear here.</div>'; return; }
  const ready = D.recipes.filter(r => r.cons.every(c => picked.has(c)));
  const near = D.recipes.filter(r => r.cons.filter(c => !picked.has(c)).length === 1);
  const gen = generate();
  const genShown = showAllGen ? gen : gen.slice(0, 9);
  let h = '';
  h += `<section class="group"><h3>Ready to cook · ${ready.length}</h3><p class="note">Recipes from the Freezer Kitchen set you can make right now.</p>`;
  h += ready.length ? `<div class="grid">${ready.map(r => curatedCard(r)).join('')}</div>` : '<div class="empty">None yet. Add a protein and a veg or two.</div>';
  h += '</section>';
  if (gen.length){
    h += `<section class="group"><h3>New combinations · ${gen.length}</h3><p class="note">Made from your containers. Pick what to serve it with.</p><div class="grid">${genShown.map(genCard).join('')}</div>`;
    if (gen.length > 9) h += `<div class="more"><button class="btn-s" id="moreGen">${showAllGen?'Show fewer':'Show all '+gen.length}</button></div>`;
    h += '</section>';
  }
  if (near.length){
    h += `<section class="group"><h3>One container away · ${near.length}</h3><p class="note">Cook one more container and these open up.</p><div class="grid">${near.map(r => curatedCard(r, r.cons.filter(c => !picked.has(c)))).join('')}</div></section>`;
  }
  box.innerHTML = h;
}
function itemFromKey(key){
  if (key[0] === 'R'){ const r = D.recipes.find(x => x.n === +key.slice(1)); return {key, name:r.name, cat:r.cat, cons:r.cons, num:r.n, fresh:r.fresh}; }
  const carb = key.slice(-1), cons = key.slice(1,-1).split('-').map(Number);
  return {key, name: genName(cons), cat: PROT_CAT[split(cons).p] || 'Veggie', cons, carb};
}
function orderCode(){ return 'FK.' + basket.map(b => b.key).join('.'); }
function money(n){ return '£' + n.toFixed(2); }
function renderBar(){
  const n = basket.length, need = Math.max(0, SHOP.min - n);
  $('#barCount').textContent = n ? `${n} magnet${n>1?'s':''} · ${money(n*SHOP.price)}` : 'No magnets yet';
  $('#barNote').textContent = n === 0 ? `Add any recipe as an 8 × 8 cm fridge magnet. Minimum ${SHOP.min}.` : need ? `Add ${need} more to order (minimum ${SHOP.min})` : 'Ready to order';
  $('#meter').style.width = Math.min(100, n / SHOP.min * 100) + '%';
  $('#review').disabled = n === 0;
  $('#review').textContent = need ? 'Review' : 'Order';
}
function renderOrder(){
  const n = basket.length, need = Math.max(0, SHOP.min - n);
  let gi = 0;
  $('#mags').innerHTML = basket.map((b, i) => {
    const col = D.cats[b.cat];
    const lines = b.cons.map(c => `<li style="--dc:${CON[c].col}">${esc(CON[c].name)}</li>`).join('') + ((b.carb && CARB[b.carb]) || b.fresh ? `<li style="--dc:#fff;box-shadow:none" class="fr">${esc(b.fresh || ('Fresh ' + CARB[b.carb]))}</li>` : '');
    const num = b.num ? String(b.num).padStart(2,'0') : 'C' + (++gi);
    return `<div class="mag"><div class="hb" style="--c:${col}"><i>${num}</i><span>${esc(b.name)}</span></div><ul>${lines}</ul>
      <button class="rm" data-rm="${b.key}" aria-label="Remove ${esc(b.name)}">×</button></div>`;
  }).join('');
  $('#oCount').textContent = `${n} magnet${n===1?'':'s'}`;
  $('#oTotal').textContent = money(n * SHOP.price);
  $('#oCode').textContent = orderCode();
  const cta = $('#checkout');
  cta.disabled = !!need || n > SHOP.max;
  cta.textContent = need ? `Add ${need} more magnet${need>1?'s':''} to order` : n > SHOP.max ? `Maximum ${SHOP.max} per order` : (SHOP.domain && SHOP.variantId ? 'Checkout securely' : 'Place order');
  cta.style.opacity = cta.disabled ? .5 : 1;
}
function save(){ store.set('picked', [...picked]); store.set('basket', basket); }
function toast(t){ const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(()=>el.classList.remove('on'), 1600); }
function refresh(){ renderPicker(); renderResults(); renderBar(); save(); }

document.addEventListener('click', e => {
  const p = e.target.closest('[data-pick]');
  if (p){ const id = +p.dataset.pick; picked.has(id) ? picked.delete(id) : picked.add(id); refresh(); return; }
  const a = e.target.closest('[data-add]');
  if (a){
    const key = a.dataset.add;
    if (inBasket(key)){ basket = basket.filter(b => b.key !== key); toast('Removed'); }
    else if (basket.length >= SHOP.max){ toast(`Maximum ${SHOP.max} magnets`); }
    else { basket.push(itemFromKey(key)); const need = SHOP.min - basket.length; toast(need > 0 ? `Added · ${need} more to go` : 'Added'); }
    renderResults(); renderBar(); save(); return;
  }
  const r = e.target.closest('[data-rm]');
  if (r){ basket = basket.filter(b => b.key !== r.dataset.rm); renderOrder(); renderResults(); renderBar(); save(); return; }
  if (e.target.id === 'moreGen'){ showAllGen = !showAllGen; renderResults(); return; }
  if (e.target.id === 'all'){ D.containers.forEach(c => picked.add(c.id)); refresh(); return; }
  if (e.target.id === 'none'){ picked.clear(); refresh(); return; }
  if (e.target.id === 'review'){ renderOrder(); $('#sheet').classList.add('open'); return; }
  if (e.target.id === 'close' || e.target.id === 'sheet'){ $('#sheet').classList.remove('open'); return; }
  if (e.target.id === 'copy'){ navigator.clipboard?.writeText(orderCode()).then(()=>toast('Order code copied'), ()=>toast('Select the code to copy it')); return; }
  if (e.target.id === 'checkout') checkout();
});
document.addEventListener('change', e => {
  const s = e.target.closest('[data-carb]');
  if (s){ carbChoice[s.dataset.carb] = s.value; renderResults(); }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') $('#sheet').classList.remove('open'); });

function checkout(){
  const n = basket.length;
  if (n < SHOP.min || n > SHOP.max) return;
  const code = orderCode();
  if (SHOP.domain && SHOP.variantId){
    const f = document.createElement('form');
    f.method = 'POST'; f.action = `https://${SHOP.domain}/cart/add`;
    const add = (k, v) => { const i = document.createElement('input'); i.type = 'hidden'; i.name = k; i.value = v; f.appendChild(i); };
    add('id', SHOP.variantId); add('quantity', n);
    add('properties[Order code]', code);
    add('properties[Magnets]', basket.map(b => b.name).join(' · '));
    add('return_to', '/cart');
    document.body.appendChild(f); f.submit();
  } else if (SHOP.email){
    const body = `Hello,\n\nI'd like to order ${n} Freezer Kitchen magnets.\n\nOrder code: ${code}\n\n${basket.map((b,i)=>`${i+1}. ${b.name}`).join('\n')}\n\nName:\nDelivery address:\n`;
    location.href = `mailto:${SHOP.email}?subject=${encodeURIComponent('Magnet order ' + code.slice(0,40))}&body=${encodeURIComponent(body)}`;
  } else {
    $('#soon').hidden = false; $('#soon').scrollIntoView({behavior:'smooth', block:'nearest'});
  }
}
refresh();
"""

HTML = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Freezer Kitchen · Plan meals from your freezer</title>
<meta name="description" content="Tap the containers in your freezer and see every baby meal you can make. Order any recipe as a fridge magnet.">
<meta name="theme-color" content="#F6F1EA">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231F1B17'/%3E%3Crect x='14' y='14' width='16' height='16' rx='3' fill='%23C98A3D'/%3E%3Crect x='34' y='14' width='16' height='16' rx='3' fill='%23B4472F'/%3E%3Crect x='14' y='34' width='16' height='16' rx='3' fill='%237A9A6E'/%3E%3Crect x='34' y='34' width='16' height='16' rx='3' fill='%234E6577'/%3E%3C/svg%3E">
<style>{CSS}</style></head><body>
<div class="wrap">
<div class="top"><a class="brand" href="../">Freezer <em>Kitchen</em></a><a href="../#recipes">All 30 recipes →</a></div>
<header class="hero"><p class="eyebrow">Meal planner</p>
<h1>What's in your <em>freezer?</em></h1>
<p>Tap the containers you've got. You'll see every meal you can make, plus new combinations. Turn any of them into a fridge magnet.</p></header>
<div class="step"><b>01</b><h2>Your containers</h2></div>
<div class="tools"><button class="btn-s" id="all">Select all</button><button class="btn-s" id="none">Clear</button></div>
<div class="picker" id="picker"></div>
<div class="step"><b>02</b><h2>Your meals</h2></div>
<div id="results"></div>
</div>
<div class="bar"><div class="wrap"><div class="info"><b id="barCount"></b><small id="barNote"></small><div class="meter"><i id="meter"></i></div></div>
<button class="go" id="review" disabled>Review</button></div></div>
<div class="sheet" id="sheet"><div class="panel" role="dialog" aria-modal="true" aria-labelledby="oh">
<header><h2 id="oh">Your magnets</h2><button class="x" id="close" aria-label="Close">×</button></header>
<p class="fine" style="margin:0">Each magnet is 8 × 8 cm, printed and cut to order. Minimum 10 per order.</p>
<div class="mags" id="mags"></div>
<div class="sum"><span id="oCount"></span><b id="oTotal"></b></div>
<p class="fine">Your order code (we print from this):</p>
<div class="code" id="oCode"></div><button class="btn-s" id="copy">Copy code</button>
<button class="cta" id="checkout">Place order</button>
<div id="soon" hidden><p class="fine"><b>Online checkout opens soon.</b> Copy your order code above. It holds your exact magnets, so you can send it to us to order.</p></div>
<p class="fine">UK delivery. Not a toy: keep magnets away from young children.</p>
</div></div>
<div class="toast" id="toast"></div>
<script type="application/json" id="data">{json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>{JS}</script>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("written", os.path.abspath(OUT))
