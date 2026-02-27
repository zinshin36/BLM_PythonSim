import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QListWidget,
    QLabel, QComboBox
)

from xiv_api import (
    detect_highest_ilvl,
    fetch_gear_range,
    get_expansion_versions
)

from gear_manager import separate_by_slot
from solver import find_best_set
from blm_simulator import set_expansion
from logger import setup_logger, log_info
from config import ILVL_WINDOW


setup_logger()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM Gear Optimizer")
        self.resize(1000, 850)

        self.max_ilvl = None
        self.slots = None
        self.blacklist = set()

        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        layout.addWidget(QLabel("Expansion Formula:"))
        self.expansion_dropdown = QComboBox()
        self.expansion_dropdown.addItem("Dawntrail")
        layout.addWidget(self.expansion_dropdown)

        layout.addWidget(QLabel("Blacklist Gear:"))
        self.blacklist_widget = QListWidget()
        layout.addWidget(self.blacklist_widget)

        self.btn_update = QPushButton("Update Expansions From API")
        self.btn_update.clicked.connect(self.update_expansions)
        layout.addWidget(self.btn_update)

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

    def update_expansions(self):
        self.log_msg("Updating expansions from XIVAPI...")
        expansions = get_expansion_versions()

        if not expansions:
            self.log_msg("Failed to fetch expansions.")
            return

        self.expansion_dropdown.clear()
        for exp in expansions:
            self.expansion_dropdown.addItem(exp)

        self.log_msg("Expansion list updated.")

    def detect_ilvl(self):
        self.log_msg("Detecting highest iLvl...")
        self.max_ilvl = detect_highest_ilvl()

        if self.max_ilvl:
            self.log_msg(f"Highest iLvl: {self.max_ilvl}")
        else:
            self.log_msg("Failed to detect iLvl.")

    def fetch_gear(self):
        if not self.max_ilvl:
            self.log_msg("Detect iLvl first.")
            return

        min_ilvl = self.max_ilvl - ILVL_WINDOW
        self.log_msg(f"Fetching gear {min_ilvl}-{self.max_ilvl}")

        gear = fetch_gear_range(min_ilvl, self.max_ilvl)
        self.slots = separate_by_slot(gear)

        self.blacklist_widget.clear()
        for item in gear:
            self.blacklist_widget.addItem(item["name"])

        self.log_msg("Gear loaded.")

    def solve(self):
        if not self.slots:
            self.log_msg("Fetch gear first.")
            return

        selected_expansion = self.expansion_dropdown.currentText()
        set_expansion(selected_expansion)

        self.log_msg(f"Using expansion formula: {selected_expansion}")

        self.blacklist = set(
            item.text() for item in self.blacklist_widget.selectedItems()
        )

        best_set, score = find_best_set(self.slots, self.blacklist)

        if not best_set:
            self.log_msg("No valid gear set found.")
            return

        self.log_msg(f"Best DPS Score: {score}")

        for slot, item in best_set.items():
            self.log_msg(f"{slot}: {item['name']} (ilvl {item['ilvl']})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
