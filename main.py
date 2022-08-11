#!/usr/bin/python3

import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from forms.mainWindow import MainWindow
import utils.cache


if __name__ == "__main__":
    cache_dir = utils.cache.get_cache_path()
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
        print("Handle exception")
