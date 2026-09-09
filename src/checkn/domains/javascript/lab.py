"""
NameLab for the JavaScript domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class JavaScriptLab(NameLab):
    """
    Registers the JavaScript domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover JavaScript NameProbes.
        """
        super().__init__(
            title="javascript",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.javascript.probes",
        )
