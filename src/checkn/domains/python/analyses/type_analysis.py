"""
Python name classification analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class TypeAnalysis(NameAnalysis):
    """
    Classifies a name by its most specific role in common Python usage.
    """

    title = "type"

    def _analyze(self, name: str) -> str:
        """
        Apply the Python classification precedence chain to the cached test results.
        """
        lab = self.lab

        if lab.execute("keyword", name):
            return "keyword"
        if lab.execute("builtin class", name):
            return "builtin class"
        if lab.execute("builtin module", name):
            return "builtin module"
        if lab.execute("standard module", name):
            return "stdlib module"
        if lab.execute("installed module", name):
            return "installed module"
        if lab.execute("import name", name):
            return "import name"
        if lab.execute("pypi module", name):
            return "uninstalled module"
        return ""
