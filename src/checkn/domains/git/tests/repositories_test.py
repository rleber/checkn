"""
GitHub repository enumeration probe, for the current user.
"""

import os

import requests

from checkn.core.cacheable_test import CacheableNameTest


class RepositoriesTest(CacheableNameTest):
    """
    Fetches every GitHub repository owned by the current user.
    """

    title = "repositories"
    domain = "git"

    def _fetch_all(self) -> list[str]:
        """
        List all owned repositories via the GitHub API.
        Side-effects: network request.
        """
        headers = {
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github+json",
        }
        names = []
        page = 1
        while True:
            response = requests.get(
                "https://api.github.com/user/repos",
                headers=headers,
                params={"type": "owner", "per_page": 100, "page": page},
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            names.extend(repo["name"] for repo in data)
            page += 1
        return names
