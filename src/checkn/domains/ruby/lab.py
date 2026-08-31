"""
NameLab for the Ruby domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class RubyLab(NameLab):
    """
    Registers the Ruby domain's NameTest classes.
    """

    def __init__(self) -> None:
        """
        Discover Ruby NameTests.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="ruby",
            path=Path(__file__).parent / "tests",
            package_prefix="checkn.domains.ruby.tests",
        )
