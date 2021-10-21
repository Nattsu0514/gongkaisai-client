import importlib, importlib.util
import os
import pkgutil


class PluginLoader:
    def __init__(self):
        print(self.load_basic_plugins())

    def get_plugins(self, module_dir):
        return [f"{module_dir}.{name}"
                for path_finder, name, __ in pkgutil.iter_modules(
                [os.path.relpath(module_dir, os.getcwd())])]

    def load_basic_plugins(self):
        return self.load_plugin("sunrise.basic_plugins")

    def load_plugin(self, module_name):
        _m = [importlib.import_module(name) for name in self.get_plugins(module_name)]

        if not _m:
            if importlib.util.find_spec(module_name):
                return importlib.import_module(module_name)
            # warning ...
        return _m
