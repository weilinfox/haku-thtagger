class ThtException(Exception):
    def __init__(self, info: str):
        super().__init__(self)
        self.errorInfo = info

    def __str__(self):
        return self.errorInfo
