from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ArgumentDoc:
    name: str
    annotation: Optional[str]
    comment: str
    lineno: int


@dataclass
class FunctionDoc:
    name: str
    docstring: str
    arguments: List[ArgumentDoc]
    returns: Optional[str]
    returns_self: bool
    decorators: List[str]
    signature: str
    lineno: int
    is_private: bool


@dataclass
class AttributeDoc:
    name: str
    annotation: str
    comment: str
    lineno: int


@dataclass
class EnumVariantDoc:
    name: str
    comment: str
    lineno: int


@dataclass
class EnumDoc:
    name: str
    docstring: str
    variants: List[EnumVariantDoc]
    lineno: int
    is_private: bool


@dataclass
class ClassDoc:
    name: str
    bases: List[str]
    docstring: str
    methods: List[FunctionDoc]
    attributes: List[AttributeDoc]
    lineno: int
    is_private: bool


@dataclass
class FileDoc:
    path: str
    module_name: str
    docstring: str
    classes: List[ClassDoc] = field(default_factory=list)
    enums: List[EnumDoc] = field(default_factory=list)
    functions: List[FunctionDoc] = field(default_factory=list)


@dataclass
class ModuleDoc:
    name: str
    path: str
    files: List[FileDoc] = field(default_factory=list)


@dataclass
class ProjectDoc:
    name: str
    root_path: str
    modules: List[ModuleDoc] = field(default_factory=list)
