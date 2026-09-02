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
        Inspect the cached function list.
        """
        return "function" if self.lab.execute("function", name) else ""
