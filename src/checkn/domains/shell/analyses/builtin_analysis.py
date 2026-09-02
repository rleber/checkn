"""
Builtin command definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class BuiltinAnalysis(NameAnalysis):
    """
    Determines if the target name is a shell builtin command.
    """

    title = "builtin"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached builtin list.
        """
        return "builtin" if self.lab.execute("builtin", name) else ""
