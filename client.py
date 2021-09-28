import asyncio
import importlib
import os
import pkgutil
import sys
from typing import Optional, Type

from PyQt5.QtWidgets import QApplication
from quamash import QEventLoop

import hook
import server
from engines import Engine
from mainwindow import MainWindow
from options import ClearCache

_main: Optional[MainWindow] = None
_engine: Optional[Engine] = None

_http_server = server.Http("127.0.0.1", 8000)

clear_cache = ClearCache()


def get_engine():
    if _engine is None:
        raise ValueError

    return _engine


def apply_engine(engine_module) -> Type[Engine]:
    if _main is None:
        raise ValueError

    module = importlib.import_module(engine_module)
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
    # _class(_main)


def run():
    global _proxy_server, _http_server

    for path_finder, name, __ in pkgutil.iter_modules([os.path.relpath("plugins", os.getcwd())]):
        print(name)
        path_finder.find_module(f"plugins.{name}").load_module(f"plugins.{name}")

    _main.show()
    _http_server = server.Http("127.0.0.1", 8000)
    _http_server.start()

    _proxy_server = server.Proxy("127.0.0.1", 8099)
    _proxy_server.run()

    # app.exec_()
    os._exit(0)
