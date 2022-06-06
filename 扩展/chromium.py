from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from sunrise import engines


class Engine(QWebEngineView, engines.Engine):
    name = "chromium_qwebengine"
    rendering_engine_name = "chromium"

    def __init__(self, main_window):
        super().__init__(main_window)
        self.resize(1100, 600)
        self.move(0, 23)
        self.load(QUrl("http://helpx.adobe.com/flash-player.html"))

    def open_page(self, url: str):
        self.load(QUrl(url))

    def refresh(self):
        self.refresh()
