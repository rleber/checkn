"""
Shell alias enumeration probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.shell import run_command


class AliasTest(CacheableNameTest):
    """
    Fetches every alias currently defined in an interactive login zsh.
    """

    title = "alias"
    domain = "shell"

    def _fetch_all(self) -> list[str]:
        """
        List all shell aliases via `alias`.
        Side-effects: subprocess execution.
        """
        result = run_command(["zsh", "-lic", "alias"])
        names = []
        for line in result.stdout.splitlines():
            if "=" not in line:
                continue
            names.append(line.split("=", 1)[0])
        return names
