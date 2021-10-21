import asyncio
import importlib
import os
import pkgutil
import sys
from typing import Optional, Type

from PyQt5.QtWidgets import QApplication
from quamash import QEventLoop

from sunrise import hook, server
from sunrise.engines import Engine
from sunrise.mainwindow import MainWindow
from sunrise.manager import PluginLoader
from sunrise.options import clear_cache

_main: Optional[MainWindow] = None
_engine: Optional[Engine] = None

_http_server = server.Http("127.0.0.1", 8000)


def get_engine():
    if _engine is None:
        raise ValueError

    return _engine


def apply_engine(engine_module) -> Type[Engine]:
    if _main is None:
        raise ValueError

    module = importlib.import_module(f"sunrise.{engine_module}")
    engine = getattr(module, "Engine")

    if _engine is None:
        return engine(_main)
    # else:
    # _engine.close()


@hook.main_window_instantiate
def run_server():
    clear_cache.start()


@hook.main_window_shutdown
def shutdown_server():
    _proxy_server.terminate()
    _http_server.terminate()
    _http_server.wait()


def init(engine_module: Optional[str] = None):
    global _main, _engine
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    _main = MainWindow("公开赛测试")
    _engine = apply_engine(engine_module)
    plugin_loader = PluginLoader()
    plugin_loader.load_plugin("plugins")


def run():
    global _proxy_server, _http_server

    _main.show()
    _http_server = server.Http("127.0.0.1", 8000)
    _http_server.start()

    _proxy_server = server.Proxy("127.0.0.1", 8099)
    _proxy_server.run()

    # app.exec_()
    os._exit(0)
