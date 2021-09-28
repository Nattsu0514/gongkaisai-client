from PyQt5.QtCore import QThread, QProcess
from pycaw.utils import AudioUtilities


class ClearCache(QThread):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        print(0)
        process = QProcess()
        process.start("cmd", ["/c", "RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "8"])
        process.waitForStarted()
        process.waitForFinished()


def Singleton(cls):
    instance = {}

    def _singleton_wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _singleton_wrapper


def setMute(mute: bool):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "python.exe":
            volume.SetMasterVolume(1.0, None) if mute else volume.SetMasterVolume(0, None)
