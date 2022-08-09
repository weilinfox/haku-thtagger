import json

from .baseReader import BaseReader
from models.metadata import Metadata


class JsonReader(BaseReader):
    def __init__(self, path: str):
        super().__init__(path)

    def read(self) -> list[Metadata]:
        with open(self._key) as jf:
            content = jf.read()
            js = json.dumps(content)

