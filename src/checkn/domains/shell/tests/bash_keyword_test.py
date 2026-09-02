"""
Bash reserved keyword enumeration probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.shell import run_command


class BashKeywordTest(CacheableNameTest):
    """
    Fetches every reserved keyword in bash.
    """

    title = "bash keyword"
    domain = "shell"

    def _fetch_all(self) -> list[str]:
        """
        List all bash reserved keywords via `compgen -k`.
        Side-effects: subprocess execution.
        """
        result = run_command(["bash", "-c", "compgen -k"])
        return result.stdout.splitlines()
