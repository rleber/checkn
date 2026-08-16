#!/usr/bin/env python3

"""
checkn.py

Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

usage:
pip install checkn
checkn foo
"""

import argparse
import sys

from checkn import __version__
from checkn.git_definition import GitDefinition
from checkn.python_definition import PythonDefinition
from checkn.ruby_definition import RubyDefinition
from checkn.shell_definition import ShellDefinition


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="checkn",
        description="Check if a name is defined Python name",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("name", help="Name to check")
    parsed_args = parser.parse_args(args)
    name = parsed_args.name
    results = check_contexts(name)

    definition_count = 0
    for info in results:
        if info.definition is not None:
            print(f"{info.context}: {info.definition}")
            definition_count += 1

    if definition_count == 0:
        print("undefined")


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
