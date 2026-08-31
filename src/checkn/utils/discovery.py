"""
Dynamic module discovery utilities.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path


def discover_classes(
    directory: Path, package_prefix: str, base_class: type, suffix: str
) -> list[type]:
    """
    Discover, sort, and return classes subclassing base_class from modules in
    directory whose names end with suffix.
    """
    discovered: list[type] = []

    if not directory.exists() or not directory.is_dir():
        return discovered

    for _, module_name, _ in pkgutil.iter_modules([str(directory)]):
        if not module_name.endswith(suffix):
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
