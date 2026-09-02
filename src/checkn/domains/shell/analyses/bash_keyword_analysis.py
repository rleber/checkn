"""
Bash keyword definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class BashKeywordAnalysis(NameAnalysis):
    """
    Determines if the target name is a reserved bash keyword.
    """

    title = "bash keyword"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached bash keyword list.
        """
        return "bash keyword" if self.lab.execute("bash keyword", name) else ""
