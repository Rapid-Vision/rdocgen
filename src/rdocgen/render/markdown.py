"""
Markdown renderer for rdocgen outputs.
"""

import os
import posixpath
import re
from typing import Iterable, Sequence

from ..config import RenderOptions
from ..model import ClassDoc, EnumDoc, FileDoc, FunctionDoc, ModuleDoc, ProjectDoc


class MarkdownRenderer:
    """Render Project/Module/File docs into Markdown."""

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
                module_path = self._url_path(
                    "modules",
                    *module.name.split("."),
                    f"index{self.options.extension}",
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
        """Render a module index page with file links and item anchors."""
        content = [f"# Module: `{module.name}`", ""]

        content.append("## Files")
        content.append("")
        if not module.files:
            content.append("_No files found._")
        else:
            for file_doc in module.files:
                relpath = self.file_output_relpath(file_doc, module.name)
                target = self._url_path(f"{relpath}{self.options.extension}")
                label = f"`{os.path.basename(file_doc.path)}`"
                content.append(
                    self._link(
                        label,
                        target,
                    )
                )
        content.append("")

        class_links: list[str] = []
        function_links: list[str] = []
        enum_links: list[str] = []
        for file_doc in module.files:
            relpath = self.file_output_relpath(file_doc, module.name)
            file_target = self._url_path(f"{relpath}{self.options.extension}")
            for cls in self._filter_items(file_doc.classes, "class"):
                anchor = self._item_anchor("class", cls.name)
                class_links.append(
                    self._link(f"`class {cls.name}`", f"{file_target}#{anchor}")
                )
            for func in self._filter_items(file_doc.functions, "function"):
                anchor = self._item_anchor("function", func.name)
                function_links.append(
                    self._link(f"`{func.name}`", f"{file_target}#{anchor}")
                )
            for enm in self._filter_items(file_doc.enums, "enum"):
                anchor = self._item_anchor("enum", enm.name)
                enum_links.append(
                    self._link(f"`{enm.name}`", f"{file_target}#{anchor}")
                )

        content.append("## Classes")
        content.append("")
        if class_links:
            content.extend(class_links)
        else:
            content.append("_No classes found._")
        content.append("")

        content.append("## Functions")
        content.append("")
        if function_links:
            content.extend(function_links)
        else:
            content.append("_No functions found._")
        content.append("")

        content.append("## Enums")
        content.append("")
        if enum_links:
            content.extend(enum_links)
        else:
            content.append("_No enums found._")
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

    def _section_for_classes(
        self,
        classes: Iterable[ClassDoc],  # classes to render
        *,
        section_level: int,  # heading level for the section
        include_section_heading: bool = True,  # include the "Classes" heading
    ) -> list[str]:
        classes = list(classes)
        if not classes:
            return []

        content: list[str] = []
        if include_section_heading:
            content.extend([f"{'#' * section_level} Classes", ""])
            item_heading_level = section_level + 1
        else:
            item_heading_level = section_level
        for cls in classes:
            anchor = self._item_anchor("class", cls.name)
            content.append(
                f"{'#' * item_heading_level} `class {cls.name}` {{#{anchor}}}"
            )
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
                            heading_level=item_heading_level + 2,
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
        include_section_heading: bool = True,  # include the "Enums" heading
    ) -> list[str]:
        enums = list(enums)
        if not enums:
            return []

        content: list[str] = []
        if include_section_heading:
            content.extend([f"{'#' * section_level} Enums", ""])
            item_heading_level = section_level + 1
        else:
            item_heading_level = section_level
        for enm in enums:
            anchor = self._item_anchor("enum", enm.name)
            content.append(f"{'#' * item_heading_level} {enm.name} {{#{anchor}}}")
            docstring = self._rewrite_docstring(enm.docstring)
            if docstring:
                content.append(docstring)
                content.append("")

            if enm.variants:
                content.append("::: details Variants")
                content.append("")
                content.append("| Name | Description |")
                content.append("| - | - |")
                for variant in enm.variants:
                    desc = variant.comment or ""
                    content.append(f"| `{variant.name}` | {desc} |")
                content.append("")
                content.append(":::")
            content.append("")
            content.append("---")
            content.append("")
        return content

    def _section_for_functions(
        self,
        functions: Iterable[FunctionDoc],  # functions to render
        *,
        section_level: int,  # heading level for the section
        include_section_heading: bool = True,  # include the "Functions" heading
    ) -> list[str]:
        functions = list(functions)
        if not functions:
            return []

        content: list[str] = []
        if include_section_heading:
            content.extend([f"{'#' * section_level} Functions", ""])
            item_heading_level = section_level + 1
        else:
            item_heading_level = section_level
        for func in functions:
            anchor = self._item_anchor("function", func.name)
            content.extend(
                self._function_block(
                    func, heading_level=item_heading_level, anchor=anchor
                )
            )
        return content

    def _function_block(
        self,
        func: FunctionDoc,  # function to render
        *,
        heading_level: int,  # heading level for the title
        anchor: str | None = None,  # custom anchor for the heading
    ) -> list[str]:
        heading = "#" * heading_level
        anchor_suffix = f" {{#{anchor}}}" if anchor else ""
        content = [f"{heading} `{func.name}`{anchor_suffix}", ""]

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
        return f"`{annotation}`"

    def _code_block(self, code: str) -> str:  # code to wrap in a fenced block
        suffix = self._code_fence_suffix()
        return f"```{self.options.code_fence_language}{suffix}\n{code}\n```"

    def _rewrite_docstring(self, docstring: str) -> str:  # docstring text to rewrite
        if not docstring:
            return ""
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
        suffix = self._code_fence_suffix()
        if self.options.docstring_style == "preserve":
            if suffix.strip() and suffix.strip() in fence:
                return fence
            return f"{fence}{suffix}" if fence != "```" else f"```{suffix}"
        if self.options.docstring_style == "python-fences":
            if fence == "```":
                return f"```{self.options.code_fence_language}{suffix}"
            if suffix.strip() and suffix.strip() in fence:
                return fence
            return f"{fence}{suffix}"
        return fence

    def _code_fence_suffix(self) -> str:  # extra tokens for opening fences
        if not self.options.code_fence_suffix.strip():
            return ""
        return f" {self.options.code_fence_suffix.strip()}"

    def _item_anchor(self, kind: str, name: str) -> str:  # anchor slug for headings
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not slug:
            slug = "item"
        return f"{kind}-{slug}"

    def _url_path(self, *parts: str) -> str:  # build a URL path with optional prefix
        clean_parts = [p.replace(os.sep, "/") for p in parts if p]
        return posixpath.join(*clean_parts)
