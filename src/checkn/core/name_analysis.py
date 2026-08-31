"""
Base interface for dynamically loaded NameAnalysis classes.

A NameAnalysis interprets one or more cached NameTest results (fetched
from its NameLab by test title) and returns a classification string for
a name. By convention, an empty string means "no match".
"""

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from checkn.core.name_lab import NameLab


class NameAnalysis(abc.ABC):
    """
    Abstract base for dynamic, per-name-cached analyses of NameTest results.
    """

    title: str

    def __init__(self, lab: "NameLab") -> None:
        """
        Initialize with the NameLab used to run underlying tests, and the per-name result cache.
        """
        self._lab = lab
        self._cache: dict[str, str] = {}

    @property
    def lab(self) -> "NameLab":
        """
        Retrieve the NameLab this analysis draws test results from.
        """
        return self._lab

    def run(self, name: str) -> str:
        """
        Return the (possibly cached) analysis result for name.
        """
        if name not in self._cache:
            self._cache[name] = self._analyze(name)
        return self._cache[name]

    @abc.abstractmethod
    def _analyze(self, name: str) -> str:
        """
        Analyze the relevant NameTest result(s) and return a classification.
        """
