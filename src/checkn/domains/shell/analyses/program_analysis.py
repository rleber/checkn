"""
Executable program definition analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class ProgramAnalysis(NameAnalysis):
    """
    Determines if the target name is an executable program.
    """

    title = "program"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached `type -aw` result for a command marker that is not a builtin.
        """
        result = self.lab.execute("type -aw", name)
        if f"{name}: command" in result and f"{name}: builtin" not in result:
            return "program"
        return ""
