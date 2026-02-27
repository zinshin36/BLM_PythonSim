import requests
from logger import log_info

BASE = "https://v2.xivapi.com/api"
HEADERS = {"User-Agent": "BLM-Optimizer"}


def get_expansion_versions():
    try:
        r = requests.get(f"{BASE}/versions", headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        versions = []
        for entry in data.get("versions", []):
            name = entry.get("version")
            if name:
                versions.append(name)

        return versions

    except Exception as e:
        log_info(f"Expansion fetch error: {e}")
        return []


def detect_highest_ilvl():
    try:
        r = requests.get(
            f"{BASE}/sheet/Item",
            params={"limit": 1, "sort": "LevelItem", "order": "desc"},
            headers=HEADERS
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if results:
            return results[0].get("LevelItem")
    except Exception as e:
        log_info(f"Detect iLvl error: {e}")
    return None


def fetch_gear_range(min_ilvl, max_ilvl):
    try:
        r = requests.get(
            f"{BASE}/sheet/Item",
            params={"limit": 1000},
            headers=HEADERS
        )
        r.raise_for_status()

        gear = []
        for item in r.json().get("results", []):
            ilvl = item.get("LevelItem", 0)
            if not (min_ilvl <= ilvl <= max_ilvl):
                continue

            gear.append({
                "name": item["Name"],
                "ilvl": ilvl,
                "slot": item.get("EquipSlotCategory", {}).get("Name", "Unknown"),
                "stats": item.get("Stats", {}),
                "materia_slots": item.get("MateriaSlotCount", 0),
                "crafted": item.get("IsCrafted", False)
            })

        return gear

    except Exception as e:
        log_info(f"Fetch gear error: {e}")
        return []
