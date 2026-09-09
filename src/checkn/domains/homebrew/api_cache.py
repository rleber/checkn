"""
Shared access to Homebrew's own locally cached formula/cask name lists.

FORMULA_NAMES_PATH and CASK_NAMES_PATH point at Homebrew's private on-disk
cache of every known formula/cask name, kept fresh by the user's own
`brew update`. This is *not* a documented, versioned Homebrew API -- it is
simply the same file Homebrew's own CLI happens to read internally (true
as of Homebrew 6.x, observed by inspecting ~/Library/Caches/Homebrew/api/
directly). A future Homebrew release could move, rename, or reformat it
without notice.

Nothing here depends on the file being present or well-formed to keep
working: read_names() treats a missing file or an implausibly small one
(almost certainly truncated, empty, or holding something other than a
plain name-per-line list -- e.g. an error page) as a failed read and
returns [], the same "fetch failed" signal every other probe uses. That
lets CacheableNameProbe.reload() do what it already does for any failed
fetch: warn on stderr, leave whatever was previously cached untouched, and
report the probe as failed in `checkn-cache status` -- rather than the
probe crashing or silently caching an empty/wrong result as if it were
real data.
"""

import sys
from pathlib import Path

HOMEBREW_API_CACHE_DIR = Path.home() / "Library/Caches/Homebrew/api"
FORMULA_NAMES_PATH = HOMEBREW_API_CACHE_DIR / "formula_names.txt"
CASK_NAMES_PATH = HOMEBREW_API_CACHE_DIR / "cask_names.txt"

# Real formula/cask lists run into the thousands (~8,500 formulas, ~7,700
# casks as of this writing). Anything drastically smaller almost certainly
# means the file is empty, truncated, or holds something other than a
# plain name-per-line list -- not that Homebrew's catalog genuinely
# shrank overnight.
MIN_PLAUSIBLE_ENTRIES = 100


def read_names(path: Path, label: str) -> list[str]:
    """
    Read a Homebrew name-list cache file and return its lines. If the file
    is missing, or has implausibly few lines to be genuine, print an
    informative warning to stderr and return [] instead of raising or
    returning something that looks like real (but wrong) data.
    """
    if not path.exists():
        print(
            f"warning: Homebrew's {label} name cache is missing ({path}) -- "
            "try running `brew update`.",
            file=sys.stderr,
        )
        return []

    names = path.read_text().splitlines()
    if len(names) < MIN_PLAUSIBLE_ENTRIES:
        print(
            f"warning: Homebrew's {label} name cache at {path} has only "
            f"{len(names)} entries, which looks truncated or malformed "
            "rather than genuine -- try running `brew update`.",
            file=sys.stderr,
        )
        return []

    return names
