import sys
from PyQt6.QtWidgets import QApplication
from database.db import init_db
from views.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
