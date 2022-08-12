import mimetypes
import os
import traceback

import mutagen.wave
import mutagen.mp3
import mutagen.flac
import mutagen.id3
import mutagen._riff
from mutagen._util import loadfile

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont, QPixmap, QImage

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
        path = os.path.normpath(path)
        split = os.path.splitext(path)
        name1 = split[0]
        suffix = split[1].lower()
        if len(suffix) == 0 or suffix[1:] not in self.valid_formats:
            raise Exception("Unsupport file format %s" % suffix)
        suffix = suffix[1:]
        # path = <parent_path>/<filename>.<format>
        self.__path = path
        self.__filename = os.path.basename(name1)
        self.__parent_path = os.path.dirname(name1)
        self.__format = suffix
        self.__metadata = Metadata()
        self.__mutagen_file = None

        # edit flag
        self.__new_path = ""
        self.__new_metadata = False

        # riff info encoding
        self.__riff_info_encoding = "cp1252"

        if suffix == self.mp3:
            self.__mutagen_file = mutagen.mp3.MP3(path)
            self.__metadata.length = self.__mutagen_file.info.length
            self.__metadata.bitrate = self.__mutagen_file.info.bitrate
            self.__metadata.channels = self.__mutagen_file.info.channels
            self.__metadata.sample_rate = self.__mutagen_file.info.sample_rate
            if self.__mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.CBR:
                self.__metadata.bitrate_mode = "CBR"
            elif self.__mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.VBR:
                self.__metadata.bitrate_mode = "VBR"
            elif self.__mutagen_file.info.bitrate_mode == mutagen.mp3.BitrateMode.ABR:
                self.__metadata.bitrate_mode = "ABR"
            else:
                self.__metadata.bitrate_mode = "UNKNOWN"
        elif suffix == self.flac:
            self.__mutagen_file = mutagen.flac.FLAC(path)
            self.__metadata.length = self.__mutagen_file.info.length
            self.__metadata.bitrate = self.__mutagen_file.info.bitrate
            self.__metadata.sample_rate = self.__mutagen_file.info.sample_rate
            self.__metadata.bits_per_sample = self.__mutagen_file.info.bits_per_sample
            self.__metadata.channels = self.__mutagen_file.info.channels
        elif suffix == self.wav:
            self.__mutagen_file = mutagen.wave.WAVE(path)
            self.__metadata.length = self.__mutagen_file.info.length
            self.__metadata.bitrate = self.__mutagen_file.info.bitrate
            self.__metadata.channels = self.__mutagen_file.info.channels
            self.__metadata.sample_rate = self.__mutagen_file.info.sample_rate
            self.__metadata.bits_per_sample = self.__mutagen_file.info.bits_per_sample

        if suffix == self.wav or suffix == self.mp3:
            # ID3
            self.__metadata.title = self.__get_tag_id3_field("TIT2")
            self.__metadata.artist = self.__get_tag_id3_field("TPE1")
            self.__metadata.album_artist = self.__get_tag_id3_field("TPE2")
            self.__metadata.album = self.__get_tag_id3_field("TALB")
            self.__metadata.year = self.__get_tag_id3_field("TDRC")
            self.__metadata.disk_number = self.__get_tag_id3_field("TPOS")
            self.__metadata.track_number = self.__get_tag_id3_field("TRCK")
            self.__metadata.genre = self.__get_tag_id3_field("TCON")
            self.__metadata.comment = self.__get_tag_id3_field("COMM")

            if self.__mutagen_file.tags is not None:
                picture = self.__mutagen_file.tags.getall("APIC")
                if picture:
                    self.__metadata.cover_extract = picture[0].data
        elif suffix == self.flac:
            # Vorbis comment
            # print(self.__mutagen_file.tags)
            vorbis_dict = {}
            if isinstance(self.__mutagen_file.tags, list):
                for f in self.__mutagen_file.tags:
                    vorbis_dict.update({f[0].lower(): f[1]})
            elif isinstance(self.__mutagen_file.tags, dict):
                for k, v in self.__mutagen_file.tags.items():
                    vorbis_dict.update({k.lower(): v})
            self.__metadata.title = self.__get_tag_vorbis_field(vorbis_dict, "TITLE")
            self.__metadata.artist = self.__get_tag_vorbis_field(vorbis_dict, "ARTIST")
            self.__metadata.album_artist = self.__get_tag_vorbis_field(vorbis_dict, "ALBUMARTIST")
            self.__metadata.album = self.__get_tag_vorbis_field(vorbis_dict, "ALBUM")
            self.__metadata.year = self.__get_tag_vorbis_field(vorbis_dict, "DATE")
            self.__metadata.disk_number = self.__get_tag_vorbis_field(vorbis_dict, "DISCNUMBER")
            self.__metadata.track_number = self.__get_tag_vorbis_field(vorbis_dict, "TRACKNUMBER")
            self.__metadata.genre = self.__get_tag_vorbis_field(vorbis_dict, "GENRE")
            self.__metadata.comment = self.__get_tag_vorbis_field(vorbis_dict, "COMMENT")

            if self.__mutagen_file.pictures:
                self.__metadata.cover_extract = self.__mutagen_file.pictures[0].data

    def __get_tag_id3_field(self, field: str) -> str:
        if self.__mutagen_file.tags is None:
            return ""
        obj = self.__mutagen_file.tags.get(field)
        if obj is not None:
            return str(obj.text[0])

    @staticmethod
    def __get_tag_vorbis_field(vorbis_dict: dict, field: str) -> str:
        return vorbis_dict.get(field.lower(), "")

    def get_metadata(self):
        """
        元数据
        :return: class Metadata
        """
        return self.__metadata

    def edit_metadata(self, new_data: Metadata):
        """
        编辑元数据
        :param new_data:
        :return:
        """
        self.__metadata.copy_metadata(new_data)
        self.__new_metadata = True

    def save_metadata(self):
        """
        保存元数据
        :return:
        """
        if not self.__new_metadata:
            return
        cover_mime = mimetypes.guess_type(self.__metadata.cover_file)[0]
        with open(self.__metadata.cover_file, "rb") as f:
            cover_data = f.read()
        if self.__format == self.mp3 or self.__format == self.wav:
            if self.__mutagen_file.tags is None:
                self.__mutagen_file.tags = mutagen.id3.ID3()
            self.__mutagen_file.tags.setall("TIT2", [mutagen.id3.TIT2(encodings=3, text=self.__metadata.title)])
            self.__mutagen_file.tags.setall("TPE1", [mutagen.id3.TPE1(encodings=3, text=self.__metadata.artist)])
            self.__mutagen_file.tags.setall("TPE2", [mutagen.id3.TPE2(encodings=3, text=self.__metadata.album_artist)])
            self.__mutagen_file.tags.setall("TALB", [mutagen.id3.TALB(encodings=3, text=self.__metadata.album)])
            self.__mutagen_file.tags.setall("TDRC", [mutagen.id3.TDRC(encodings=3, text=self.__metadata.year)])
            self.__mutagen_file.tags.setall("TPOS", [mutagen.id3.TPOS(encodings=3, text=self.__metadata.disk_number)])
            self.__mutagen_file.tags.setall("TRCK", [mutagen.id3.TRCK(encodings=3, text=self.__metadata.track_number)])
            self.__mutagen_file.tags.setall("TCON", [mutagen.id3.TCON(encodings=3, text=self.__metadata.genre)])
            self.__mutagen_file.tags.setall("COMM", [mutagen.id3.COMM(encodings=3, text=self.__metadata.comment)])
            self.__mutagen_file.tags.setall("APIC", [mutagen.id3.APIC(encodings=3, type=3,
                                                                      mime=cover_mime, data=cover_data)])

            self.__mutagen_file.tags.save(self.__mutagen_file.filename)

            # RIFF INFO
            # https://github.com/metabrainz/picard/blob/master/picard/formats/wav.py#L39-L219
            if self.__format == self.wav:
                self.save_riff_info(self.__path)
        elif self.__format == self.flac:
            self.__mutagen_file.delete()
            if self.__mutagen_file.tags is None:
                self.__mutagen_file.add_tags()
            self.__mutagen_file.tags.update({"TITLE": self.__metadata.title})
            self.__mutagen_file.tags.update({"ARTIST": self.__metadata.artist})
            self.__mutagen_file.tags.update({"ALBUM": self.__metadata.album})
            self.__mutagen_file.tags.update({"ALBUMARTIST": self.__metadata.album_artist})
            self.__mutagen_file.tags.update({"DATE": self.__metadata.year})
            self.__mutagen_file.tags.update({"DISCNUMBER": self.__metadata.disk_number})
            self.__mutagen_file.tags.update({"TRACKNUMBER": self.__metadata.track_number})
            self.__mutagen_file.tags.update({"GENRE": self.__metadata.genre})
            self.__mutagen_file.tags.update({"COMMENT": self.__metadata.comment})
            self.__mutagen_file.tags.update({"ENCODER": "Thtagger with Mutagen"})

            self.__mutagen_file.clear_pictures()
            image = QImage(self.__metadata.cover_file)
            pixmap = QPixmap(image)
            picture = mutagen.flac.Picture()
            picture.type = mutagen.id3.PictureType.COVER_FRONT
            picture.mime = cover_mime
            picture.data = cover_data
            picture.height, picture.width, picture.depth = pixmap.height(), pixmap.width(), pixmap.depth()
            self.__mutagen_file.add_picture(picture)

            self.__mutagen_file.save()

        self.__new_metadata = False

    @loadfile(writable=True)
    def save_riff_info(self, file):
        """
        保存 wav riff info
        :param file: 文件名
        :return:
        """
        riff_file = mutagen._riff.RiffFile(file.fileobj)
        info_chunk = None
        for c in riff_file.root.subchunks():
            if c.id == 'LIST' and c.name == 'INFO':
                info_chunk = c
                break

        if info_chunk is not None:
            info_chunk.delete()
        info_chunk = riff_file.insert_chunk('LIST', b'INFO')
        self.__save_riff_info_chunk_data(info_chunk, "INAM", self.__metadata.title)
        self.__save_riff_info_chunk_data(info_chunk, "IART", self.__metadata.artist)
        self.__save_riff_info_chunk_data(info_chunk, "IPRD", self.__metadata.album)
        self.__save_riff_info_chunk_data(info_chunk, "ICRD", self.__metadata.year)
        self.__save_riff_info_chunk_data(info_chunk, "ITRK", self.__metadata.track_number)
        self.__save_riff_info_chunk_data(info_chunk, "IGNR", self.__metadata.genre)

    def __save_riff_info_chunk_data(self, chunk, name: str, value: str):
        """
        保存一个 riff info 字段
        :param chunk:
        :param name: 字段名
        :param value: 字段值
        :return:
        """
        data = value.encode(self.__riff_info_encoding, errors='replace') + b'\x00'
        chunk.insert_chunk(name, data)

    def set_riff_info_encoding(self, encoding: str):
        """
        设置 riff info 字符编码
        :param encoding: 字符编码
        :return:
        """
        self.__riff_info_encoding = encoding

    def is_metadata_edited(self):
        """
        元数据是否被更改
        :return:
        """
        return self.__new_metadata

    def set_new_path(self, name: str):
        """
        设置新路径
        :param name: 文件名 不包含后缀
        :return:
        """
        self.__new_path = os.path.normpath(os.path.join(self.__parent_path, "%s.%s" % (name, self.__format)))
        if self.__new_path == self.__path:
            self.__new_path = ""

    def get_new_path(self):
        """
        获取新路径
        :return: 新路径
        """
        return self.__new_path

    def is_renamed(self):
        """
        是否设置了新路径
        :return:
        """
        return self.__new_path != ""

    def submit_rename(self):
        """
        重命名文件
        :return:
        """
        os.rename(self.__path, self.__new_path)
        self.__path = self.__new_path

    def get_path(self):
        """
        获取文件路径
        :return: 文件路径
        """
        return self.__path


