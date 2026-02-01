from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParseOptions:
    include_paths: list[str] = field(default_factory=list)
    exclude_paths: list[str] = field(default_factory=list)
    follow_symlinks: bool = False
    module_depth: Optional[int] = 1
    fail_on_parse_error: bool = False


@dataclass
class RenderOptions:
    output_format: str = "md-nextra"
    output_extension: str | None = None
    include_types: list[str] = field(default_factory=list)
    exclude_types: list[str] = field(default_factory=list)
    include_private: bool = False
    include_dunder: bool = False
    sort: str = "source-order"  # source-order, alpha
    flatten: bool = False
    split: str = "off"  # off, only, hybrid
    index_title: str = "Overview"
    docstring_style: str = "python-fences"  # raw, python-fences, preserve
    code_fence_language: str = "python"
    show_line_numbers: bool = True

    @property
    def extension(self) -> str:
        if self.output_extension:
            return self.output_extension
        return ".mdx" if self.output_format == "md-nextra" else ".md"


@dataclass
class ExportOptions:
    render: RenderOptions = field(default_factory=RenderOptions)
    parse: ParseOptions = field(default_factory=ParseOptions)
    clean: bool = True
