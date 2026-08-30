"""
Base interface for all dynamically loaded context checks.
"""

import abc


class BaseCheck(abc.ABC):
    """
    Abstract base for dynamic checks defining evaluation contract and execution priority.
    """

    priority: int = 100

    @abc.abstractmethod
    def evaluate(self, name: str) -> str | None:
        """
        Evaluate the target name and return its type identifier if matched.
        """
