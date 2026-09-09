"""
Ruby name classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class TypeAnalysis(NameAnalysis):
    """
    Classifies a name by its most specific role in common Ruby usage.
    """

    title = "type"

    def _analyze(self, name: str) -> str:
        """
        Apply the Ruby classification precedence chain to the cached test results.

        Builtin class and installed gem are both local checks, so both are
        tried before gem's rubygems.org network request -- which only needs
        to run at all when neither of those already answered the question.
        """
        lab = self.lab

        if lab.execute("keyword", name):
            return "keyword"
        if lab.execute("builtin class", name):
            return "builtin class"
        if lab.execute("installed gem", name):
            return "installed gem"
        if lab.execute("gem", name):
            return "uninstalled gem"
        return ""
