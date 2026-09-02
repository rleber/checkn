"""
RubyGems.org gem existence probe.
"""

import requests

from checkn.core.cacheable_test import CacheableNameTest


class GemTest(CacheableNameTest):
    """
    Checks whether the target name is a published gem on rubygems.org.
    """

    title = "gem"
    domain = "ruby"

    def _fetch_all(self) -> list[str]:
        """
        Fetch every gem name ever published on rubygems.org.
        Side-effects: network request.
        """
        response = requests.get("https://rubygems.org/names")
        response.raise_for_status()
        return [line for line in response.text.splitlines() if line != "---"]
