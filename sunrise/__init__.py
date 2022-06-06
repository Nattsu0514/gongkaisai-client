import importlib
import sys
from typing import Optional, Type

from PyQt5.QtWidgets import QApplication

from sunrise import hook
from sunrise.config import env
from sunrise.engines import Engine
from sunrise.filter import MetaFilter
from sunrise.mainwindow import MainWindow
from sunrise.manager import PluginManager
from sunrise.util import clear_cache

_main: Optional[MainWindow] = None
_engine: Optional[Engine] = None
_filter: Optional[MetaFilter] = None
pid: Optional[int] = None
plugin_manager: Optional[PluginManager] = None


def get_filter():
    if _filter is None:
        raise ValueError

    return _filter


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
    clear_cache.start()


@hook.main_window_close
def shutdown_server():
    _filter.shutdown()


def init():
    global _main, _engine, _filter, app, pid
    app = QApplication(sys.argv)
    _main = MainWindow("sunrise公开赛专属登录器正式版")
    _engine = set_engine(env.ENGINE_MODULE)
    pid = _main.pid
    _filter = getattr(importlib.import_module(env.FILTER_MODULE), "Filter")()
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugin("plugins")


def run():
    _main.show()
    _filter.startup()
    sys.exit(app.exec_())
