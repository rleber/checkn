"""
NameLab: a registry of NameProbe objects discovered from a directory.
"""

from checkn.core.name_manager import NameManager
from checkn.core.name_probe import NameProbe


class NameLab(NameManager):
    """
    Discovers and dispatches NameProbe classes defined in files matching
    "xxx_probe.py" within its directory.
    """

    _file_suffix = "_probe"
    _item_base_class = NameProbe

    def _instantiate(self, item_class: type[NameProbe]) -> NameProbe:
        """
        Construct a NameProbe instance.
        """
        return item_class()
