import importlib
import importlib.util
import os
import pkgutil

from typing import Sequence


class BaseModuleManager:
    def get_modules(self, module_dir):
        return [f"{module_dir}.{name}"
                for path_finder, name, __ in pkgutil.iter_modules([os.path.relpath(module_dir, os.getcwd())])]

    def load_module(self, module_name):
        if importlib.util.find_spec(module_name):
            return importlib.import_module(module_name)


class PluginManager(BaseModuleManager):
    def __init__(self):
        self.load_basic_plugins()

    def load_plugin(self, module_name):
        try:
            self.load_module(module_name)
        except Exception:

            return

    def load_plugins(self, module_name: Sequence[str]):
        for i in module_name:
            self.load_plugin(i)

    def load_all_plugin(self, module_dir):
        module_list = self.get_modules(module_dir)
        for i in module_list:
            self.load_plugin(i)

    def load_basic_plugins(self):
        return self.load_plugin("sunrise.basic_plugins")


