"""
Builtin command definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class BuiltinCheck(BaseCheck):
    """
    Evaluates if the target name is an builtin command.
    """

    priority = 40

    def evaluate(self, name: str) -> str | None:
        """
        Check builtin status using system PATH resolution.
        """
        # Subprocess fallback using non-interactive shell to prevent banner interference
        quoted_name = quote(name)
        result = run_command(["zsh", "-c", f"type -aw {quoted_name}"])

        if result.returncode == 0 and f"{name}: builtin" in result.stdout:
            return "builtin"

        return None
