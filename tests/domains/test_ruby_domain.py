"""
test_ruby_domain.py

Run tests on RubyDomain

Usage: pytest tests/domains/test_ruby_domain.py
"""

from checkn.domains.ruby.domain import RubyDomain


def domain() -> RubyDomain:
    return RubyDomain()


def test_type_keyword():
    assert domain().execute("type", "while") == "keyword"


def test_type_gem():
    assert domain().execute("type", "rails") == "gem"


def test_type_builtin_class():
    assert domain().execute("type", "basic_object") == "builtin class"
    assert domain().execute("type", "BasicObject") == "builtin class"


def test_singleton():
    assert RubyDomain() is RubyDomain()
    assert RubyDomain().lab is RubyDomain().lab
