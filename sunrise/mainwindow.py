import ctypes
import ctypes.wintypes
from typing import Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from sunrise.bar import MainMenuBar


class MainWindow(QMainWindow):
    start_set = set()

    shutdown_set = set()

    def __init__(self, title: Optional[str] = None):
        super().__init__()
        [func() for func in self.start_set]
        self.setWindowTitle(title)
        self.resize(960, 583)
        self.setMenuBar(MainMenuBar())
        self.setWindowIcon(QIcon('Logo.ico'))

    @property
    def hwnd(self):
        return ctypes.windll.user32.FindWindowW('Qt5152QWindowIcon', self.windowTitle())

    @property
    def pid(self):
        pid = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(self.hwnd, ctypes.byref(pid))
        print(self.hwnd, pid, self.windowTitle())
        return pid.value

    def closeEvent(self, event) -> None:
        [func() for func in self.shutdown_set]
        event.accept()
