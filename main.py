import sys
import os
import logging
import traceback
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QSpinBox
)

from solver_engine import BLMSolver

# ---------------- LOGGING ----------------

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    base_path = get_base_path()
    log_path = os.path.join(base_path, "app_debug.log")

    logging.basicConfig(
        filename=log_path,
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("=========================================")
    logging.info("Application Launch: %s", datetime.now())
    logging.info("Python Version: %s", sys.version)
    logging.info("Executable Path: %s", sys.executable)

setup_logging()

# ---------------- UI ----------------

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLM Planner - Nothing Escapes Edition")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        self.label = QLabel("Fight Duration (seconds):")
        layout.addWidget(self.label)

        self.duration_input = QSpinBox()
        self.duration_input.setRange(10, 1000)
        self.duration_input.setValue(60)
        layout.addWidget(self.duration_input)

        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.run_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_simulation(self):
        try:
            duration = self.duration_input.value()
            logging.info(f"User started simulation for {duration}s")

            solver = BLMSolver(duration)
            results = solver.simulate()

            self.output.clear()
            self.output.append("\n".join(results))

        except Exception:
            logging.critical("Simulation error:")
            logging.critical(traceback.format_exc())
            self.output.append("ERROR - See app_debug.log")


# ---------------- MAIN ----------------

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    except Exception:
        logging.critical("Fatal crash:")
        logging.critical(traceback.format_exc())
        print(traceback.format_exc())
        input("Press Enter to exit...")
