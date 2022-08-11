import requests
import traceback
from PySide6.QtCore import QObject, Signal, QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import QApplication

from .thtException import ThtException
from utils import localDb, remoteDb


class Metadata:
    def __init__(self):
        self.length = 0.0
        self.bitrate = 0
        self.channels = 0
        self.sample_rate = 0
        # wave only
        self.bits_per_sample = 0
        # mp3 only
        self.bitrate_mode = ""

        # TIT2
        self.title = ""
        # TPE1
        self.artist = ""
        # TPE2
        self.circle = ""
        # TALB
        self.album = ""
        # TDRC
        self.date = ""
        # TPOS
        self.disk_number = ""
        # TRCK
        self.track_number = ""
        # TCON
        self.genre = ""
        # APIC COVER_FRONT
        self.cover_file = ""
        # COMM
        self.comment = ""


class MetadataTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        # list[(<标题1>, ...), (<数据1>, ...)]
        self.__data = data

    def rowCount(self, parent=QModelIndex()) -> int:
        if self.__data is None:
            return 0
        return len(self.__data) - 1

    def columnCount(self, parent=QModelIndex()) -> int:
        if self.__data is None:
            return 0
        return len(self.__data[0])

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        elif role == Qt.DisplayRole:
            return str(self.__data[index.row() + 1][index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.__data[0][section]
        elif orientation == Qt.Vertical:
            return section


class MetadataReq(QObject):
    album_search_finished = Signal()
    metadata_search_finished = Signal()
    exception_raise = Signal(ThtException)

    def __init__(self, index: int, key: str = ""):
        super().__init__()

        self.__index = index
        self.__key = key

        # 查询状态 0 未查询 1 album 搜索 2 metadata 查询完成
        self.__status = 0
        # album 查询结果 tuple(list[<界面显示数据>], list[<metadata 查询数据>]) 首元素为标题
        self.__source_album_list = ()
        # metadata 查询结果
        # tuple(list[(title, artist, album, date, diskno, trackno, genre, comment)], list[(cover)]) 首元素为标题
        self.__source_metadata_list = ()

        self.__source_table_model = None

    def __to_main_thread(self):
        self.moveToThread(QApplication.instance().thread())

    def search_album(self):
        try:
            if self.__index == 0:
                self.__source_album_list = remoteDb.thb_search_album(self.__key)
                self.__status = 1
                self.__source_table_model = MetadataTableModel(self.__source_album_list[0])
                self.album_search_finished.emit()
            elif self.__index == 1:
                self.__source_metadata_list = localDb.json_load(self.__key)
                self.__status = 2
                self.__source_table_model = MetadataTableModel([("undefined1", "undefined2")])
                self.metadata_search_finished.emit()
        except requests.Timeout:
            self.exception_raise.emit(ThtException("Search request timeout"))
        except requests.ConnectionError:
            self.exception_raise.emit(ThtException("Internet connection error"))
        except Exception:
            self.exception_raise.emit(ThtException(traceback.format_exc()))
        finally:
            self.__to_main_thread()

    def search_metadata(self):
        try:
            if self.__index == 0:
                self.__source_metadata_list = remoteDb.thb_get_metadata(self.__key)
            else:
                return
            self.__source_table_model = MetadataTableModel(self.__source_metadata_list[0])
            self.__status = 2
            self.metadata_search_finished.emit()
        except requests.Timeout:
            self.exception_raise.emit(ThtException("Search request timeout"))
        except requests.ConnectionError:
            self.exception_raise.emit(ThtException("Internet connection error"))
        except Exception:
            self.exception_raise.emit(ThtException(traceback.format_exc()))
        finally:
            self.__to_main_thread()

    def set_key(self, key: str):
        self.__key = key

    def get_status(self):
        return self.__status

    def get_source_album_list(self):
        return self.__source_album_list

    def get_source_metadata_list(self):
        return self.__source_metadata_list

    def get_source_table_model(self):
        return self.__source_table_model
