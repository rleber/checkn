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

        Builtin class is checked before gem so that the rubygems.org network
        request is skipped whenever the name is already a known Ruby class.
        """
        lab = self.lab

        if lab.execute("keyword", name):
            return "keyword"
        if lab.execute("builtin class", name):
            return "builtin class"
        if lab.execute("gem", name):
            return "gem"
        return ""
