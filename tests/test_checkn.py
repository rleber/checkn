"""
test_checkn.py

Run tests on the checkn CLI.

Usage: pytest tests/test_checkn.py
"""

import subprocess

from typer.testing import CliRunner

from checkn import __version__
from checkn.cli import app

runner = CliRunner()


def run_checkn_for(word: str) -> list[str]:
    result = runner.invoke(app, [word])
    output_lines = result.stdout.split("\n")
    if result.exit_code != 0:
        return ["checkn aborted:"] + output_lines
    if output_lines[-1] == "":
        output_lines.pop()
    return output_lines


def test_undefined_word():
    assert run_checkn_for("foobarbazbat") == ["undefined"]


def test_python_word():
    assert run_checkn_for("itertools") == [
        "javascript: uninstalled module",
        "python: builtin module",
    ]


def test_ruby_word():
    assert run_checkn_for("sidekiq") == [
        "javascript: uninstalled module",
        "ruby: uninstalled gem",
    ]


def test_python_and_ruby_word():
    assert run_checkn_for("dict") == [
        "homebrew: uninstalled formula",
        "javascript: uninstalled module",
        "python: builtin class",
        "ruby: uninstalled gem",
    ]


def test_python_git_and_shell_word():
    assert run_checkn_for("checkn") == [
        "git: repository",
        "javascript: uninstalled module",
        "python: installed module",
        "shell: program",
    ]


def test_shell_word():
    assert run_checkn_for("gpoa") == ["shell: alias"]


def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_version_flag_short():
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_list_domains():
    result = runner.invoke(app, ["--list-domains"])
    assert result.exit_code == 0
    assert "Available domains:" in result.stdout
    for domain in ("git", "python", "ruby", "shell"):
        assert f"  - {domain}" in result.stdout


def test_list_domains_short():
    result = runner.invoke(app, ["-l"])
    assert result.exit_code == 0
    assert "Available domains:" in result.stdout


def test_list_domains_empty(monkeypatch):
    monkeypatch.setattr("checkn.cli.get_domains", lambda: {})
    result = runner.invoke(app, ["--list-domains"])
    assert result.exit_code == 0
    assert "No domains found." in result.stdout


def test_missing_name_errors():
    result = runner.invoke(app, [])
    assert result.exit_code == 1
    assert "Missing argument 'NAME'" in result.stderr


def test_unknown_domain_warns_but_still_checks_others():
    result = runner.invoke(app, ["itertools", "-d", "python", "-d", "nonexistent"])
    assert "Warning: Domain 'nonexistent' not found." in result.stderr
    assert "python: builtin module" in result.stdout


def test_checkn_entrypoint_end_to_end():
    """One real subprocess invocation, to confirm the installed console-script actually works."""
    result = subprocess.run(["checkn", "itertools"], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == "javascript: uninstalled module\npython: builtin module"
