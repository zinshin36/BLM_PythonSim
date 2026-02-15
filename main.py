import sys
import os
import json
import requests
import logging
from pathlib import Path

# ===============================
# FORCE LOG FILE CREATION
# ===============================

BASE_DIR = Path(os.getcwd())
LOG_FILE = BASE_DIR / "blm_bis.log"
CACHE_FILE = BASE_DIR / "gear_cache.json"
API_BASE = "https://v2.xivapi.com"

# Create log file immediately
LOG_FILE.touch(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("========== PROGRAM START ==========")

# ===============================
# IMPORT GUI AFTER LOGGING SETUP
# ===============================

try:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QLabel,
        QPushButton, QSlider, QMessageBox
    )
    from PyQt6.QtCore import Qt
except Exception as e:
    logging.critical(f"PyQt6 import failed: {e}")
    print("PyQt6 is not installed. Run: pip install PyQt6")
    sys.exit(1)

# ===============================
# API FUNCTIONS
# ===============================

def fetch_highest_ilvl():
    try:
        logging.info("Detecting highest ilvl...")
        url = f"{API_BASE}/search"

        params = {
            "query": "Black Mage",
            "indexes": "Item",
            "limit": 1,
            "sort_field": "LevelItem",
            "sort_order": "desc"
        }

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "results" in data and data["results"]:
            highest = data["results"][0]["LevelItem"]
            logging.info(f"Highest ilvl detected: {highest}")
            return highest

    except Exception as e:
        logging.error(f"Failed detecting ilvl: {e}")
        return None


def fetch_gear(ilvl_min, ilvl_max):
    try:
        logging.info(f"Fetching gear {ilvl_min}-{ilvl_max}")

        url = f"{API_BASE}/search"
        params = {
            "query": "Black Mage",
            "indexes": "Item",
            "limit": 200,
            "filters": f"LevelItem>={ilvl_min},LevelItem<={ilvl_max}"
        }

        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        results = data.get("results", [])
        logging.info(f"Gear count: {len(results)}")
        return results

    except Exception as e:
        logging.error(f"Fetch gear failed: {e}")
        return []

# ===============================
# GUI
# ===============================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM Perfect BiS Solver")
        self.setGeometry(200, 200, 500, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("iLvl Range: Not Detected")
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(500)
        self.slider.setMaximum(800)
        self.slider.setValue(660)
        self.slider.valueChanged.connect(self.update_label)
        self.layout.addWidget(self.slider)

        self.detect_button = QPushButton("Detect Highest iLvl")
        self.detect_button.clicked.connect(self.detect_ilvl)
        self.layout.addWidget(self.detect_button)

        self.refresh_button = QPushButton("Refresh Gear (Expansion)")
        self.refresh_button.clicked.connect(self.refresh_gear)
        self.layout.addWidget(self.refresh_button)

        self.calc_button = QPushButton("Recalculate BiS")
        self.calc_button.clicked.connect(self.calculate_bis)
        self.layout.addWidget(self.calc_button)

        self.theme_button = QPushButton("Toggle Light/Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_button)

        self.setLayout(self.layout)
        self.dark_mode = True
        self.apply_dark_mode()

        logging.info("GUI initialized")

    def update_label(self):
        self.label.setText(
            f"iLvl Range: {self.slider.value()-60} - {self.slider.value()}"
        )

    def detect_ilvl(self):
        highest = fetch_highest_ilvl()
        if highest:
            self.slider.setValue(highest)
            self.update_label()
            QMessageBox.information(self, "Detected", f"Highest iLvl: {highest}")
        else:
            QMessageBox.warning(self, "Error", "Failed to detect highest iLvl.")

    def refresh_gear(self):
        highest = fetch_highest_ilvl()
        if not highest:
            QMessageBox.warning(self, "Error", "Cannot detect highest ilvl.")
            return

        gear = fetch_gear(highest-60, highest)

        with open(CACHE_FILE, "w") as f:
            json.dump(gear, f, indent=2)

        logging.info("Gear cache updated")

        QMessageBox.information(self, "Success", f"Gear refreshed: {len(gear)} items")

    def calculate_bis(self):
        if not CACHE_FILE.exists():
            QMessageBox.warning(self, "Error", "No gear cache found. Refresh first.")
            return

        with open(CACHE_FILE, "r") as f:
            gear = json.load(f)

        if not gear:
            QMessageBox.warning(self, "Error", "No gear found in selected ilvl window.")
            return

        best = max(gear, key=lambda x: x.get("LevelItem", 0))

        QMessageBox.information(
            self,
            "BiS Result",
            f"{best.get('Name')} (iLvl {best.get('LevelItem')})"
        )

        logging.info("BiS calculated successfully")

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.dark_mode = False
        else:
            self.apply_dark_mode()
            self.dark_mode = True

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: white; }
            QPushButton { background-color: #333; padding: 6px; }
        """)

# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    logging.info("Launching application...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
