"""
test_shell_definition.py

Run tests on ShellDefinition class

Usage: pytest test_shell_definition.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "checkn"))

from shell_definition import ShellDefinition


def test_is_zsh_keyword():
    assert ShellDefinition("if").is_zsh_keyword  # if is a zsh keyword
    assert not ShellDefinition("in").is_zsh_keyword  # in is a bash keyword
    assert not ShellDefinition("gpoa").is_zsh_keyword  # gpoa is a shell alias
    assert not ShellDefinition("cdp").is_zsh_keyword  # cdp is a shell function
    assert not ShellDefinition("code").is_zsh_keyword  # code is a program
    assert not ShellDefinition(
        "foo"
    ).is_zsh_keyword  # foo is not a special name to the shell


def test_is_bash_keyword():
    assert ShellDefinition("if").is_bash_keyword  # if is a zsh keyword
    assert ShellDefinition("in").is_bash_keyword  # in is a bash keyword
    assert not ShellDefinition("gpoa").is_bash_keyword  # gpoa is a shell alias
    assert not ShellDefinition("cdp").is_bash_keyword  # cdp is a shell function
    assert not ShellDefinition("code").is_bash_keyword  # code is a program
    assert not ShellDefinition(
        "foo"
    ).is_bash_keyword  # foo is not a special name to the shell


def test_is_alias():
    assert not ShellDefinition("if").is_alias  # if is a zsh keyword
    assert not ShellDefinition("in").is_alias  # in is a bash keyword
    assert ShellDefinition("gpoa").is_alias  # gpoa is a shell alias
    assert not ShellDefinition("cdp").is_alias  # cdp is a shell function
    assert not ShellDefinition("code").is_alias  # code is a program
    assert not ShellDefinition("foo").is_alias  # foo is not a special name to the shell


def test_is_function():
    assert not ShellDefinition("if").is_function  # if is a zsh keyword
    assert not ShellDefinition("in").is_function  # in is a bash keyword
    assert not ShellDefinition("gpoa").is_function  # gpoa is a shell alias
    assert ShellDefinition("cdp").is_function  # cdp is a shell function
    assert not ShellDefinition("code").is_function  # code is a program
    assert not ShellDefinition(
        "foo"
    ).is_function  # foo is not a special name to the shell


def test_is_program():
    assert not ShellDefinition("if").is_program  # if is a zsh keyword
    assert not ShellDefinition("in").is_program  # in is a bash keyword
    assert not ShellDefinition("gpoa").is_program  # gpoa is a shell alias
    assert not ShellDefinition("cdp").is_program  # cdp is a shell function
    assert ShellDefinition("code").is_program  # code is a program
    assert not ShellDefinition(
        "foo"
    ).is_program  # foo is not a special name to the shell


def test_type():
    assert ShellDefinition("if").type == "zsh keyword"  # if is a zsh keyword
    assert ShellDefinition("in").type == "bash keyword"  # in is a bash keyword
    assert ShellDefinition("gpoa").type == "alias"  # gpoa is a shell alias
    assert ShellDefinition("cdp").type == "function"  # cdp is a shell function
    assert ShellDefinition("code").type == "program"  # code is a program
    assert ShellDefinition("foo").type is None  # foo is a special name to the shell


def test_info():
    assert ShellDefinition("gpoa").info._asdict() == {
        "context": "shell",
        "name": "gpoa",
        "definition": "alias",
        "details": {},
    }
