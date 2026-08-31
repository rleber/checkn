"""
Installed Python distribution membership probe.
"""

from importlib import metadata

from checkn.core.name_test import NameTest


class InstalledModuleTest(NameTest):
    """
    Checks whether the target name is an installed distribution.
    """

    title = "installed module"

    def _perform(self, name: str) -> str:
        """
        Test membership among installed distribution metadata names.
        """
        installed = [pkg.metadata["Name"] for pkg in metadata.distributions()]
        return name if name in installed else ""
