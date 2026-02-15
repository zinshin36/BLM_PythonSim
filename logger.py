import logging
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

def get_logger():
    return logging.getLogger("BLM_BIS")
