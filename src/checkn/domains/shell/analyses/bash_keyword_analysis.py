"""
Bash keyword definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class BashKeywordAnalysis(NameAnalysis):
    """
    Determines if the target name is a reserved bash keyword.
    """

    title = "bash keyword"
    priority = 20

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached bash `type` result for a keyword marker.
        """
        result = self.lab.execute("bash type", name)
        if "keyword" in result:
            return "bash keyword"
        return ""
