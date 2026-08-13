#!/usr/bin/env python3

"""
base_definition.py
Base class for context definition classes (e.g. RubyDefinition)
"""

from typing import NamedTuple


class BaseDefinition:
    class Definition(NamedTuple):
        context: str
        name: str
        definition: str
        details: dict
