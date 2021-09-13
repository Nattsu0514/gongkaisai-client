from PyQt5.QtCore import QThread, QProcess


class ClearCache(QThread):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        process = QProcess()
        process.start("cmd", ["/c", "RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "8"])
        process.waitForStarted()
        process.waitForFinished()
