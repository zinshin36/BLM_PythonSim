import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QListWidget, QLabel
)
from xiv_api import (
    detect_highest_ilvl,
    fetch_gear_range,
    update_expansion_data
)
from gear_manager import separate_by_slot
from solver import find_best_set
from materia_engine import recommend_materia
from config import ILVL_WINDOW, STAT_PROFILES
from logger import setup_logger, log_info


setup_logger()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM Gear Optimizer")
        self.resize(1000, 800)

        self.max_ilvl = None
        self.slots = None
        self.blacklist = set()

        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        layout.addWidget(QLabel("Blacklist (Select items to exclude from BiS):"))
        self.blacklist_widget = QListWidget()
        layout.addWidget(self.blacklist_widget)

        self.btn_update = QPushButton("Update Expansion Data")
        self.btn_update.clicked.connect(self.update_data)
        layout.addWidget(self.btn_update)

        self.btn_detect = QPushButton("Detect Highest iLvl")
        self.btn_detect.clicked.connect(self.detect_ilvl)
        layout.addWidget(self.btn_detect)

        self.btn_fetch = QPushButton("Fetch Gear")
        self.btn_fetch.clicked.connect(self.fetch_gear)
        layout.addWidget(self.btn_fetch)

        self.btn_ss = QPushButton("Solve SpellSpeed BiS")
        self.btn_ss.clicked.connect(lambda: self.solve("spell_speed"))
        layout.addWidget(self.btn_ss)

        self.btn_cr = QPushButton("Solve Critical BiS")
        self.btn_cr.clicked.connect(lambda: self.solve("critical"))
        layout.addWidget(self.btn_cr)

        self.setLayout(layout)

    def log_msg(self, msg):
        self.log.append(msg)
        log_info(msg)

    def update_data(self):
        self.log_msg("Updating expansion data...")
        result = update_expansion_data()
        self.log_msg(result)

    def detect_ilvl(self):
        self.log_msg("Detecting highest iLvl...")
        self.max_ilvl = detect_highest_ilvl()
        if self.max_ilvl:
            self.log_msg(f"Highest iLvl detected: {self.max_ilvl}")
        else:
            self.log_msg("Failed to detect highest iLvl.")

    def fetch_gear(self):
        if not self.max_ilvl:
            self.log_msg("Detect iLvl first.")
            return

        min_ilvl = self.max_ilvl - ILVL_WINDOW
        self.log_msg(f"Fetching gear from ilvl {min_ilvl} to {self.max_ilvl}...")
        gear = fetch_gear_range(min_ilvl, self.max_ilvl)

        self.slots = separate_by_slot(gear)
        self.blacklist_widget.clear()

        for item in gear:
            self.blacklist_widget.addItem(item["name"])

        self.log_msg("Gear loaded.")

    def solve(self, profile):
        if not self.slots:
            self.log_msg("Fetch gear first.")
            return

        self.blacklist = set(
            item.text() for item in self.blacklist_widget.selectedItems()
        )

        weights = STAT_PROFILES[profile]
        self.log_msg(f"Solving {profile} BiS...")

        best_set, score = find_best_set(
            self.slots,
            weights,
            self.blacklist
        )

        if not best_set:
            self.log_msg("No valid set found.")
            return

        self.log_msg(f"Best Score: {score}")

        for slot, item in best_set.items():
            self.log_msg(f"{slot}: {item['name']} (ilvl {item['ilvl']})")
            materia = recommend_materia(item, weights)
            self.log_msg(f"  Materia: {materia}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
