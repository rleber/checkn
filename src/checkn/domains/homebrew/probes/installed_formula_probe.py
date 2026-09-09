"""
Installed Homebrew formula membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class InstalledFormulaProbe(CacheableNameProbe):
    """
    Checks whether the target name is a Homebrew formula installed on this
    system.
    """

    title = "installed formula"
    domain = "homebrew"

    def _fetch_all(self) -> list[str]:
        """
        List every installed formula via `brew list --formula`.
        Side-effects: subprocess execution.
        """
        result = run_command(["brew", "list", "--formula"])
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
