"""
Python standard-library module membership probe.
"""

import sys

from checkn.core.name_probe import NameProbe


class StandardModuleProbe(NameProbe):
    """
    Checks whether the target name is a standard-library module.
    """

    title = "standard module"

    def _perform(self, name: str) -> str:
        """
        Test membership in sys.stdlib_module_names.
        """
        return name if name in sys.stdlib_module_names else ""
