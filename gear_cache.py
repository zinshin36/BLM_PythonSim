import json
from pathlib import Path
from api_client import search_gear_ids, fetch_full_item
from stat_parser import parse_stats

CACHE_FILE = Path("data/gear_cache.json")

def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_cache(gear_list, max_ilvl, theme="Dark"):
    CACHE_FILE.parent.mkdir(exist_ok=True)
    data = {"max_ilvl": max_ilvl, "theme": theme, "gear": gear_list}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def refresh_gear_cache():
    basic_items = search_gear_ids()
    full_gear = []
    for item in basic_items:
        try:
            data = fetch_full_item(item["ID"])
            full_gear.append({
                "ID": item["ID"],
                "Name": item["Name"],
                "LevelItem": item["LevelItem"],
                "Slot": item.get("EquipSlotCategory", {}).get("Name_en"),
                "MateriaSlots": data.get("MateriaSlotCount", 0),
                "Stats": parse_stats(data)
            })
        except:
            continue
    max_ilvl = max([g["LevelItem"] for g in full_gear], default=0)
    save_cache(full_gear, max_ilvl)
    return full_gear, max_ilvl
