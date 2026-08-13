"""
test_git_definition.py

Run tests on GitDefinition class

Usage: pytest test_git_definition.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "checkn"))

from ruby_definition import RubyDefinition


def test_is_gem():
    assert RubyDefinition("rails").is_gem
    assert not RubyDefinition("basic_object").is_gem
    assert not RubyDefinition("BasicObject").is_gem


def test_is_builtin_class():
    assert not RubyDefinition("rails").is_builtin_class
    assert RubyDefinition("basic_object").is_builtin_class
    assert RubyDefinition("BasicObject").is_builtin_class


def test_type():
    assert RubyDefinition("rails").type == "gem"
    assert RubyDefinition("basic_object").type == "builtin class"
    assert RubyDefinition("BasicObject").type == "builtin class"
