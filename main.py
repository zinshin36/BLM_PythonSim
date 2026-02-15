import sys
import os
import traceback
import logging

# Always create log file in same folder as exe
def setup_logging():
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    log_path = os.path.join(base_path, "app_debug.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    logging.info("==== Application Start ====")
    return log_path


log_file_path = setup_logging()

try:
    logging.info("Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication, QLabel
    from PyQt6.QtCore import Qt

    logging.info("Creating QApplication...")
    app = QApplication(sys.argv)

    logging.info("Creating window...")
    label = QLabel("App started successfully.")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.resize(400, 200)
    label.show()

    logging.info("Entering event loop...")
    sys.exit(app.exec())

except Exception as e:
    logging.error("Fatal error occurred:")
    logging.error(traceback.format_exc())

    # If GUI fails, print to console too
    print("Fatal error. See app_debug.log")
    print(traceback.format_exc())

    input("Press Enter to exit...")
