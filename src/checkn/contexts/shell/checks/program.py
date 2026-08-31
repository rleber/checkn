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
        Check binary executable status using system PATH resolution.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-c", f"type -aw {quoted_name}"])
        if (
            result.returncode == 0
            and f"{name}: command" in result.stdout
            and f"{name}: builtin" not in result.stdout
        ):
            return "program"

        return None
