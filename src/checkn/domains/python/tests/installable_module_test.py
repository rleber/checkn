"""
Installable Python module membership probe.
"""

import pkgutil

from checkn.core.name_test import NameTest


class InstallableModuleTest(NameTest):
    """
    Checks whether the target name is an importable module on sys.path.
    """

    title = "installable module"

    def _perform(self, name: str) -> str:
        """
        Test membership among modules discoverable via pkgutil.
        """
        installable = [module.name for module in pkgutil.iter_modules()]
        return name if name in installable else ""
