class Engine:
    name: str
    url: str

    def __init__(self):
        pass

    def refresh(self):
        raise NotImplementedError

    def open_page(self, url: str):
        raise NotImplementedError
