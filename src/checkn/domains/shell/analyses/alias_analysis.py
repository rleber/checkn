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
        Inspect the cached interactive `type -aw` result for an alias marker.
        """
        result = self.lab.execute("type -aw interactive", name)
        if f"{name}: alias" in result:
            return "alias"
        return ""
