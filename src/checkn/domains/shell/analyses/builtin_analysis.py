"""
Builtin command definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class BuiltinAnalysis(NameAnalysis):
    """
    Determines if the target name is a shell builtin command.
    """

    title = "builtin"
    priority = 40

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached `type -aw` result for a builtin marker.
        """
        result = self.lab.execute("type -aw", name)
        if f"{name}: builtin" in result:
            return "builtin"
        return ""
