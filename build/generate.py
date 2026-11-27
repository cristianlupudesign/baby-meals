"""Rules for generated recipes and order codes. Mirrored exactly in app/index.html (JS).

Order code:  FK.<item>.<item>...
  R09            curated recipe 9
  G8-2-4-6p      generated: containers 8,2,4,6 + carb letter
Carb letters: r rice, p pasta, m mash, c couscous, q quinoa, n none
"""
from data import RECIPES

PROTEIN = {8: "Chicken", 9: "Beef", 10: "Turkey", 11: "Bean"}
PROT_CAT = {8: "Chicken", 9: "Beef", 10: "Turkey", 11: "Beans & lentils"}
VEG_SHORT = {1: "Green Veg", 2: "Roots", 3: "Squash", 4: "Spinach", 5: "Sweetcorn"}
SAUCE_WORD = {6: "Tomato", 7: "Cheesy"}
CARBS = {"r": "rice", "p": "pasta", "m": "mash", "c": "couscous", "q": "quinoa", "n": None}
FINISH = {"rice": "Stir through the rice.", "pasta": "Toss with the pasta.", "mash": "Serve with the mash.",
          "couscous": "Stir through the couscous.", "quinoa": "Stir through the quinoa.",
          None: "Mash a little if it's chunky."}


def split(cons):
    p = next((c for c in cons if c in PROTEIN), None)
    s = next((c for c in cons if c in SAUCE_WORD), None)
    v = [c for c in cons if c in VEG_SHORT]
    return p, v, s


def gen_name(cons):
    p, v, s = split(cons)
    pre = (SAUCE_WORD[s] + " ") if s else ""
    vs = " & ".join(VEG_SHORT[x] for x in v)
    if p:
        return f"{pre}{PROTEIN[p]}, {vs}" if len(v) > 1 else f"{pre}{PROTEIN[p]} & {vs}"
    return f"{pre}{vs}"


def gen_recipe(cons, carb_letter, num):
    """Return a recipe tuple in the same shape as data.RECIPES."""
    p, v, s = split(cons)
    cat = PROT_CAT.get(p, "Veggie")
    carb = CARBS[carb_letter]
    return (num, gen_name(cons), cat, list(cons), [], carb, FINISH[carb])


def parse_code(code):
    parts = code.strip().split(".")
    if not parts or parts[0].upper() != "FK":
        raise ValueError("Order code must start with FK.")
    R = {r[0]: r for r in RECIPES}
    out = []; g = 0
    for i, it in enumerate(parts[1:], 1):
        if it[0] in "Rr":
            r = R[int(it[1:])]
            out.append(r)
        elif it[0] in "Gg":
            body, carb = it[1:-1], it[-1]
            cons = [int(x) for x in body.split("-")]
            g += 1
            out.append(gen_recipe(cons, carb, f"C{g}"))
        else:
            raise ValueError(f"Unknown item {it}")
    return out
