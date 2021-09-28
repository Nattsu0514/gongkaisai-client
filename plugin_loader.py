from typing import Optional, Any

from PyQt5.QtWidgets import QAction, QMenu

from bar import MainMenuBar
from options import ClearCache
from server import Proxy


class PluginMenu(QMenu):
    actions: set = set()

    def __init__(self, title: str):
        self.menubar = MainMenuBar()
        super().__init__(title, self.menubar)
        self.menubar.addMenu(self)

    def button_action(self, name: str):
        def warp(func):
            action = PluginAction(name, func, checkable=False, auto_responder_rule=False)
            self.addAction(action)
            return action

        return warp

    def checkable_action(self, name: str):
        def warp(func):
            action = PluginAction(name, func, auto_responder_rule=False, checkable=True)
            self.addAction(action)
            return action

        return warp

    def checkable_rule_action(self, name: str):
        def warp(func):
            action = PluginAction(name, func, checkable=True)
            self.addAction(action)
            return action

        return warp


class PluginAction(QAction):
    def __init__(self,
                 name: str,
                 plugin: Any,
                 auto_responder_rule: bool = True,
                 checkable: Optional[bool] = None):
        super().__init__(name)
        if checkable:
            self.plugin = plugin()

            self.setCheckable(checkable)
            self.triggered.connect(self.plugin.switch)
        else:
            self.triggered.connect(plugin)

        if auto_responder_rule:
            Proxy.add_addon(self.plugin)
            self.cache = ClearCache()
            self.triggered.connect(self.cache.start)
