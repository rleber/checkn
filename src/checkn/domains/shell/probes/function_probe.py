"""
Shell function enumeration probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class FunctionProbe(CacheableNameProbe):
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
