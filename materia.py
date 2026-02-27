from logger import log

def apply_materia_logic(gear_set):
    optimized = []

    for item in gear_set:
        crafted = item.get("IsCraftable", False)

        if crafted:
            meld_slots = 5  # overmeld allowed
        else:
            meld_slots = 2  # normal cap

        item_copy = item.copy()
        item_copy["MateriaSlotsUsed"] = meld_slots

        optimized.append(item_copy)

    log("Materia logic applied")
    return optimized
