"""
NameDomain for apt-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.apt.lab import AptLab


class AptDomain(NameDomain):
    """
    Registers the apt domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover apt NameAnalyses, backed by the apt NameLab.
        """
        super().__init__(
            title="apt",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.apt.analyses",
            lab=AptLab(),
        )
