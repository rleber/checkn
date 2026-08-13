#!/usr/bin/env python3

# Check how a name is defined in common Ruby usage (if at all)


import subprocess

import requests

from checkn.case_conversion import upper_camel_case


class RubyDefinition:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

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
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout == "true\n"
        else:
            return False

    @property
    def type(self):
        if self.is_gem:
            return "gem"
        elif self.is_builtin_class:
            return "builtin class"
        else:
            return None
