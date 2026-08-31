"""
NameLab for the Git domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class GitLab(NameLab):
    """
    Registers the Git domain's NameTest classes.
    """

    def __init__(self) -> None:
        """
        Discover Git NameTests.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="git",
            path=Path(__file__).parent / "tests",
            package_prefix="checkn.domains.git.tests",
        )
