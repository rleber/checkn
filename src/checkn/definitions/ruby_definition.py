#!/usr/bin/env python3
"""
ruby_definition.py

Check how a name is defined in common Ruby usage (if at all)
"""

# TODO Check rails reserved words

import subprocess

import requests

from checkn.case_conversion import upper_camel_case
from checkn.definitions.base_definition import BaseDefinition


class RubyDefinition(BaseDefinition):
    # Per https://ruby-doc.org/core-3.1.2/doc/keywords_rdoc.html
    KEYWORDS = (
        "__ENCODING__",
        "__LINE__",
        "__FILE__",
        "BEGIN",
        "END",
        "alias",
        "and",
        "begin",
        "break",
        "case",
        "class",
        "def",
        "defined?",
        "do",
        "else",
        "elsif",
        "end",
        "ensure",
        "false",
        "for",
        "if",
        "in",
        "module",
        "next",
        "nil",
        "not",
        "or",
        "redo",
        "rescue",
        "retry",
        "return",
        "self",
        "super",
        "then",
        "true",
        "undef",
        "unless",
        "until",
        "when",
        "while",
        "yield",
    )

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_keyword(self):
        return self.name in self.KEYWORDS

    @property
    def is_gem(self):
        if self.is_builtin_class:
            return False
        url = f"https://rubygems.org/gems/{self.name}"
        response = requests.get(url, timeout=5)
        return response.status_code == 200

    @property
    def is_builtin_class(self):
        class_name = upper_camel_case(self.name)
        ruby_script = f'"puts Module.const_defined?(\\"{class_name}\\").inspect"'
        result = subprocess.run(
            [f"ruby -e {ruby_script}"],
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout == "true\n"
        else:
            return False

    @property
    def type(self):
        if self.is_keyword:
            return "keyword"
        elif self.is_gem:
            return "gem"
        elif self.is_builtin_class:
            return "builtin class"
        else:
            return None

    @property
    def info(self):
        return BaseDefinition.Definition("ruby", self.name, self.type, {})
