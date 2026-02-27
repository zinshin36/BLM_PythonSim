import requests
from logger import log_info

BASE = "https://v2.xivapi.com/api/search"
HEADERS = {"User-Agent": "BLM-Optimizer"}


def detect_highest_ilvl():
    try:
        r = requests.get(
            BASE,
            params={
                "sheet": "Item",
                "query": "LevelItem>0",
                "sort": "-LevelItem",
                "fields": "LevelItem",
                "limit": 1
            },
            headers=HEADERS
        )
        r.raise_for_status()
        results = r.json().get("results", [])
        if results:
            return results[0]["LevelItem"]
    except Exception as e:
        log_info(f"Detect iLvl error: {e}")
    return None


def fetch_gear_range(min_ilvl, max_ilvl):
    gear = []
    page = 1

    try:
        while True:
            r = requests.get(
                BASE,
                params={
                    "sheet": "Item",
                    "query": f"LevelItem>={min_ilvl} AND LevelItem<={max_ilvl}",
                    "fields":
                        "Name,LevelItem,EquipSlotCategory.Name,"
                        "ClassJobCategory.Name,Stats,MateriaSlotCount,IsCrafted",
                    "limit": 100,
                    "page": page
                },
                headers=HEADERS
            )
            r.raise_for_status()

            data = r.json()
            results = data.get("results", [])

            if not results:
                break

            for item in results:
                job = item.get("ClassJobCategory", {}).get("Name", "")
                if "Black Mage" not in job:
                    continue

                gear.append({
                    "name": item["Name"],
                    "ilvl": item["LevelItem"],
                    "slot": item.get("EquipSlotCategory", {}).get("Name", "Unknown"),
                    "stats": item.get("Stats", {}),
                    "materia_slots": item.get("MateriaSlotCount", 0),
                    "crafted": item.get("IsCrafted", False)
                })

            if not data.get("pagination", {}).get("has_next"):
                break

            page += 1

        return gear

    except Exception as e:
        log_info(f"Fetch gear error: {e}")
        return []
