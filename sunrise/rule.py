from dataclasses import dataclass
from typing import Union, Pattern, AnyStr, Dict

from sunrise import get_filter
from sunrise.util import Singleton


@dataclass
class Rule:
    pattern: Union[str, Pattern[AnyStr]]
    respond: Union[str, int]
    priority: int = 0


@Singleton
class RuleManager:

    def __init__(self):
        self._filter_rule = get_filter().Rules
        self._Rules: Dict[str, Rule] = dict()

    def add(self, name: str, rule, enable: bool = False):
        self._Rules.update({name: rule})
        if enable:
            self.enable_rule(name)

    def new_rule(self,
                 name: str,
                 pattern: Union[str, Pattern[str]],
                 respond: Union[str, int],
                 priority: int = 0,
                 enable: bool = False):

        rule = Rule(pattern, respond, priority)
        self.add(name, rule, enable)

    def get_status(self, name: str) -> bool:
        if self._Rules.get(name):
            return False
        elif self._filter_rule.get(name):
            return True
        else:
            raise ValueError

    def enable_rule(self, name: str):
        self._filter_rule.update({name: self._Rules.pop(name)})

    def disable_rule(self, name: str):
        self._Rules.update({name: self._filter_rule.pop(name)})

    def switch(self, name: str):
        if self.get_status(name):
            self.disable_rule(name)
        else:
            self.enable_rule(name)

    def get(self, name: str):
        value = self._Rules.get(name)
        if value is not None:
            return self._filter_rule.get(name)
        else:
            return value

    def remove(self, name: str):
        pass
