"""
NameDomain for Python-specific definitions.
"""

from pathlib import Path

from checkn.core.name_domain import NameDomain
from checkn.domains.python.lab import PythonLab


class PythonDomain(NameDomain):
    """
    Registers the Python domain's NameAnalysis classes.
    """

    def __init__(self) -> None:
        """
        Discover Python NameAnalyses, backed by the Python NameLab.
        Side-effects: filesystem read.
        """
        super().__init__(
            title="python",
            path=Path(__file__).parent / "analyses",
            package_prefix="checkn.domains.python.analyses",
            lab=PythonLab(),
        )
