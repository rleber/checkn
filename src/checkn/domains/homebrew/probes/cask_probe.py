"""
Published Homebrew cask membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.domains.homebrew.api_cache import CASK_NAMES_PATH, read_names


class CaskProbe(CacheableNameProbe):
    """
    Checks whether the target name is a cask known to Homebrew, whether or
    not it's installed.
    """

    title = "cask"
    domain = "homebrew"

    def _fetch_all(self) -> list[str]:
        """
        Read every known cask name from Homebrew's own local API cache
        (kept fresh by the user's `brew update`), rather than querying the
        network ourselves. See api_cache.py for why this is undocumented
        and how a missing/malformed cache is handled.
        """
        return read_names(CASK_NAMES_PATH, "cask")
