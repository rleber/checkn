"""
GitHub repository existence probe, for the current user.
"""

import subprocess

from checkn.core.name_test import NameTest


class LsRemoteTest(NameTest):
    """
    Checks whether a GitHub repository named name exists under the current user.
    """

    title = "ls-remote"

    @classmethod
    def current_user(cls) -> str:
        """
        Retrieve the configured GitHub username.
        """
        result = subprocess.run(
            ["git", "config", "github.user"], capture_output=True, text=True, check=True
        )
        return result.stdout.rstrip("\r\n")

    def _perform(self, name: str) -> str:
        """
        Test repository existence via `git ls-remote`.
        Side-effects: network request (to github).
        """
        result = subprocess.run(
            ["git", "ls-remote", f"https://github.com/{self.current_user()}/{name}"],
            capture_output=True,
            check=False,
            text=True,
        )
        return name if result.returncode == 0 else ""
