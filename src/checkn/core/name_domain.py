"""
NameDomain: a registry of NameAnalysis objects discovered from a directory,
backed by a NameLab.
"""

from pathlib import Path

from checkn.core.name_analysis import NameAnalysis
from checkn.core.name_lab import NameLab
from checkn.core.name_manager import NameManager


class NameDomain(NameManager):
    """
    Discovers and dispatches NameAnalysis classes defined in files matching
    "xxx_analysis.py" within its directory, giving each one access to this
    domain's NameLab.
    """

    _file_suffix = "_analysis"
    _item_base_class = NameAnalysis

    def __init__(self, title: str, path: Path, package_prefix: str, lab: NameLab) -> None:
        """
        Store the NameLab before discovery, since analyses are constructed with it.
        Side-effects: filesystem read (via discovery).
        """
        if getattr(self, "_initialized", False):
            return
        self._lab = lab
        super().__init__(title, path, package_prefix)

    @property
    def lab(self) -> NameLab:
        """
        Retrieve this domain's NameLab.
        """
        return self._lab

    def _instantiate(self, item_class: type[NameAnalysis]) -> NameAnalysis:
        """
        Construct a NameAnalysis instance bound to this domain's NameLab.
        """
        return item_class(self._lab)
