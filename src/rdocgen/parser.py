"""
AST parser that converts Python source into structured documentation models.
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
    """Parse a single Python source file into documentation data classes."""
    def __init__(
        self,
        source: str,  # source code text to parse
        *,
        path: str,  # source path for diagnostics
        module_name: str,  # dotted module path for this file
    ) -> None:
        self.source = source
        self.path = path
        self.module_name = module_name
        self.module = ast.parse(source)
        self.comments = self._collect_comments(source)

    def _collect_comments(
        self, src: str  # source code text to scan for comments
    ) -> dict[int, list[tuple[int, str]]]:
        comments: dict[int, list[tuple[int, str]]] = {}
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        for tok_type, tok_string, start, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                comments.setdefault(start[0], []).append((start[1], tok_string[1:].strip()))
        return comments

    def _node_comments(
        self, node: ast.AST  # AST node whose lines are scanned for comments
    ) -> str:
        start = getattr(node, "lineno", None)
        end = getattr(node, "end_lineno", start)
        if start is None or end is None:
            return ""

        parts: list[str] = []
        for line in range(start, end + 1):
            for _, comment in self.comments.get(line, []):
                parts.append(comment)
        return "\n".join(parts)

    def _argument_comments(
        self,
        arg: ast.arg,  # argument node whose trailing comments to collect
        *,
        signature_end: int,  # end line of the function argument list
        next_arg_start: int | None,  # starting line of the next argument, if any
    ) -> str:
        start = getattr(arg, "lineno", None)
        if start is None:
            return ""

        end = next_arg_start - 1 if next_arg_start is not None else signature_end
        if end < start:
            end = start

        parts: list[str] = []
        min_col = getattr(arg, "col_offset", 0)
        for line in range(start, end + 1):
            for col, comment in self.comments.get(line, []):
                if line != start or col >= min_col:
                    parts.append(comment)
        return "\n".join(parts)

    def _parse_arguments(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef  # function node to inspect
    ) -> list[ArgumentDoc]:
        args: list[ArgumentDoc] = []
        if func.body:
            signature_end = func.body[0].lineno - 1
        else:
            signature_end = getattr(func.args, "end_lineno", func.lineno)
        all_args: list[tuple[ast.arg, str]] = []

        for arg in func.args.posonlyargs:
            all_args.append((arg, ""))
        for arg in func.args.args:
            all_args.append((arg, ""))
        for arg in func.args.kwonlyargs:
            all_args.append((arg, ""))
        if func.args.vararg is not None:
            all_args.append((func.args.vararg, "*"))
        if func.args.kwarg is not None:
            all_args.append((func.args.kwarg, "**"))

        def add_arg(
            arg: ast.arg,  # argument node to add
            next_arg_start: int | None,  # start line of the next argument
            prefix: str = "",  # prefix to apply for var/kw args
        ) -> None:
            name = f"{prefix}{arg.arg}"
            ann = ast.unparse(arg.annotation) if arg.annotation else None
            comment = self._argument_comments(
                arg,
                signature_end=signature_end,
                next_arg_start=next_arg_start,
            )
            args.append(
                ArgumentDoc(
                    name=name,
                    annotation=ann,
                    comment=comment,
                    lineno=arg.lineno,
                )
            )

        for index, (arg, prefix) in enumerate(all_args):
            next_arg_start = None
            if index + 1 < len(all_args):
                next_arg_start = all_args[index + 1][0].lineno
            add_arg(arg, next_arg_start=next_arg_start, prefix=prefix)

        return args

    def _parse_function(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef  # function node to parse
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

    def _parse_attribute(
        self, assign: ast.AnnAssign  # annotated assignment to parse
    ) -> AttributeDoc:
        annotation = ast.unparse(assign.annotation)
        return AttributeDoc(
            name=assign.target.id if isinstance(assign.target, ast.Name) else "",
            annotation=annotation,
            comment=self._node_comments(assign),
            lineno=assign.lineno,
        )

    def _parse_class(
        self, class_node: ast.ClassDef  # class node to parse
    ) -> ClassDoc:
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

    def _parse_enum(
        self, class_node: ast.ClassDef  # enum class node to parse
    ) -> EnumDoc:
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
            if isinstance(node, ast.ClassDef) and is_enum_class(node):
                module_doc.enums.append(self._parse_enum(node))
            elif isinstance(node, ast.ClassDef):
                module_doc.classes.append(self._parse_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                module_doc.functions.append(self._parse_function(node))

        return module_doc


def is_enum_class(
    class_node: ast.AST  # candidate class node to test for Enum inheritance
) -> bool:
    """Check if a class inherits from Enum (by name)."""
    if not isinstance(class_node, ast.ClassDef):
        return False

    for base in class_node.bases:
        if isinstance(base, ast.Name) and base.id == "Enum":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "Enum":
            return True
    return False


def check_function_returns_self(
    func: ast.FunctionDef | ast.AsyncFunctionDef  # function node to analyze
) -> bool:
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


def get_function_signature(
    node: ast.FunctionDef | ast.AsyncFunctionDef  # function node to stringify
) -> str:
    new_node: ast.FunctionDef | ast.AsyncFunctionDef
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
    source: str,  # source code text to parse
    *,
    path: str = "<memory>",  # source path for diagnostics
    module_name: str = "<module>",  # dotted module path for this file
) -> FileDoc:
    """Parse a Python source string into a structured documentation tree."""
    return Parser(source, path=path, module_name=module_name).parse()


def parse_file(
    path: str,  # file path to parse
    encoding: str = "utf-8",  # file encoding
    *,
    module_name: Optional[str] = None,  # dotted module path for this file
    fail_on_parse_error: bool = False,  # raise if a SyntaxError occurs
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
