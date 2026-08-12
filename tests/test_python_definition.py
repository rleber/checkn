import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "checkn"))

from python_definition import PythonDefinition


def test_is_builtin_class():
    assert PythonDefinition("str").is_builtin_class  # str is a builtin class
    assert not PythonDefinition("math").is_builtin_class  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_builtin_class  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_builtin_class  # build123d is an installed module
    assert not PythonDefinition("git").is_builtin_class  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_builtin_class  # Path is an identifier in a stdlib module # Path is an identifier in a stdlib module


def test_is_module():
    assert not PythonDefinition("str").is_module  # str is a builtin class
    assert PythonDefinition("math").is_module  # math is a builtin module
    assert PythonDefinition("collections").is_module  # collections is a stdlib module
    assert PythonDefinition("build123d").is_module  # build123d is an installed module
    assert PythonDefinition("git").is_module  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_module  # Path is an identifier in a stdlib module


def test_is_builtin_module():
    assert not PythonDefinition("str").is_builtin_module  # str is a builtin class
    assert PythonDefinition("math").is_builtin_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_builtin_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_builtin_module  # build123d is an installed module
    assert not PythonDefinition("git").is_builtin_module  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_builtin_module  # Path is an identifier in a stdlib module


def test_is_stdlib_module():
    assert not PythonDefinition("str").is_stdlib_module  # str is a builtin class
    assert not PythonDefinition("math").is_stdlib_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_stdlib_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_stdlib_module  # build123d is an installed module
    assert not PythonDefinition("git").is_stdlib_module  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_stdlib_module  # Path is an identifier in a stdlib module


def test_is_installed_module():
    assert not PythonDefinition("str").is_installed_module  # str is a builtin class
    assert not PythonDefinition("math").is_installed_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_installed_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_installed_module  # build123d is an installed module
    assert not PythonDefinition("git").is_installed_module  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_installed_module  # Path is an identifier in a stdlib module


def test_is_known_module():
    assert not PythonDefinition("str").is_known_module  # str is a builtin class
    assert PythonDefinition("math").is_known_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_known_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_known_module  # build123d is an installed module
    assert not PythonDefinition("git").is_known_module  # git is an known module
    assert not PythonDefinition(
        "Path"
    ).is_known_module  # Path is an identifier in a stdlib module


def test_is_add_on_module():
    assert not PythonDefinition("str").is_add_on_module  # str is a builtin class
    assert not PythonDefinition("math").is_add_on_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_add_on_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_add_on_module  # build123d is an installed module
    assert PythonDefinition("git").is_add_on_module  # git is an add_on module
    assert not PythonDefinition(
        "Path"
    ).is_add_on_module  # Path is an identifier in a stdlib module


def test_is_contributed_module():
    assert not PythonDefinition("str").is_contributed_module  # str is a builtin class
    assert not PythonDefinition(
        "math"
    ).is_contributed_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_contributed_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_contributed_module  # build123d is an installed module
    assert PythonDefinition("git").is_contributed_module  # git is an contributed module
    assert not PythonDefinition(
        "Path"
    ).is_contributed_module  # Path is an identifier in a stdlib module


def test_is_defined_module():
    assert not PythonDefinition("str").is_defined_module  # str is a builtin class
    assert PythonDefinition("math").is_defined_module  # math is a builtin module
    assert PythonDefinition(
        "collections"
    ).is_defined_module  # collections is a stdlib module
    assert PythonDefinition(
        "build123d"
    ).is_defined_module  # build123d is an installed module
    assert PythonDefinition("git").is_defined_module  # git is an defined module
    assert not PythonDefinition(
        "Path"
    ).is_defined_module  # Path is an identifier in a stdlib module


def test_is_other_module():
    assert not PythonDefinition("str").is_other_module  # str is a builtin class
    assert not PythonDefinition("math").is_other_module  # math is a builtin module
    assert not PythonDefinition(
        "collections"
    ).is_other_module  # collections is a stdlib module
    assert not PythonDefinition(
        "build123d"
    ).is_other_module  # build123d is an installed module
    assert PythonDefinition("git").is_other_module  # git is an other module
    assert not PythonDefinition(
        "Path"
    ).is_other_module  # Path is an identifier in a stdlib module


def test_basic_type():
    assert PythonDefinition("str").basic_type == "builtin class"
    assert PythonDefinition("math").basic_type == "builtin module"
    assert PythonDefinition("collections").basic_type == "stdlib module"
    assert PythonDefinition("build123d").basic_type == "installed module"
    assert PythonDefinition("git").basic_type == "other module"
    assert (
        PythonDefinition("Path").basic_type is None
    )  # Path is an identifier in a stdlib module


def test_installer():
    # build123d => "uv"
    # argparse => "pip"
    # math => None
    # Path => None
    pass
