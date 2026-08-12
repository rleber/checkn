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
        """
        class_list = definition.get_all_stdlib_classes()
        matching_modules = [cls_info for cls_info in class_list if cls_info[2] == name]
        if len(matching_modules) == 0:
            print(f"{name} is not a module or class in the Python standard library")
            exit(1)
        for module_name, installer, _ in matching_modules:
            if installer is None:
                print(
                    f"{name} is a class in the {module_name} module of the Python standard library"
                )
            else:
                print(
                    f"{name} is a class in the {matching_modules} modules installed by {installer}"
                )"""


main()
