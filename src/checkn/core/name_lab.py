"""
NameLab: a registry of NameTest objects discovered from a directory.
"""

from checkn.core.name_manager import NameManager
from checkn.core.name_test import NameTest


class NameLab(NameManager):
    """
    Discovers and dispatches NameTest classes defined in files matching
    "xxx_test.py" within its directory.
    """

    _file_suffix = "_test"
    _item_base_class = NameTest

    def _instantiate(self, item_class: type[NameTest]) -> NameTest:
        """
        Construct a NameTest instance.
        """
        return item_class()
