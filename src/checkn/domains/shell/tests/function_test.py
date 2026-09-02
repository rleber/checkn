"""
Shell function enumeration probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.shell import run_command


class FunctionTest(CacheableNameTest):
    """
    Fetches every function currently defined in an interactive login zsh.
    """

    title = "function"
    domain = "shell"

    def _fetch_all(self) -> list[str]:
        """
        List all shell functions via the zsh `functions` associative array.
        Side-effects: subprocess execution.
        """
        result = run_command(["zsh", "-lic", "print -l ${(ok)functions}"])
        return [line for line in result.stdout.splitlines() if line]
