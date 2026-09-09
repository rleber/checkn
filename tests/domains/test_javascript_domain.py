"""
test_javascript_domain.py

Run tests on JavaScriptDomain

Usage: pytest tests/domains/test_javascript_domain.py
"""

from checkn.domains.javascript.domain import JavaScriptDomain


def domain() -> JavaScriptDomain:
    return JavaScriptDomain()


def test_type_keyword():
    assert domain().execute("type", "while") == "keyword"


def test_type_builtin_class():
    assert domain().execute("type", "Array") == "builtin class"


def test_type_builtin_module():
    assert domain().execute("type", "fs") == "builtin module"


def test_type_installed_module():
    assert domain().execute("type", "joplin") == "installed module"


def test_type_uninstalled_module():
    assert domain().execute("type", "express") == "uninstalled module"


def test_type_undefined():
    assert domain().execute("type", "foobarbazbat") == ""


def test_singleton():
    assert JavaScriptDomain() is JavaScriptDomain()
    assert JavaScriptDomain().lab is JavaScriptDomain().lab
