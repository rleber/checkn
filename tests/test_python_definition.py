"""
test_python_definition.py

Run tests on PythonDefinition class

Usage: pytest test_python_definition.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "checkn"))

from python_definition import PythonDefinition

uninstalled_module = "30fcd23745efe32ce681__mypyc"


def test_uninstalled_modules():
    uninstalled_modules = PythonDefinition.uninstalled_modules()
    assert uninstalled_module in uninstalled_modules


def test_is_builtin_class():
    assert PythonDefinition("str").is_builtin_class  # str is a builtin class
    assert not PythonDefinition("math").is_builtin_class  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_builtin_class  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_builtin_class  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_builtin_class  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_builtin_class  # Path is an identifier in a stdlib module # Path is an identifier in a stdlib module


def test_is_builtin_module():
    assert not PythonDefinition("str").is_builtin_module  # str is a builtin class
    assert PythonDefinition("math").is_builtin_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_builtin_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_builtin_module  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_builtin_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_builtin_module  # Path is an identifier in a stdlib module


def test_is_standard_module():
    assert not PythonDefinition("str").is_standard_module  # str is a builtin class
    assert PythonDefinition("math").is_standard_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_standard_module  # collections is a standard module
    assert not PythonDefinition(
        "build123d"
    ).is_standard_module  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_standard_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_standard_module  # Path is an identifier in a standard module


def test_is_installed_module():
    assert not PythonDefinition("str").is_installed_module  # str is a builtin class
    assert not PythonDefinition("math").is_installed_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_installed_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_installed_module  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_installed_module  # this is an installed module
    assert not PythonDefinition(
        "Path"
    ).is_installed_module  # Path is an identifier in a stdlib module


def test_is_installable_module():
    assert not PythonDefinition("str").is_installable_module  # str is a builtin class
    assert not PythonDefinition(
        "math"
    ).is_installable_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_installable_module  # collections is a standard module
    assert PythonDefinition(
        "build123d"
    ).is_installable_module  # build123d is an defined module
    assert PythonDefinition(
        uninstalled_module
    ).is_installable_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_installable_module  # Path is an identifier in a standard module


def test_is_module():
    assert not PythonDefinition("str").is_module  # str is a builtin class
    assert PythonDefinition("math").is_module  # math is a builtin module
    assert PythonDefinition("collections").is_module  # collections is a stdlib module
    assert PythonDefinition("build123d").is_module  # build123d is an defined module
    assert PythonDefinition(
        uninstalled_module
    ).is_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_module  # Path is an identifier in a stdlib module


def test_is_builtin():
    assert PythonDefinition("str").is_builtin  # str is a builtin class
    assert PythonDefinition("math").is_builtin  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_builtin  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_builtin  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_builtin  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_builtin  # Path is an identifier in a stdlib module


def test_is_stdlib_module():
    assert not PythonDefinition("str").is_stdlib_module  # str is a builtin class
    assert not PythonDefinition("math").is_stdlib_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_stdlib_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_stdlib_module  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_stdlib_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_stdlib_module  # Path is an identifier in a stdlib module


def test_is_standard():
    assert PythonDefinition("str").is_standard  # str is a builtin class
    assert PythonDefinition("math").is_standard  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_standard  # collections is a standard module
    assert not PythonDefinition(
        "build123d"
    ).is_standard  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_standard  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_standard  # Path is an identifier in a standard module


def test_is_known_module():
    assert not PythonDefinition("str").is_known_module  # str is a builtin class
    assert PythonDefinition("math").is_known_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_known_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_known_module  # build123d is an defined module
    assert PythonDefinition(
        uninstalled_module
    ).is_known_module  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_known_module  # Path is an identifier in a stdlib module


def test_is_known():
    assert PythonDefinition("str").is_known  # str is a builtin class
    assert PythonDefinition("math").is_known  # math is a builtin module
    assert PythonDefinition("collections").is_known  # collections is a stdlib module
    assert PythonDefinition("build123d").is_known  # build123d is an defined module
    assert PythonDefinition(
        uninstalled_module
    ).is_known  # this is another installable (but uninstalled) module
    assert not PythonDefinition(
        "Path"
    ).is_known  # Path is an identifier in a stdlib module


def test_is_other_module():
    assert not PythonDefinition("str").is_other_module  # str is a builtin class
    assert not PythonDefinition("math").is_other_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_other_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_other_module  # build123d is an defined module
    assert not PythonDefinition(
        uninstalled_module
    ).is_other_module  # this is another installable (but uninstalled) module
    # I don't think there is an example of a known module that is "other"
    assert not PythonDefinition(
        "Path"
    ).is_other_module  # Path is an identifier in a stdlib module


def test_type():
    assert PythonDefinition("str").type == "builtin class"
    assert PythonDefinition("math").type == "builtin module"
    assert PythonDefinition("collections").type == "stdlib module"
    assert PythonDefinition("typer").type == "installed module"
    assert PythonDefinition("build123d").type == "installed module"
    assert PythonDefinition("30fcd23745efe32ce681__mypyc").type == "installable module"
    # I don't think there is an example of a known module that is "other"
    assert (
        PythonDefinition("Path").type is None
    )  # Path is an identifier in a stdlib module


def test_installer():
    assert PythonDefinition("str").installer == None
    assert PythonDefinition("math").installer == None
    assert PythonDefinition("collections").installer == None
    assert PythonDefinition("typer").installer == "pip"
    assert PythonDefinition("build123d").installer == "uv"
    assert PythonDefinition(uninstalled_module).installer == None
    assert PythonDefinition("Path").installer is None
