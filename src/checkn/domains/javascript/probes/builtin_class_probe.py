"""
JavaScript builtin class/constructor membership probe.
"""

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class BuiltinClassProbe(CacheableNameProbe):
    """
    Checks whether the target name is a builtin JavaScript class or
    constructor function (e.g. Array, Map, Promise).
    """

    title = "builtin class"
    domain = "javascript"

    def _fetch_all(self) -> list[str]:
        """
        List every capitalized, function-valued global a fresh Node
        interpreter defines. Side-effects: subprocess execution.
        """
        result = run_command(
            [
                "node",
                "-e",
                "Object.getOwnPropertyNames(globalThis)"
                ".filter(n => /^[A-Z]/.test(n) && typeof globalThis[n] === 'function')"
                ".forEach(n => console.log(n))",
            ]
        )
        if result.returncode != 0:
            return []
        return result.stdout.splitlines()
