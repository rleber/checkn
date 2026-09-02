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
        Inspect the cached reserved-word list.
        """
        return "zsh keyword" if self.lab.execute("zsh keyword", name) else ""
