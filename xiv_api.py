import requests
import time
import os
import json
from logger import log

BASE_URL = "https://xivapi.com"
RATE_LIMIT_DELAY = 0.25
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

HIGHEST_ILVL_CACHE = os.path.join(CACHE_DIR, "highest_ilvl.json")
GEAR_CACHE_FILE = os.path.join(CACHE_DIR, "gear.json")


def _request(endpoint, params, retries=3):
    """
    Perform a GET request with retry logic for transient errors.
    """
    for attempt in range(retries):
        try:
            time.sleep(RATE_LIMIT_DELAY)
            r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=20)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            log(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise
        except requests.RequestException as e:
            log(f"Request exception: {e}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                raise


def load_cache(file_path):
    """
    Load cached JSON data if available.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_cache(file_path, data):
    """
    Save JSON data to cache file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"Failed to save cache {file_path}: {e}")


def detect_highest_ilvl():
    """
    Detect the highest item level using the XIVAPI /search endpoint,
    with caching and retry support.
    """
    cached = load_cache(HIGHEST_ILVL_CACHE)
    if cached:
        log(f"Loaded highest iLvl from cache: {cached}")
        return cached

    log("Detecting highest iLvl via XIVAPI...")

    try:
        data = _request("/search", {
            "indexes": "Item",
            "filters": "LevelItem>=0",
            "sort": "LevelItem",
            "order": "desc",
            "limit": 1
        })

        max_ilvl = data["Results"][0]["LevelItem"]
        log(f"Detected highest iLvl: {max_ilvl}")
        save_cache(HIGHEST_ILVL_CACHE, max_ilvl)
        return max_ilvl

    except Exception as e:
        log(f"iLvl detect failed: {e}")
        return None


def _extract_stats(item):
    """
    Extract relevant stats from an item record.
    """
    stats = {}
    if "BaseParamValue" in item:
        for entry in item["BaseParamValue"]:
            stat = entry["BaseParam"]["Name"]
            stats[stat] = entry["Value"]

    if item.get("DamageMag"):
        stats["WeaponDamage"] = item["DamageMag"]

    return stats


def fetch_gear_range(min_ilvl, max_ilvl, job_category=34, use_cache=True):
    """
    Fetch gear for a job category and iLvl range
    with XIVAPI /search using filters, retry, and caching.
    """
    if use_cache:
        cached = load_cache(GEAR_CACHE_FILE)
        if cached:
            log(f"Loaded {len(cached)} gear items from cache")
            return cached

    log(f"Fetching gear from XIVAPI: iLvl {min_ilvl}-{max_ilvl}, job category {job_category}")

    gear = []
    page = 1

    while True:
        query_filter = f"LevelItem>={min_ilvl} AND LevelItem<={max_ilvl} AND ClassJobCategory={job_category}"

        try:
            data = _request("/search", {
                "indexes": "Item",
                "filters": query_filter,
                "columns": "ID,Name,LevelItem,EquipSlotCategory,IsCraftable,DamageMag,BaseParamValue",
                "limit": 100,
                "page": page
            })
        except Exception as e:
            log(f"Gear fetch failed: {e}")
            break

        results = data.get("Results", [])
        if not results:
            break

        for item in results:
            stats = _extract_stats(item)
            gear.append({
                "name": item["Name"],
                "slot": item["EquipSlotCategory"],
                "ilvl": item["LevelItem"],
                "crafted": item.get("IsCraftable", False),
                "stats": stats,
                "materia_slots": 2
            })

        page += 1

    log(f"Fetched {len(gear)} gear items")

    if gear:
        save_cache(GEAR_CACHE_FILE, gear)

    return gear
