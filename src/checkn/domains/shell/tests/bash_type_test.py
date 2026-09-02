"""
`type` probe, run in bash (used to detect bash reserved keywords).
"""

from checkn.core.name_test import NameTest
from checkn.utils.shell import quote, run_command


class BashTypeTest(NameTest):
    """
    Runs `type <name>` in bash and returns its output.
    """

    title = "bash type"

    def _perform(self, name: str) -> str:
        """
        Resolve name via bash type inspection.
        """
        quoted_name = quote(name)
        result = run_command(["bash", "-c", f"type {quoted_name}"])
        return result.stdout
