import traceback

import mutagen.wave
import mutagen.mp3
import mutagen.flac
import os

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont

from .metadata import Metadata
from .thtException import ThtException


def is_supported(file: str):
    """
    支持文件格式
    :param file: 文件路径
    :return: 支持否
    """
    suffix = os.path.splitext(file)[1]
    if len(suffix) > 0:
        suffix = suffix[1:]
    return suffix.lower() in TagItem.valid_formats


class TagItem:
    mp3 = "mp3"
    flac = "flac"
    wav = "wav"
    valid_formats = [mp3, flac, wav]

    def __init__(self, path: str):
        split = os.path.splitext(path)
        name1 = split[0]
        suffix = split[1].lower()
        if len(suffix) == 0 or suffix[1:] not in self.valid_formats:
            raise Exception("Unsupport file format %s" % suffix)
        suffix = suffix[1:]
        # path = <parent_path>/<filename>.<format>
        self.path = path
        self.filename = os.path.basename(name1)
        self.parent_path = os.path.dirname(name1)
        self.format = suffix
        self.metadata = Metadata()
        self.new_path = ""
        self.mutagen_file = None
        if suffix == self.mp3:
            self.mutagen_file = mutagen.mp3.MP3(path)
            self.metadata.length = self.mutagen_file.info.length
            self.metadata.bitrate = self.mutagen_file.info.bitrate
            self.metadata.channels = self.mutagen_file.info.channels
            self.metadata.sample_rate = self.mutagen_file.info.sample_rate
            if self.mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.CBR:
                self.metadata.bitrate_mode = "CBR"
            elif self.mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.VBR:
                self.metadata.bitrate_mode = "VBR"
            elif self.mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.ABR:
                self.metadata.bitrate_mode = "ABR"
            else:
                self.metadata.bitrate_mode = "UNKNOWN"
        elif suffix == self.flac:
            self.mutagen_file = mutagen.flac.FLAC(path)
            self.metadata.length = self.mutagen_file.info.length
            self.metadata.bitrate = self.mutagen_file.info.bitrate
            self.metadata.channels = self.mutagen_file.info.channels
        elif suffix == self.wav:
            self.mutagen_file = mutagen.wave.WAVE(path)
            self.metadata.length = self.mutagen_file.info.length
            self.metadata.bitrate = self.mutagen_file.info.bitrate
            self.metadata.channels = self.mutagen_file.info.channels
            self.metadata.sample_rate = self.mutagen_file.info.sample_rate
            self.metadata.bits_per_sample = self.mutagen_file.info.bits_per_sample

        if self.mutagen_file.tags is not None:
            obj = self.mutagen_file.tags.get('TIT2')
            if obj is not None:
                self.metadata.title = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TPE1')
            if obj is not None:
                self.metadata.artist = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TPE2')
            if obj is not None:
                self.metadata.album_artist = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TALB')
            if obj is not None:
                self.metadata.album = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TDRC')
            if obj is not None:
                self.metadata.year = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TPOS')
            if obj is not None:
                self.metadata.disk_number = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TRCK')
            if obj is not None:
                self.metadata.track_number = str(obj.text[0])
            obj = self.mutagen_file.tags.get('TCON')
            if obj is not None:
                self.metadata.genre = str(obj.text[0])
            obj = self.mutagen_file.tags.get('COMM')
            if obj is not None:
                self.metadata.comment = str(obj.text[0])


