import abc

from typing import Set, Callable, Union, Pattern

proxy_startup_set: Set[Callable] = set()
proxy_shutdown_set: Set[Callable] = set()


class MetaFilter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass


class MetaRuleManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_rule(self, name: str, rule):
        pass

    @abc.abstractmethod
    def new_rule(self, name: str, pattern: Union[str, Pattern[str]], respond: Union[str, int]):
        pass

    @abc.abstractmethod
    def get(self, name: str):
        pass

    @abc.abstractmethod
    def remove(self, name: str):
        pass


