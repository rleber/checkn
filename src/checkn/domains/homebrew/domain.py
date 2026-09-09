"""
NameDomain for Homebrew-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.homebrew.lab import HomebrewLab


class HomebrewDomain(NameDomain):
    """
    Registers the Homebrew domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover Homebrew NameAnalyses, backed by the Homebrew NameLab.
        """
        super().__init__(
            title="homebrew",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.homebrew.analyses",
            lab=HomebrewLab(),
        )
