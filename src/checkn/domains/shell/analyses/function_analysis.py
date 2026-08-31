"""
Shell function definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class FunctionAnalysis(NameAnalysis):
    """
    Determines if the target name is a shell function.
    """

    title = "function"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached interactive `type -aw` result for a function marker.
        """
        result = self.lab.execute("type -aw interactive", name)
        if f"{name}: function" in result:
            return "function"
        return ""
