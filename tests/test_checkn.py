"""
test_checkn.py

Run tests on checkn utility

Usage: pytest test_checkn.py
"""

import subprocess


def run_checkn_for(word):
    result = subprocess.run(["checkn", word], capture_output=True, text=True)
    output_lines = result.stdout.split("\n")
    if result.returncode != 0:
        return ["checkn aborted:"] + output_lines
    if output_lines[-1] == "":
        output_lines.pop()
    return output_lines


def test_undefined_word():
    assert run_checkn_for("foobarbazbat") == ["undefined"]


def test_python_word():
    assert run_checkn_for("itertools") == ["python: builtin module"]


def test_ruby_word():
    assert run_checkn_for("foo") == ["ruby: gem"]


def test_python_and_ruby_word():
    assert run_checkn_for("dict") == ["python: builtin class", "ruby: gem"]


def test_python_git_and_shell_word():
    assert run_checkn_for("checkn") == [
        "git: repository",
        "python: installed module",
        "shell: program",
    ]


def test_shell_word():
    assert run_checkn_for("gpoa") == ["shell: alias"]
