from __future__ import annotations

import os
from typing import Iterable, Sequence

from ..config import RenderOptions
from ..model import (
    AttributeDoc,
    ClassDoc,
    EnumDoc,
    FileDoc,
    FunctionDoc,
    ModuleDoc,
    ProjectDoc,
)


class MarkdownRenderer:
    """Render Project/Module/File docs into Markdown or Nextra-flavored Markdown."""

    def __init__(
        self,
        options: RenderOptions,  # rendering configuration
    ) -> None:
        self.options = options

    def project_index(
        self,
        project: ProjectDoc,  # project to render
        *,
        include_module_links: bool = True,  # whether to render module links
    ) -> str:
        """Render the root project index page."""
        content = [
            f"# {self.options.index_title}",
            "",
            f"Project: `{project.name}`",
            "",
            "## Modules",
            "",
        ]
        if not project.modules:
            content.append("_No modules found._")
        elif include_module_links:
            for module in project.modules:
                module_path = os.path.join(
                    "modules", *module.name.split("."), f"index{self.options.extension}"
                )
                content.append(self._link(module.name, module_path))
        else:
            content.append("_Module links omitted in flattened output._")
        content.append("")
        return "\n".join(content)

    def module_index(
        self,
        module: ModuleDoc,  # module to render
    ) -> str:
        """Render a module index page, optionally listing split outputs."""
        content = [f"# Module: `{module.name}`", ""]

        if self.options.split != "off":
            content.append("## Classes")
            content.append("")
            class_items = []
            for file_doc in module.files:
                for cls in self._filter_items(file_doc.classes, "class"):
                    rel = self.item_output_relpath(file_doc, module.name, cls.name)
                    class_items.append(
                        self._link(
                            cls.name,
                            os.path.join("classes", f"{rel}{self.options.extension}"),
                        )
                    )
            if class_items:
                content.extend(class_items)
            else:
                content.append("_No classes found._")
            content.append("")

            content.append("## Functions")
            content.append("")
            function_items = []
            for file_doc in module.files:
                for func in self._filter_items(file_doc.functions, "function"):
                    rel = self.item_output_relpath(file_doc, module.name, func.name)
                    function_items.append(
                        self._link(
                            func.name,
                            os.path.join("functions", f"{rel}{self.options.extension}"),
                        )
                    )
            if function_items:
                content.extend(function_items)
            else:
                content.append("_No functions found._")
            content.append("")

            content.append("## Enums")
            content.append("")
            enum_items = []
            for file_doc in module.files:
                for enm in self._filter_items(file_doc.enums, "enum"):
                    rel = self.item_output_relpath(file_doc, module.name, enm.name)
                    enum_items.append(
                        self._link(
                            enm.name,
                            os.path.join("enums", f"{rel}{self.options.extension}"),
                        )
                    )
            if enum_items:
                content.extend(enum_items)
            else:
                content.append("_No enums found._")
            content.append("")
            if self.options.split == "only":
                return "\n".join(content)

        content.append("## Files")
        content.append("")
        if not module.files:
            content.append("_No files found._")
        else:
            for file_doc in module.files:
                relpath = self.file_output_relpath(file_doc, module.name)
                target = f"{relpath}{self.options.extension}"
                label = f"`{os.path.basename(file_doc.path)}`"
                content.append(
                    self._link(
                        label,
                        target,
                    )
                )
        content.append("")
        return "\n".join(content)

    def file_doc(
        self,
        file_doc: FileDoc,  # file to render
        *,
        heading_level: int = 1,  # heading level for top title
    ) -> str:
        """Render a single file page with classes, enums, and functions."""
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
        content.extend(
            self._section_for_functions(functions, section_level=section_level)
        )

        return "\n".join(content).rstrip() + "\n"

    def _link(
        self,
        label: str,  # label shown in markdown
        relpath: str,  # relative path to the target file
    ) -> str:
        return f"- [{label}]({relpath})"

    def class_doc(
        self,
        cls: ClassDoc,  # class to render
    ) -> str:
        """Render a standalone class page."""
        content: list[str] = [f"# `class {cls.name}`", ""]
        if cls.bases:
            content.append(f"Inherits from: {', '.join(f'`{b}`' for b in cls.bases)}")
            content.append("")

        docstring = self._rewrite_docstring(cls.docstring)
        if docstring:
            content.append(docstring)
            content.append("")

        methods = self._filter_items(cls.methods, "function")
        attributes = self._filter_items(cls.attributes, "attribute")

        if attributes:
            content.append("::: details Attributes")
            content.append("")
            content.append("| Name | Type | Description |")
            content.append("| - | - | - |")
            for attr in attributes:
                desc = attr.comment or ""
                content.append(f"| `{attr.name}` | `{attr.annotation}` | {desc} |")
            content.append("")
            content.append(":::")
            content.append("")

        if methods:
            content.append("::: details Methods")
            content.append("")
            for method in methods:
                content.extend(
                    self._function_markdown(
                        method,
                        heading_level=5,
                        code_heading=True,
                        include_separator=False,
                    )
                )
            content.append(":::")
            content.append("")

        return "\n".join(content).rstrip() + "\n"

    def function_doc(
        self,
        func: FunctionDoc,  # function to render
    ) -> str:
        """Render a standalone function page."""
        return "\n".join(self._function_block(func, heading_level=1)).rstrip() + "\n"

    def enum_doc(
        self,
        enm: EnumDoc,  # enum to render
    ) -> str:
        """Render a standalone enum page."""
        content = [f"# {enm.name}", ""]
        docstring = self._rewrite_docstring(enm.docstring)
        if docstring:
            content.append(docstring)
            content.append("")

        if enm.variants:
            content.append("## Variants")
            content.append("")
            for variant in enm.variants:
                content.append(f"- `{variant.name}`")
                if variant.comment:
                    content.append(f"  - {variant.comment}")
        return "\n".join(content).rstrip() + "\n"

    def filter_items(
        self,
        items: Sequence,  # list of items to filter
        item_type: str,  # item type label (class/function/enum/attribute)
    ) -> list:
        """Public wrapper around item filtering used by exporters."""
        return self._filter_items(items, item_type)

    def file_output_relpath(
        self,
        file_doc: FileDoc,  # source file doc
        module_prefix: str,  # module grouping prefix
    ) -> str:
        """Compute the relative output path for a file within a module."""
        base = os.path.basename(file_doc.path)
        stem = os.path.splitext(base)[0]
        module_name = file_doc.module_name

        rel = module_name
        if module_prefix and module_name.startswith(f"{module_prefix}."):
            rel = module_name[len(module_prefix) + 1 :]
        elif module_name == module_prefix:
            rel = ""

        parts = [p for p in rel.split(".") if p]
        if stem == "__init__":
            parts.append("__init__")
        elif not parts:
            parts.append(stem)
        return os.path.join(*parts)

    def item_output_relpath(
        self,
        file_doc: FileDoc,  # source file doc
        module_prefix: str,  # module grouping prefix
        item_name: str,  # class/function/enum name
    ) -> str:
        """Compute the relative output path for a class/function/enum item."""
        rel = self.file_output_relpath(file_doc, module_prefix)
        base_dir = os.path.dirname(rel)
        file_stem = os.path.splitext(os.path.basename(file_doc.path))[0]
        if base_dir:
            return os.path.join(base_dir, file_stem, item_name)
        return os.path.join(file_stem, item_name)

    def _section_for_classes(
        self,
        classes: Iterable[ClassDoc],  # classes to render
        *,
        section_level: int,  # heading level for the section
    ) -> list[str]:
        classes = list(classes)
        if not classes:
            return []

        content = [f"{'#' * section_level} Classes", ""]
        for cls in classes:
            content.append(f"{'#' * (section_level + 1)} `class {cls.name}`")
            if cls.bases:
                content.append(
                    f"Inherits from: {', '.join(f'`{b}`' for b in cls.bases)}"
                )
                content.append("")

            docstring = self._rewrite_docstring(cls.docstring)
            if docstring:
                content.append(docstring)
                content.append("")

            methods = self._filter_items(cls.methods, "function")
            attributes = self._filter_items(cls.attributes, "attribute")

            if attributes:
                content.append("::: details Attributes")
                content.append("")
                content.append("| Name | Type | Description |")
                content.append("| - | - | - |")
                for attr in attributes:
                    desc = attr.comment or ""
                    content.append(f"| `{attr.name}` | `{attr.annotation}` | {desc} |")
                content.append("")
                content.append(":::")
                content.append("")

            if methods:
                content.append("::: details Methods")
                content.append("")
                for method in methods:
                    content.extend(
                        self._function_markdown(
                            method,
                            heading_level=section_level + 3,
                            code_heading=True,
                            include_separator=False,
                        )
                    )
                content.append(":::")
                content.append("")

            content.append("---")
            content.append("")
        return content

    def _section_for_enums(
        self,
        enums: Iterable[EnumDoc],  # enums to render
        *,
        section_level: int,  # heading level for the section
    ) -> list[str]:
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

    def _section_for_functions(
        self,
        functions: Iterable[FunctionDoc],  # functions to render
        *,
        section_level: int,  # heading level for the section
    ) -> list[str]:
        functions = list(functions)
        if not functions:
            return []

        content = [f"{'#' * section_level} Functions", ""]
        for func in functions:
            content.extend(self._function_block(func, heading_level=section_level + 1))
        return content

    def _function_block(
        self,
        func: FunctionDoc,  # function to render
        *,
        heading_level: int,  # heading level for the title
    ) -> list[str]:
        heading = "#" * heading_level
        content = [f"{heading} `{func.name}`", ""]

        summary = (
            func.docstring.strip().splitlines()[0] if func.docstring.strip() else ""
        )
        if summary:
            content.append(summary)
            content.append("")

        content.append("::: details Details")
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

        content.append(":::")
        content.append("")
        return content

    def _function_markdown(
        self,
        func: FunctionDoc,  # function to render
        *,
        heading_level: int,  # heading level for the title
        code_heading: bool = False,  # wrap heading in backticks
        include_separator: bool = True,  # append section separator
    ) -> list[str]:
        heading = "#" * heading_level
        title = f"`{func.name}`" if code_heading else func.name
        content = [f"{heading} {title}", ""]

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

        if include_separator:
            content.append("---")
            content.append("")
        return content

    def _attribute_markdown(
        self,
        attr: AttributeDoc,  # attribute to render
        *,
        heading_level: int,  # heading level for the title
    ) -> list[str]:
        heading = "#" * heading_level
        content = [f"{heading} `{attr.name}`", ""]
        content.append(f"Type: {self._inline_type(attr.annotation)}")
        content.append("")
        if attr.comment:
            content.append(attr.comment)
            content.append("")
        return content

    def _filter_items(
        self,
        items: Sequence,  # items to filter
        item_type: str,  # item type label (class/function/enum/attribute)
    ) -> list:
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

    def _name_allowed(self, name: str) -> bool:  # item name to check visibility rules
        if name.startswith("__") and name.endswith("__"):
            return self.options.include_dunder
        if name.startswith("_"):
            return self.options.include_private
        return True

    def _returns_line(
        self, func: FunctionDoc  # function to render return info for
    ) -> str | None:
        if func.returns_self:
            return f"**Returns**: {self._inline_type('Self')}"
        if func.returns:
            return f"**Returns**: {self._inline_type(func.returns)}"
        return None

    def _inline_type(self, annotation: str) -> str:  # type annotation to format
        if self.options.output_format == "md-nextra":
            return f"`{annotation}{{:python}}`"
        return f"`{annotation}`"

    def _code_block(self, code: str) -> str:  # code to wrap in a fenced block
        if self.options.output_format == "md-nextra":
            suffix = " showLineNumbers" if self.options.show_line_numbers else ""
            return f"```python copy{suffix}\n{code}\n```"
        return f"```python\n{code}\n```"

    def _rewrite_docstring(self, docstring: str) -> str:  # docstring text to rewrite
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

    def _rewrite_opening_fence(
        self, fence: str  # opening fence line to rewrite
    ) -> str:
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
