import sys

from PySide6.QtWidgets import QApplication
from gui.main_window import QuantumStateGUI

app = QApplication(sys.argv)

window = QuantumStateGUI()

window.show()

sys.exit(app.exec())