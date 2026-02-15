from xiv_api import fetch_gear_by_job
from logger import get_logger

logger = get_logger()

def detect_current_tier(job="BLM"):
    """
    Detect highest item level and suggest ilvl window for raid/crafting gear.
    """
    gear = fetch_gear_by_job(job=job, min_ilvl=100, max_ilvl=2000)
    if not gear:
        logger.warning("No gear found for tier detection.")
        return 0, 0

    max_ilvl = max(item.get("ItemLevel", 0) for item in gear)
    min_ilvl = max_ilvl - 30  # Include crafting/tome gear
    logger.info(f"Detected max_ilvl={max_ilvl}, min_ilvl={min_ilvl}")
    return min_ilvl, max_ilvl
