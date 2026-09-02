"""
Shell alias definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class AliasAnalysis(NameAnalysis):
    """
    Determines if the target name is a shell alias.
    """

    title = "alias"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached alias list.
        """
        return "alias" if self.lab.execute("alias", name) else ""
