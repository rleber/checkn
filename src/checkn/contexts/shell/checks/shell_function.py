"""
Shell function definition check.
"""

from checkn.contexts.base_check import BaseCheck
from checkn.utils.shell import quote, run_command


class FunctionCheck(BaseCheck):
    """
    Evaluates if the target name is a shell function.
    """

    priority = 30

    def evaluate(self, name: str) -> str | None:
        """
        Check function definition status via zsh typeset utility.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-lic", f"typeset -f {quoted_name}"])

        # Ensure returncode is 0 and output contains body definition, not just startup banners
        if result.returncode == 0 and f"{name} ()" in result.stdout:
            return "function"
        return None
