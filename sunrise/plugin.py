from typing import Optional, Dict, Type

from PyQt5.QtWidgets import QAction, QMenu

from sunrise.bar import MainMenuBar
from sunrise.rule import RuleManager, Rule
from sunrise.util import ClearCache


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
            action = PluginAction(name, func, checkable=False)
            self.addAction(action)
            return action

        return warp

    def checkable_action(self, name: str):
        def warp(func):
            action = PluginAction(name, func, checkable=True)
            self.addAction(action)
            return action

        return warp

    def checkable_rule_action(self, name: str, rule):
        def warp(func):
            action = PluginAction(name, func, rule, checkable=True)
            self.addAction(action)
            return action

        return warp


class PluginAction(QAction):
    def __init__(self,
                 name: str,
                 plugin: Type,
                 rule: Optional[Rule] = None,
                 checkable: Optional[bool] = None):
        super().__init__(name)

        if checkable:
            self.setCheckable(checkable)
            self.plugin = plugin()
            self.triggered.connect(self.plugin)
        else:
            self.triggered.connect(plugin)

        if rule is not None:
            RuleManager().add(name, rule)
            self.plugin.name = name
            self.cache = ClearCache()
            self.triggered.connect(self.cache.start)


plugins_dict: Dict[str, PluginMenu] = dict()
