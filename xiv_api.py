import requests
from logger import log_info
from config import CACHE_FILE

BASE_URL = "https://v2.xivapi.com"

def fetch_max_ilvl_for_job(job_name):
    try:
        r = requests.get(f"{BASE_URL}/job/search", params={"name": job_name})
        r.raise_for_status()
        results = r.json().get("Results")
        if results:
            return max([job["MaxItemLevel"] for job in results if "MaxItemLevel" in job])
    except Exception as e:
        log_info(f"Error detecting max ilvl: {e}")
    return None

def fetch_gear(job_name, min_ilvl, max_ilvl):
    try:
        params = {
            "indexes": "item",
            "filters": f"JobCategory.Name={job_name};LevelItem>= {min_ilvl};LevelItem<= {max_ilvl}",
            "columns": "ID,Name,LevelItem,ClassJobCategoryTargetID,EquipSlotCategoryTargetID,Stats,MateriaSlots"
        }
        r = requests.get(f"{BASE_URL}/search", params=params)
        r.raise_for_status()
        items = r.json().get("Results", [])
        gear_list = []
        for i in items:
            gear_list.append({
                "name": i["Name"],
                "ilvl": i["LevelItem"],
                "slot": i.get("EquipSlotCategoryTargetID", "Unknown"),
                "stats": i.get("Stats", {}),
                "materia_slots": i.get("MateriaSlots", 0)
            })
        return gear_list
    except Exception as e:
        log_info(f"Error fetching gear: {e}")
        return []
