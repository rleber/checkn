"""
Ruby builtin class membership probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.case_conversion import upper_camel_case
from checkn.utils.shell import run_command


class BuiltinClassTest(CacheableNameTest):
    """
    Checks whether the target name is a builtin Ruby class/module.
    """

    title = "builtin class"
    domain = "ruby"

    def _cache_key(self, name: str) -> str:
        """
        Ruby class names are UpperCamelCase.
        """
        return upper_camel_case(name)

    def _fetch_all(self) -> list[str]:
        """
        List every top-level constant a fresh Ruby interpreter defines.
        Side-effects: subprocess execution.
        """
        result = run_command(["ruby", "-e", "puts Object.constants"])
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
