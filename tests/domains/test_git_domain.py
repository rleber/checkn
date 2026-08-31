"""
test_git_domain.py

Run tests on GitDomain

Usage: pytest tests/domains/test_git_domain.py
"""

from checkn.domains.git.domain import GitDomain


def domain() -> GitDomain:
    return GitDomain()


def test_repository():
    assert domain().execute("repository", "foo") == ""
    assert domain().execute("repository", "checkn") == "repository"


def test_singleton():
    assert GitDomain() is GitDomain()
    assert GitDomain().lab is GitDomain().lab
