import os

from PySide6.QtCore import QStringListModel

from .tagEditor import is_supported
from .thtException import ThtException


class FileList:
    def __init__(self):
        self.__pathList = []
        self.__fileList = []
        self.__fullPathList = []
        self.__listModel = QStringListModel()

    def add(self, path: str) -> list[str]:
        """
        添加目录
        :param path: 目录路径
        :return: 新加文件列表
        """
        if os.path.isdir(path):
            if path in self.__pathList:
                raise ThtException("Folder already opened")
            file_list = os.listdir(path)
        else:
            return []

        support_list = []
        support_full_list = []
        for p in file_list:
            full_p = os.path.join(path, p)
            if os.path.isfile(full_p) and is_supported(p):
                support_list.append(p)
        support_list.sort()
        for p in support_list:
            full_p = os.path.join(path, p)
            support_full_list.append(full_p)

        if len(support_list) == 0:
            raise ThtException("No Supported file found")

        self.__pathList.append(path)
        for f in support_list:
            self.__fileList.append(f)
        for f in support_full_list:
            self.__fullPathList.append(f)
        self.update_list()

        return support_full_list

    def get_list(self) -> list:
        """
        获取 QListView 需要的 ListModel
        :return: QStringListModel
        """
        return self.__listModel

    def update_list(self):
        """
        刷新 QListView
        :return:
        """
        self.__listModel.setStringList(self.__fileList)

    def reload(self) -> list[str]:
        """
        重载所有路径
        :return:
        """
        old_list = self.__pathList.copy()
        new_list = []
        self.clear()
        for p in old_list:
            try:
                nl = self.add(p)
            except ThtException:
                pass
            else:
                for i in nl:
                    new_list.append(i)
        return new_list

    def clear(self):
        """
        清空
        :return:
        """
        self.__pathList.clear()
        self.__fileList.clear()
        self.__fullPathList.clear()
        self.update_list()

    def delete(self, item: int):
        """
        删除文件项
        :param item: 下标
        :return:
        """
        self.__fileList.pop(item)
        self.__fullPathList.pop(item)
        self.update_list()

    def swap(self, f1: int, f2: int) -> int:
        """
        交换文件项
        :param f1: 原始下标
        :param f2: 目标下标
        :return: 新下标位置
        """
        if f1 < 0 or f2 < 0 or f1 >= len(self.__fileList) or f2 >= len(self.__fileList):
            return f1
        self.__fileList[f1], self.__fileList[f2] = self.__fileList[f2], self.__fileList[f1]
        self.__fullPathList[f1], self.__fullPathList[f2] = self.__fullPathList[f2], self.__fullPathList[f1]
        self.update_list()
        return f2
