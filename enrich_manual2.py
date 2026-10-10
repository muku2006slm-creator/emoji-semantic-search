# One description per concept — variants share text.

CONCEPTS = {
    "person":     "someone, somebody, individual, human, neutral, anyone",
    "bald":       "hair loss, shaved head, no hair, smooth, chemotherapy, aging",
    "blond":      "fair hair, light hair, golden hair",
    "student":    "studying, university, college, exams, learning, degree, campus, cap",
    "cook":       "chef, cooking, kitchen, restaurant, recipe, culinary, food preparation",
    "artist":     "painting, creative, canvas, drawing, art, studio, design, imagination",
    "pilot":      "flying, aviation, airline, captain, cockpit, travel, flight",
    "turban":     "sikh, headwrap, cultural dress, traditional, religious dress",
    "veil":       "wedding, bride, marriage, ceremony, getting married, engaged",
    "standing":   "waiting, upright, idle, doing nothing, bored, in line, still",
    "wheelchair_motor": "accessibility, disability, mobility, electric chair, assisted, independence",
    "wheelchair_manual": "accessibility, disability, mobility, self propelled, assisted, independence",
    "family":     "household, relatives, parents, children, together, home, kin",
    "deer":       "forest, gentle, graceful, shy, antlers, wildlife, nature, timid",
    "rhino":      "thick skinned, tough, armoured, charge, endangered, powerful, africa",
    "rosette":    "award, ribbon, prize, winner, decoration, honour, badge",
    "watermelon": "summer, picnic, refreshing, juicy, slice, seeds, hot day, sweet",
    "greenapple": "tart, crisp, healthy, snack, sour, teacher, orchard",
    "pear":       "sweet, soft, autumn, juicy, snack, orchard, ripe",
    "kiwi":       "tangy, tropical, green inside, vitamin, fuzzy, new zealand, sour",
    "olive":      "mediterranean, salty, brine, martini, pizza topping, greek, oil",
    "sandwich":   "lunch, quick meal, packed, deli, snack, between slices, filling",
    "cannedfood": "tinned, preserved, pantry, shelf stable, emergency, stockpile, cheap",
    "ricecracker": "japanese, crispy, savoury, snack, light, senbei",
    "cookedrice": "staple, plain, side dish, asian, steamed, bowl, grain",
    "curryrice":  "indian, japanese, spicy, comfort food, gravy, warm meal",
    "sweetpotato": "roasted, winter, street food, warm, sweet, filling, baked",
    "milk":       "dairy, calcium, bedtime, warm drink, soothing, night, white",
    "mate":       "argentina, herbal, gourd, caffeine, south american, bitter, sharing",
    "carpstreamer": "japanese, children's day, koi, banner, may, boys, tradition",
    "moonviewing": "autumn, japanese, harvest, tsukimi, moon festival, quiet, tradition",
    "tickets":    "event, concert, admission, entry, cinema, show, booking",
    "flyingdisc": "frisbee, park, throw, catch, outdoor, ultimate, dog",
    "mahjong":    "tile game, chinese, gambling, strategy, table game, winning tile",
}

VARIANTS = {
    # person
    "1F9D1": "person",
    "1F9D1-200D-1F9B2": "bald",
    "1F471-200D-2642-FE0F": "blond",
    # student
    "1F9D1-200D-1F393": "student",
    "1F468-200D-1F393": "student",
    "1F469-200D-1F393": "student",
    # cook
    "1F9D1-200D-1F373": "cook",
    "1F468-200D-1F373": "cook",
    "1F469-200D-1F373": "cook",
    # artist
    "1F9D1-200D-1F3A8": "artist",
    "1F468-200D-1F3A8": "artist",
    "1F469-200D-1F3A8": "artist",
    # pilot
    "1F9D1-200D-2708-FE0F": "pilot",
    "1F468-200D-2708-FE0F": "pilot",
    "1F469-200D-2708-FE0F": "pilot",
    # turban
    "1F473": "turban",
    "1F473-200D-2642-FE0F": "turban",
    "1F473-200D-2640-FE0F": "turban",
    # veil
    "1F470": "veil",
    "1F470-200D-2642-FE0F": "veil",
    # standing
    "1F9CD": "standing",
    "1F9CD-200D-2642-FE0F": "standing",
    "1F9CD-200D-2640-FE0F": "standing",
    # motorized wheelchair
    "1F9D1-200D-1F9BC": "wheelchair_motor",
    "1F9D1-200D-1F9BC-200D-27A1-FE0F": "wheelchair_motor",
    "1F468-200D-1F9BC": "wheelchair_motor",
    "1F468-200D-1F9BC-200D-27A1-FE0F": "wheelchair_motor",
    "1F469-200D-1F9BC": "wheelchair_motor",
    "1F469-200D-1F9BC-200D-27A1-FE0F": "wheelchair_motor",
    # manual wheelchair
    "1F9D1-200D-1F9BD": "wheelchair_manual",
    "1F9D1-200D-1F9BD-200D-27A1-FE0F": "wheelchair_manual",
    "1F468-200D-1F9BD": "wheelchair_manual",
    "1F468-200D-1F9BD-200D-27A1-FE0F": "wheelchair_manual",
    "1F469-200D-1F9BD": "wheelchair_manual",
    "1F469-200D-1F9BD-200D-27A1-FE0F": "wheelchair_manual",
    # family
    "1F46A": "family",
    "1F9D1-200D-1F9D1-200D-1F9D2": "family",
    "1F9D1-200D-1F9D1-200D-1F9D2-200D-1F9D2": "family",
    "1F9D1-200D-1F9D2": "family",
    "1F9D1-200D-1F9D2-200D-1F9D2": "family",
    # animals
    "1F98C": "deer",
    "1F98F": "rhino",
    # plants
    "1F3F5": "rosette",
    # fruit
    "1F349": "watermelon",
    "1F34F": "greenapple",
    "1F350": "pear",
    "1F95D": "kiwi",
    "1FAD2": "olive",
    # food
    "1F96A": "sandwich",
    "1F96B": "cannedfood",
    "1F358": "ricecracker",
    "1F35A": "cookedrice",
    "1F35B": "curryrice",
    "1F360": "sweetpotato",
    # drink
    "1F95B": "milk",
    "1F9C9": "mate",
    # celebration
    "1F38F": "carpstreamer",
    "1F391": "moonviewing",
    "1F39F": "tickets",
    # activities
    "1F94F": "flyingdisc",
    "1F004": "mahjong",
}

MANUAL2 = {hx: CONCEPTS[c] for hx, c in VARIANTS.items()}

if __name__ == "__main__":
    print(f"{len(CONCEPTS)} concepts -> {len(MANUAL2)} entries")