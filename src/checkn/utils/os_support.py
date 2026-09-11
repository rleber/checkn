"""
OS-compatibility checking for probes that only work on a specific platform.

checkn itself is only really exercised on macOS today (see README), but the
architecture shouldn't assume that forever: a probe that only makes sense on
one platform (e.g. an `apt`/`dpkg`-backed probe, which needs Linux) declares
that via NameProbe.required_os rather than hardcoding a check against
whatever OS happens to be the "normal" one. Nothing in this module or its
callers has been exercised on a real non-macOS system -- the Linux/Windows
mappings below are written from documented `platform.system()` values, not
verified against real hardware. Treat them as a reasonable assumption, not a
confirmed fact, until someone actually runs checkn there.
"""

import platform

MACOS = "macos"
LINUX = "linux"
WINDOWS = "windows"

_PLATFORM_SYSTEM_TO_OS = {
    "Darwin": MACOS,
    "Linux": LINUX,
    "Windows": WINDOWS,
}


def current_os() -> str:
    """
    Return checkn's normalized name for the current OS (one of MACOS,
    LINUX, WINDOWS), or platform.system()'s own lowercased value if it's
    not one we recognize.
    """
    system = platform.system()
    return _PLATFORM_SYSTEM_TO_OS.get(system, system.lower())


def is_supported(required_os: str | None) -> bool:
    """
    Check whether the current OS satisfies a probe's required_os
    declaration. None means "no restriction, works on any OS".
    """
    return required_os is None or current_os() == required_os
