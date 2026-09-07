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

from datetime import datetime
from typing import Annotated

import typer

from checkn.cache import CacheDB
from checkn.cli import get_domains
from checkn.core.cacheable_probe import CacheableNameProbe

app = typer.Typer(
    name="checkn-cache",
    help="Manage checkn's persistent cache",
    add_completion=False,
)

DomainOption = Annotated[
    list[str] | None,
    typer.Option("-d", "--domain", help="Limit to specific domain(s)."),
]


def _cacheable_probes(domains: list[str] | None) -> list[CacheableNameProbe]:
    """
    Collect every CacheableNameProbe instance across all domains, or only the
    requested ones.
    """
    all_domains = get_domains()
    if domains:
        requested = {d.lower() for d in domains}
        all_domains = {k: v for k, v in all_domains.items() if k in requested}

    probes = []
    for name_domain in all_domains.values():
        lab = name_domain.lab
        for title in lab.list():
            item = lab.item(title)
            if isinstance(item, CacheableNameProbe):
                probes.append(item)
    return probes


@app.command()
def build() -> None:
    """
    Ensure the cache schema exists and reload every cacheable probe.
    """
    cache = CacheDB()
    for probe in _cacheable_probes(domains=None):
        print(f"reloading {probe.domain}: {probe.title}...")
        probe.reload(cache)


@app.command()
def reload(domain: DomainOption = None) -> None:
    """
    Reload cacheable probes, for all domains or only the ones given.
    """
    cache = CacheDB()
    probes = _cacheable_probes(domain)
    if not probes:
        print("No cacheable probes match.")
        raise typer.Exit(code=1)
    for probe in probes:
        print(f"reloading {probe.domain}: {probe.title}...")
        probe.reload(cache)


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


def _format_updated_at(value: str | None) -> str:
    """
    Render a stored UTC ISO timestamp as a simplified, local-time string.
    """
    if value is None:
        return "(never)"
    return datetime.fromisoformat(value).astimezone().strftime("%Y-%m-%d %H:%M %Z")


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

    print(f"{'domain':<10} {'probe':<20} {'entries':>10}  updated_at (local)")
    for row in rows:
        updated_at = _format_updated_at(row.updated_at)
        print(f"{row.domain:<10} {row.probe:<20} {row.entry_count:>10,}  {updated_at}")


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
