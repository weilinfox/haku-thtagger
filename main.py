#!/usr/bin/python3
import os
import sys
from PySide6.QtWidgets import QApplication

from forms.mainWindow import MainWindow


if __name__ == "__main__":
    root_dir = os.path.dirname(__file__)
    cache_dir = os.path.join(root_dir, "cache")
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir, 0o755)
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

