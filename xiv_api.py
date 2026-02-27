import requests
from logger import log

BASE_URL = "https://xivapi.com"

def detect_highest_ilvl():
    log("Detecting highest iLvl...")

    try:
        url = f"{BASE_URL}/search"
        params = {
            "indexes": "Item",
            "columns": "LevelItem",
            "sort": "LevelItem",
            "order": "desc",
            "limit": 1
        }

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        max_ilvl = data["Results"][0]["LevelItem"]
        log(f"Detected highest iLvl: {max_ilvl}")
        return max_ilvl

    except Exception as e:
        log(f"Detect iLvl error: {e}")
        return None


def fetch_gear_range(min_ilvl, max_ilvl, job_category=34):
    """
    job_category 34 = Caster DPS
    Change if needed.
    """

    log(f"Fetching gear between {min_ilvl} - {max_ilvl}")

    try:
        url = f"{BASE_URL}/search"
        query = f"LevelItem>={min_ilvl} LevelItem<={max_ilvl} ClassJobCategory={job_category}"

        params = {
            "indexes": "Item",
            "columns": "ID,Name,LevelItem,EquipSlotCategory,IsCraftable",
            "query": query,
            "limit": 1000
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        results = data.get("Results", [])
        log(f"Fetched {len(results)} gear items")
        return results

    except Exception as e:
        log(f"Gear fetch error: {e}")
        return []
