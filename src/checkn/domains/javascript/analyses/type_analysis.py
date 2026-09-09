"""
JavaScript name classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class TypeAnalysis(NameAnalysis):
    """
    Classifies a name by its most specific role in common JavaScript/Node
    usage. Mirrors the Python domain's precedence chain, minus two tiers
    that have no JavaScript equivalent: a standard-vs-builtin-module split
    (Node has one flat module list) and import-name-vs-package-name
    (require()/import always match the npm package name exactly).
    """

    title = "type"

    def _analyze(self, name: str) -> str:
        """
        Apply the JavaScript classification precedence chain to the cached
        (or, for npm module, live-queried) probe results.
        """
        lab = self.lab

        if lab.execute("keyword", name):
            return "keyword"
        if lab.execute("builtin class", name):
            return "builtin class"
        if lab.execute("builtin module", name):
            return "builtin module"
        if lab.execute("installed module", name):
            return "installed npm module"
        if lab.execute("npm module", name):
            return "uninstalled npm module"
        return ""
