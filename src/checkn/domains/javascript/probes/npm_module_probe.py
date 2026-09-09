"""
Published npm package membership probe -- live lookup, not cached.
"""

import sys

import requests

from checkn.core.name_probe import NameProbe


class NpmModuleProbe(NameProbe):
    """
    Checks whether the target name is a package published on the public
    npm registry, whether or not it's installed.

    Unlike the bulk-cached probes elsewhere in checkn (pypi_module, gem,
    formula, cask), npm has no compact bulk index to fetch and cache: a
    full dump of the registry's ~4.3 million package names runs to
    roughly 430MB via its CouchDB replication API (checked directly, not
    a documented bulk-listing endpoint), which isn't reasonable to
    download and cache locally. So this probe queries the registry
    directly for the one name being checked, every time, instead -- slower
    and network-dependent on every single check, unlike every other
    membership probe in checkn. It runs on every interactive `checkn`
    call (not just the nightly cache reload), so a short timeout is
    applied here explicitly, to fail fast rather than hang a foreground
    command.
    """

    title = "npm module"

    def _perform(self, name: str) -> str:
        """
        Query the npm registry directly for this exact name.
        Side-effects: network request.
        """
        try:
            response = requests.head(f"https://registry.npmjs.org/{name}", timeout=10)
        except requests.RequestException as exc:
            print(f"warning: npm registry lookup for {name!r} failed: {exc}", file=sys.stderr)
            return ""
        return name if response.status_code == 200 else ""
