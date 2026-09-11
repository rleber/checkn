"""
Published apt package name probe.
"""

import re

import requests

from checkn.core.cacheable_probe import CacheableNameProbe

# Debian's own plain-text dump of every package known to a given suite --
# see https://packages.debian.org/<suite>/allpackages. "stable" is used
# rather than "unstable"/"sid" since it's the version most systems
# actually run. The URL asks for the gzipped variant (much smaller over
# the wire), but requests auto-decodes the response's `Content-Encoding:
# x-gzip` header, so response.text is already plain text -- verified
# directly against the live endpoint, not assumed. Each entry looks like:
#   0ad (0.27.0-2+b1) Real-time strategy game of ancient warfare
# preceded by a few header/copyright lines that don't match _ENTRY_PATTERN
# and are naturally skipped.
ALLPACKAGES_URL = "https://packages.debian.org/stable/allpackages?format=txt.gz"
_ENTRY_PATTERN = re.compile(r"^(\S+) \(")


class PackageProbe(CacheableNameProbe):
    """
    Checks whether the target name is a package known to Debian's package
    archive, whether or not it's installed. Unlike InstalledPackageProbe,
    this doesn't need apt/dpkg at all -- it fetches Debian's own published
    index over the network -- so it isn't restricted to Linux.
    """

    title = "package"
    domain = "apt"

    def _fetch_all(self) -> list[str]:
        """
        Fetch and parse Debian's "all packages" text dump for the stable
        suite. A given name can legitimately appear on more than one line
        (e.g. present in both "main" and "contrib"), so duplicates are
        collapsed here -- the cache's (domain, probe, name) uniqueness
        constraint would otherwise reject the reload outright. Side-
        effects: network request.
        """
        response = requests.get(ALLPACKAGES_URL)
        response.raise_for_status()
        names = (
            m.group(1)
            for line in response.text.splitlines()
            if (m := _ENTRY_PATTERN.match(line))
        )
        return list(dict.fromkeys(names))
