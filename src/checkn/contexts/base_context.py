"""
Base interface for context evaluation classes.
"""

import abc
from typing import Any, NamedTuple


class BaseContext(abc.ABC):
    """
    Abstract base class for all context evaluators.
    """

    class Definition(NamedTuple):
        """
        Encapsulates metadata defining a matched resource.
        """

        context: str
        name: str
        definition: str | None
        details: dict[str, Any]

    def __init__(self, name: str) -> None:
        """
        Initialize the context with a target name.
        """
        self._name = name

    @property
    def name(self) -> str:
        """
        Retrieve the target name.
        """
        return self._name

    @property
    @abc.abstractmethod
    def info(self) -> Definition:
        """
        Retrieve the structured definition record for the target.
        """
