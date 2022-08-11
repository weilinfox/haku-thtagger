#!/usr/bin/python3

import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from forms.mainWindow import MainWindow


if __name__ == "__main__":
    root_dir = os.path.dirname(__file__)
    cache_dir = os.path.join(root_dir, "cache")
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir, 0o755)

    window = None
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())
    except Exception as e:
        if window is not None:
            QMessageBox.critical(window, "Unhandled Exception", traceback.format_exc(),
                                 QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.NoButton)
        else:
            print(e)
