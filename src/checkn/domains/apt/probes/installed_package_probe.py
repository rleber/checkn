"""
Installed apt package membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils import os_support
from checkn.utils.shell import run_command


class InstalledPackageProbe(CacheableNameProbe):
    """
    Checks whether the target name is an apt/dpkg package installed on
    this system.

    Linux-only: dpkg itself doesn't exist elsewhere, so this declares
    required_os rather than letting `dpkg-query` fail as a missing command.
    """

    title = "installed package"
    domain = "apt"
    required_os = os_support.LINUX

    def _fetch_all(self) -> list[str]:
        """
        List every installed package via `dpkg-query`, which reports only
        packages actually present on this system (unlike
        `dpkg --get-selections`, which also lists packages marked for
        removal). Side-effects: subprocess execution.
        """
        result = run_command(["dpkg-query", "-W", "-f=${Package}\n"])
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
