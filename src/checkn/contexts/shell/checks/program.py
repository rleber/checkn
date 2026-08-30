"""
Executable program definition check.
"""

import shutil

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
        # Fast path: check current environment PATH directly
        if shutil.which(name) is not None:
            return "program"

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
        if "not found" in last_line or "reserved" in last_line:
            return None

        return "program"
