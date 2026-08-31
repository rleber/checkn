"""
NameDomain for Git-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.git.lab import GitLab


class GitDomain(NameDomain):
    """
    Registers the Git domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover Git NameAnalyses, backed by the Git NameLab.
        """
        super().__init__(
            title="git",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.git.analyses",
            lab=GitLab(),
        )
