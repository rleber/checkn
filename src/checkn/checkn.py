#!/usr/bin/env python3

# Check if a name is in common use (e.g. as a Python module, Ruby gem, etc.)

import argparse
import sys

import inflect
from python_definition import PythonDefinition

# TODO Should have a refresh function


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="checkn",
        description="Check if a name is defined Python name",
    )
    parser.add_argument("name", help="Name to check")
    parsed_args = parser.parse_args(args)
    name = parsed_args.name
    definition = PythonDefinition(name)
    module_type = definition.basic_type

    p = inflect.engine()

    if module_type:
        print(f"{name} is {p.a(module_type)}")
    else:
        print(f"{name} is unknown")


main()
