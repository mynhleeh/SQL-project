import sys
from PyQt6.QtWidgets import QApplication
import database
from gui import MainWindow

if __name__ == "__main__":
    database.init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
