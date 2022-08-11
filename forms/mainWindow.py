
import os
import threading

from PySide6.QtCore import QThread, QSize, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QListView, QAbstractItemView, QFileDialog

import ui
from ui.ui_MainWindow import Ui_MainWindow
from models import fileList, metadata
from models.thtException import ThtException

_app_name = "thtagger %s" % ui.__version__


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 文件列表显示
        self.__fileList = fileList.FileList()

        # source 列表 index 参考 models.metadata
        self.__source_item = ['THB Wiki', 'Json file']
        self.__source_btn_enabled = [False] * 1 + [True]
        self.__source_btn_text = ["Search"] * 1 + ["Load"]

        # MetadataReq
        self.__source_metadata_req = None
        # http 请求线程
        self.__source_search_lock = threading.Lock()
        self.__source_search_thread = None

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

        self.ui.infoTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.infoTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.infoTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.infoTableView.doubleClicked.connect(self.on_source_album_selected)
        self.ui.infoTableView.clicked.connect(self.on_source_metadata_selected)

        self.ui.albumCoverLable.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.ui.albumCover.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

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
                else:
                    self.ui.infoSearchKeyText.setText(os.path.basename(filelist[0]))

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
        self.ui.infoTableView.setModel(None)
        self.ui.albumCover.setText("No image")
        self.ui.albumCoverLable.clear()
        index = self.ui.infoSourceCombo.currentIndex()
        key = self.ui.infoSearchKeyText.text()
        # 在新线程中处理请求
        with self.__source_search_lock:
            if self.__source_search_thread is not None:
                if self.__source_search_thread.isRunning:
                    self.__source_search_thread.exit()
            self.__source_metadata_req = metadata.MetadataReq(index, key)
            self.__source_search_thread = QThread(self)
            self.__source_search_thread.started.connect(self.__source_metadata_req.search_album)
            self.__source_metadata_req.album_search_finished.connect(self.on_source_album_finished)
            self.__source_metadata_req.metadata_search_finished.connect(self.on_source_metadata_finished)
            self.__source_metadata_req.exception_raise.connect(self.on_source_exception)
            self.__source_metadata_req.moveToThread(self.__source_search_thread)
        # 专辑搜索
        self.__source_search_thread.start()

    def stop_source_request_thread(self):
        with self.__source_search_lock:
            if self.__source_search_thread is not None:
                self.__source_search_thread.exit()
                self.__source_search_thread = None

    def on_source_album_finished(self):
        """
        专辑搜索完成
        :return:
        """
        if self.__source_metadata_req.get_status() != 1:
            return

        # 在表格中显示
        self.ui.infoTableView.setModel(self.__source_metadata_req.get_source_table_model())
        self.ui.infoTableView.resizeColumnsToContents()
        self.ui.infoTableView.resizeRowsToContents()

        self.stop_source_request_thread()

    def on_source_album_selected(self):
        """
        选中专辑
        :return:
        """
        if self.__source_metadata_req.get_status() != 1:
            return
        index = self.ui.infoTableView.selectedIndexes()
        if len(index) == 0:
            return
        index = index[0].row() + 1
        # print(self.__source_metadata_req.get_source_album_list()[0][index])

        self.__source_metadata_req.set_key(self.__source_metadata_req.get_source_album_list()[1][index])

        # 在新线程中处理请求
        with self.__source_search_lock:
            if self.__source_search_thread is not None:
                if self.__source_search_thread.isRunning:
                    self.__source_search_thread.exit()
            self.__source_search_thread = QThread(self)
            self.__source_search_thread.started.connect(self.__source_metadata_req.search_metadata)
            self.__source_metadata_req.moveToThread(self.__source_search_thread)
        # 获取整专元数据
        self.__source_search_thread.start()

    def on_source_metadata_finished(self):
        """
        元数据搜索完成
        :return:
        """
        if self.__source_metadata_req.get_status() != 2:
            return

        # 在表格中显示
        self.ui.infoTableView.setModel(self.__source_metadata_req.get_source_table_model())
        self.ui.infoTableView.resizeColumnsToContents()
        self.ui.infoTableView.resizeRowsToContents()

        self.stop_source_request_thread()

    def on_source_metadata_selected(self):
        """
        选中曲目
        :return:
        """
        if self.__source_metadata_req.get_status() != 2:
            return
        index = self.ui.infoTableView.selectedIndexes()
        if len(index) == 0:
            return
        index = index[0].row() + 1
        cover_file = self.__source_metadata_req.get_source_metadata_list()[1][index][0]
        image = QImage(cover_file)
        pixmap = QPixmap.fromImage(image)
        height, width = self.ui.albumCover.height(), self.ui.albumCover.width()
        p_height, p_width = pixmap.height(), pixmap.width()
        pixmap = pixmap.scaled(QSize(width, height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.albumCover.setPixmap(pixmap)
        self.ui.albumCoverLable.setText("%d x %d" % (p_width, p_height))

    def on_source_exception(self, exception: ThtException):
        """
        搜索字线程异常捕获
        :param exception:
        :return:
        """
        print(exception)
        self.stop_source_request_thread()

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
