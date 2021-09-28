from typing import Optional

from PyQt5.QtWidgets import QMainWindow

from bar import MainMenuBar


class MainWindow(QMainWindow):
    start_set = set()

    shutdown_set = set()

    def __init__(self, title: Optional[str] = None):
        super().__init__()
        [func() for func in self.start_set]
        self.setWindowTitle(title)
        self.resize(960, 583)
        self.setMenuBar(MainMenuBar())

    def closeEvent(self, event) -> None:
        [func() for func in self.shutdown_set]
        event.accept()