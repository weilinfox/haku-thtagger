import json
import os

from PySide6.QtWidgets import QApplication, QFileDialog

_json_title = ("title", "artist", "album", "circle", "date", "disk_no", "track_no", "Genre", "Comment", "Cover_url")
_show_title = ("Title", "Artist", "Album", "Album artist", "Year", "Disk no", "Track no", "Genre", "Comment", "Cover")


def json_load(key: str) -> tuple:
    """
    载入本地 json
    :param key: 旧路径
    :return: list[(title, artist, album, date, diskno, trackno, genre, comment)], list[(cover)]
    """
    path = ""
    if os.path.isfile(key):
        if os.path.splitext(key)[1] != ".json":
            path = os.path.dirname(key)
    elif os.path.isdir(key):
        path = key
    else:
        path = os.path.expandvars("$HOME")
    if path:
        key = ""
        dialog = QFileDialog(QApplication.topLevelWidgets()[0])
        dialog.setWindowTitle("Select json file")
        dialog.setDirectory(path)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Json files (*.json)")
        if dialog.exec():
            filelist = dialog.selectedFiles()
            if len(filelist) == 1:
                key = filelist[0]

    if not key:
        return [_show_title[:-1]], [_show_title[-1:]]
    else:
        ans = []
        with open(key, "r") as f:
            content = f.read()
            js = json.loads(content)
            if not isinstance(js, list):
                raise Exception("Json file content is not a list")
            for it in js:
                if not isinstance(it, dict):
                    raise Exception("Json file item is not a dictionary")
                item = tuple([it.get(k, "") for k in _json_title])
                flag = False
                for i in item:
                    if i:
                        flag = True
                        break
                if not flag:
                    raise Exception("Empty json line? %s" % str(it))
                ans.append(item)
        ans.insert(0, _show_title)

        ans_covers = []
        for i in range(len(ans)):
            ans_covers.append(ans[i][-1:])
            ans[i] = ans[i][:-1]

        return ans, ans_covers


def json_save(data: list):
    save_data = []
    for d in data:
        save_data.append({_json_title[i]: d[i] for i in range(len(_show_title))})
    for d in save_data:
        for k in d.keys():
            if d[k] is None:
                d[k] = ""
            if not isinstance(d[k], str):
                d[k] = str(d[k])

    dialog = QFileDialog(QApplication.topLevelWidgets()[0])
    dialog.setWindowTitle("Save json template")
    dialog.setDirectory(os.path.expandvars("$HOME"))
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setDefaultSuffix("json")
    dialog.setNameFilter("Json files (*.json)")
    if dialog.exec():
        filelist = dialog.selectedFiles()
        if len(filelist) == 1:
            path = filelist[0]
            with open(path, "w") as f:
                f.write(json.dumps(save_data, indent=4, ensure_ascii=False))
