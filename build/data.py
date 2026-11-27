BASE = "https://cristianlupudesign.github.io/baby-meals/"

# id, name, colour, contents, prep steps
CONTAINERS = [
    (1, "Green veg", "#7A9A6E", "Peas, broccoli, green beans",
     ["Steam peas, broccoli florets and green beans for 5–6 minutes until soft.",
      "Chop small or mash lightly."]),
    (2, "Root veg", "#A0673F", "Carrot, parsnip, swede",
     ["Peel and dice carrot, parsnip and swede.",
      "Steam or boil for about 15 minutes until soft.",
      "Mash or chop into small pieces."]),
    (3, "Orange mash", "#C98A3D", "Sweet potato, butternut squash",
     ["Roast sweet potato and butternut squash at 200 °C for about 40 minutes.",
      "Scoop out the flesh and mash."]),
    (4, "Leafy greens", "#3F5E4C", "Spinach, kale",
     ["Wilt spinach and kale in a pan with a splash of water for 2–3 minutes.",
      "Squeeze out the water and chop very fine."]),
    (5, "Sunny veg", "#B8962E", "Sweetcorn, peppers, courgette",
     ["Dice courgette and peppers and soften in a little oil for 8–10 minutes.",
      "Stir in the sweetcorn and mash lightly."]),
    (6, "Red sauce", "#B4472F", "Tomato, onion, garlic",
     ["Soften chopped onion and garlic in olive oil.",
      "Add no-salt tinned chopped tomatoes and simmer for 20 minutes.",
      "Blend smooth."]),
    (7, "Cauli cheese", "#7D5A7B", "Cauliflower, cheese sauce",
     ["Boil cauliflower until soft.",
      "Make a white sauce with butter, flour and milk, then stir in mild cheddar.",
      "Blend the cauliflower into the sauce."]),
    (8, "Chicken", "#C27C62", "Shredded chicken",
     ["Poach chicken thighs in water for about 20 minutes until cooked through.",
      "Shred very fine."]),
    (9, "Beef mince", "#7A2E2E", "Beef mince",
     ["Brown in a dry pan, breaking it up small, until no pink is left.",
      "Drain off the fat."]),
    (10, "Turkey mince", "#8C7A68", "Turkey mince",
     ["Cook like the beef until no pink is left.",
      "Stir in a spoon of red sauce so it stays moist."]),
    (11, "Beans & lentils", "#4E6577", "Lentils, chickpeas, kidney & butter beans",
     ["Simmer red lentils for 15–20 minutes until soft.",
      "Rinse no-salt tinned chickpeas and beans.",
      "Mash everything together."]),
    (12, "Fruit mix", "#A33B5C", "Apple, pear, mango, berries",
     ["Peel and chop apple and pear, then stew with a splash of water for 10 minutes.",
      "Stir in mango and berries and mash."]),
]
C = {c[0]: c for c in CONTAINERS}

CATS = {
    "Chicken": "#C27C62", "Beef": "#7A2E2E", "Turkey": "#8C7A68",
    "Beans & lentils": "#4E6577", "Veggie": "#5E7F5E", "Sweet": "#A33B5C",
}

FRESH = {
    "rice": ("Fresh rice", "Cook a small handful of rice for 10–12 minutes."),
    "pasta": ("Fresh small pasta", "Cook small pasta shapes for 8–10 minutes."),
    "mash": ("Fresh mash", "Boil peeled potato chunks for 15 minutes and mash with a little milk."),
    "mashtop": ("Fresh mash on top", "Boil peeled potato chunks for 15 minutes and mash with a little milk."),
    "couscous": ("Fresh couscous", "Pour boiling water over couscous, cover for 5 minutes, fluff with a fork."),
    "quinoa": ("Fresh quinoa", "Rinse and simmer quinoa for 12–15 minutes."),
    "oats": ("Fresh porridge oats", "Simmer oats in milk for 3–5 minutes."),
    "ricemilk": ("Rice cooked in milk", "Simmer cooked rice in milk for 10 minutes until creamy."),
    "yoghurt": ("Plain yoghurt", None),
}

