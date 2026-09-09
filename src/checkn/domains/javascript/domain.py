"""
NameDomain for JavaScript-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.javascript.lab import JavaScriptLab


class JavaScriptDomain(NameDomain):
    """
    Registers the JavaScript domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover JavaScript NameAnalyses, backed by the JavaScript NameLab.
        """
        super().__init__(
            title="javascript",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.javascript.analyses",
            lab=JavaScriptLab(),
        )
