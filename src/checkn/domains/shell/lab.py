"""
NameLab for the shell domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class ShellLab(NameLab):
    """
    Registers the shell domain's NameTest classes.
    """

    def __init__(self) -> None:
        """
        Discover shell NameTests.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="shell",
            path=Path(__file__).parent / "tests",
            package_prefix="checkn.domains.shell.tests",
        )
