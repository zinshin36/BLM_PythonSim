import requests
from config import API_SEARCH_URL, API_ITEM_URL, MAX_API_RESULTS

def search_gear_ids():
    params = {
        "indexes": "Item",
        "filters": "ClassJobCategory.Name_en=Caster",
        "columns": "ID,Name,LevelItem,EquipSlotCategory.Name_en",
        "limit": MAX_API_RESULTS
    }
    resp = requests.get(API_SEARCH_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("Results", [])

def fetch_full_item(item_id):
    resp = requests.get(f"{API_ITEM_URL}/{item_id}", timeout=30)
    resp.raise_for_status()
    return resp.json()
