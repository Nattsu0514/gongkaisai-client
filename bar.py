from typing import Optional

from PyQt5.QtWidgets import QAction, QMainWindow, QMenuBar

import client
from options import ClearCache, Singleton


@Singleton
class MainMenuBar(QMenuBar):
    def __init__(self, parent: Optional[QMainWindow] = None):
        super().__init__(parent)

        # self.add_action()

    def add_action(self) -> None:
        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(client.get_engine().refresh())
        self.menu.addAction(refresh_action)

        clear_cache_action = QAction("清缓", self)
        clear_cache_action.triggered.connect(ClearCache.start)
        self.menu.addAction(clear_cache_action)
