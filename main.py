import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QListWidget, QLabel
)

from xiv_api import detect_highest_ilvl, fetch_gear_range
from gear_manager import separate_by_slot
from solver import find_best_set
from logger import setup_logger, log_info
from config import ILVL_WINDOW

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

        layout.addWidget(QLabel("Blacklist Gear (Select to Exclude):"))
        self.blacklist_widget = QListWidget()
        layout.addWidget(self.blacklist_widget)

        self.btn_detect = QPushButton("Detect Highest iLvl")
        self.btn_detect.clicked.connect(self.detect_ilvl)
        layout.addWidget(self.btn_detect)

        self.btn_fetch = QPushButton("Fetch Gear")
        self.btn_fetch.clicked.connect(self.fetch_gear)
        layout.addWidget(self.btn_fetch)

        self.btn_solve = QPushButton("Solve Best In Slot")
        self.btn_solve.clicked.connect(self.solve)
        layout.addWidget(self.btn_solve)

        self.setLayout(layout)

    def log_msg(self, msg):
        self.log.append(msg)
        log_info(msg)

    def detect_ilvl(self):
        self.log_msg("Detecting highest iLvl...")
        self.max_ilvl = detect_highest_ilvl()

        if self.max_ilvl:
            self.log_msg(f"Highest iLvl detected: {self.max_ilvl}")
        else:
            self.log_msg("Failed to detect iLvl.")

    def fetch_gear(self):
        if not self.max_ilvl:
            self.log_msg("Detect iLvl first.")
            return

        min_ilvl = self.max_ilvl - ILVL_WINDOW
        self.log_msg(f"Fetching gear {min_ilvl}-{self.max_ilvl}...")

        gear = fetch_gear_range(min_ilvl, self.max_ilvl)
        self.slots = separate_by_slot(gear)

        self.blacklist_widget.clear()
        for item in gear:
            self.blacklist_widget.addItem(item["name"])

        self.log_msg(f"{len(gear)} gear pieces loaded.")

    def solve(self):
        if not self.slots:
            self.log_msg("Fetch gear first.")
            return

        self.blacklist = set(
            item.text() for item in self.blacklist_widget.selectedItems()
        )

        best_set, score = find_best_set(self.slots, self.blacklist)

        if not best_set:
            self.log_msg("No valid set found.")
            return

        self.log_msg(f"Best DPS Score: {score:.2f}")

        for slot, item in best_set.items():
            self.log_msg(
                f"{slot}: {item['name']} (ilvl {item['ilvl']}) | Materia: {item['materia']}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
