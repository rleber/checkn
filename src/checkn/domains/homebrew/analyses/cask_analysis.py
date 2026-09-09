"""
Homebrew cask classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class CaskAnalysis(NameAnalysis):
    """
    Determines if the target name is a Homebrew cask, distinguishing
    installed from merely published.
    """

    title = "cask"

    def _analyze(self, name: str) -> str:
        """
        Prefer the local, installed check -- it doesn't need the published
        cask list at all, so it's tried first.
        """
        if self.lab.execute("installed cask", name):
            return "installed cask"
        if self.lab.execute("cask", name):
            return "uninstalled cask"
        return ""
