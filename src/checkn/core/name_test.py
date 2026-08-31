"""
Base interface for dynamically loaded NameTest classes.

A NameTest performs one raw, cacheable probe of a name (e.g. running
`type -aw <name>` in a shell) and returns the result as a string. It does
not interpret the result -- that is the job of a NameAnalysis. By
convention, an empty string means "no match"; any non-empty string means
"matched" (and may also carry raw diagnostic output an analysis needs).
"""

import abc


class NameTest(abc.ABC):
    """
    Abstract base for dynamic, per-name-cached probes.
    """

    title: str

    def __init__(self) -> None:
        """
        Initialize the per-name result cache.
        """
        self._cache: dict[str, str] = {}

    def run(self, name: str) -> str:
        """
        Return the (possibly cached) result of testing name.
        """
        if name not in self._cache:
            self._cache[name] = self._perform(name)
        return self._cache[name]

    @abc.abstractmethod
    def _perform(self, name: str) -> str:
        """
        Perform the underlying probe and return its result.
        """
