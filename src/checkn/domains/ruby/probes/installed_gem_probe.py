"""
Installed Ruby gem membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class InstalledGemProbe(CacheableNameProbe):
    """
    Checks whether the target name is a gem installed on this system.
    """

    title = "installed gem"
    domain = "ruby"

    def _fetch_all(self) -> list[str]:
        """
        List every gem installed locally, via RubyGems' own specification
        index. Side-effects: subprocess execution.
        """
        result = run_command(["ruby", "-e", "puts Gem::Specification.map(&:name).uniq"])
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
