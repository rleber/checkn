"""
test_python_domain.py

Run tests on PythonDomain

Usage: pytest tests/domains/test_python_domain.py
"""

from checkn.domains.python.domain import PythonDomain


def domain() -> PythonDomain:
    return PythonDomain()


def test_type_keyword():
    assert domain().execute("type", "assert") == "keyword"


def test_type_builtin_class():
    assert domain().execute("type", "str") == "builtin class"


def test_type_builtin_module():
    assert domain().execute("type", "itertools") == "builtin module"


def test_type_stdlib_module():
    assert domain().execute("type", "collections") == "stdlib module"


def test_type_installed_module():
    assert domain().execute("type", "checkn") == "installed module"


def test_type_undefined():
    assert domain().execute("type", "foobarbazbat") == ""


def test_singleton():
    assert PythonDomain() is PythonDomain()
    assert PythonDomain().lab is PythonDomain().lab
