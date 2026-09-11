"""
NameLab for the apt domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class AptLab(NameLab):
    """
    Registers the apt domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover apt NameProbes.
        """
        super().__init__(
            title="apt",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.apt.probes",
        )
