#!/usr/bin/env python3

"""
checkn.py

Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

usage:
pip install checkn
checkn foo
"""

# TODO Change context classes to inherit from a ContextDefinition root class
# TODO Change return to use context.info method and return structured data

import argparse
import sys

from checkn.git_definition import GitDefinition
from checkn.python_definition import PythonDefinition
from checkn.ruby_definition import RubyDefinition

# TODO Should have a refresh function


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="checkn",
        description="Check if a name is defined Python name",
    )
    parser.add_argument("name", help="Name to check")
    parsed_args = parser.parse_args(args)
    name = parsed_args.name
    results = check_contexts(name)

    definition_count = 0
    for result in results:
        context, type = result
        if type:
            print(f"{context}: {type}")
            definition_count += 1

    if definition_count == 0:
        print("undefined")


CONTEXTS = {
    "git": GitDefinition,
    "python": PythonDefinition,
    "ruby": RubyDefinition,
}


def check_contexts(name: str) -> None:
    context_definitions = []
    for context_name, context_class in CONTEXTS.items():
        context_definitions.append((context_name, check_context(context_class, name)))
    return context_definitions


def check_context(context_class: type, name: str) -> str:
    return context_class(name).type
