from itertools import product
from logger import log_info

def score_gear_set(gear_set: dict, weights: dict):
    """Score a gear set based on weights for each stat."""
    total_stats = {}
    for item in gear_set.values():
        for stat, value in item["stats"].items():
            total_stats[stat] = total_stats.get(stat, 0) + value

    score = sum(value * weights.get(stat, 0) for stat, value in total_stats.items())
    return score

def find_best_set(slots: dict, weights: dict):
    """Brute-force search for best gear set using given weights."""
    slot_keys = list(slots.keys())
    best_score = -1
    best_set = None

    combinations = product(*(slots[k] for k in slot_keys))
    for combo in combinations:
        gear_set = {slot_keys[i]: combo[i] for i in range(len(slot_keys))}
        score = score_gear_set(gear_set, weights)
        if score > best_score:
            best_score = score
            best_set = gear_set

    log_info(f"Best score: {best_score}")
    return best_set, best_score
