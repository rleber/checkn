"""
JavaScript keyword membership probe.
"""

from checkn.core.name_probe import NameProbe


class KeywordProbe(NameProbe):
    """
    Checks whether the target name is a reserved JavaScript keyword.
    """

    # Per https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#keywords
    # (unlike Python's `keyword` module, JavaScript has no runtime API to
    # introspect this, so it's hardcoded here, same approach as Ruby's
    # KeywordProbe). Includes always-reserved words, strict-mode-reserved
    # words, and contextual keywords in common use (let, async, await, etc.).
    KEYWORDS = (
        "await",
        "break",
        "case",
        "catch",
        "class",
        "const",
        "continue",
        "debugger",
        "default",
        "delete",
        "do",
        "else",
        "enum",
        "export",
        "extends",
        "false",
        "finally",
        "for",
        "function",
        "if",
        "implements",
        "import",
        "in",
        "instanceof",
        "interface",
        "let",
        "new",
        "null",
        "package",
        "private",
        "protected",
        "public",
        "return",
        "static",
        "super",
        "switch",
        "this",
        "throw",
        "true",
        "try",
        "typeof",
        "var",
        "void",
        "while",
        "with",
        "yield",
    )

    title = "keyword"

    def _perform(self, name: str) -> str:
        """
        Test membership in the JavaScript reserved keyword list.
        """
        return name if name in self.KEYWORDS else ""
