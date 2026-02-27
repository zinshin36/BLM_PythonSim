from itertools import product

def score_set(gear_set, weights):
    total = 0
    for item in gear_set.values():
        for stat, val in item["stats"].items():
            total += val * weights.get(stat, 0)
    return total


def find_best_set(slots, weights, blacklist):
    slot_keys = list(slots.keys())
    best_score = -1
    best_set = None

    for combo in product(*(slots[k] for k in slot_keys)):
        gear_set = {}
        valid = True

        for i, item in enumerate(combo):
            if item["name"] in blacklist:
                valid = False
                break
            gear_set[slot_keys[i]] = item

        if not valid:
            continue

        score = score_set(gear_set, weights)

        if score > best_score:
            best_score = score
            best_set = gear_set

    return best_set, best_score
