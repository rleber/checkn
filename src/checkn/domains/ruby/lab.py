"""
NameLab for the Ruby domain.
"""

from pathlib import Path

from checkn.core.name_lab import NameLab


class RubyLab(NameLab):
    """
    Registers the Ruby domain's NameProbe classes.
    """

    def __init__(self) -> None:
        """
        Discover Ruby NameProbes.
        """
        super().__init__(
            title="ruby",
            path=Path(__file__).parent / "probes",
            package_prefix="checkn.domains.ruby.probes",
        )
