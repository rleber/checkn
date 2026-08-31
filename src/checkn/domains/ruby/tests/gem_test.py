"""
RubyGems.org gem existence probe.
"""

import requests

from checkn.core.name_test import NameTest


class GemTest(NameTest):
    """
    Checks whether the target name is a published gem on rubygems.org.
    """

    title = "gem"

    def _perform(self, name: str) -> str:
        """
        Test gem page existence on rubygems.org.
        Side-effects: network request.
        """
        url = f"https://rubygems.org/gems/{name}"
        response = requests.get(url, timeout=5)
        return name if response.status_code == 200 else ""
