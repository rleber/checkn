"""
NameLab for the Python domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class PythonLab(NameLab):
    """
    Registers the Python domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover Python NameProbes.
        """
        super().__init__(
            title="python",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.python.probes",
        )
