def detect_max_ilvl(gear_list):
    if not gear_list:
        return 0
    return max(item.get("LevelItem", 0) for item in gear_list)

def filter_by_ilvl_window(gear_list, max_ilvl, window):
    min_ilvl = max_ilvl - window
    return [g for g in gear_list if min_ilvl <= g.get("LevelItem",0) <= max_ilvl]
