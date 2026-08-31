"""
NameDomain for Ruby-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.ruby.lab import RubyLab


class RubyDomain(NameDomain):
    """
    Registers the Ruby domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover Ruby NameAnalyses, backed by the Ruby NameLab.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="ruby",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.ruby.analyses",
            lab=RubyLab(),
        )
