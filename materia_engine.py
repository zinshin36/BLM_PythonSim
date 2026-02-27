def apply_optimal_materia(item):
    slots = item["materia_slots"]
    if item["crafted"]:
        slots += 2

    if slots <= 0:
        item["materia"] = "None"
        return

    best_stat = "CriticalHit"
    item["materia"] = f"{best_stat} x{slots}"
    item["stats"][best_stat] = item["stats"].get(best_stat, 0) + (36 * slots)
