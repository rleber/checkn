"""
Base interface for NameTest classes backed by a persistent, bulk-loaded cache.
"""

import abc

from checkn.cache import CacheDB
from checkn.core.name_test import NameTest


class CacheableNameTest(NameTest):
    """
    A NameTest whose full result set is fetched and cached in bulk, rather
    than probed one name at a time. Subclasses declare `domain` (their
    owning NameDomain's title) and implement `_fetch_all`; lazy reload-when-
    empty and cache lookups are handled here.
    """

    domain: str

    def _perform(self, name: str) -> str:
        """
        Reload the cache if this test's section has never been loaded, then
        look name up in it.
        """
        cache = CacheDB()
        if not cache.is_loaded(self.domain, self.title):
            self.reload(cache)
        return name if cache.contains(self.domain, self.title, self._cache_key(name)) else ""

    def _cache_key(self, name: str) -> str:
        """
        Normalize name into the form used as a cache lookup key. Override
        when the fetched name set uses a different convention than the raw
        input (e.g. case conversion).
        """
        return name

    def reload(self, cache: CacheDB | None = None) -> None:
        """
        Fetch the full name set and replace this test's cached section with it.
        """
        cache = cache or CacheDB()
        cache.replace_name_set(self.domain, self.title, self._fetch_all())

    @abc.abstractmethod
    def _fetch_all(self) -> list[str]:
        """
        Fetch the full set of names this test should recognize.
        """
