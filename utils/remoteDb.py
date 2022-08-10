
import requests


def thb_search_album(key: str) -> tuple:
    """
    thb 专辑搜索
    https://thwiki.cc/%E5%B8%AE%E5%8A%A9:%E9%9F%B3%E4%B9%90%E8%B5%84%E6%96%99API#%E6%90%9C%E7%B4%A2%E4%B8%93%E8%BE%91
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
    res = requests.get(url=url, params=params, timeout=60)
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


def thb_get_metadata(key: str) -> list:
    print(key)
    return []
