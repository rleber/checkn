#!/usr/bin/env python3

"""
Time how long each NameTest probe takes to run, averaged across a handful of
sample names. Intended to identify which probes are the best caching
candidates (see instructions.md).

usage:
python scripts/time_tests.py
python scripts/time_tests.py -d python -d ruby
python scripts/time_tests.py -n requests -n flask
"""

from __future__ import annotations

import statistics
import time
from datetime import datetime
from typing import Annotated

import typer

from checkn.cli import get_domains

app = typer.Typer(add_completion=False)

SAMPLE_NAMES = ["requests", "flask", "os", "class", "print", "zzzqqqnotarealname"]


def time_test(execute: "callable[[str, str], str]", title: str, names: list[str]) -> list[float]:
    """
    Run one NameTest by title against each sample name and return elapsed
    seconds per run.
    """
    durations = []
    for name in names:
        start = time.perf_counter()
        try:
            execute(title, name)
        except Exception as exc:  # noqa: BLE001 -- report and keep timing others
            print(f"    error running {title!r} on {name!r}: {exc}")
            continue
        durations.append(time.perf_counter() - start)
    return durations


@app.command()
def main(
    domain: Annotated[
        list[str] | None,
        typer.Option("-d", "--domain", help="Limit to specific domain(s)."),
    ] = None,
    names: Annotated[
        list[str] | None,
        typer.Option("-n", "--names", help="Sample names to average over."),
    ] = None,
    quiet: Annotated[
        bool, typer.Option("-q", "--quiet", help="Silence per-test timing output.")
    ] = False,
) -> None:
    """
    Time every registered NameTest and print average duration, slowest first.
    """
    run_started_at = datetime.now()
    run_start = time.perf_counter()

    sample_names = names if names else SAMPLE_NAMES

    domains = get_domains()
    if domain:
        requested = {d.lower() for d in domain}
        domains = {k: v for k, v in domains.items() if k in requested}

    results = []
    for domain_key, name_domain in sorted(domains.items()):
        lab = name_domain.lab
        for title in lab.list():
            if not quiet:
                print(f"timing {domain_key}: {title}...")
            durations = time_test(lab.execute, title, sample_names)
            if not durations:
                continue
            results.append((domain_key, title, statistics.mean(durations), len(durations)))

    results.sort(key=lambda r: r[2], reverse=True)

    total_elapsed = time.perf_counter() - run_start

    if not quiet:
        print()
    print("scripts/time_tests.py")
    print("Time average execution time of tests in checkn")
    print(f"run at: {run_started_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"total elapsed: {total_elapsed * 1000:,.2f} ms")
    print()
    print(f"{'domain':<10} {'test':<25} {'avg ms':>10} {'samples':>8}")
    for domain_key, title, avg_seconds, sample_count in results:
        print(f"{domain_key:<10} {title:<25} {avg_seconds * 1000:>10,.2f} {sample_count:>8}")


if __name__ == "__main__":
    app()
