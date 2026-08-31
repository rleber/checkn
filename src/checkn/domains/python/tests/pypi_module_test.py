"""
PyPI package index membership probe.
"""

import requests

from checkn.core.name_test import NameTest


class PypiModuleTest(NameTest):
    """
    Checks whether the target name is a package published on PyPI.
    """

    title = "pypi module"

    def _perform(self, name: str) -> str:
        """
        Test membership in the PyPI simple package index.
        Side-effects: network request.
        """
        url = "https://pypi.org/simple/"
        headers = {"Accept": "application/vnd.pypi.simple.v1+json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        packages = [project["name"] for project in data.get("projects", [])]
        return name if name in packages else ""
