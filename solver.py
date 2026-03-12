from itertools import product
from heapq import nlargest

from blm_simulator import simulate_dps
from materia_engine import apply_optimal_materia


def find_best_sets(slots, blacklist, top_n=200):

    slot_keys = list(slots.keys())

    results = []

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

        results.append((score, gear_set))

    best = nlargest(top_n, results, key=lambda x: x[0])

    return best