class TagEditor(QAbstractTableModel):
    tag_title = ("File", "Title", "Artist", "Album", "Album artist", "Year", "Disk no", "Track no", "Genre", "Comment",
                 "Length", "Bitrate", "Channels", "Sample rate", "Bits per sample", "Bitrate mode")

    def __init__(self):
        super().__init__()

        self.__data: list[TagItem] = []

        # riff info 编码 CJK
        self.__riff_info_encoding = "cp936"

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
            if self.__data[index.row()].is_metadata_edited() or self.__data[index.row()].is_renamed():
                font = QFont()
                font.setBold(True)
                return font
        elif role == Qt.DisplayRole:
            if index.column() == 0:
                if self.__data[index.row()].is_renamed():
                    return "* " + os.path.basename(self.__data[index.row()].get_new_path())
                if self.__data[index.row()].is_metadata_edited():
                    return "* " + os.path.basename(self.__data[index.row()].get_path())
                return os.path.basename(self.__data[index.row()].get_path())
            elif index.column() == 1:
                return self.__data[index.row()].get_metadata().title
            elif index.column() == 2:
                return self.__data[index.row()].get_metadata().artist
            elif index.column() == 3:
                return self.__data[index.row()].get_metadata().album
            elif index.column() == 4:
                return self.__data[index.row()].get_metadata().album_artist
            elif index.column() == 5:
                return str(self.__data[index.row()].get_metadata().year)
            elif index.column() == 6:
                return self.__data[index.row()].get_metadata().disk_number
            elif index.column() == 7:
                return self.__data[index.row()].get_metadata().track_number
            elif index.column() == 8:
                return self.__data[index.row()].get_metadata().genre
            elif index.column() == 9:
                return self.__data[index.row()].get_metadata().comment
            elif index.column() == 10:
                length = self.__data[index.row()].get_metadata().length
                minutes = int(length / 60)
                seconds = length - minutes * 60
                return "%02d:%05.2f" % (minutes, seconds)
            elif index.column() == 11:
                return str(self.__data[index.row()].get_metadata().bitrate)
            elif index.column() == 12:
                return str(self.__data[index.row()].get_metadata().channels)
            elif index.column() == 13:
                return "%.3f kHz" % (float(self.__data[index.row()].get_metadata().sample_rate) / 1000.0)
            elif index.column() == 14:
                if self.__data[index.row()].get_metadata().bits_per_sample < 0:
                    return ""
                return "%d bits" % self.__data[index.row()].get_metadata().bits_per_sample
            elif index.column() == 15:
                return self.__data[index.row()].get_metadata().bitrate_mode
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
        try:
            item = self.new_tag_item(file)
            index = len(self.__data)
        except Exception:
            raise ThtException(traceback.format_exc())

        self.beginInsertRows(QModelIndex(), index, index)
        self.__data.append(item)
        self.endInsertRows()

    def insert_file(self, index: int, file: TagItem):
        """
        插入项目对象
        :param index: 位置
        :param file: 对象
        :return:
        """
        if index > len(self.__data):
            return
        self.beginInsertRows(QModelIndex(), index, index)
        self.__data.insert(index, file)
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
        self.endRemoveRows()

    def clear_file(self):
        """
        清空文件
        :return:
        """
        self.beginRemoveRows(QModelIndex(), 0, len(self.__data) - 1)
        self.__data.clear()
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
        obj1, obj2 = self.__data[i1], self.__data[i2]

        self.remove_file(i1)
        self.insert_file(i1, obj2)
        self.remove_file(i2)
        self.insert_file(i2, obj1)

    def edit_file(self, index: int, data: Metadata):
        """
        编辑元数据
        :param index: 索引
        :param data: 新元数据
        :return:
        """
        self.__data[index].edit_metadata(data)

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
        if index >= len(self.__data):
            return
        if fmt.strip() == "":
            return

        try:
            item = self.__data[index]
            fmt = fmt.replace("%{title}", item.get_metadata().title)
            fmt = fmt.replace("%{artist}", item.get_metadata().artist)
            fmt = fmt.replace("%{album_artist}", item.get_metadata().album_artist)
            fmt = fmt.replace("%{album}", item.get_metadata().album)
            fmt = fmt.replace("%{year}", item.get_metadata().year)
            fmt = fmt.replace("%{disk}",
                              "%02d" % (int(item.get_metadata().disk_number)
                                        if item.get_metadata().disk_number else 0))
            fmt = fmt.replace("%{track}",
                              "%02d" % (int(item.get_metadata().track_number)
                                        if item.get_metadata().track_number else 0))
            fmt = fmt.replace("%{genre}", item.get_metadata().genre)
            fmt = fmt.replace("%{comment}", item.get_metadata().comment)
        except Exception:
            raise ThtException(traceback.format_exc())

        if fmt.strip() == "":
            raise ThtException("Get empty file name when rename file \"%s\"" % os.path.basename(item.__path))

        item.set_new_path(fmt)

        top_left = QModelIndex()
        top_left.sibling(index, 0)
        bottom_right = QModelIndex()
        bottom_right.sibling(index, 0)
        self.dataChanged.emit(top_left, bottom_right)

    def save_files(self):
        """
        保存修改的文件
        :return:
        """
        for i in range(len(self.__data)):
            try:
                # 保存元数据更改
                self.__data[i].save_metadata()

                # 重命名
                if self.__data[i].is_renamed():
                    self.__data[i].submit_rename()
            except Exception:
                raise ThtException("Error occur while saving changes:\n" + traceback.format_exc())
            finally:
                # 重新载入
                new_item = self.new_tag_item(self.__data[i].get_path())
                self.__data[i] = new_item

                top_left = QModelIndex()
                top_left.sibling(i, 0)
                bottom_right = QModelIndex()
                bottom_right.sibling(i, len(self.tag_title) - 1)
                self.dataChanged.emit(top_left, bottom_right)

    def new_tag_item(self, path: str) -> TagItem:
        """
        构造新 TagItem
        :param path: 文件路径
        :return: TagItem
        """
        item = TagItem(path)
        item.set_riff_info_encoding(self.__riff_info_encoding)
        return item

    def count(self) -> int:
        """
        项目总数
        :return: 总数
        """
        return len(self.__data)

    def get_data(self, index: int):
        """
        根据行获取 TagItem
        :param index: 索引
        :return: TagItem
        """
        if index < len(self.__data):
            return self.__data[index]
        return None
