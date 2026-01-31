"""
Pure parser that converts Python source into a structured, renderer-agnostic
representation. Exporters (Markdown, HTML, JSON, etc.) should consume these
data classes instead of the Python AST directly.
"""

import ast
import io
import tokenize
from pathlib import Path
from typing import Optional

from .model import (
    ArgumentDoc,
    AttributeDoc,
    ClassDoc,
    EnumDoc,
    EnumVariantDoc,
    FileDoc,
    FunctionDoc,
)


class Parser:
    def __init__(self, source: str, *, path: str, module_name: str) -> None:
        self.source = source
        self.path = path
        self.module_name = module_name
        self.module = ast.parse(source)
        self.comments = self._collect_comments(source)

    def _collect_comments(self, src: str) -> dict[int, str]:
        comments: dict[int, str] = {}
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        for tok_type, tok_string, start, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                comments[start[0]] = tok_string[1:].strip()
        return comments

    def _node_comments(self, node: ast.AST) -> str:
        start = getattr(node, "lineno", None)
        end = getattr(node, "end_lineno", start)
        if start is None or end is None:
            return ""

        parts: list[str] = []
        for line in range(start, end + 1):
            comment = self.comments.get(line)
            if comment is not None:
                parts.append(comment)
        return "\n".join(parts)

    def _parse_arguments(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> list[ArgumentDoc]:
        args: list[ArgumentDoc] = []

        def add_arg(arg: ast.arg, prefix: str = "") -> None:
            name = f"{prefix}{arg.arg}"
            ann = ast.unparse(arg.annotation) if arg.annotation else None
            comment = self._node_comments(arg)
            args.append(
                ArgumentDoc(
                    name=name,
                    annotation=ann,
                    comment=comment,
                    lineno=arg.lineno,
                )
            )

        for arg in func.args.posonlyargs:
            add_arg(arg)
        for arg in func.args.args:
            add_arg(arg)
        for arg in func.args.kwonlyargs:
            add_arg(arg)

        if func.args.vararg is not None:
            add_arg(func.args.vararg, prefix="*")
        if func.args.kwarg is not None:
            add_arg(func.args.kwarg, prefix="**")

        return args

    def _parse_function(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> FunctionDoc:
        return FunctionDoc(
            name=func.name,
            docstring=ast.get_docstring(func) or "",
            arguments=self._parse_arguments(func),
            returns=ast.unparse(func.returns) if func.returns else None,
            returns_self=check_function_returns_self(func),
            decorators=[ast.unparse(dec) for dec in func.decorator_list],
            signature=get_function_signature(func),
            lineno=func.lineno,
            is_private=func.name.startswith("_"),
        )

    def _parse_attribute(self, assign: ast.AnnAssign) -> AttributeDoc:
        annotation = ast.unparse(assign.annotation)
        return AttributeDoc(
            name=assign.target.id if isinstance(assign.target, ast.Name) else "",
            annotation=annotation,
            comment=self._node_comments(assign),
            lineno=assign.lineno,
        )

    def _parse_class(self, class_node: ast.ClassDef) -> ClassDoc:
        methods = [
            self._parse_function(method)
            for method in class_node.body
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        attributes = [
            self._parse_attribute(assign)
            for assign in class_node.body
            if isinstance(assign, ast.AnnAssign)
        ]

        return ClassDoc(
            name=class_node.name,
            bases=[ast.unparse(base) for base in class_node.bases],
            docstring=ast.get_docstring(class_node) or "",
            methods=methods,
            attributes=attributes,
            lineno=class_node.lineno,
            is_private=class_node.name.startswith("_"),
        )

    def _parse_enum(self, class_node: ast.ClassDef) -> EnumDoc:
        variants: list[EnumVariantDoc] = []
        for node in class_node.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                variants.append(
                    EnumVariantDoc(
                        name=node.targets[0].id,
                        comment=self._node_comments(node),
                        lineno=node.lineno,
                    )
                )

        return EnumDoc(
            name=class_node.name,
            docstring=ast.get_docstring(class_node) or "",
            variants=variants,
            lineno=class_node.lineno,
            is_private=class_node.name.startswith("_"),
        )

    def parse(self) -> FileDoc:
        module_doc = FileDoc(
            path=self.path,
            module_name=self.module_name,
            docstring=ast.get_docstring(self.module) or "",
        )

        for node in self.module.body:
            if is_enum_class(node):
                module_doc.enums.append(self._parse_enum(node))
            elif isinstance(node, ast.ClassDef):
                module_doc.classes.append(self._parse_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                module_doc.functions.append(self._parse_function(node))

        return module_doc


def is_enum_class(class_node) -> bool:
    """Check if a class inherits from Enum (by name)."""
    if not isinstance(class_node, ast.ClassDef):
        return False

    for base in class_node.bases:
        if isinstance(base, ast.Name) and base.id == "Enum":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "Enum":
            return True
    return False


def check_function_returns_self(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    count = 0
    for stmt in func.body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Return):
                if not isinstance(node.value, ast.Name):
                    return False
                count += 1

    if count == 0:
        return False
    return True


def get_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    if isinstance(node, ast.AsyncFunctionDef):
        new_node = ast.AsyncFunctionDef(
            name=node.name,
            args=node.args,
            body=[],
            decorator_list=node.decorator_list,
            returns=node.returns,
            type_comment=node.type_comment,
        )
    else:
        new_node = ast.FunctionDef(
            name=node.name,
            args=node.args,
            body=[],
            decorator_list=node.decorator_list,
            returns=node.returns,
            type_comment=node.type_comment,
        )
    new_node.lineno = 0
    return ast.unparse(new_node)[:-1]


def parse_source(
    source: str, *, path: str = "<memory>", module_name: str = "<module>"
) -> FileDoc:
    """Parse a Python source string into a structured documentation tree."""
    return Parser(source, path=path, module_name=module_name).parse()


def parse_file(
    path: str,
    encoding: str = "utf-8",
    *,
    module_name: Optional[str] = None,
    fail_on_parse_error: bool = False,
) -> Optional[FileDoc]:
    """Parse a file path into a structured documentation tree."""
    file_path = Path(path)
    try:
        with file_path.open("r", encoding=encoding) as fin:
            resolved_module_name = module_name or file_path.stem
            return parse_source(
                fin.read(),
                path=str(file_path),
                module_name=resolved_module_name,
            )
    except SyntaxError:
        if fail_on_parse_error:
            raise
        return None
