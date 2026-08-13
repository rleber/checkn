"""
test_git_definition.py

Run tests on GitDefinition class

Usage: pytest test_git_definition.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "checkn"))

from git_definition import GitDefinition


def test_is_repository():
    assert not GitDefinition("foo").is_repository
    assert GitDefinition("checkn").is_repository


def test_type():
    assert GitDefinition("foo").type is None
    assert GitDefinition("checkn").type == "repository"


def test_info():
    assert GitDefinition("checkn").info._asdict() == {
        "context": "git",
        "name": "checkn",
        "definition": "repository",
        "details": {},
    }
