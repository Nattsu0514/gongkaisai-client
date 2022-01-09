import asyncio
import importlib
import os
import sys
from typing import Optional, Type, Any

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from quamash import QEventLoop

from sunrise import hook, browser_proxy_setting
from sunrise.config import Env
from sunrise.engines import Engine
from sunrise.filter import mitmproxy
from sunrise.mainwindow import MainWindow
from sunrise.manager import PluginManager
from sunrise.util import clear_cache

_main: Optional[MainWindow] = None
_engine: Optional[Engine] = None
_proxy_server: Any = None
plugin_manager: Optional[PluginManager] = None


def get_engine():
    if _engine is None:
        raise ValueError

    return _engine


def set_engine(engine_module) -> Type[Engine]:
    if _main is None:
        raise ValueError

    module = importlib.import_module(engine_module)
    engine = getattr(module, "Engine")

    if _engine is None:
        return engine(_main)
    # else:
    # _engine.close()


@hook.main_window_instantiate
def init_server():
    browser_proxy_setting.set_proxy_settings("127.0.0.1", 8099)
    clear_cache.start(QThread.LowestPriority)


@hook.main_window_shutdown
def shutdown_server():
    browser_proxy_setting.set_proxy_settings("127.0.0.1", 8099, on=False)
    _proxy_server.shutdown()


def init():
    global _main, _engine, plugin_manager

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    plugin_manager = PluginManager()

    _main = MainWindow("sunrise公开赛专属登录器正式版")
    _engine = set_engine(Env().ENGINE_MODULE)


def run():
    global _proxy_server
    _main.show()

    _proxy_server = mitmproxy.Filter()
    _proxy_server.run()

    os._exit(0)
