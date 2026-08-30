"""
Zsh keyword definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import run_command


class ZshKeywordCheck(BaseCheck):
    """
    Evaluates if the target name is a reserved zsh keyword.
    """

    priority = 10

    def evaluate(self, name: str) -> str | None:
        """
        Check keyword status via zsh syntax parsing.
        """
        result = run_command(["zsh", "-n", "-c", name])
        if result.returncode != 0:
            return "zsh keyword"
        return None
