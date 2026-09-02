#!/usr/bin/env python3

"""
Time how long each NameTest probe takes to run, averaged across a handful of
sample names. Intended to identify which probes are the best caching
candidates (see instructions.md).

usage:
python scripts/time_tests.py
python scripts/time_tests.py -d python -d ruby
"""

from __future__ import annotations

import argparse
import statistics
import time

from checkn.cli import get_domains

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


def main() -> None:
    """
    Time every registered NameTest and print average duration, slowest first.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-d", "--domain", action="append", help="Limit to specific domain(s)."
    )
    parser.add_argument(
        "-n",
        "--names",
        nargs="+",
        default=SAMPLE_NAMES,
        help="Sample names to average over.",
    )
    args = parser.parse_args()

    domains = get_domains()
    if args.domain:
        requested = {d.lower() for d in args.domain}
        domains = {k: v for k, v in domains.items() if k in requested}

    results = []
    for domain_key, name_domain in sorted(domains.items()):
        lab = name_domain.lab
        for title in lab.list():
            print(f"timing {domain_key}: {title}...")
            durations = time_test(lab.execute, title, args.names)
            if not durations:
                continue
            results.append((domain_key, title, statistics.mean(durations), len(durations)))

    results.sort(key=lambda r: r[2], reverse=True)

    print()
    print(f"{'domain':<10} {'test':<25} {'avg ms':>10} {'samples':>8}")
    for domain_key, title, avg_seconds, sample_count in results:
        print(f"{domain_key:<10} {title:<25} {avg_seconds * 1000:>10.2f} {sample_count:>8}")


if __name__ == "__main__":
    main()
