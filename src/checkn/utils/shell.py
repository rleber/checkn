"""Shell execution and string formatting utilities."""

import re
import shlex
import subprocess
import sys

UNSAFE_SHELL_PATTERN = re.compile(r"[\s\t\n\r$1~\{\}*?[<>|&'\"\]`#(),;=\\]")

# An orphaned background child of the command (e.g. a shell startup plugin
# that backgrounds a helper process without closing its inherited stdout/
# stderr) can hold run_command's output pipes open indefinitely, hanging
# subprocess.run forever even though the command we actually asked for has
# finished. Bound it so one wedged probe can't stall the whole cache reload.
DEFAULT_TIMEOUT = 180


def quote(s: str) -> str:
    """
    Escape string for safe shell evaluation.
    """
    if UNSAFE_SHELL_PATTERN.search(s):
        return shlex.quote(s)
    return s


def run_command(
    args: list[str],
    check: bool = False,
    shell: bool = False,
    timeout: float | None = DEFAULT_TIMEOUT,
) -> subprocess.CompletedProcess[str]:
    """
    Execute a subprocess command. If it doesn't finish within timeout,
    return a failed result (empty output, returncode 1) instead of hanging.
    """
    try:
        return subprocess.run(
            args, capture_output=True, check=check, text=True, shell=shell, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        print(f"run_command timed out after {timeout}s: {args}", file=sys.stderr)
        return subprocess.CompletedProcess(
            args=args,
            returncode=1,
            stdout=_decode(exc.stdout),
            stderr=_decode(exc.stderr),
        )


def _decode(value: str | bytes | None) -> str:
    """
    Normalize a TimeoutExpired capture to str -- despite text=True, cpython
    can still hand back bytes here depending on when the timeout landed.
    """
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value
