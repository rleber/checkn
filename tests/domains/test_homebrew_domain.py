"""
test_homebrew_domain.py

Run tests on HomebrewDomain

Usage: pytest tests/domains/test_homebrew_domain.py
"""

from checkn.domains.homebrew.domain import HomebrewDomain


def domain() -> HomebrewDomain:
    return HomebrewDomain()


def test_installed_formula():
    assert domain().execute("formula", "ca-certificates") == "installed formula"


def test_uninstalled_formula():
    assert domain().execute("formula", "wget") == "uninstalled formula"


def test_installed_cask():
    assert domain().execute("cask", "iterm2") == "installed cask"


def test_uninstalled_cask():
    assert domain().execute("cask", "google-chrome") == "uninstalled cask"


def test_undefined():
    assert domain().execute("formula", "foobarbazbat") == ""
    assert domain().execute("cask", "foobarbazbat") == ""


def test_singleton():
    assert HomebrewDomain() is HomebrewDomain()
    assert HomebrewDomain().lab is HomebrewDomain().lab
