import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "blm_bis.log")

# Default fight length in seconds
FIGHT_LENGTH = 480  

# Default toggles
FULL_MATERIA = True
INCLUDE_CRIT_WINDOWS = True
INCLUDE_FOOD = True
INCLUDE_POTION = True
INCLUDE_RAID_BUFFS = True
