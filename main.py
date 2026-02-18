import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
)
from xiv_api import fetch_max_ilvl_for_job, fetch_gear
from gear_manager import separate_by_slot
from solver import find_best_set
from materia_engine import recommend_materia
from config import JOB_CATEGORY, ILVL_WINDOW, STAT_PROFILES
from logger import setup_logger, log_info

# Initialize logger
setup_logger()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM Gear Optimizer")
        self.resize(800, 700)

        layout = QVBoxLayout()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.btn_detect = QPushButton("Detect Highest iLvl")
        self.btn_detect.clicked.connect(self.detect_ilvl)
        layout.addWidget(self.btn_detect)

        self.btn_fetch = QPushButton("Fetch Gear")
        self.btn_fetch.clicked.connect(self.fetch_gear)
        layout.addWidget(self.btn_fetch)

        self.btn_ss = QPushButton("Solve SpellSpeed BiS")
        self.btn_ss.clicked.connect(lambda: self.solve_bis("spell_speed"))
        layout.addWidget(self.btn_ss)

        self.btn_cr = QPushButton("Solve Critical BiS")
        self.btn_cr.clicked.connect(lambda: self.solve_bis("critical"))
        layout.addWidget(self.btn_cr)

        self.setLayout(layout)

    def log_msg(self, msg: str):
        self.log.append(msg)
        log_info(msg)

    def detect_ilvl(self):
        max_ilvl = fetch_max_ilvl_for_job(JOB_CATEGORY)
        if max_ilvl:
            self.max_ilvl = max_ilvl
            self.log_msg(f"Detected max ilvl: {self.max_ilvl}")
        else:
            self.log_msg("Failed to detect max ilvl.")

    def fetch_gear(self):
        if not hasattr(self,"max_ilvl"):
            self.log_msg("Detect iLvl first.")
            return
        min_ilvl = self.max_ilvl - ILVL_WINDOW
        gear_list = fetch_gear(JOB_CATEGORY, min_ilvl, self.max_ilvl)
        self.slots = separate_by_slot(gear_list)
        self.log_msg(f"Gear fetched and separated into {len(self.slots)} slots")

    def solve_bis(self, profile_name):
        if not hasattr(self,"slots"):
            self.log_msg("Fetch gear first.")
            return
        self.log_msg(f"Solving {profile_name} BiS build...")
        weights = STAT_PROFILES.get(profile_name)
        best_set, score = find_best_set(self.slots, weights)
        self.log_msg(f"Best Score ({profile_name}): {score}")
        for slot,item in best_set.items():
            self.log_msg(f"{slot}: {item['name']} ilvl {item['ilvl']}")
            materia = recommend_materia(item["materia_slots"], item["stats"], weights)
            self.log_msg(f" → Materia: {materia}")

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
