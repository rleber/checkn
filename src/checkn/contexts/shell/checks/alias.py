"""
Shell alias definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class AliasCheck(BaseCheck):
    """
    Evaluates if the target name is a shell alias.
    """

    priority = 30

    def evaluate(self, name: str) -> str | None:
        """
        Check alias status via zsh shell evaluation.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-lic", f"alias {quoted_name}"])

        # Check return code AND ensure output actually contains an alias definition
        if result.returncode == 0 and f"{name}=" in result.stdout:
            return "alias"
        return None
