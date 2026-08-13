#!/usr/bin/env python3
"""
python_definition.py

Check how a name is defined in common Python usage (if at all)
"""

import builtins
import inspect
import pkgutil
import sys
from importlib import metadata

# TODO Change result of type checking functions to structured data


"""
TODO Possible future development:

It is possible to retrieve the names of classes (or other objects)
defined in a importable module, using pkgutil
"""


class PythonDefinition:
    @classmethod
    def builtin_classes(cls) -> list[str]:
        classes = [name for name, _ in inspect.getmembers(builtins, inspect.isclass)]
        return classes

    @classmethod
    def builtin_modules(cls) -> list[str]:
        return list(sys.builtin_module_names)

    @classmethod
    def standard_modules(cls) -> list[str]:
        return list(sys.stdlib_module_names)

    @classmethod
    def installed_modules(cls) -> list[str]:
        installed_list = [pkg.metadata["Name"] for pkg in metadata.distributions()]
        return installed_list

    @classmethod
    def installed_modules_with_unknown_installer(cls) -> list[str]:
        installed_list = cls.installed_modules()
        unknowns = []
        for module in installed_list:
            defn = cls(module)
            if not defn.installer or defn.installer == "unknown":
                unknowns.append(module)
        return unknowns

    @classmethod
    def installable_modules(cls) -> list[str]:
        installable_list = [module.name for module in pkgutil.iter_modules()]
        return installable_list

    @classmethod
    def all_modules(cls) -> list[str]:
        return list(
            set(cls.installable_modules())
            + set(cls.installed_modules())
            + set(cls.standard_modules())
        )

    @classmethod
    def uninstalled_modules(cls) -> list[str]:
        installable = set(cls.installable_modules())
        installed = set(cls.installed_modules())
        uninstalled = installable - installed
        return list(uninstalled)

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
    def is_standard_module(self):
        return self.name in self.standard_modules()

    @property
    def is_installed_module(self):
        return self.name in self.installed_modules()

    @property
    def is_installable_module(self):
        return self.name in self.installable_modules()

    @property
    def is_standard(self):
        return self.is_builtin or self.is_standard_module

    @property
    def is_available_module(self):
        return self.is_standard_module or self.is_installed_module

    @property
    def is_available(self):
        return self.is_available_module or self.is_builtin_class

    @property
    def is_builtin(self):
        return self.is_builtin_class or self.is_builtin_module

    @property
    def is_stdlib_module(self):
        return self.is_standard_module and not self.is_builtin_module

    @property
    def is_add_on_module(self):
        return self.is_installable_module and not self.is_stdlib_module

    @property
    def is_other_module(self):
        return self.is_installed_module and not self.is_known_module

    @property
    def is_known_module(self):
        return self.is_standard_module or self.is_installable_module

    @property
    def is_known(self):
        return self.is_builtin_class or self.is_known_module

    @property
    def is_module(self):
        return self.is_known_module or self.is_other_module

    @property
    def type(self):
        if self.is_builtin_class:
            return "builtin class"
        elif self.is_builtin_module:
            return "builtin module"
        elif self.is_stdlib_module:
            return "stdlib module"
        elif self.is_installed_module:
            return "installed module"
        elif self.is_installable_module:
            return "installable module"
        elif self.is_other_module:
            return "other module"
        else:
            return None

        # identifier defined in an defined Python module: Disable stdout
        #   Importing the packages this and antigravity have weird side-effects
        #   Use pkgutil.py pkgutil.iter_importers
        #   Distinguish between classes, methods, etc?

    @property
    def installer(self):
        try:
            installer = metadata.distribution(self.name).read_text("INSTALLER")
        except metadata.PackageNotFoundError:
            installer = None
        if installer:
            return installer.strip()
        elif self.is_installed_module:
            return "unknown"
        else:
            return None
