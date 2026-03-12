import requests
import time
from logger import log

BASE_URL = "https://xivapi.com"
RATE_LIMIT_DELAY = 0.25


def _request(endpoint, params):
    time.sleep(RATE_LIMIT_DELAY)

    r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def detect_highest_ilvl():
    log("Detecting highest iLvl")

    try:
        data = _request("/search", {
            "indexes": "Item",
            "columns": "LevelItem",
            "sort": "LevelItem",
            "order": "desc",
            "limit": 1
        })

        return data["Results"][0]["LevelItem"]

    except Exception as e:
        log(f"iLvl detect failed: {e}")
        return None


def _extract_stats(item):
    stats = {}

    if "BaseParamValue" in item:
        for entry in item["BaseParamValue"]:
            stat = entry["BaseParam"]["Name"]
            stats[stat] = entry["Value"]

    if item.get("DamageMag"):
        stats["WeaponDamage"] = item["DamageMag"]

    return stats


def fetch_gear_range(min_ilvl, max_ilvl, job_category=34):

    log(f"Fetching gear {min_ilvl}-{max_ilvl}")

    page = 1
    gear = []

    while True:

        data = _request("/search", {
            "indexes": "Item",
            "query": f"LevelItem>={min_ilvl} LevelItem<={max_ilvl} ClassJobCategory={job_category}",
            "columns": "ID,Name,LevelItem,EquipSlotCategory,IsCraftable,DamageMag,BaseParamValue",
            "limit": 100,
            "page": page
        })

        results = data.get("Results", [])

        if not results:
            break

        for item in results:

            stats = _extract_stats(item)

            gear.append({
                "name": item["Name"],
                "slot": item["EquipSlotCategory"],
                "ilvl": item["LevelItem"],
                "crafted": item["IsCraftable"],
                "stats": stats,
                "materia_slots": 2
            })

        page += 1

    log(f"Fetched {len(gear)} items")

    return gear
