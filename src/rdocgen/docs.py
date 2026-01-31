from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .parser import (
    AttributeDoc,
    ClassDoc,
    EnumDoc,
    FileDoc,
    FunctionDoc,
    ModuleDoc,
    ParseOptions,
    ProjectDoc,
    parse_path,
)


@dataclass
class ExportOptions:
    output_format: str = "md-nextra"
    output_extension: str | None = None
    clean: bool = True
    include_types: list[str] = field(default_factory=list)
    exclude_types: list[str] = field(default_factory=list)
    include_private: bool = False
    include_dunder: bool = False
    sort: str = "source-order"  # source-order, alpha
    flatten: bool = False
    index_title: str = "Overview"
    docstring_style: str = "python-fences"  # raw, python-fences, preserve
    code_fence_language: str = "python"
    show_line_numbers: bool = True
    parse_options: ParseOptions = field(default_factory=ParseOptions)

    @property
    def extension(self) -> str:
        if self.output_extension:
            return self.output_extension
        return ".mdx" if self.output_format == "md-nextra" else ".md"


class MarkdownExporter:
    def __init__(self, options: ExportOptions) -> None:
        self.options = options

    def export_project(self, project: ProjectDoc, outdir: str) -> None:
        self._prepare_output_dir(outdir)

        index_path = os.path.join(outdir, f"index{self.options.extension}")
        with open(index_path, "w", encoding="utf-8") as fout:
            fout.write(self._project_overview(project))

        if self.options.flatten:
            with open(index_path, "a", encoding="utf-8") as fout:
                for module in project.modules:
                    fout.write(f"\n## Module: `{module.name}`\n\n")
                    for file_doc in module.files:
                        fout.write(self._file_markdown(file_doc, heading_level=3))
            return

        modules_dir = os.path.join(outdir, "modules")
        os.makedirs(modules_dir, exist_ok=True)

        for module in project.modules:
            module_dir = os.path.join(modules_dir, module.name)
            os.makedirs(module_dir, exist_ok=True)
            module_index = os.path.join(module_dir, f"index{self.options.extension}")
            with open(module_index, "w", encoding="utf-8") as fout:
                fout.write(self._module_overview(module))

            for file_doc in module.files:
                file_name = self._file_output_name(file_doc)
                file_path = os.path.join(module_dir, f"{file_name}{self.options.extension}")
                with open(file_path, "w", encoding="utf-8") as fout:
                    fout.write(self._file_markdown(file_doc))

    def _prepare_output_dir(self, outdir: str) -> None:
        if os.path.exists(outdir) and self.options.clean:
            shutil.rmtree(outdir)
        os.makedirs(outdir, exist_ok=True)

    def _project_overview(self, project: ProjectDoc) -> str:
        content = [f"# {self.options.index_title}", "", f"Project: `{project.name}`", "", "## Modules", ""]
        if not project.modules:
            content.append("_No modules found._")
        else:
            for module in project.modules:
                content.append(f"- `{module.name}`")
        content.append("")
        return "\n".join(content)

    def _module_overview(self, module: ModuleDoc) -> str:
        content = [f"# Module: `{module.name}`", "", "## Files", ""]
        if not module.files:
            content.append("_No files found._")
        else:
            for file_doc in module.files:
                content.append(f"- `{self._file_output_name(file_doc)}`")
        content.append("")
        return "\n".join(content)

    def _file_output_name(self, file_doc: FileDoc) -> str:
        base = os.path.basename(file_doc.path)
        name = os.path.splitext(base)[0]
        if name == "__init__":
            return "index"
        return name

    def _file_markdown(self, file_doc: FileDoc, *, heading_level: int = 1) -> str:
        file_heading = "#" * heading_level
        content: list[str] = [
            f"{file_heading} File: `{os.path.basename(file_doc.path)}`",
            "",
        ]

        docstring = self._rewrite_docstring(file_doc.docstring)
        if docstring:
            content.append(docstring)
            content.append("")

        classes = self._filter_items(file_doc.classes, "class")
        enums = self._filter_items(file_doc.enums, "enum")
        functions = self._filter_items(file_doc.functions, "function")

        section_level = heading_level + 1
        content.extend(self._section_for_classes(classes, section_level=section_level))
        content.extend(self._section_for_enums(enums, section_level=section_level))
        content.extend(self._section_for_functions(functions, section_level=section_level))

        return "\n".join(content).rstrip() + "\n"

    def _section_for_classes(self, classes: Iterable[ClassDoc], *, section_level: int) -> list[str]:
        classes = list(classes)
        if not classes:
            return []

        content = [f"{'#' * section_level} Classes", ""]
        for cls in classes:
            content.append(f"{'#' * (section_level + 1)} {cls.name}")
            if cls.bases:
                content.append(f"Inherits from: {', '.join(f'`{b}`' for b in cls.bases)}")
                content.append("")

            docstring = self._rewrite_docstring(cls.docstring)
            if docstring:
                content.append(docstring)
                content.append("")

            methods = self._filter_items(cls.methods, "function")
            attributes = self._filter_items(cls.attributes, "attribute")

            if methods:
                content.append(f"{'#' * (section_level + 2)} Methods")
                content.append("")
                for method in methods:
                    content.extend(self._function_markdown(method, heading_level=section_level + 3))

            if attributes:
                content.append(f"{'#' * (section_level + 2)} Attributes")
                content.append("")
                for attr in attributes:
                    content.extend(self._attribute_markdown(attr, heading_level=section_level + 3))

            content.append("---")
            content.append("")
        return content

    def _section_for_enums(self, enums: Iterable[EnumDoc], *, section_level: int) -> list[str]:
        enums = list(enums)
        if not enums:
            return []

        content = [f"{'#' * section_level} Enums", ""]
        for enm in enums:
            content.append(f"{'#' * (section_level + 1)} {enm.name}")
            docstring = self._rewrite_docstring(enm.docstring)
            if docstring:
                content.append(docstring)
                content.append("")

            if enm.variants:
                content.append(f"{'#' * (section_level + 2)} Variants")
                content.append("")
                for variant in enm.variants:
                    content.append(f"- `{variant.name}`")
                    if variant.comment:
                        content.append(f"  - {variant.comment}")
            content.append("")
            content.append("---")
            content.append("")
        return content

    def _section_for_functions(self, functions: Iterable[FunctionDoc], *, section_level: int) -> list[str]:
        functions = list(functions)
        if not functions:
            return []

        content = [f"{'#' * section_level} Functions", ""]
        for func in functions:
            content.extend(self._function_markdown(func, heading_level=section_level + 1))
        return content

    def _function_markdown(self, func: FunctionDoc, *, heading_level: int) -> list[str]:
        heading = "#" * heading_level
        content = [f"{heading} {func.name}", ""]

        docstring = self._rewrite_docstring(func.docstring)
        if docstring:
            content.append(docstring)
            content.append("")

        content.append("**Signature**")
        content.append("")
        content.append(self._code_block(func.signature))
        content.append("")

        content.append("**Arguments**")
        content.append("")
        for arg in func.arguments:
            if arg.name == "self" or arg.name.startswith("_"):
                continue
            line = f"- **`{arg.name}`**"
            if arg.annotation:
                line += f" : {self._inline_type(arg.annotation)}"
            if arg.comment:
                line += f" — {arg.comment}"
            content.append(line)
        content.append("")

        returns_line = self._returns_line(func)
        if returns_line:
            content.append(returns_line)
            content.append("")

        content.append("---")
        content.append("")
        return content

    def _attribute_markdown(self, attr: AttributeDoc, *, heading_level: int) -> list[str]:
        heading = "#" * heading_level
        content = [f"{heading} `{attr.name}`", ""]
        content.append(f"Type: {self._inline_type(attr.annotation)}")
        content.append("")
        if attr.comment:
            content.append(attr.comment)
            content.append("")
        return content

    def _filter_items(self, items: Sequence, item_type: str) -> list:
        include_types = set(self.options.include_types)
        exclude_types = set(self.options.exclude_types)
        if include_types and item_type not in include_types:
            return []
        if exclude_types and item_type in exclude_types:
            return []

        filtered = []
        for item in items:
            name = getattr(item, "name", "")
            if not self._name_allowed(name):
                continue
            filtered.append(item)

        if self.options.sort == "alpha":
            filtered.sort(key=lambda obj: getattr(obj, "name", "").lower())
        return filtered

    def _name_allowed(self, name: str) -> bool:
        if name.startswith("__") and name.endswith("__"):
            return self.options.include_dunder
        if name.startswith("_"):
            return self.options.include_private
        return True

    def _returns_line(self, func: FunctionDoc) -> str | None:
        if func.returns_self:
            return f"**Returns**: {self._inline_type('Self')}"
        if func.returns:
            return f"**Returns**: {self._inline_type(func.returns)}"
        return None

    def _inline_type(self, annotation: str) -> str:
        if self.options.output_format == "md-nextra":
            return f"`{annotation}{{:python}}`"
        return f"`{annotation}`"

    def _code_block(self, code: str) -> str:
        if self.options.output_format == "md-nextra":
            suffix = " showLineNumbers" if self.options.show_line_numbers else ""
            return f"```python copy{suffix}\n{code}\n```"
        return f"```python\n{code}\n```"

    def _rewrite_docstring(self, docstring: str) -> str:
        if not docstring:
            return ""
        if self.options.output_format == "md-plain":
            return docstring
        if self.options.output_format != "md-nextra":
            raise ValueError(f"Unsupported output format: {self.options.output_format}")
        if self.options.docstring_style == "raw":
            return docstring

        lines = docstring.splitlines()
        output: list[str] = []
        in_code = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                if not in_code:
                    output.append(self._rewrite_opening_fence(stripped))
                    in_code = True
                else:
                    output.append("```")
                    in_code = False
            else:
                output.append(line)
        return "\n".join(output)

    def _rewrite_opening_fence(self, fence: str) -> str:
        suffix = " showLineNumbers" if self.options.show_line_numbers else ""
        if self.options.docstring_style == "preserve":
            if "copy" in fence:
                return fence if suffix.strip() in fence else f"{fence}{suffix}"
            return f"{fence} copy{suffix}" if fence != "```" else f"``` copy{suffix}"
        if self.options.docstring_style == "python-fences":
            if fence == "```":
                return f"```{self.options.code_fence_language} copy{suffix}"
            if "copy" in fence:
                return fence if suffix.strip() in fence else f"{fence}{suffix}"
            return f"{fence} copy{suffix}"
        return fence


def export_docs(codepath: str, outdir: str, options: ExportOptions) -> None:
    project = parse_path(codepath, options=options.parse_options)
    exporter = MarkdownExporter(options)
    exporter.export_project(project, outdir)
