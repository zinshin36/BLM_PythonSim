def recommend_materia(item, weights):
    slots = item["materia_slots"]
    if slots <= 0:
        return "None"

    sorted_stats = sorted(weights.items(), key=lambda x: x[1], reverse=True)

    if item["crafted"]:
        slots += 2  # allow overmeld simulation for crafted

    return ", ".join([stat for stat, _ in sorted_stats[:slots]])
