import logging
import os
import sys

def setup_logger():
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    log_path = os.path.join(exe_dir, "app_debug.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        filemode="a"
    )

    logging.info("===================================")
    logging.info("Application Started")


def log_info(msg):
    print(msg)
    logging.info(msg)
