"""
This module is used as an example of doc generation.

It doesn't have any useful functions or classes but is meant to represent everything that this project can generate.
"""

from enum import Enum
from typing import Literal, Optional, Callable
import random


class ExampleClass:
    """
    This is an example of class doc generation
    """

    literal_attr: Literal["one", "two"]  # example of a literal attribute
    name: str  # instance name
    count: int  # instance counter

    def __init__(
        self,
        name: str,  # example constructor name
        count: int = 0,  # example counter value
    ):
        """__init__ method mock"""
        self.name = name
        self.count = count

    def increment(
        self,
        step: int,  # value to add
    ) -> int:
        """
        Increase the internal counter by the given step.
        """
        self.count += step
        return self.count

    def rename(
        self,
        new_name: str,  # new name to set
    ) -> "ExampleClass":
        """
        Return self after changing the name.
        """
        self.name = new_name
        return self


class ExampleEnum(Enum):
    """
    This is an example enum used for variant rendering.
    """

    FIRST = "first"  # first option
    SECOND = "second"  # second option


def example_function(
    value: int,  # input integer
    label: Optional[str] = None,  # optional label
    test: Callable[
        [random.Random], dict | int
    ] = None,  # Samples a params dict from RNG
) -> str:
    """
    Format a value with an optional label.
    """
    if label:
        return f"{label}: {value}"
    return str(value)


def example_returns_self(
    value: int,  # value used to build the instance
) -> ExampleClass:
    """
    Example of a function returning a new instance.
    """
    return ExampleClass(name=str(value), count=value)
