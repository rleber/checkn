"""
Zsh keyword definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class ZshKeywordCheck(BaseCheck):
    """
    Evaluates if the target name is a reserved zsh keyword.
    """

    priority = 10

    def evaluate(self, name: str) -> str | None:
        """
        Check keyword status via zsh syntax parsing.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-c", f"type -aw {quoted_name}"])
        if result.returncode == 0 and f"{name}: reserved" in result.stdout:
            return "zsh keyword"
        return None
