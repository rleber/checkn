#!/usr/bin/env python3

"""
github_definition.py
Check if a name is in use as a repository on Github
- By the current user only
"""

# TODO Check if the repository name is in use by anyone
# TODO Check if a repository of that name is defined anywhere on this system
# TODO Check if a repository of that name is cloned anywhere on this system

import subprocess

from checkn.base_definition import BaseDefinition


class GitDefinition(BaseDefinition):
    @classmethod
    def current_user(cls):
        result = subprocess.run(
            ["git", "config", "github.user"], capture_output=True, text=True, check=True
        )
        return result.stdout.rstrip("\r\n")

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_repository(self):
        result = subprocess.run(
            [
                "git",
                "ls-remote",
                f"https://github.com/{self.current_user()}/{self.name}",
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        return result.returncode == 0

    @property
    def type(self):
        if self.is_repository:
            return "repository"
        else:
            return None

    @property
    def info(self):
        return BaseDefinition.Definition("git", self.name, self.type, {})
