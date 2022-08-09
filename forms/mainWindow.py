
import os

from PySide6.QtWidgets import QMainWindow, QListView, QAbstractItemView, QFileDialog

import ui
from ui.ui_MainWindow import Ui_MainWindow
from models import fileList
from models.thtException import ThtException
from utils import remoteDb

_app_name = "thtagger %s" % ui.__version__


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__fileList = fileList.FileList()
        self.__source_item = ['THB Wiki', 'Json file']
        self.__source_func = [remoteDb.thb_search, self.on_json_load]
        self.__source_btn_enabled = [False] * 1 + [True]
        self.__source_btn_text = ["Search"] * 1 + ["Load"]

        self.bind()

    def bind(self):
        self.setWindowTitle(_app_name)

        # file area
        self.ui.fileListView.setModel(self.__fileList.get_list())
        self.ui.fileListView.setMovement(QListView.Static)
        self.ui.fileListView.setFlow(QListView.TopToBottom)
        self.ui.fileListView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.ui.fileSelectButton.clicked.connect(self.on_file_select)
        self.ui.fileReloadButton.clicked.connect(self.on_file_reload)
        self.ui.fileClearButton.clicked.connect(lambda: self.__fileList.clear())
        self.ui.fileDeleteButton.clicked.connect(self.on_file_delete)
        self.ui.fileUpButton.clicked.connect(lambda: self.on_file_move(-1))
        self.ui.fileDownButton.clicked.connect(lambda: self.on_file_move(1))

        # track area
        for i in range(len(self.__source_item)):
            self.ui.infoSourceCombo.addItem(self.__source_item[i])
        self.ui.infoSourceCombo.setCurrentIndex(0)
        self.ui.infoSearchButton.setText(self.__source_btn_text[0])
        self.ui.infoSearchButton.setEnabled(self.__source_btn_enabled[0])
        self.ui.infoSourceCombo.currentIndexChanged.connect(self.on_source_changed)
        self.ui.infoSearchKeyText.textChanged.connect(self.on_source_key_changed)
        self.ui.infoSearchButton.clicked.connect(self.on_source_request)

        self.ui.fileRenameCheck.setChecked(False)
        self.ui.fileRenameText.setEnabled(False)
        self.ui.fileRenameText.setText("%{track} %{title}")
        self.ui.fileRenameCheck.clicked.connect(self.on_rename_check)

    def on_file_select(self):
        """
        导入目录
        :return:
        """
        default_path = self.ui.fileSelectText.text()
        if os.path.exists(default_path):
            default_path = os.path.normpath(default_path)
            default_path = os.path.normcase(default_path)
            if not os.path.isdir(default_path):
                default_path = os.path.dirname(default_path)
        else:
            default_path = os.path.expandvars("$HOME")

        dialog = QFileDialog(self)
        dialog.setWindowTitle("Select file or folder")
        dialog.setDirectory(default_path)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            filelist = dialog.selectedFiles()
            if len(filelist) > 0:
                self.ui.fileSelectText.setText(filelist[0])
                try:
                    self.__fileList.add(filelist[0])
                except ThtException as e:
                    print(e)

    def on_file_reload(self):
        """
        目录重载
        :return:
        """
        try:
            self.__fileList.reload()
        except ThtException:
            pass

    def on_file_delete(self):
        """
        文件列表删除
        :return:
        """
        selected = self.ui.fileListView.selectedIndexes()
        if len(selected) == 1 and selected[0].row() < self.ui.fileListView.model().rowCount():
            self.__fileList.delete(selected[0].row())
            if selected[0].row() < self.ui.fileListView.model().rowCount():
                self.ui.fileListView.setCurrentIndex(selected[0])
            else:
                self.ui.fileListView.setCurrentIndex(selected[0].siblingAtRow(selected[0].row()-1))

    def on_file_move(self, direction: int):
        """
        文件列表移动
        :param direction: 1 下移 -1 上移
        :return:
        """
        if direction not in [1, -1]:
            return
        selected = self.ui.fileListView.selectedIndexes()
        if len(selected) == 1:
            index = selected[0].row()
            dest = self.__fileList.swap(index, index + direction)
            self.ui.fileListView.setCurrentIndex(selected[0].siblingAtRow(dest))

    def on_source_changed(self):
        """
        根据 source 变换控件状态
        :return:
        """
        index = self.ui.infoSourceCombo.currentIndex()
        self.ui.infoSearchButton.setText(self.__source_btn_text[index])
        self.ui.infoSearchButton.setEnabled(self.__source_btn_enabled[index])
        self.on_source_key_changed()

    def on_source_key_changed(self):
        """
        动态启用搜索按钮
        :return:
        """
        text_len = len(self.ui.infoSearchKeyText.text())
        btn_enabled = self.ui.infoSearchButton.isEnabled()
        if not text_len and btn_enabled:
            index = self.ui.infoSourceCombo.currentIndex()
            self.ui.infoSearchButton.setEnabled(self.__source_btn_enabled[index])
        elif text_len and not btn_enabled:
            index = self.ui.infoSourceCombo.currentIndex()
            self.ui.infoSearchButton.setEnabled(not self.__source_btn_enabled[index])

    def on_source_request(self):
        """
        从 source 获取专辑信息
        :return:
        """
        index = self.ui.infoSourceCombo.currentIndex()
        self.__source_func[index](self.ui.infoSearchKeyText.text())

    def on_json_load(self, key: str):
        """
        选取本地 json 专辑信息
        :param key: 旧路径
        :return:
        """
        if os.path.isfile(key):
            key = os.path.dirname(key)
        elif not os.path.isdir(key):
            key = os.path.expandvars("$HOME")
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Select json file")
        dialog.setDirectory(key)
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec():
            filelist = dialog.selectedFiles()
            if len(filelist) > 0:
                self.ui.infoSearchKeyText.setText(filelist[0])

    def on_rename_check(self):
        """
        文件重命名功能状态
        :return:
        """
        if self.ui.fileRenameCheck.isChecked():
            self.ui.fileRenameText.setEnabled(True)
        else:
            self.ui.fileRenameText.setEnabled(False)
