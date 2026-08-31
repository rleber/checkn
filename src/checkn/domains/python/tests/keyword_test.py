"""
Python keyword membership probe.
"""

import keyword

from checkn.core.name_test import NameTest


class KeywordTest(NameTest):
    """
    Checks whether the target name is a Python keyword.
    """

    title = "keyword"

    def _perform(self, name: str) -> str:
        """
        Test membership in the Python keyword list.
        """
        return name if name in keyword.kwlist else ""
