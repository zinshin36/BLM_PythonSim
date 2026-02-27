import requests
from logger import log_info

BASE = "https://v2.xivapi.com"

def detect_highest_ilvl():
    try:
        params = {
            "indexes": "Item",
            "sort_field": "LevelItem",
            "sort_order": "desc",
            "limit": 1
        }
        r = requests.get(f"{BASE}/search", params=params)
        r.raise_for_status()
        results = r.json()["Results"]
        if results:
            return results[0]["LevelItem"]
    except Exception as e:
        log_info(f"Detect iLvl error: {e}")
    return None


def fetch_gear_range(min_ilvl, max_ilvl):
    try:
        params = {
            "indexes": "Item",
            "filters": f"LevelItem>={min_ilvl};LevelItem<={max_ilvl}",
            "columns": "ID,Name,LevelItem,EquipSlotCategory,Stats,MateriaSlotCount,ItemUICategory"
        }
        r = requests.get(f"{BASE}/search", params=params)
        r.raise_for_status()
        items = r.json()["Results"]

        gear = []
        for i in items:
            gear.append({
                "id": i["ID"],
                "name": i["Name"],
                "ilvl": i["LevelItem"],
                "slot": str(i.get("EquipSlotCategory", {}).get("Name", "Unknown")),
                "stats": i.get("Stats", {}),
                "materia_slots": i.get("MateriaSlotCount", 0),
                "crafted": "Crafting" in str(i.get("ItemUICategory", ""))
            })
        return gear

    except Exception as e:
        log_info(f"Fetch gear error: {e}")
        return []


def update_expansion_data():
    try:
        r = requests.get(f"{BASE}/patch")
        r.raise_for_status()
        return "Expansion data refreshed."
    except Exception as e:
        return f"Update failed: {e}"
