#!/usr/bin/env python3

"""
Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

The checks appropriate for each context (e.g. Ruby) are defined by a
NameDomain, backed by a NameLab of NameTests and its own NameAnalyses.
Domains live in subdirectories of the domains directory and are dynamically
loaded from there -- so additional domains may easily be defined by adding
a new subdirectory.

usage:
pip install checkn
checkn foo
checkn foo -c python -c ruby
checkn -l
"""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Annotated, NamedTuple

import typer

from checkn import __version__
from checkn.core.name_domain import NameDomain

app = typer.Typer(
    name="checkn",
    help="Check if a name is already defined somewhere",
    add_completion=False,
)


class DomainResult(NamedTuple):
    """
    Encapsulates the non-empty definitions a domain found for a name.
    """

    domain: str
    name: str
    definitions: list[str]


def version_callback(value: bool) -> None:
    """Output application version and exit execution. Side-effects: stdout, sys.exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def list_domains_callback(value: bool) -> None:
    """List all available domains and exit execution. Side-effects: stdout, sys.exit."""
    if value:
        domains = get_domains()
        if not domains:
            typer.echo("No domains found.")
        else:
            typer.echo("Available domains:")
            for key in sorted(domains.keys()):
                typer.echo(f"  - {key}")
        raise typer.Exit()


def get_domains() -> dict[str, NameDomain]:
    """Scan the 'domains' directory and instantiate each domain's NameDomain."""
    domains_dir = Path(__file__).parent / "domains"
    registry: dict[str, NameDomain] = {}

    if not domains_dir.exists() or not domains_dir.is_dir():
        return registry

    for entry in sorted(domains_dir.iterdir()):
        if not entry.is_dir() or not (entry / "domain.py").exists():
            continue

        full_module_name = f"checkn.domains.{entry.name}.domain"
        try:
            module = importlib.import_module(full_module_name)
        except ImportError:
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, NameDomain)
                and obj is not NameDomain
                and obj.__module__ == full_module_name
            ):
                domain_key = obj.__name__.removesuffix("Domain").lower()
                registry[domain_key] = obj()

    return registry


def filter_domains(
    available_domains: dict[str, NameDomain],
    selected_domains: list[str] | None,
) -> dict[str, NameDomain]:
    """Filter domain registry against user-requested domain keys. Side-effects: stderr."""
    if not selected_domains:
        return available_domains

    requested_keys: set[str] = set()
    for item in selected_domains:
        for sub_item in item.split(","):
            cleaned = sub_item.strip().lower()
            if cleaned:
                requested_keys.add(cleaned)

    filtered: dict[str, NameDomain] = {}
    for key in requested_keys:
        if key in available_domains:
            filtered[key] = available_domains[key]
        else:
            typer.echo(
                f"Warning: Domain '{key}' not found. Available: {', '.join(sorted(available_domains.keys()))}",
                err=True,
            )

    return filtered


def check_domain(domain: NameDomain, name: str) -> DomainResult:
    """Check the meaning of a name in a single domain."""
    definitions = [result for result in domain.execute_all(name).values() if result]
    return DomainResult(domain.title, name, definitions)


def check_domains(domains: dict[str, NameDomain], name: str) -> list[DomainResult]:
    """Check the meaning of a name across multiple domains."""
    return [check_domain(domain, name) for domain in domains.values()]


def list_definitions(
    name: str, selected_domains: list[str] | None = None
) -> list[DomainResult]:
    """Retrieve domain definitions for a given target, constrained by optional domain filters."""
    domains = get_domains()
    active_domains = filter_domains(domains, selected_domains)
    return check_domains(active_domains, str(name))


def print_definitions(definitions: list[DomainResult]) -> None:
    """Print formatted non-empty definition records. Side-effects: stdout."""
    for info in definitions:
        if info.definitions:
            defs_str = ", ".join(info.definitions)
            typer.echo(f"{info.domain}: {defs_str}")


@app.command()
def check_name(
    name: Annotated[
        str | None,
        typer.Argument(help="Name to check"),
    ] = None,
    domain: Annotated[
        list[str] | None,
        typer.Option(
            "-c",
            "--domain",
            help="Limit check to specific domain(s) (e.g. -c python -c ruby).",
        ),
    ] = None,
    list_domains: Annotated[
        bool | None,
        typer.Option(
            "-l",
            "--list-domains",
            callback=list_domains_callback,
            is_eager=True,
            help="List all dynamically registered domains and exit.",
        ),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the version and exit.",
        ),
    ] = False,
) -> None:
    """Check the meaning of a name in multiple domains. Side-effects: stdout, stderr."""
    if name is None:
        typer.echo("Error: Missing argument 'NAME'. Use --help for usage.", err=True)
        raise typer.Exit(code=1)

    results = list_definitions(str(name), selected_domains=domain)

    # Filter for domains that yielded one or more definitions
    defined_results = [r for r in results if r.definitions]

    if not defined_results:
        typer.echo("undefined")
    else:
        print_definitions(defined_results)


def entry() -> None:
    """CLI entrypoint launcher. Side-effects: app invocation."""
    app()


if __name__ == "__main__":
    app()
