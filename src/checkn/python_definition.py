#!/usr/bin/env python3

# Check how a name is defined in common Python usage (if at all)

import builtins
import importlib.metadata
import inspect
import pkgutil
import sys

# TODO Change result of type checking functions to structured data


class PythonDefinition:
    @classmethod
    def builtin_classes(cls) -> list[str]:
        classes = [name for name, _ in inspect.getmembers(builtins, inspect.isclass)]
        return classes

    @classmethod
    def builtin_modules(cls) -> list[str]:
        return list(sys.builtin_module_names)

    @classmethod
    def stdlib_modules(cls) -> list[str]:
        return list(sys.stdlib_module_names)

    @classmethod
    def installed_modules(cls) -> list[str]:
        installed_list = [
            pkg.metadata["Name"] for pkg in importlib.metadata.distributions()
        ]
        return installed_list

    @classmethod
    def add_on_modules(cls) -> list[str]:
        defined_list = [module.name for module in pkgutil.iter_modules()]
        return defined_list

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_builtin_class(self):
        return self.name in self.builtin_classes()

    @property
    def is_builtin_module(self):
        return self.name in self.builtin_modules()

    @property
    def is_stdlib_module(self):
        # List of standard library modules includes builtin modules
        if self.is_builtin_module:
            return False
        return self.name in self.stdlib_modules()

    @property
    def is_installed_module(self):
        return self.name in self.installed_modules()

    @property
    def is_add_on_module(self):
        return self.name in self.add_on_modules()

    @property
    def is_contributed_module(self):
        return self.is_add_on_module and not self.is_stdlib_module

    @property
    def is_defined_module(self):
        return self.is_builtin_module or self.is_add_on_module

    @property
    def is_other_module(self):
        return self.is_defined_module and not self.is_known_module

    @property
    def is_known_module(self):
        return (
            self.is_builtin_module or self.is_stdlib_module or self.is_installed_module
        )

    @property
    def is_module(self):
        return self.is_known_module or self.is_other_module

    @property
    def basic_type(self):
        if self.is_builtin_class:
            return "builtin class"
        elif self.is_builtin_module:
            return "builtin module"
        elif self.is_stdlib_module:
            return "stdlib module"
        elif self.is_installed_module:
            return "installed module"
        elif self.is_known_module:
            return "known module"
        elif self.is_defined_module:
            return "other module"
        else:
            return None
        # builtin Python class
        # builtin Python module
        # Python stdlib module: Avoid this, antigravity
        # Python installed module
        # other Python module
        # not a Python module

        # identifier defined in an installed Python module: Disable stdout
        #   Use pkgutil.py pkgutil.iter_importers
        #   Distinguish between classes, methods, etc?

    @property
    def installer(self):
        # e.g. pip, uv, None
        return None
