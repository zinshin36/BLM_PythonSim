def recommend_materia(slots: int, stats: dict, weights: dict):
    """Simplified recommendation based on highest weighted stats."""
    if slots == 0:
        return "None"
    sorted_stats = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    return ", ".join([s[0] for s in sorted_stats[:slots]])
