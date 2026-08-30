"""
Bash keyword definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class BashKeywordCheck(BaseCheck):
    """
    Evaluates if the target name is a reserved bash keyword.
    """

    priority = 20

    def evaluate(self, name: str) -> str | None:
        """
        Check keyword status via bash type inspection.
        """
        quoted_name = quote(name)
        result = run_command(["bash", "-c", f"type {quoted_name}"])
        if "keyword" in result.stdout:
            return "bash keyword"
        return None
