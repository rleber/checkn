"""
NameLab for the shell domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class ShellLab(NameLab):
    """
    Registers the shell domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover shell NameProbes.
        """
        super().__init__(
            title="shell",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.shell.probes",
        )
