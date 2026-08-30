"""Shell execution and string formatting utilities."""

import re
import shlex
import subprocess

UNSAFE_SHELL_PATTERN = re.compile(r"[\s\t\n\r$1~\{\}*?[<>|&'\"\]`#(),;=\\]")


def quote(s: str) -> str:
    """
    Escape string for safe shell evaluation.
    """
    if UNSAFE_SHELL_PATTERN.search(s):
        return shlex.quote(s)
    return s


def run_command(
    args: list[str], check: bool = False, shell: bool = False
) -> subprocess.CompletedProcess[str]:
    """
    Execute a subprocess command.
    """
    return subprocess.run(
        args, capture_output=True, check=check, text=True, shell=shell
    )
