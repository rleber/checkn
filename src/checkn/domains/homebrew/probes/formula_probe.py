"""
Published Homebrew formula membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.domains.homebrew.api_cache import FORMULA_NAMES_PATH, read_names


class FormulaProbe(CacheableNameProbe):
    """
    Checks whether the target name is a formula known to Homebrew, whether
    or not it's installed.
    """

    title = "formula"
    domain = "homebrew"

    def _fetch_all(self) -> list[str]:
        """
        Read every known formula name from Homebrew's own local API cache
        (kept fresh by the user's `brew update`), rather than querying the
        network ourselves. See api_cache.py for why this is undocumented
        and how a missing/malformed cache is handled.
        """
        return read_names(FORMULA_NAMES_PATH, "formula")
