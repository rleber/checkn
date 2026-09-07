"""
Python import-name membership probe.
"""

import pkgutil

from checkn.core.name_probe import NameProbe


class ImportNameProbe(NameProbe):
    """
    Checks whether the target name is an importable module on sys.path.
    """

    title = "import name"

    def _perform(self, name: str) -> str:
        """
        Test membership among modules discoverable via pkgutil.
        """
        importable = [module.name for module in pkgutil.iter_modules()]
        return name if name in importable else ""
