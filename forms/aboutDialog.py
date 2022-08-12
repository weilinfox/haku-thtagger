
import sys

import mutagen
import PySide6
from PySide6.QtWidgets import QDialog

import ui
from ui.ui_AboutDialog import Ui_AboutDialog

_app_name = "thtagger %s" % ui.__version__


class AboutDialog(QDialog):

    def __init__(self):
        super(AboutDialog, self).__init__()
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("About %s" % _app_name)

        self.ui.aboutLabel.setText("""
<h2>白玉楼製作所</h2>
<p><a href="https://github.com/weilinfox/haku-thtagger">thtagger</a>&nbsp;version:&nbsp;%s</p>
<p><a href="https://www.python.org/">Python</a>&nbsp;version:&nbsp;%s</p>
<p><a href="https://www.qt.io/">Qt</a>&nbsp;version:&nbsp;%s</p>
<p><a href="https://github.com/quodlibet/mutagen">Mutagen</a>&nbsp;version:&nbsp;%s</p>

</br><p>License: GNU General Public License Version 2</p>
        """ % (ui.__version__, sys.version, PySide6.__version__,  mutagen.version_string))
