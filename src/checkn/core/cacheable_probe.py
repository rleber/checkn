"""
Base interface for NameProbe classes backed by a persistent, bulk-loaded cache.
"""

import abc
import sys

import requests

from checkn.cache import CacheDB
from checkn.core.name_probe import NameProbe
from checkn.utils import os_support


class CacheableNameProbe(NameProbe):
    """
    A NameProbe whose full result set is fetched and cached in bulk, rather
    than probed one name at a time. Subclasses declare `domain` (their
    owning NameDomain's title) and implement `_fetch_all`; lazy reload-when-
    empty and cache lookups are handled here.
    """

    domain: str

    def _perform(self, name: str) -> str:
        """
        Reload the cache if this probe's section has never been loaded, then
        look name up in it.
        """
        cache = CacheDB()
        if not cache.is_loaded(self.domain, self.title):
            self.reload(cache)
        return (
            name
            if cache.contains(self.domain, self.title, self._cache_key(name))
            else ""
        )

    def _cache_key(self, name: str) -> str:
        """
        Normalize name into the form used as a cache lookup key. Override
        when the fetched name set uses a different convention than the raw
        input (e.g. case conversion).
        """
        return name

    def reload(self, cache: CacheDB | None = None) -> bool | None:
        """
        Fetch the full name set and replace this probe's cached section with
        it. Returns True on success.

        Returns None, without attempting the fetch at all, if this probe's
        required_os isn't met on the current system -- e.g. an `apt`-backed
        probe running on macOS. That's expected and not a failure: it warns
        on stderr with its own distinct wording, records itself as "not
        applicable" (see CacheDB.mark_not_applicable) rather than failed,
        and leaves any existing cached section untouched. Callers should
        not count a None return towards a failure count.

        Also returns None, without touching the existing cached section,
        if the fetch failed because the network was unreachable (a
        requests.exceptions.ConnectionError or Timeout -- e.g. no internet
        access). Like an OS mismatch, that's not a code problem to
        investigate: it's recorded as "network unavailable" (see
        CacheDB.mark_network_unavailable), distinct in `checkn-cache
        status` from a genuine failure, and doesn't count towards a
        failure count. No retry is attempted here -- if the network is
        down, the next scheduled reload should simply try again on its own
        schedule, not loop retrying within this one.

        Returns False if the probe *did* attempt the fetch but it came back
        empty, or _fetch_all() raised anything else (e.g. a malformed
        response or a non-connectivity HTTP error). Every probe expects a
        real, non-trivial result set, so an empty fetch almost certainly
        means the underlying fetch failed rather than genuinely finding
        nothing -- in either case, warn on stderr and leave the existing
        cached section untouched (stale-but-correct beats silently wiping
        out a good cache, or one probe's error aborting every other
        probe's reload) rather than replacing it or raising.
        """
        cache = cache or CacheDB()

        if not os_support.is_supported(self.required_os):
            reason = (
                f"requires {self.required_os}, this system is {os_support.current_os()}"
            )
            print(
                f"not applicable: {self.domain}: {self.title} ({reason}) -- skipping",
                file=sys.stderr,
            )
            cache.mark_not_applicable(self.domain, self.title, reason)
            return None

        try:
            names = self._fetch_all()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as exc:
            print(
                f"network unavailable: {self.domain}: {self.title} ({exc}) -- "
                "leaving existing cache section unchanged",
                file=sys.stderr,
            )
            cache.mark_network_unavailable(self.domain, self.title, str(exc))
            return None
        except Exception as exc:  # noqa: BLE001 -- one probe's bug must not abort every other probe's reload
            print(
                f"warning: {self.domain}: {self.title} raised {exc!r} while fetching -- "
                "leaving existing cache section unchanged",
                file=sys.stderr,
            )
            cache.mark_failed(self.domain, self.title)
            return False

        if not names:
            print(
                f"warning: {self.domain}: {self.title} fetched 0 entries "
                "(likely a failed fetch, not a genuinely empty result) -- "
                "leaving existing cache section unchanged",
                file=sys.stderr,
            )
            cache.mark_failed(self.domain, self.title)
            return False
        cache.replace_name_set(self.domain, self.title, names)
        return True

    @abc.abstractmethod
    def _fetch_all(self) -> list[str]:
        """
        Fetch the full set of names this probe should recognize.
        """
