"""
test_shell.py

Run tests on checkn.utils.shell.

Usage: pytest tests/test_shell.py
"""

import time

from checkn.utils.shell import run_command


def test_run_command_returns_stdout():
    result = run_command(["echo", "hello"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_run_command_survives_orphaned_child_holding_pipe_open():
    """
    Reproduces the real-world hang: a command backgrounds a child that
    inherits (and never closes) the parent's stdout/stderr, so reading
    until EOF would otherwise block forever even after the command itself
    has exited.
    """
    start = time.monotonic()
    result = run_command(
        ["sh", "-c", "sleep 5 & echo done"],
        timeout=1,
    )
    elapsed = time.monotonic() - start

    assert elapsed < 3, "run_command waited on the orphaned child instead of timing out"
    assert result.returncode == 1
    assert isinstance(result.stdout, str)
