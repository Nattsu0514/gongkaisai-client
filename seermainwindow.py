import asyncio
import os
import pkgutil
import sys

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QAction
from quamash import QEventLoop

import server
from options import ClearCache
from plugin_loader import PluginMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('公开赛测试登录器')
        self.resize(960, 583)

        self.clear_cache = ClearCache()
        self.clear_cache.start()

        self.axWidget = QAxWidget('{8856F961-340A-11D0-A96B-00C04FD705A2}', self)
        self.axWidget.dynamicCall('Navigate(const QString&)', r'http://seer.61.com/play.shtml')
        self.axWidget.resize(1100, 600)
        self.axWidget.move(0, 23)

        self.menubar = self.menuBar()
        self.menu = self.menubar.addMenu('菜单')
        self.plugin = PluginMenu(self.menubar)
        self.add_action()

        self.httpd = server.Http('127.0.0.1', 8000)
        self.httpd.start()
        # self.hwnd = ctypes.windll.user32.FindWindowW('Qt5150QWindowIcon', self.windowTitle())

    def add_action(self) -> None:
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh)
        self.menu.addAction(refresh_action)

        clear_cache_action = QAction("清缓", self)
        clear_cache_action.triggered.connect(self.clear_cache.start)
        self.menu.addAction(clear_cache_action)

    def closeEvent(self, event) -> None:
        self.httpd.terminate()
        self.httpd.wait()
        proxy.terminate()

        event.accept()

    def refresh(self):
        self.axWidget.dynamicCall("Refresh()")


if __name__ == '__main__':
    for path_finder, name, __ in pkgutil.iter_modules([os.path.relpath("plugins", os.getcwd())]):
        path_finder.find_module(f"plugins.{name}").load_module(f"plugins.{name}")
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    w = MainWindow()
    w.show()
    proxy = server.Proxy('127.0.0.1', 8087)
    proxy.run()

    os._exit(0)
