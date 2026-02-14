import requests
import json
from pathlib import Path

API_URL = "https://xivapi.com/search"

# Change this when new raid tier launches
MIN_ILVL = 700   # adjust to current tier
MAX_ILVL = 999

JOB_CATEGORY = "Caster"

OUTPUT_FILE = Path("data/current_tier.json")

def fetch_gear():
    print("Fetching gear from XIVAPI...")

    params = {
        "indexes": "Item",
        "filters": f"LevelItem>={MIN_ILVL},LevelItem<={MAX_ILVL},EquipSlotCategoryTargetID>=1,ClassJobCategory.Name_en={JOB_CATEGORY}",
        "columns": "ID,Name,LevelItem,EquipSlotCategory.Name_en,DamageMag,BaseParam.Value,BaseParam.Special",
        "limit": 200
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    gear_list = []

    for item in data["Results"]:
        gear_list.append({
            "ID": item.get("ID"),
            "Name": item.get("Name"),
            "ItemLevel": item.get("LevelItem"),
            "Slot": item.get("EquipSlotCategory", {}).get("Name_en")
        })

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(gear_list, f, indent=2)

    print(f"Saved {len(gear_list)} items to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_gear()
