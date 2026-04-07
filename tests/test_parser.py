"""
Unit tests for the AST parser.
"""

import pathlib

import pytest

from rdocgen.parser import ParseError, parse_file, parse_source


def test_parse_source_extracts_top_level_items() -> None:
    source = '''
from enum import Enum

"""Module docstring."""

class ExampleEnum(Enum):
    """Enum docstring."""
    FIRST = 1  # first option
    SECOND = 2  # second option

class ExampleClass:
    """Class docstring."""
    name: str  # instance name

    def method(self, value: int) -> str:
        """Return the value."""
        return str(value)

def example_function(arg: int) -> int:
    """Return incremented."""
    return arg + 1
'''
    file_doc = parse_source(source, path="sample.py", module_name="sample")

    assert file_doc.module_name == "sample"
    assert len(file_doc.enums) == 1
    assert len(file_doc.classes) == 1
    assert len(file_doc.functions) == 1

    enum_doc = file_doc.enums[0]
    assert enum_doc.name == "ExampleEnum"
    assert len(enum_doc.variants) == 2
    assert enum_doc.variants[0].comment == "first option"

    class_doc = file_doc.classes[0]
    assert class_doc.name == "ExampleClass"
    assert len(class_doc.attributes) == 1
    assert class_doc.attributes[0].comment == "instance name"

    func_doc = file_doc.functions[0]
    assert func_doc.name == "example_function"


def test_parse_source_keeps_trailing_comments_for_multiline_arguments() -> None:
    source = '''
import random
import typing

class ExampleClass:
    def set_sampler(
        self,
        sampler: typing.Callable[
            [random.Random], dict
        ] = (
            lambda _rng: {}
        ),  # Samples a params dict from RNG
    ) -> None:
        pass
'''
    file_doc = parse_source(source, path="sample.py", module_name="sample")

    method = file_doc.classes[0].methods[0]
    sampler_arg = method.arguments[1]
    assert sampler_arg.name == "sampler"
    assert sampler_arg.comment == "Samples a params dict from RNG"


def test_parse_file_raises_with_location_for_syntax_error(
    tmp_path: pathlib.Path,
) -> None:
    source_path = tmp_path / "broken.py"
    source_path.write_text("def broken(:\n    pass\n", encoding="utf-8")

    with pytest.raises(ParseError, match=r"Failed to parse .*broken.py:1:12"):
        parse_file(str(source_path))
