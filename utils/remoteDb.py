
import requests


def thb_search_album(key: str) -> dict:
    if len(key) == 0:
        return {}
    url = "https://thwiki.cc/album.php"
    params = {
        "m": "sa",
        "g": 0,
        "d": "kv",
        "v": key
    }
    res = requests.get(url=url, params=params, timeout=60)
    if res.status_code == 200:
        return res.json()

    return {}


def thb_search_metadata(key: str) -> dict:
    pass
