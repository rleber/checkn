"""
Python builtin module membership probe.
"""

import sys

from checkn.core.name_test import NameTest


class BuiltinModuleTest(NameTest):
    """
    Checks whether the target name is a builtin (compiled-in) module.
    """

    title = "builtin module"

    def _perform(self, name: str) -> str:
        """
        Test membership in sys.builtin_module_names.
        """
        return name if name in sys.builtin_module_names else ""
