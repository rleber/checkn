"""
Zsh keyword definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class ZshKeywordAnalysis(NameAnalysis):
    """
    Determines if the target name is a reserved zsh keyword.
    """

    title = "zsh keyword"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached `type -aw` result for a reserved-word marker.
        """
        result = self.lab.execute("type -aw", name)
        if f"{name}: reserved" in result:
            return "zsh keyword"
        return ""
