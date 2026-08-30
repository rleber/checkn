"""
Dynamic shell context evaluator.
"""

from pathlib import Path

from checkn.contexts.base_check import BaseCheck, BaseContext
from checkn.utils.discovery import load_checks


class ShellContext(BaseContext):
    """
    Evaluates shell-specific definitions using dynamically loaded check modules.
    """

    _registry: list[type[BaseCheck]] | None = None

    def __init__(self, name: str) -> None:
        """
        Initialize shell context.
        """
        super().__init__(name)
        self._checks = self._load_checks()

    @classmethod
    def _load_checks(cls) -> list[type[BaseCheck]]:
        """
        Retrieve cached or newly discovered shell checks.
        """
        if cls._registry is not None:
            return cls._registry

        checks_dir = Path(__file__).parent / "shell" / "checks"
        package_prefix = "checkn.contexts.shell.checks"
        cls._registry = load_checks(checks_dir, package_prefix)
        return cls._registry

    @property
    def info(self) -> BaseContext.Definition:
        """
        Execute registered checks to determine shell definition.
        """
        definition_type = None

        for check_class in self._checks:
            result = check_class().evaluate(self.name)
            if result:
                definition_type = result
                break

        return BaseContext.Definition("shell", self.name, definition_type, {})
