from logger import log

def filter_blacklist(items, blacklist):
    if not blacklist:
        return items

    filtered = [i for i in items if i["Name"] not in blacklist]
    log(f"Blacklist removed {len(items) - len(filtered)} items")
    return filtered


def split_by_slot(items):
    slots = {}
    for item in items:
        slot = str(item["EquipSlotCategory"])
        slots.setdefault(slot, []).append(item)
    return slots


def pick_highest_ilvl_per_slot(slots):
    best = []
    for slot, items in slots.items():
        sorted_items = sorted(items, key=lambda x: x["LevelItem"], reverse=True)
        best.append(sorted_items[0])
    return best


def build_best_set(items, blacklist=None):
    if blacklist is None:
        blacklist = []

    items = filter_blacklist(items, blacklist)
    slots = split_by_slot(items)
    best = pick_highest_ilvl_per_slot(slots)

    log(f"Built best set with {len(best)} pieces")
    return best
