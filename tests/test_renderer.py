"""
Unit tests for markdown rendering.
"""

from rdocgen.model import AttributeDoc, ClassDoc, FileDoc, FunctionDoc, ModuleDoc
from rdocgen.render.markdown import MarkdownRenderer
from rdocgen.config import RenderOptions


def test_module_index_links_to_file_anchors() -> None:
    file_doc = FileDoc(
        path="src/example.py",
        module_name="example",
        docstring="",
        classes=[ClassDoc(name="Sample", bases=[], docstring="", methods=[], attributes=[], lineno=1, is_private=False)],
        functions=[FunctionDoc(name="do_work", docstring="", arguments=[], returns=None, returns_self=False, decorators=[], signature="def do_work():", lineno=1, is_private=False)],
        enums=[],
    )
    module = ModuleDoc(name="example", path="src", files=[file_doc])
    renderer = MarkdownRenderer(RenderOptions())

    content = renderer.module_index(module)

    assert "`class Sample`" in content
    assert "example.md#class-sample" in content
    assert "`do_work`" in content
    assert "example.md#function-do-work" in content


def test_file_doc_renders_custom_anchors() -> None:
    file_doc = FileDoc(
        path="src/example.py",
        module_name="example",
        docstring="",
        classes=[ClassDoc(name="Sample", bases=[], docstring="", methods=[], attributes=[], lineno=1, is_private=False)],
        functions=[FunctionDoc(name="do_work", docstring="", arguments=[], returns=None, returns_self=False, decorators=[], signature="def do_work():", lineno=1, is_private=False)],
        enums=[],
    )
    renderer = MarkdownRenderer(RenderOptions())

    content = renderer.file_doc(file_doc)

    assert "{#class-sample}" in content
    assert "{#function-do-work}" in content


def test_file_doc_escapes_pipes_in_attribute_tables() -> None:
    file_doc = FileDoc(
        path="src/example.py",
        module_name="example",
        docstring="",
        classes=[
            ClassDoc(
                name="Sample",
                bases=[],
                docstring="",
                methods=[],
                attributes=[
                    AttributeDoc(
                        name="value",
                        annotation="int | None",
                        comment="optional | may be empty",
                        lineno=1,
                    )
                ],
                lineno=1,
                is_private=False,
            )
        ],
        functions=[],
        enums=[],
    )
    renderer = MarkdownRenderer(RenderOptions())

    content = renderer.file_doc(file_doc)

    assert "| `value` | `int \\| None` | optional \\| may be empty |" in content
