from models.metadata import Metadata


class BaseReader:
    __abstract__ = True

    def __init__(self, key: str):
        self._key = key

    def read(self) -> list[Metadata]:
        pass
