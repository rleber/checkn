"""
Executable program definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class ProgramCheck(BaseCheck):
    """
    Evaluates if the target name is an executable program.
    """

    priority = 50

    def evaluate(self, name: str) -> str | None:
        """
        Check binary executable status via zsh path resolution.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-lic", f"which {quoted_name}"])
        if result.returncode != 0:
            return None
        if "reserved" in result.stdout:
            return None
        return "program"
