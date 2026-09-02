#!/usr/bin/env python3

"""
Benchmark the overall wall-clock time of `checkn <name>` (all domains) across
a representative set of names, and report mean/median/min/max/stdev. Intended
to compare before/after results of the caching optimizations described in
instructions.md.

Each name below was chosen -- and verified against the current domain
analyses -- to land in one specific category, so that every NameTest probe
in every domain gets exercised at least once, with 5 known-to-exist names
per category. A handful of clearly-fake names are included so the
"not found anywhere" path is measured too.

Without caching in place, a full default run makes several hundred real
subprocess/network calls and can take a few minutes -- that slowness is
the baseline this script exists to measure.

usage:
python scripts/benchmark_checkn.py
python scripts/benchmark_checkn.py -r 3
"""

from __future__ import annotations

import statistics
import subprocess
import time
from typing import Annotated

import typer

app = typer.Typer(add_completion=False)

NAMES = [
    # git: repository (owned by the current github.user)
    "checkn", "ftype", "ripl", "lnmap", "elmer",
    # python: keyword
    "if", "for", "class", "import", "return",
    # python: builtin class
    "int", "str", "list", "dict", "bool",
    # python: builtin module
    "sys", "itertools", "errno", "gc", "marshal",
    # python: stdlib module
    "os", "json", "re", "collections", "pathlib",
    # python: installed module (distribution metadata name)
    "requests", "click", "typer", "rich", "pytest",
    # python: installable module (importable, but not the registered dist name)
    "dotenv", "yaml", "PIL", "jinja2", "markupsafe",
    # python: uninstallable module (real PyPI package, not installed locally)
    "Django", "Scrapy", "celery", "gunicorn", "uvicorn",
    # ruby: keyword
    "module", "elsif", "unless", "begin", "yield",
    # ruby: builtin class (converted via upper_camel_case)
    "string", "array", "hash", "integer", "object",
    # ruby: gem
    "rails", "rspec", "nokogiri", "rake", "sinatra",
    # shell: bash keyword / zsh keyword
    "then", "fi", "while", "done", "esac",
    # shell: builtin
    "cd", "echo", "pwd", "read", "export",
    # shell: program
    "curl", "python3", "cat", "less", "find",
    # shell: alias (discovered via the current interactive zsh)
    "ls", "grep", "git", "ll", "la",
    # shell: function (discovered via the current interactive zsh)
    "compinit", "compdef", "clipcopy", "git_prompt_status", "omz_urlencode",
    # not found in any domain
    "zzqqxxnonexistentnamezz123", "qzxvbnmasdfghjklqwert99",
    "thisisnotarealnameatall42", "xkcdfoobarbazqux77", "nonexistentnamexyz2026",
]


def time_run(name: str) -> float:
    """
    Run `checkn <name>` once and return its wall-clock duration in seconds.
    """
    start = time.perf_counter()
    subprocess.run(["checkn", name], capture_output=True, check=False)
    return time.perf_counter() - start


@app.command()
def main(
    repeat: Annotated[
        int, typer.Option("-r", "--repeat", help="Runs per name.")
    ] = 1,
    quiet: Annotated[
        bool, typer.Option("-q", "--quiet", help="Silence per-name timing output.")
    ] = False,
) -> None:
    """
    Time `checkn <name>` for every name (repeated -r times each) and print
    per-name and aggregate timing statistics.
    """
    durations = []
    for name in NAMES:
        for _ in range(repeat):
            elapsed = time_run(name)
            durations.append(elapsed)
            if not quiet:
                print(f"{name:<30} {elapsed * 1000:>10.2f} ms")

    if not quiet:
        print()
    print(f"runs:    {len(durations)}")
    print(f"total:   {sum(durations) * 1000:.2f} ms")
    print(f"mean:    {statistics.mean(durations) * 1000:.2f} ms")
    print(f"median:  {statistics.median(durations) * 1000:.2f} ms")
    print(f"min:     {min(durations) * 1000:.2f} ms")
    print(f"max:     {max(durations) * 1000:.2f} ms")
    print(f"stdev:   {(statistics.stdev(durations) if len(durations) > 1 else 0.0) * 1000:.2f} ms")


if __name__ == "__main__":
    app()