# num, name, category, containers, extras, fresh, finish
RECIPES = [
    (1, "Chicken Korma", "Chicken", [8, 3], ["Pinch of cumin", "Plain yoghurt"], "rice",
     "Take off the heat and stir in a spoon of plain yoghurt."),
    (2, "Chicken Cheesy Bake", "Chicken", [8, 7, 1], [], "mash", "Spoon over the mash and stir through."),
    (3, "Chicken Veg Rice", "Chicken", [8, 1, 5], [], "rice", "Stir through the rice."),
    (4, "Chicken Casserole", "Chicken", [8, 2, 6], [], "mash", "Serve with the mash."),
    (5, "Chicken Tomato Pasta", "Chicken", [8, 6, 1], [], "pasta", "Toss with the pasta."),
    (6, "Chicken Quinoa Bowl", "Chicken", [8, 5, 4], [], "quinoa", "Stir through the quinoa."),
    (7, "Chicken & Bean Stew", "Chicken", [8, 11, 6, 5], [], None, "Mash a little if it's chunky."),
    (8, "Beef Bolognese", "Beef", [9, 6, 4], [], "pasta", "Toss with the pasta."),
    (9, "Cottage Pie", "Beef", [9, 2, 1, 6], [], "mashtop", "Spoon into a bowl and top with the mash."),
    (10, "Beef Chilli", "Beef", [9, 11, 6, 5], ["Pinch of paprika"], "rice", "Serve with the rice."),
    (11, "Beef Stew", "Beef", [9, 2, 4], [], "mash", "Serve with the mash."),
    (12, "Beef & Squash Rice", "Beef", [9, 3, 1], [], "rice", "Stir through the rice."),
    (13, "Mild Beef Curry", "Beef", [9, 3, 1], ["Pinch of cumin"], "rice", "Serve with the rice."),
    (14, "Turkey Bolognese", "Turkey", [10, 6, 5], [], "pasta", "Toss with the pasta."),
    (15, "Turkey Shepherd's Pie", "Turkey", [10, 2, 1], [], "mashtop", "Spoon into a bowl and top with the mash."),
    (16, "Turkey Couscous", "Turkey", [10, 5, 3], ["Pinch of cinnamon"], "couscous", "Stir through the couscous."),
    (17, "Cheesy Turkey Pasta", "Turkey", [10, 7, 4], [], "pasta", "Toss with the pasta."),
    (18, "Turkey Root Mash", "Turkey", [10, 2, 3], [], None, "Mash together."),
    (19, "Turkey Tomato Rice", "Turkey", [10, 6, 1], [], "rice", "Stir through the rice."),
    (20, "Lentil Dhal", "Beans & lentils", [11, 3], ["Pinch of cumin"], "rice", "Serve with the rice."),
    (21, "Veggie Chilli", "Beans & lentils", [11, 5, 6], ["Pinch of paprika"], "rice", "Serve with the rice."),
    (22, "Sweet Potato Lentil Stew", "Beans & lentils", [11, 3, 4, 6], [], None, "Mash a little if it's chunky."),
    (23, "Bean Pasta", "Beans & lentils", [11, 6, 4], [], "pasta", "Toss with the pasta."),
    (24, "Lentil Bolognese", "Beans & lentils", [11, 6, 2], [], "pasta", "Toss with the pasta."),
    (25, "Cauli Cheese Pasta", "Veggie", [7, 1], [], "pasta", "Toss with the pasta."),
    (26, "Green Risotto", "Veggie", [1, 4, 7], [], "rice", "Stir through the rice until creamy."),
    (27, "Cheesy Veg Mash", "Veggie", [7, 2, 1], [], "mash", "Stir into the mash."),
    (28, "Fruity Porridge", "Sweet", [12], ["Pinch of cinnamon"], "oats", "Stir the fruit through the porridge."),
    (29, "Fruit Yoghurt Bowl", "Sweet", [12], [], "yoghurt", "Thaw the fruit, warm briefly, cool, then swirl into yoghurt."),
    (30, "Fruity Rice Pudding", "Sweet", [12], ["Pinch of cinnamon"], "ricemilk", "Swirl the fruit through the rice pudding."),
]


def ingredient_lines(r):
    """Short lines for printed cards."""
    num, name, cat, cons, extras, fresh, finish = r
    lines = [(C[i][1], C[i][2]) for i in cons]
    lines += [(e, None) for e in extras]
    if fresh:
        lines.append((FRESH[fresh][0], None))
    return lines


def method(r):
    num, name, cat, cons, extras, fresh, finish = r
    steps = []
    if fresh and FRESH[fresh][1]:
        steps.append(FRESH[fresh][1])
    ns = [C[i][1].lower() for i in cons]
    names = ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]
    if cat == "Sweet":
        steps.append("Thaw 2 cubes of fruit mix in a small pan or the microwave until piping hot.")
    else:
        pin = [x.lower() for x in extras if "pinch" in x.lower()]
        sp = (", plus a " + pin[0]) if pin else ""
        steps.append(f"Put 2 cubes each of {names} in a pan with a splash of water{sp}.")
        steps.append("Cover and heat for 5–7 minutes, stirring, until piping hot all the way through.")
    if cat == "Sweet" and any("pinch" in e.lower() for e in extras):
        steps.append("Add the pinch of cinnamon.")
    steps.append(finish)
    steps.append("Let it cool before serving.")
    return steps
