# Module: `rdocgen`

## Files

- [`__init__.py`](__init__.md)
- [`cli.py`](cli.md)
- [`config.py`](config.md)
- [`discovery.py`](discovery.md)
- [`docs.py`](docs.md)
- [`example.py`](example.md)
- [`exporter.py`](exporter.md)
- [`model.py`](model.md)
- [`parser.py`](parser.md)
- [`project.py`](project.md)
- [`markdown.py`](render/markdown.md)

## Classes

- [`class ParseOptions`](config.md#class-parseoptions)
- [`class RenderOptions`](config.md#class-renderoptions)
- [`class ExportOptions`](config.md#class-exportoptions)
- [`class ExampleClass`](example.md#class-exampleclass)
- [`class ArgumentDoc`](model.md#class-argumentdoc)
- [`class FunctionDoc`](model.md#class-functiondoc)
- [`class AttributeDoc`](model.md#class-attributedoc)
- [`class EnumVariantDoc`](model.md#class-enumvariantdoc)
- [`class EnumDoc`](model.md#class-enumdoc)
- [`class ClassDoc`](model.md#class-classdoc)
- [`class FileDoc`](model.md#class-filedoc)
- [`class ModuleDoc`](model.md#class-moduledoc)
- [`class ProjectDoc`](model.md#class-projectdoc)
- [`class ParseError`](parser.md#class-parseerror)
- [`class Parser`](parser.md#class-parser)
- [`class MarkdownRenderer`](render/markdown.md#class-markdownrenderer)

## Functions

- [`main`](cli.md#function-main)
- [`iter_python_files`](discovery.md#function-iter-python-files)
- [`module_name_from_path`](discovery.md#function-module-name-from-path)
- [`path_allowed`](discovery.md#function-path-allowed)
- [`export_docs`](docs.md#function-export-docs)
- [`example_function`](example.md#function-example-function)
- [`example_returns_self`](example.md#function-example-returns-self)
- [`export_project`](exporter.md#function-export-project)
- [`export_single_file`](exporter.md#function-export-single-file)
- [`is_enum_class`](parser.md#function-is-enum-class)
- [`check_function_returns_self`](parser.md#function-check-function-returns-self)
- [`get_function_signature`](parser.md#function-get-function-signature)
- [`parse_source`](parser.md#function-parse-source)
- [`parse_file`](parser.md#function-parse-file)
- [`build_project`](project.md#function-build-project)

## Enums

- [`ExampleEnum`](example.md#enum-exampleenum)
