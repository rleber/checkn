"""
Zsh builtin command enumeration probe.
"""

from checkn.core.cacheable_test import CacheableNameTest
from checkn.utils.shell import run_command


class BuiltinTest(CacheableNameTest):
    """
    Fetches every builtin command in zsh, excluding names zsh also treats
    as reserved words (e.g. `local`, `export`) -- `type -aw` classifies
    those as reserved, not builtin.
    """

    title = "builtin"
    domain = "shell"

    def _fetch_all(self) -> list[str]:
        """
        List all zsh builtins via the `zsh/parameter` module, minus reserved words.
        Side-effects: subprocess execution.
        """
        builtins = run_command(
            ["zsh", "-c", "zmodload zsh/parameter; print -l ${(k)builtins}"]
        ).stdout.splitlines()
        reswords = set(
            run_command(
                ["zsh", "-c", "zmodload zsh/parameter; print -l ${(k)reswords}"]
            ).stdout.splitlines()
        )
        return [name for name in builtins if name not in reswords]