class TagEditor(QAbstractTableModel):
    tag_title = ("File", "Title", "Artist", "Album", "Album artist", "Year", "Disk no", "Track no", "Genre", "Comment",
                 "Length", "Bitrate", "Channels", "Sample rate", "Bits per sample", "Bitrate mode")

    def __init__(self):
        super().__init__()

        self.__data: list[TagItem] = []
        # 元数据修改标志
        self.__edit_tags: list[bool] = []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.tag_title)

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        elif role == Qt.FontRole:
            if self.__edit_tags[index.row()] or self.__data[index.row()].new_path:
                font = QFont()
                font.setBold(True)
                return font
        elif role == Qt.DisplayRole:
            if index.column() == 0:
                if self.__data[index.row()].new_path:
                    return "* " + os.path.basename(self.__data[index.row()].new_path)
                if self.__edit_tags[index.row()]:
                    return "* " + os.path.basename(self.__data[index.row()].path)
                return os.path.basename(self.__data[index.row()].path)
            elif index.column() == 1:
                return self.__data[index.row()].metadata.title
            elif index.column() == 2:
                return self.__data[index.row()].metadata.artist
            elif index.column() == 3:
                return self.__data[index.row()].metadata.album
            elif index.column() == 4:
                return self.__data[index.row()].metadata.album_artist
            elif index.column() == 5:
                return str(self.__data[index.row()].metadata.year)
            elif index.column() == 6:
                return self.__data[index.row()].metadata.disk_number
            elif index.column() == 7:
                return self.__data[index.row()].metadata.track_number
            elif index.column() == 8:
                return self.__data[index.row()].metadata.genre
            elif index.column() == 9:
                return self.__data[index.row()].metadata.comment
            elif index.column() == 10:
                length = self.__data[index.row()].metadata.length
                minutes = int(length / 60)
                seconds = length - minutes * 60
                return "%02d:%05.2f" % (minutes, seconds)
            elif index.column() == 11:
                return str(self.__data[index.row()].metadata.bitrate)
            elif index.column() == 12:
                return str(self.__data[index.row()].metadata.channels)
            elif index.column() == 13:
                return "%.3f kHz" % (float(self.__data[index.row()].metadata.sample_rate) / 1000.0)
            elif index.column() == 14:
                return "%d bits" % self.__data[index.row()].metadata.bits_per_sample
            elif index.column() == 15:
                return self.__data[index.row()].metadata.bitrate_mode
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.tag_title[section]
        elif orientation == Qt.Vertical:
            return section + 1

    def add_file(self, file: str):
        """
        插入新文件
        :param file: 文件路径
        :return:
        """
        item = TagItem(file)
        index = len(self.__data)

        self.beginInsertRows(QModelIndex(), index, index)
        self.__data.append(item)
        self.__edit_tags.append(False)
        self.endInsertRows()

    def insert_file(self, index: int, file: TagItem, flag: bool):
        """
        插入项目对象
        :param index: 位置
        :param file: 对象
        :param flag: 编辑标记
        :return:
        """
        if index > len(self.__data):
            return
        self.beginInsertRows(QModelIndex(), index, index)
        self.__data.insert(index, file)
        self.__edit_tags.insert(index, flag)
        self.endInsertRows()

    def remove_file(self, index: int):
        """
        删除文件
        :param index: 索引
        :return:
        """
        if index >= len(self.__data):
            return

        self.beginRemoveRows(QModelIndex(), index, index)
        self.__data.pop(index)
        self.__edit_tags.pop(index)
        self.endRemoveRows()

    def clear_file(self):
        """
        清空文件
        :return:
        """
        self.beginRemoveRows(QModelIndex(), 0, len(self.__data) - 1)
        self.__data.clear()
        self.__edit_tags.clear()
        self.endRemoveRows()

    def swap_file(self, i1: int, i2: int):
        """
        交换两个对象位置
        :param i1: 索引1
        :param i2: 索引2
        :return:
        """
        if i1 >= len(self.__data) or i2 >= len(self.__data) or i1 < 0 or i2 < 0:
            return
        flag1, flag2 = self.__edit_tags[i1], self.__edit_tags[i2]
        obj1, obj2 = self.__data[i1], self.__data[i2]

        self.remove_file(i1)
        self.insert_file(i1, obj2, flag2)
        self.remove_file(i2)
        self.insert_file(i2, obj1, flag1)

    def edit_file(self, index: int, data: Metadata):
        """
        编辑元数据
        :param index: 索引
        :param data: 新元数据
        :return:
        """
        self.__data[index].metadata.copy_metadata(data)
        self.__edit_tags[index] = True

        top_left = QModelIndex()
        top_left.sibling(index, 0)
        bottom_right = QModelIndex()
        bottom_right.sibling(index, len(self.tag_title) - 1)
        self.dataChanged.emit(top_left, bottom_right)

    def edit_file_name(self, index: int, fmt: str):
        """
        重命名文件
        :param index: 索引
        :param fmt: 格式
        :return:
        """
        if fmt.strip() == "":
            return

        item = self.__data[index]
        fmt = fmt.replace("%{title}", item.metadata.title)
        fmt = fmt.replace("%{artist}", item.metadata.artist)
        fmt = fmt.replace("%{album_artist}", item.metadata.album_artist)
        fmt = fmt.replace("%{album}", item.metadata.album)
        fmt = fmt.replace("%{year}", item.metadata.year)
        fmt = fmt.replace("%{disk}", "%02d" % (int(item.metadata.disk_number) if item.metadata.disk_number else 0))
        fmt = fmt.replace("%{track}", "%02d" % (int(item.metadata.track_number) if item.metadata.track_number else 0))
        fmt = fmt.replace("%{genre}", item.metadata.genre)
        fmt = fmt.replace("%{comment}", item.metadata.comment)

        if fmt.strip() == "":
            raise ThtException("Get empty file name when rename file \"%s\"" % os.path.basename(item.path))

        item.new_path = os.path.join(item.parent_path, "%s.%s" % (fmt, item.format))

        top_left = QModelIndex()
        top_left.sibling(index, 0)
        bottom_right = QModelIndex()
        bottom_right.sibling(index, 0)
        self.dataChanged.emit(top_left, bottom_right)

    def save_files(self):
        try:
            for i in range(len(self.__data)):
                if not self.__edit_tags[i]:
                    continue
                # 保存更改

                # self.__edit_tags[i] = False

                top_left = QModelIndex()
                top_left.sibling(i, 0)
                bottom_right = QModelIndex()
                bottom_right.sibling(i, len(self.tag_title) - 1)
                self.dataChanged.emit(top_left, bottom_right)
        except Exception:
            raise ThtException("Error occur while saving changes:\n" + traceback.format_exc())

    def count(self) -> int:
        return len(self.__data)
