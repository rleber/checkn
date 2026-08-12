#!/usr/bin/env python3

# Check how a name is defined in common Python usage (if at all)

import builtins
import inspect

# TODO Change result of type checking functions to structured data


class PythonDefinition:
    classes_cache = None

    @classmethod
    def builtin_classes(cls) -> list[str]:
        global classes_cache

        if classes_cache is None:
            classes_cache = [
                name for name, _ in inspect.getmembers(builtins, inspect.isclass)
            ]
        return classes_cache

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_builtin_class(self):
        return self.name in self.builtin_classes()

    @property
    def basic_type(self):
        if self.is_builtin_class:
            return "builtin class"
        else:
            return "Unknown"
        # builtin Python class
        # builtin Python module
        # Python stdlib module: Avoid this, antigravity
        # Python installed module
        # other Python module
        # not a Python module

        # class defined in an installed Python module: Disable stdout
        #   Use pkgutil.py pkgutil.iter_importers
        # method defined in an installed Python module

    @property
    def installer(self):
        # e.g. pip, uv, None
        pass
