"""
Git repository existence analysis.
"""

from checkn.core.name_analysis import NameAnalysis


class RepositoryAnalysis(NameAnalysis):
    """
    Determines if the target name is a GitHub repository owned by the current user.
    """

    title = "repository"

    def _analyze(self, name: str) -> str:
        """
        Inspect the cached `git ls-remote` result.
        """
        if self.lab.execute("ls-remote", name):
            return "repository"
        return ""
