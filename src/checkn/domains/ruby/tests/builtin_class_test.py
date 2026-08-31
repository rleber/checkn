"""
Ruby builtin class membership probe.
"""

import subprocess

from checkn.core.name_test import NameTest
from checkn.utils.case_conversion import upper_camel_case


class BuiltinClassTest(NameTest):
    """
    Checks whether the target name is a builtin Ruby class/module.
    """

    title = "builtin class"

    def _perform(self, name: str) -> str:
        """
        Test class existence via a Ruby subprocess.
        Side-effects: subprocess execution.
        """
        class_name = upper_camel_case(name)
        ruby_script = f'"puts Module.const_defined?(\\"{class_name}\\").inspect"'
        result = subprocess.run(
            [f"ruby -e {ruby_script}"],
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout == "true\n":
            return name
        return ""
