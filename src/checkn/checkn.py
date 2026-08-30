#!/usr/bin/env python3

"""
checkn.py

Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

usage:
pip install checkn
checkn foo
"""

from typing import Annotated

import typer

from checkn import __version__
from checkn.definitions.git_definition import GitDefinition
from checkn.definitions.python_definition import PythonDefinition
from checkn.definitions.ruby_definition import RubyDefinition
from checkn.definitions.shell_definition import ShellDefinition

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


@app.command()
def main(
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
    """Execute name resolution check and display findings to stdout."""
    results = check_contexts(str(name))

    definition_count = 0
    for info in results:
        if info.definition is not None:
            typer.echo(f"{info.context}: {info.definition}")
            definition_count += 1

    if definition_count == 0:
        typer.echo("undefined")


def entry():
    app()


if __name__ == "__main__":
    app()


CONTEXTS = {
    "git": GitDefinition,
    "python": PythonDefinition,
    "ruby": RubyDefinition,
    "shell": ShellDefinition,
}


def check_contexts(name: str) -> None:
    context_definitions = []
    for context_class in CONTEXTS.values():
        definition = context_class(name)
        context_definitions.append(definition.info)
    return context_definitions


def check_context(context_class: type, name: str) -> str:
    return context_class(name).info
