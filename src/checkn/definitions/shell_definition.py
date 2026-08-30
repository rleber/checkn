#!/usr/bin/env python3

"""
shell_definition.py

Check if a name is in use as a shell resource, e.g.
- A shell function
- A shell alias
- Another executable
"""

import re
import shlex
import subprocess

from checkn.definitions.base_definition import BaseDefinition


class ShellDefinition(BaseDefinition):
    # TODO Move __init__ and name property to BaseDefinition

    def __init__(self, name: str):
        self._name = name

    # TODO Use @staticmethod in other places instead of @classmethod

    # TODO Shell methods are useful; move them to a separate module
    @staticmethod
    def break_script_lines(script: str) -> list[str]:
        lines = script.splitlines()
        return [line.strip() for line in lines if len(line.strip()) > 0]

    @staticmethod
    def join_script_lines(script: list[str]) -> str:
        return ";".join([line.strip() for line in script if len(line.strip()) > 0])

    @staticmethod
    def flatten_script_lines(script: str) -> str:
        return ShellDefinition.join_script_lines(
            ShellDefinition.break_script_lines(script)
        )

    UNSAFE_SHELL_PATTERN = re.compile(r"[\s\t\n\r$1~\{\}*?[<>|&'\"\]`#(),;=\\]")

    @staticmethod
    def quote(s: str) -> str:
        if ShellDefinition.UNSAFE_SHELL_PATTERN.search(s):
            return shlex.quote(s)
        return s

    @property
    def quoted_name(self) -> str:
        return ShellDefinition.quote(self.name)

    @staticmethod
    def exec(args: list, check=False, shell=False) -> subprocess.CompletedProcess:
        return subprocess.run(
            args, capture_output=True, check=check, text=True, shell=shell
        )

    @property
    def name(self):
        return self._name

    @property
    def is_executable(self):
        result = self.exec(["zsh", "-lic", f"which {self.quoted_name}"])
        if result.returncode != 0:
            return False
        return not "reserved" in result.stdout  # Which doesn't fail for reserved words

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ShellDefinition({self.name!r})"

    @property
    def is_zsh_keyword(self):
        result = self.exec(["zsh", "-n", "-c", self.name])
        return result.returncode != 0

    @property
    def is_bash_keyword(self):
        result = self.exec(["bash", "-c", f"type {self.quoted_name}"])
        return "keyword" in result.stdout

    @property
    def is_function(self):
        result = self.exec(["zsh", "-lic", f"typeset -f {self.quoted_name}"])
        return result.returncode == 0

    @property
    def is_alias(self):
        result = self.exec(["zsh", "-lic", f"alias {self.quoted_name}"])
        return result.returncode == 0

    @property
    def is_program(self):
        if self.is_function or self.is_alias:
            return False
        return self.is_executable

    @property
    def type(self):
        if self.is_zsh_keyword:
            return "zsh keyword"
        elif self.is_bash_keyword:
            return "bash keyword"
        elif self.is_alias:
            return "alias"
        elif self.is_function:
            return "function"
        elif self.is_program:
            return "program"
        else:
            return None

    @property
    def info(self):
        return BaseDefinition.Definition("shell", self.name, self.type, {})
