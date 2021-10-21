from typing import Optional, Any, Dict, Set, Type

from PyQt5.QtWidgets import QAction, QMenu

from sunrise.bar import MainMenuBar
from sunrise.options import ClearCache
from sunrise.server import Proxy


class PluginMenu(QMenu):
    actions: set = set()

    def __new__(cls, title: str):
        if menu := plugins_dict.get(title):
            return menu
        else:
            return super().__new__(cls)
            #

    def __init__(self, title: str):
        if plugins_dict.get(title):
            return

        self.menubar = MainMenuBar()
        super().__init__(title, self.menubar)

        self.menubar.addMenu(self)
        plugins_dict[title] = self

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


plugins_dict: Dict[str, PluginMenu] = dict()
