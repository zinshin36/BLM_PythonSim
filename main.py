import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal
from logger import get_logger
from solver_engine import SolverEngine
from tier_engine import detect_current_tier
from xiv_api import fetch_gear_by_job
from config import FIGHT_LENGTH

logger = get_logger()

class SolverThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, job="BLM"):
        super().__init__()
        self.job = job
        self.solver = SolverEngine()

    def run(self):
        min_ilvl, max_ilvl = detect_current_tier(self.job)
        self.progress_signal.emit(f"Fetching gear {min_ilvl}-{max_ilvl}")
        gear = fetch_gear_by_job(self.job, min_ilvl, max_ilvl)
        if not gear:
            self.progress_signal.emit("No gear found in ilvl window")
            logger.warning("No gear found during solver run")
            return
        self.progress_signal.emit("Calculating BIS...")
        self.solver.calculate_bis(gear)
        self.progress_signal.emit("BIS calculation completed")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM BiS Engine")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(QLabel("Live Log"))
        layout.addWidget(self.log_view)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.update_button = QPushButton("Update Expansion Data")
        self.update_button.clicked.connect(self.update_expansion)
        layout.addWidget(self.update_button)

        self.calc_button = QPushButton("Calculate BiS")
        self.calc_button.clicked.connect(self.calculate_bis)
        layout.addWidget(self.calc_button)

        self.setLayout(layout)
        self.solver_thread = None

    def log(self, message):
        self.log_view.append(message)
        logger.info(message)

    def update_expansion(self):
        self.log("Updating expansion data...")
        min_ilvl, max_ilvl = detect_current_tier()
        self.log(f"Detected tier: {min_ilvl}-{max_ilvl}")

    def calculate_bis(self):
        self.log("Starting BIS calculation...")
        self.solver_thread = SolverThread()
        self.solver_thread.progress_signal.connect(self.log)
        self.solver_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
