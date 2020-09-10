class DicTypeNotSupported(Exception):
    def __init__(self, txt=None):
        self.txt = txt


class DicTypeNotFound(Exception):
    def __init__(self, txt=None):
        self.txt = txt
