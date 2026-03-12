from logger import log

def filter_blacklist(items, blacklist):
    if not blacklist:
        return items
    filtered = [i for i in items if i["name"] not in blacklist]
    log(f"Blacklist removed {len(items) - len(filtered)} items")
    return filtered

def split_by_slot(items):
    slots = {}
    for item in items:
        slot = item["slot"]
        slots.setdefault(slot, []).append(item)
    return slots
