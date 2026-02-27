from itertools import product
from blm_simulator import simulate_dps
from materia_engine import apply_optimal_materia


def find_best_set(slots, blacklist):
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
            gear_set[slot_keys[i]] = dict(item)

        if not valid:
            continue

        for item in gear_set.values():
            apply_optimal_materia(item)

        score = simulate_dps(gear_set)

        if score > best_score:
            best_score = score
            best_set = gear_set

    return best_set, best_score
