"""
Base interface for dynamically loaded NameProbe classes.

A NameProbe performs one raw, cacheable probe of a name (e.g. running
`type -aw <name>` in a shell) and returns the result as a string. It does
not interpret the result -- that is the job of a NameAnalysis. By
convention, an empty string means "no match"; any non-empty string means
"matched" (and may also carry raw diagnostic output an analysis needs).
"""

import abc

from checkn.utils import os_support


class NameProbe(abc.ABC):
    """
    Abstract base for dynamic, per-name-cached probes.
    """

    title: str

    # Set to os_support.LINUX/MACOS/WINDOWS on a subclass that only makes
    # sense on one OS. None (the default) means "no restriction".
    required_os: str | None = None

    def __init__(self) -> None:
        """
        Initialize the per-name result cache.
        """
        self._cache: dict[str, str] = {}

    def run(self, name: str) -> str:
        """
        Return the (possibly cached) result of testing name, or "" without
        running the probe at all if required_os isn't met. Silent (no
        stderr message) because this runs once per name checked, not once
        per reload -- CacheableNameProbe.reload() is where an OS mismatch
        gets a one-time, informative message instead.
        """
        if not os_support.is_supported(self.required_os):
            return ""
        if name not in self._cache:
            self._cache[name] = self._perform(name)
        return self._cache[name]

    @abc.abstractmethod
    def _perform(self, name: str) -> str:
        """
        Perform the underlying probe and return its result.
        """
