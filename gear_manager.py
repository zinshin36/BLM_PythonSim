def separate_by_slot(gear):
    slots = {}
    for item in gear:
        slot = item["slot"]
        if slot not in slots:
            slots[slot] = []
        slots[slot].append(item)
    return slots
