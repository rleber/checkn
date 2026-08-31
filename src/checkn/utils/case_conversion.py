"""
case_conversion.py

Convert snake_case to UpperCamelCase
"""

import re


def is_snake_case(word: str):
    return word.lower() == word


def upper_camel_case(word: str) -> str:
    """Convert a snakecase name to a camelcase name"""
    if is_upper_camel_case(word):
        return word
    parts = re.split(r"[_-]", word)
    return "".join([part.capitalize() for part in parts])


def is_upper_camel_case(word: str) -> str:
    if len(word) == 0:
        return True
    if is_snake_case(word):
        return False
    if word[0].lower() == word[0]:
        return False
    return "_" not in word
