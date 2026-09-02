#!/usr/bin/env python3

"""
Manage checkn's persistent cache, kept separate from `checkn` itself so the
name-checking UX never changes.

usage:
checkn-cache build
checkn-cache reload -d python
checkn-cache status
checkn-cache clear -d python
checkn-cache path
"""

from __future__ import annotations

from typing import Annotated

import typer

from checkn.cache import CacheDB
from checkn.cli import get_domains
from checkn.core.cacheable_test import CacheableNameTest

app = typer.Typer(
    name="checkn-cache",
    help="Manage checkn's persistent cache",
    add_completion=False,
)

DomainOption = Annotated[
    list[str] | None,
    typer.Option("-d", "--domain", help="Limit to specific domain(s)."),
]


def _cacheable_tests(domains: list[str] | None) -> list[CacheableNameTest]:
    """
    Collect every CacheableNameTest instance across all domains, or only the
    requested ones.
    """
    all_domains = get_domains()
    if domains:
        requested = {d.lower() for d in domains}
        all_domains = {k: v for k, v in all_domains.items() if k in requested}

    tests = []
    for name_domain in all_domains.values():
        lab = name_domain.lab
        for title in lab.list():
            item = lab.item(title)
            if isinstance(item, CacheableNameTest):
                tests.append(item)
    return tests


@app.command()
def build() -> None:
    """
    Ensure the cache schema exists and reload every cacheable test.
    """
    cache = CacheDB()
    for test in _cacheable_tests(domains=None):
        print(f"reloading {test.domain}: {test.title}...")
        test.reload(cache)


@app.command()
def reload(domain: DomainOption = None) -> None:
    """
    Reload cacheable tests, for all domains or only the ones given.
    """
    cache = CacheDB()
    tests = _cacheable_tests(domain)
    if not tests:
        print("No cacheable tests match.")
        raise typer.Exit(code=1)
    for test in tests:
        print(f"reloading {test.domain}: {test.title}...")
        test.reload(cache)


@app.command()
def clear(domain: DomainOption = None) -> None:
    """
    Clear cached rows, for all domains or only the ones given.
    """
    cache = CacheDB()
    if domain:
        for d in domain:
            cache.clear(d.lower())
    else:
        cache.clear()


@app.command()
def status(domain: DomainOption = None) -> None:
    """
    Show entry counts and last-updated times for cached sections.
    """
    cache = CacheDB()
    if domain:
        rows = [row for d in domain for row in cache.status(d.lower())]
    else:
        rows = cache.status()

    if not rows:
        print("No cache sections loaded.")
        return

    print(f"{'domain':<10} {'test':<20} {'entries':>10}  updated_at (UTC)")
    for row in rows:
        print(f"{row.domain:<10} {row.test:<20} {row.entry_count:>10,}  {row.updated_at}")


@app.command()
def path() -> None:
    """
    Print the resolved cache database path.
    """
    print(CacheDB().path)


def entry() -> None:
    """
    checkn-cache entrypoint launcher.
    """
    app()


if __name__ == "__main__":
    app()
