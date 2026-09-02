"""
test_shell_domain.py

Run tests on ShellDomain

Usage: pytest tests/domains/test_shell_domain.py
"""

from checkn.domains.shell.domain import ShellDomain


def domain() -> ShellDomain:
    return ShellDomain()


def test_zsh_keyword():
    assert domain().execute("zsh keyword", "if") == "zsh keyword"
    assert domain().execute("zsh keyword", "in") == ""  # in is a bash keyword
    assert domain().execute("zsh keyword", "gpoa") == ""  # gpoa is a shell alias
    assert domain().execute("zsh keyword", "cdp") == ""  # cdp is a shell function
    assert domain().execute("zsh keyword", "code") == ""  # code is a program
    assert domain().execute("zsh keyword", "foo") == ""  # not special to the shell


def test_builtin():
    assert domain().execute("builtin", "if") == ""  # if is a zsh keyword
    assert domain().execute("builtin", "local") == ""  # local is a zsh keyword, not a builtin
    assert domain().execute("builtin", "gpoa") == ""  # gpoa is a shell alias
    assert domain().execute("builtin", "cdp") == ""  # cdp is a shell function
    assert domain().execute("builtin", "code") == ""  # code is a program
    assert domain().execute("builtin", "cd") == "builtin"
    assert domain().execute("builtin", "foo") == ""  # not special to the shell


def test_bash_keyword():
    assert domain().execute("bash keyword", "if") == "bash keyword"  # if is also a bash keyword
    assert domain().execute("bash keyword", "in") == "bash keyword"
    assert domain().execute("bash keyword", "gpoa") == ""  # gpoa is a shell alias
    assert domain().execute("bash keyword", "cdp") == ""  # cdp is a shell function
    assert domain().execute("bash keyword", "code") == ""  # code is a program
    assert domain().execute("bash keyword", "foo") == ""  # not special to the shell


def test_alias():
    assert domain().execute("alias", "if") == ""  # if is a zsh keyword
    assert domain().execute("alias", "in") == ""  # in is a bash keyword
    assert domain().execute("alias", "gpoa") == "alias"
    assert domain().execute("alias", "cdp") == ""  # cdp is a shell function
    assert domain().execute("alias", "code") == ""  # code is a program
    assert domain().execute("alias", "foo") == ""  # not special to the shell


def test_function():
    assert domain().execute("function", "if") == ""  # if is a zsh keyword
    assert domain().execute("function", "in") == ""  # in is a bash keyword
    assert domain().execute("function", "gpoa") == ""  # gpoa is a shell alias
    assert domain().execute("function", "cdp") == "function"
    assert domain().execute("function", "code") == ""  # code is a program
    assert domain().execute("function", "foo") == ""  # not special to the shell


def test_program():
    assert domain().execute("program", "if") == ""  # if is a zsh keyword
    assert domain().execute("program", "in") == ""  # in is a bash keyword
    assert domain().execute("program", "gpoa") == ""  # gpoa is a shell alias
    assert domain().execute("program", "cdp") == ""  # cdp is a shell function
    assert domain().execute("program", "code") == "program"
    assert domain().execute("program", "foo") == ""  # not special to the shell


def test_execute_all():
    results = domain().execute_all("gpoa")
    assert results["alias"] == "alias"
    assert all(v == "" for title, v in results.items() if title != "alias")


def test_singleton():
    assert ShellDomain() is ShellDomain()
    assert ShellDomain().lab is ShellDomain().lab
