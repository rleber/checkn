"""
Homebrew formula classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class FormulaAnalysis(NameAnalysis):
    """
    Determines if the target name is a Homebrew formula, distinguishing
    installed from merely published.
    """

    title = "formula"

    def _analyze(self, name: str) -> str:
        """
        Prefer the local, installed check -- it doesn't need the published
        formula list at all, so it's tried first.
        """
        if self.lab.execute("installed formula", name):
            return "installed formula"
        if self.lab.execute("formula", name):
            return "uninstalled formula"
        return ""
