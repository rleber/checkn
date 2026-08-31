"""
Ruby keyword membership probe.
"""

from checkn.core.name_test import NameTest


class KeywordTest(NameTest):
    """
    Checks whether the target name is a reserved Ruby keyword.
    """

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

    title = "keyword"

    def _perform(self, name: str) -> str:
        """
        Test membership in the Ruby reserved keyword list.
        """
        return name if name in self.KEYWORDS else ""
