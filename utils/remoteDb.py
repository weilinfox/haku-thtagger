import hashlib
import os

import requests

root_dir = os.path.dirname(os.path.dirname(__file__))
cache_dir = os.path.join(root_dir, "cache")


def thb_search_album(key: str) -> tuple:
    """
    THB 专辑搜索 https://thwiki.cc/帮助:音乐资料API#搜索专辑
    :param key: 搜索字串
    :return: list[(<专辑名>, <社团名>), ...], list[<SMWID>, ...]
    """
    if len(key) == 0:
        raise Exception("Request key is empty")
    url = "https://thwiki.cc/album.php"
    params = {
        "m": "sa",
        "g": 2,
        "d": "kv",
        "l": 30,
        "o": 1,
        "v": key
    }
    res = requests.get(url=url, params=params, timeout=15)
    if res.status_code == 200:
        ans = res.json()
        list_title = [("Album", "Circle"), ]
        list_id = ["", ]
        if isinstance(ans, dict):
            for k in ans.keys():
                list_title.append(tuple(ans[k]))
                list_id.append(k)
        return list_title, list_id
    else:
        raise Exception("Request get http status code %s" % res.status_code)


def thb_get_metadata(key: str) -> tuple:
    """
    THB 专辑获取 https://thwiki.cc/帮助:音乐资料API#获取专辑
    :param key: SMWID
    :return: list[(title, artist, album, date, diskno, trackno, genre, comment)], list[(cover)]
    """
    if len(key) == 0:
        raise Exception("Request key is empty")
    url = "https://thwiki.cc/album.php"
    params = {
        "m": "ga",
        "g": 2,
        "d": "kv",
        "o": 1,
        "s": "/",
        "f": "alname event year coverurl",
        "p": "name discno trackno artist ogmusic",
        "a": key
    }
    res = requests.get(url=url, params=params, timeout=15)
    if res.status_code == 200:
        ans = res.json()
        if isinstance(ans, list):
            # print(ans)
            ans_list = []
            ans_covers = []
            alname = ans[0]["alname"]
            genre = ans[0]['event']
            date = ans[0]["year"]
            cover_url = ans[0]['coverurl']
            file_name = hashlib.md5(cover_url.encode("utf-8")).hexdigest()
            file_name += "_" + os.path.basename(cover_url)
            file_path = os.path.join(cache_dir, file_name)
            if not os.path.exists(file_path):
                # print("No cache %s" % file_path)
                res = requests.get(url=cover_url)
                with open(file_path, "wb") as fp:
                    fp.write(res.content)
            for k in ans[1].values():
                ans_list.append((k["name"], k["artist"], alname, date, k["discno"], k["trackno"],
                                 genre, k["ogmusic"], file_path))
            ans_list.sort(key=lambda x: (int(x[4]), int(x[5])))
            ans_list.insert(0, ("Title", "Artist", "Album", "Date", "Disk no", "Track no",
                                "Genre", "Comment", "Cover"))
            for i in range(len(ans_list)):
                ans_covers.append(ans_list[i][-1:])
                ans_list[i] = ans_list[i][:-1]

            return ans_list, ans_covers
    else:
        raise Exception("Request get http status code %s" % res.status_code)
