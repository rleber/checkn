"""
Base class for context classes (e.g. RubyContext)
"""

from typing import NamedTuple


class BaseContext:
    class Definition(NamedTuple):
        context: str
        name: str
        definition: str
        details: dict
