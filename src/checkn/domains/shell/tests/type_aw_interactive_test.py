"""
`type -aw` probe, run in an interactive login zsh (needed to see aliases
and functions defined in shell startup files).
"""

from checkn.core.name_test import NameTest
from checkn.utils.shell import quote, run_command


class TypeAwInteractiveTest(NameTest):
    """
    Runs `type -aw <name>` in an interactive login zsh and returns its output.
    """

    title = "type -aw interactive"

    def _perform(self, name: str) -> str:
        """
        Resolve name via interactive zsh, exposing aliases and functions.
        """
        quoted_name = quote(name)
        result = run_command(["zsh", "-lic", f"type -aw {quoted_name}"])
        if result.returncode == 0:
            return result.stdout
        return ""
