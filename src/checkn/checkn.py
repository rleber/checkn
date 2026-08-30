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
    """Output application version and exit execution."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def get_contexts() -> dict[str, type[BaseContext]]:
    """
    Scan the 'contexts' directory and discover context classes.
    """
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


def check_context(
    context_class: type[BaseContext], name: str
) -> BaseContext.Definition:
    """
    Check the meaning of a name in a single context.
    """
    return context_class(name).info


def check_contexts(
    contexts: dict[str, type[BaseContext]], name: str
) -> list[BaseContext.Definition]:
    """
    Check the meaning of a name in multiple single contexts.
    """
    return [check_context(cls, name) for cls in contexts.values()]


@app.command()
def check_name(
    name: Annotated[str, typer.Argument(..., help="Name to check")],
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
    """Check the meaning of a name in multiple contexts"""

    results = list_definitions(str(name))
    if len(results) == 0:
        print("undefined")
    else:
        print_definitions(results)


def list_definitions(name: str) -> list[BaseContext.Definition]:
    contexts = get_contexts()
    return check_contexts(contexts, str(name))


def print_definitions(definitions: list[BaseContext.Definition]) -> None:
    for info in definitions:
        if info.definition is not None:
            print(f"{info.context}: {info.definition}")


def entry() -> None:
    """CLI entrypoint launcher."""
    app()


if __name__ == "__main__":
    app()
