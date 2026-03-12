def separate_by_slot(gear):
    slots = {}
    for item in gear:
        slot = item["slot"]
        slots.setdefault(slot, []).append(item)
    return slots
