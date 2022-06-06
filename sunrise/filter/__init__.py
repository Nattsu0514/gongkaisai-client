import abc
from dataclasses import dataclass
from typing import Set, Callable, Union, Pattern, Dict, AnyStr, Type

from sunrise import env

proxy_startup_set: Set[Callable] = set()
proxy_shutdown_set: Set[Callable] = set()


@dataclass
class MetaRule(metaclass=abc.ABCMeta):
    pattern: Union[str, Pattern[AnyStr]]
    respond: Union[str, int]
    priority: int = 0


class MetaFilter(metaclass=abc.ABCMeta):
    host: str = env.FILTER_HOST
    port: int = env.FILTER_PORT
    Rules: Dict[str, Type[MetaRule]] = {}

    @abc.abstractmethod
    def startup(self):
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
