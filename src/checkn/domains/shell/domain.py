"""
NameDomain for shell-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.shell.lab import ShellLab


class ShellDomain(NameDomain):
    """
    Registers the shell domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover shell NameAnalyses, backed by the shell NameLab.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="shell",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.shell.analyses",
            lab=ShellLab(),
        )
