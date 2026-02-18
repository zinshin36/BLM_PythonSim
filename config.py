import sys
from pathlib import Path

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path.cwd()))

CACHE_FILE = BASE_DIR / "gear_cache.json"
LOG_FILE = BASE_DIR / "app_debug.log"

JOB_CATEGORY = "Black Mage"
ILVL_WINDOW = 30

# Stat weight profiles for solver
STAT_PROFILES = {
    "spell_speed": {
        "Intelligence": 1.0,
        "SpellSpeed": 0.50,
        "CriticalHit": 0.25,
        "DirectHit": 0.20,
        "Determination": 0.18
    },
    "critical": {
        "Intelligence": 1.0,
        "CriticalHit": 0.50,
        "DirectHit": 0.30,
        "Determination": 0.25,
        "SpellSpeed": 0.15
    }
}
