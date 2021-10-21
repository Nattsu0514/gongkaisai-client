from PyQt5.QAxContainer import QAxWidget

from sunrise.engines import Engine
from sunrise.options import Singleton


@Singleton
class Engine(QAxWidget, Engine):
    def __init__(self, main_window):
        super().__init__('{8856F961-340A-11D0-A96B-00C04FD705A2}', main_window)
        self.dynamicCall('Navigate(const QString&)', r'http://seer.61.com/play.shtml')
        self.resize(1100, 600)
        self.move(0, 23)

    def refresh(self):
        self.dynamicCall('Navigate(const QString&)', r'http://seer.61.com/play.shtml')
        # self.dynamicCall("refresh()")

    def open_page(self, url: str):
        self.dynamicCall('Navigate(const QString&)', url)

