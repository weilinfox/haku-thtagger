
import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from thtagger.forms.mainWindow import MainWindow
import thtagger.utils.cache


if __name__ == "__main__":
    cache_dir = thtagger.utils.cache.get_cache_path()
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir, 0o755)

    window = None
    try:
        app = QApplication()

        window = MainWindow()
        window.show()

        sys.exit(app.exec())
    except Exception as e:
        if window is not None:
            QMessageBox.critical(window, "Unhandled Exception", traceback.format_exc(),
                                 QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.NoButton)
        else:
            print(e)
