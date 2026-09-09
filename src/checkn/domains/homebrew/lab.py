"""
NameLab for the Homebrew domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class HomebrewLab(NameLab):
    """
    Registers the Homebrew domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover Homebrew NameProbes.
        """
        super().__init__(
            title="homebrew",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.homebrew.probes",
        )
