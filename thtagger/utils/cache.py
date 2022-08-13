
import os
import sys

cache_dirname = "thtagger"


def get_cache_path():
    if sys.platform in ["win32", "cygwin"]:
        return os.path.join(os.getenv("LOCALAPPDATA"), cache_dirname)
    else:
        return os.path.join(os.path.join(os.getenv("HOME"), ".cache"), cache_dirname)
