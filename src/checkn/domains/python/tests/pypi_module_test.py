"""
PyPI package index membership probe.
"""

import requests

from checkn.core.cacheable_test import CacheableNameTest


class PypiModuleTest(CacheableNameTest):
    """
    Checks whether the target name is a package published on PyPI.
    """

    title = "pypi module"
    domain = "python"

    def _fetch_all(self) -> list[str]:
        """
        Fetch every project name in the PyPI simple package index.
        Side-effects: network request.
        """
        url = "https://pypi.org/simple/"
        headers = {"Accept": "application/vnd.pypi.simple.v1+json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return [project["name"] for project in data.get("projects", [])]
