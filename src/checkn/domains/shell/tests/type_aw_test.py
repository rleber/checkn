"""
`type -aw` probe, run in a non-interactive zsh.
"""

from checkn.core.name_test import NameTest
from checkn.utils.shell import quote, run_command


class TypeAwTest(NameTest):
    """
    Runs `type -aw <name>` in a non-interactive zsh and returns its output.
    """

    title = "type -aw"

    def _perform(self, name: str) -> str:
        """
        Resolve name via non-interactive zsh PATH/builtin/keyword resolution.
        Side-effects: subprocess execution.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-c", f"type -aw {quoted_name}"])
        if result.returncode == 0:
            return result.stdout
        return ""
