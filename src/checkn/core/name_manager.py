"""
Shared registry/dispatch base for NameLab and NameDomain.
"""

import abc
from pathlib import Path
from typing import Any, ClassVar

from checkn.utils.discovery import discover_classes


class NameManager(abc.ABC):
    """
    Abstract base defining the registry and dispatch functionality shared by
    NameLab and NameDomain: discovering registrable classes in a directory,
    listing their titles, and executing them by title.

    Each concrete subclass (e.g. ShellLab, ShellDomain) represents exactly
    one fixed title, so instances are cached per-class -- constructing a
    subclass more than once returns the same, already-discovered instance.
    """

    _instances: ClassVar[dict[type, "NameManager"]] = {}
    _file_suffix: ClassVar[str]
    _item_base_class: ClassVar[type]

    def __new__(cls, *args: Any, **kwargs: Any) -> "NameManager":
        """
        Return the cached singleton instance for this concrete class.
        """
        if cls not in NameManager._instances:
            NameManager._instances[cls] = super().__new__(cls)
        return NameManager._instances[cls]

    def __init__(self, title: str, path: Path, package_prefix: str) -> None:
        """
        Discover and register items, unless this cached instance already has been.
        Side-effects: filesystem read (via discovery).
        """
        if getattr(self, "_initialized", False):
            return
        self._title = title
        self._path = path
        self._package_prefix = package_prefix
        self._registry = self._discover()
        self._initialized = True

    @property
    def title(self) -> str:
        """
        Retrieve this manager's title.
        """
        return self._title

    def _discover(self) -> dict[str, Any]:
        """
        Discover, instantiate, and register items keyed by their title.
        Side-effects: filesystem read.
        """
        classes = discover_classes(
            self._path, self._package_prefix, self._item_base_class, self._file_suffix
        )
        items = [self._instantiate(cls) for cls in classes]
        return {item.title: item for item in items}

    @abc.abstractmethod
    def _instantiate(self, item_class: type) -> Any:
        """
        Construct a registered item from a discovered class.
        """

    def list(self) -> list[str]:
        """
        Retrieve the titles of all registered items.
        """
        return list(self._registry.keys())

    def execute(self, title: str, name: str) -> str:
        """
        Run the item matching title against name.
        """
        return self._registry[title].run(name)

    def execute_all(self, name: str) -> dict[str, str]:
        """
        Run every registered item against name.
        """
        return {title: item.run(name) for title, item in self._registry.items()}
