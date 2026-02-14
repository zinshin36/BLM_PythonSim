def parse_stats(item_data):
    stats = {"Crit":0,"DirectHit":0,"Determination":0,"SpellSpeed":0}
    for param in item_data.get("BaseParam", []):
        name = param.get("BaseParam", {}).get("Name_en")
        val = param.get("Value",0)
        if name == "Critical Hit":
            stats["Crit"] = val
        elif name == "Direct Hit Rate":
            stats["DirectHit"] = val
        elif name == "Determination":
            stats["Determination"] = val
        elif name == "Spell Speed":
            stats["SpellSpeed"] = val
    return stats
