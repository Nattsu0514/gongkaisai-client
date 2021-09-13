import importlib.machinery
import os
from typing import Optional, Any

from PyQt5.QtWidgets import QAction, QMenu, QMenuBar

from options import ClearCache
from server import Proxy


class PluginMenu(QMenu):
    actions: set = set()

    def __init__(self, menubar: QMenuBar):
        super().__init__('插件', menubar)
        menubar.addMenu(self)

        self.addActions(self.actions)

    @classmethod
    def add(cls, action: QAction):
        cls.actions.add(action)


class PluginAction(QAction):
    def __init__(self,
                 name: str,
                 plugin: Any,
                 auto_responder_rule: bool = True,
                 checkable: Optional[bool] = None):
        super().__init__(name)

        if checkable:
            if not callable(getattr(plugin, 'switch')):
                raise AttributeError
            self.cache = ClearCache()

            self.setCheckable(checkable)
            self.triggered.connect(plugin.switch)
            self.triggered.connect(self.cache.start)

        if auto_responder_rule:
            Proxy.add_addon(plugin)

        PluginMenu.add(self)


def checkable_action(name: str):
    def warp(func):
        return PluginAction(name, func, checkable=True)

    return warp


def load_plugins(plugins_path: str):
    for subdir, dirs, files in os.walk(plugins_path):
        for d in dirs:
            path = ''.join([plugins_path, d])
            loader = importlib.machinery.SourceFileLoader(d, path)
            loader.exec_module()
