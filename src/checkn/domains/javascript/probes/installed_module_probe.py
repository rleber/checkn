"""
Installed npm package membership probe.
"""

import json

from checkn.core.cacheable_probe import CacheableNameProbe
from checkn.utils.shell import run_command


class InstalledModuleProbe(CacheableNameProbe):
    """
    Checks whether the target name is an npm package installed globally on
    this system. "Globally" because, unlike Python's single current venv,
    npm installs are normally scoped per-project (node_modules) with no
    one obvious "current" project for checkn to consult -- global install
    is the closest npm equivalent to "installed on this system", matching
    how installed gem/formula already work in checkn.
    """

    title = "installed module"
    domain = "javascript"

    def _fetch_all(self) -> list[str]:
        """
        List every globally installed npm package via `npm ls -g --json`.
        Side-effects: subprocess execution.
        """
        result = run_command(["npm", "ls", "-g", "--json", "--depth=0"])
        if result.returncode != 0:
            return []
        try:
            data = json.loads(result.stdout)
        except ValueError:
            return []
        return list(data.get("dependencies", {}).keys())
