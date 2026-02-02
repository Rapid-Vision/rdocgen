"""
Configuration dataclasses for parsing and rendering.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class ParseOptions:
    """Configuration for filesystem traversal and parsing behavior."""

    include_paths: list[str] = field(default_factory=list)  # glob patterns to include
    exclude_paths: list[str] = field(default_factory=list)  # glob patterns to exclude
    project_name: Optional[str] = None  # override for the displayed project name
    follow_symlinks: bool = False  # follow directory symlinks in traversal
    module_depth: Optional[int] = 1  # grouping depth for module buckets
    fail_on_parse_error: bool = False  # raise on SyntaxError


@dataclass
class RenderOptions:
    """Configuration for how parsed docs are rendered into markdown."""

    output_format: Literal["md-nextra", "md-plain"] = "md-nextra"  # output format
    output_extension: str | None = None  # override for .md/.mdx
    include_types: list[str] = field(default_factory=list)  # sections to include
    exclude_types: list[str] = field(default_factory=list)  # sections to exclude
    include_private: bool = False  # include underscore-prefixed items
    include_dunder: bool = False  # include __dunder__ names
    sort: Literal["source-order", "alpha"] = "source-order"  # order of definitions
    flatten: bool = False  # emit a single output file
    split: Literal["off", "only", "hybrid"] = "off"  # split output mode
    index_title: str = "Overview"  # title for root index page
    docstring_style: str = "python-fences"  # raw, python-fences, preserve
    code_fence_language: str = "python"  # language for unlabeled fences
    show_line_numbers: bool = True  # add showLineNumbers in fences

    @property
    def extension(
        self,  # render options instance
    ) -> str:
        if self.output_extension:
            return self.output_extension
        return ".mdx" if self.output_format == "md-nextra" else ".md"


@dataclass
class ExportOptions:
    """Top-level export configuration (parse + render + output behavior)."""

    render: RenderOptions = field(default_factory=RenderOptions)  # render settings
    parse: ParseOptions = field(default_factory=ParseOptions)  # parse settings
    clean: bool = True  # delete output directory before export
