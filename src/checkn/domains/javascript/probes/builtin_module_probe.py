"""
Node.js builtin module membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class BuiltinModuleProbe(CacheableNameProbe):
    """
    Checks whether the target name is a Node.js builtin (core) module.

    Node has no equivalent of Python's compiled-in-vs-standard-library
    split -- this is Node's one flat list of core modules, playing the
    role of both `builtin_module` and `standard_module` in the Python
    domain.
    """

    title = "builtin module"
    domain = "javascript"

    def _fetch_all(self) -> list[str]:
        """
        List every builtin module via Node's own `module` API.
        Side-effects: subprocess execution.
        """
        result = run_command(
            ["node", "-e", "require('module').builtinModules.forEach(n => console.log(n))"]
        )
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
