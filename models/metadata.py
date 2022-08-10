from PySide6.QtCore import QObject, Signal

from utils import localDb, remoteDb


class Metadata:
    def __init__(self, title=""):
        self.title = title
        self.artist = ""
        self.album = ""
        self.comment = ""
        self.date = ""
        self.track_number = ""
        self.genre = ""
        self.cover = ""


class MetadataReq(QObject):
    album_search_finished = Signal(list)
    metadata_search_finished = Signal(list)

    def __init__(self, index: int, key: str = ""):
        super().__init__()

        self.__index = index
        self.__key = key

    def search_album(self):
        if self.__index == 0:
            ans = remoteDb.thb_search_album(self.__key)
            self.album_search_finished.emit([ans])
        elif self.__index == 1:
            ans = localDb.json_load(self.__key)
            self.metadata_search_finished.emit([ans])
