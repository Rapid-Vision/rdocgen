"""
Data models representing parsed documentation structure.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ArgumentDoc:
    name: str  # argument name (with * or ** prefix if applicable)
    annotation: Optional[str]  # annotation string if present
    comment: str  # inline comment text attached to the argument
    lineno: int  # source line number


@dataclass
class FunctionDoc:
    name: str  # function name
    docstring: str  # cleaned docstring text
    arguments: List[ArgumentDoc]  # parsed argument docs
    returns: Optional[str]  # return annotation string if present
    returns_self: bool  # True if all returns are a bare name (Self-like)
    decorators: List[str]  # decorator expressions as strings
    signature: str  # signature string for rendering
    lineno: int  # source line number
    is_private: bool  # True for underscore-prefixed names


@dataclass
class AttributeDoc:
    name: str  # attribute name
    annotation: str  # annotation string
    comment: str  # inline comment text attached to the attribute
    lineno: int  # source line number


@dataclass
class EnumVariantDoc:
    name: str  # enum variant name
    comment: str  # inline comment text attached to the variant
    lineno: int  # source line number


@dataclass
class EnumDoc:
    name: str  # enum class name
    docstring: str  # cleaned docstring text
    variants: List[EnumVariantDoc]  # parsed enum variants
    lineno: int  # source line number
    is_private: bool  # True for underscore-prefixed names


@dataclass
class ClassDoc:
    name: str  # class name
    bases: List[str]  # base class expressions as strings
    docstring: str  # cleaned docstring text
    methods: List[FunctionDoc]  # parsed methods
    attributes: List[AttributeDoc]  # parsed annotated attributes
    lineno: int  # source line number
    is_private: bool  # True for underscore-prefixed names


@dataclass
class FileDoc:
    path: str  # filesystem path to the source file
    module_name: str  # dotted module path for this file
    docstring: str  # module docstring text
    classes: List[ClassDoc] = field(default_factory=list)  # classes in file
    enums: List[EnumDoc] = field(default_factory=list)  # enums in file
    functions: List[FunctionDoc] = field(default_factory=list)  # functions in file


@dataclass
class ModuleDoc:
    name: str  # module grouping name
    path: str  # path used for grouping (informational)
    files: List[FileDoc] = field(default_factory=list)  # files in this module


@dataclass
class ProjectDoc:
    name: str  # project name
    root_path: str  # root path used for discovery
    modules: List[ModuleDoc] = field(default_factory=list)  # modules in project
