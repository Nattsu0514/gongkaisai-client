from typing import Optional

from PyQt5.QtWidgets import QMainWindow, QMenuBar

from sunrise.options import Singleton


@Singleton
class MainMenuBar(QMenuBar):
    def __init__(self, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
