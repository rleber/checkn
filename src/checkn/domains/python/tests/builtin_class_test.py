"""
Python builtin class membership probe.
"""

import builtins
import inspect

from checkn.core.name_test import NameTest


class BuiltinClassTest(NameTest):
    """
    Checks whether the target name is a Python builtin class.
    """

    title = "builtin class"

    def _perform(self, name: str) -> str:
        """
        Test membership in the classes defined by the builtins module.
        """
        classes = [cls_name for cls_name, _ in inspect.getmembers(builtins, inspect.isclass)]
        return name if name in classes else ""
