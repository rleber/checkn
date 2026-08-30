"""
Dynamic module discovery utilities.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path

from checkn.contexts.base_check import BaseCheck


def load_checks(
    checks_dir: Path, package_prefix: str, base_class: type[BaseCheck] = BaseCheck
) -> list[type[BaseCheck]]:
    """
    Discover, sort, and return check classes from a target directory.
    Side-effects: filesystem read.
    """
    discovered: list[type[BaseCheck]] = []

    if not checks_dir.exists() or not checks_dir.is_dir():
        return discovered

    for _, module_name, _ in pkgutil.iter_modules([str(checks_dir)]):
        if module_name.startswith("base_"):
            continue

        full_module_name = f"{package_prefix}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
        except ImportError:
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, base_class)
                and obj is not base_class
                and obj.__module__ == full_module_name
            ):
                discovered.append(obj)

    discovered.sort(key=lambda c: c.priority)
    return discovered
