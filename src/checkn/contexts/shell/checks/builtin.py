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
        result = run_command(["zsh", "-c", f"which {quoted_name}"])

        if result.returncode != 0:
            return None

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            return None

        # Check last output line for valid executable path
        last_line = lines[-1]
        if "built-in" in last_line:
            return "builtin"

        return None
