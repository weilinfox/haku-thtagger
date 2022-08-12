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
        # wave and flac
        self.bits_per_sample = -1
        # mp3 only
        self.bitrate_mode = ""

        # ID3   rename format   RIFF    VORBIS
        # TIT2  %{title}        INAM    TITLE
        self.title = ""
        # TPE1  %{artist}       IART    ARTIST
        self.artist = ""
        # TPE2  %{album_artist}         ALBUMARTIST
        self.album_artist = ""
        # TALB  %{album}        IPRD    ALBUM
        self.album = ""
        # TDRC  %{year}         ICRD    DATE
        self.year = ""
        # TPOS  %{disk}                 DISCNUMBER
        self.disk_number = ""
        # TRCK  %{track}        ITRK    TRACKNUMBER
        self.track_number = ""
        # TCON  %{genre}        IGNR    GENRE
        self.genre = ""
        # APIC COVER_FRONT
        self.cover_file = ""
        # COMM  %{comment}      ICMT    COMMENT
        self.comment = ""

    def copy_metadata(self, new_data):
        self.title = new_data.title
        self.artist = new_data.artist
        self.album_artist = new_data.album_artist
        self.album = new_data.album
        self.year = new_data.year
        self.disk_number = new_data.disk_number
        self.track_number = new_data.track_number
        self.genre = new_data.genre
        self.cover_file = new_data.cover_file
        self.comment = new_data.comment


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
            return section + 1


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
        # tuple(list[(title, artist, album, album artist, year, diskno, trackno, genre, comment)], list[(cover)])
        # 首元素为标题
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

    def generate_metadata_list(self) -> list[Metadata]:
        data_list = []
        # list[(title, artist, album, album artist, year, diskno, trackno, genre, comment)
        list1 = self.__source_metadata_list[0]
        # list[(cover)]
        list2 = self.__source_metadata_list[1]
        for i in range(1, len(list1)):
            metadata = Metadata()
            metadata.title, metadata.artist, metadata.album, metadata.album_artist, metadata.year = list1[i][:5]
            metadata.disk_number, metadata.track_number, metadata.genre, metadata.comment = list1[i][5:]
            metadata.cover_file = list2[i][0]
            data_list.append(metadata)

        return data_list
