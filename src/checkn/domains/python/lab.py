"""
NameLab for the Python domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class PythonLab(NameLab):
    """
    Registers the Python domain's NameTest classes.
    """

    def __init__(self) -> None:
        """
        Discover Python NameTests.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="python",
            path=Path(__file__).parent / "tests",
            package_prefix="checkn.domains.python.tests",
        )
