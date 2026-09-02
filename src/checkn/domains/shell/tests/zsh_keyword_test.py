"""
Zsh reserved keyword enumeration probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.shell import run_command


class ZshKeywordTest(CacheableNameTest):
    """
    Fetches every reserved keyword in zsh.
    """

    title = "zsh keyword"
    domain = "shell"

    def _fetch_all(self) -> list[str]:
        """
        List all zsh reserved words via the `zsh/parameter` module.
        Side-effects: subprocess execution.
        """
        result = run_command(
            ["zsh", "-c", "zmodload zsh/parameter; print -l ${(k)reswords}"]
        )
        return result.stdout.splitlines()
