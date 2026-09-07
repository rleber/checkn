"""
NameLab for the Git domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class GitLab(NameLab):
    """
    Registers the Git domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover Git NameProbes.
        """
        super().__init__(
            title="git",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.git.probes",
        )
