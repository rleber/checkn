#!/usr/bin/env python3

"""
Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

The checks appropriate for each context (e.g. Ruby) are defined in a context
class. Context classes are defined in files contained in the contexts directory.
Context class definitions are dynamically loaded from those files -- so additional
contexts may easily be defined by adding definitions to the definitions directory.

usage:
pip install checkn
checkn foo
checkn foo -c python -c ruby
checkn -l
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Annotated

import typer

from checkn import __version__
from checkn.contexts.base_context import BaseContext

app = typer.Typer(
    name="checkn",
    help="Check if a name is already defined somewhere",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Output application version and exit execution. Side-effects: stdout, sys.exit."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def list_contexts_callback(value: bool) -> None:
    """List all available contexts and exit execution. Side-effects: stdout, sys.exit."""
    if value:
        contexts = get_contexts()
        if not contexts:
            typer.echo("No contexts found.")
        else:
            typer.echo("Available contexts:")
            for key in sorted(contexts.keys()):
                typer.echo(f"  - {key}")
        raise typer.Exit()


def get_contexts() -> dict[str, type[BaseContext]]:
    """Scan the 'contexts' directory and discover context classes."""
    contexts_dir = Path(__file__).parent / "contexts"
    package_prefix = "checkn.contexts"
    registry: dict[str, type[BaseContext]] = {}

    if not contexts_dir.exists() or not contexts_dir.is_dir():
        return registry

    for _, module_name, _ in pkgutil.iter_modules([str(contexts_dir)]):
        if module_name == "base_context":
            continue

        full_module_name = f"{package_prefix}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
        except ImportError:
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BaseContext)
                and obj is not BaseContext
                and obj.__module__ == full_module_name
            ):
                context_key = obj.__name__.removesuffix("Context").lower()
                registry[context_key] = obj

    return registry


def filter_contexts(
    available_contexts: dict[str, type[BaseContext]],
    selected_contexts: list[str] | None,
) -> dict[str, type[BaseContext]]:
    """Filter context registry against user-requested context keys. Side-effects: stderr."""
    if not selected_contexts:
        return available_contexts

    requested_keys: set[str] = set()
    for item in selected_contexts:
        for sub_item in item.split(","):
            cleaned = sub_item.strip().lower()
            if cleaned:
                requested_keys.add(cleaned)

    filtered: dict[str, type[BaseContext]] = {}
    for key in requested_keys:
        if key in available_contexts:
            filtered[key] = available_contexts[key]
        else:
            typer.echo(
                f"Warning: Context '{key}' not found. Available: {', '.join(sorted(available_contexts.keys()))}",
                err=True,
            )

    return filtered


def check_context(
    context_class: type[BaseContext], name: str
) -> BaseContext.Definition:
    """Check the meaning of a name in a single context."""
    return context_class(name).info


def check_contexts(
    contexts: dict[str, type[BaseContext]], name: str
) -> list[BaseContext.Definition]:
    """Check the meaning of a name in multiple single contexts."""
    return [check_context(cls, name) for cls in contexts.values()]


def list_definitions(
    name: str, selected_contexts: list[str] | None = None
) -> list[BaseContext.Definition]:
    """Retrieve context definitions for a given target, constrained by optional context filters."""
    contexts = get_contexts()
    active_contexts = filter_contexts(contexts, selected_contexts)
    return check_contexts(active_contexts, str(name))


def print_definitions(definitions: list[BaseContext.Definition]) -> None:
    """Print formatted non-null definition records. Side-effects: stdout."""
    for info in definitions:
        if info.definition is not None:
            typer.echo(f"{info.context}: {info.definition}")


@app.command()
def check_name(
    name: Annotated[
        str | None,
        typer.Argument(help="Name to check"),
    ] = None,
    context: Annotated[
        list[str] | None,
        typer.Option(
            "-c",
            "--context",
            help="Limit check to specific context(s) (e.g. -c python -c ruby).",
        ),
    ] = None,
    list_contexts: Annotated[
        bool | None,
        typer.Option(
            "-l",
            "--list-contexts",
            callback=list_contexts_callback,
            is_eager=True,
            help="List all dynamically registered contexts and exit.",
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
    """Check the meaning of a name in multiple contexts. Side-effects: stdout, stderr."""
    if name is None:
        typer.echo("Error: Missing argument 'NAME'. Use --help for usage.", err=True)
        raise typer.Exit(code=1)

    results = list_definitions(str(name), selected_contexts=context)
    defined_results = [r for r in results if r.definition is not None]

    if not defined_results:
        typer.echo("undefined")
    else:
        print_definitions(results)


def entry() -> None:
    """CLI entrypoint launcher. Side-effects: app invocation."""
    app()


if __name__ == "__main__":
    app()
