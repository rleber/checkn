"""
Installed Homebrew cask membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class InstalledCaskProbe(CacheableNameProbe):
    """
    Checks whether the target name is a Homebrew cask installed on this
    system.
    """

    title = "installed cask"
    domain = "homebrew"

    def _fetch_all(self) -> list[str]:
        """
        List every installed cask via `brew list --cask`.
        Side-effects: subprocess execution.
        """
        result = run_command(["brew", "list", "--cask"])
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
