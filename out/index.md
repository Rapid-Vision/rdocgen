# Overview

Project: `src`

## Modules

- `rdocgen`

## Module: `rdocgen`

### File: `config.py`

#### Classes

##### ParseOptions
###### Attributes

####### `include_paths`

Type: `list[str]`

####### `exclude_paths`

Type: `list[str]`

####### `follow_symlinks`

Type: `bool`

####### `module_depth`

Type: `Optional[int]`

####### `fail_on_parse_error`

Type: `bool`

---

##### RenderOptions
###### Methods

####### extension

**Signature**

```python
@property
def extension(self) -> str
```

**Arguments**


**Returns**: `str`

---

###### Attributes

####### `output_format`

Type: `str`

####### `output_extension`

Type: `str | None`

####### `include_types`

Type: `list[str]`

####### `exclude_types`

Type: `list[str]`

####### `include_private`

Type: `bool`

####### `include_dunder`

Type: `bool`

####### `sort`

Type: `str`

source-order, alpha

####### `flatten`

Type: `bool`

####### `index_title`

Type: `str`

####### `docstring_style`

Type: `str`

raw, python-fences, preserve

####### `code_fence_language`

Type: `str`

####### `show_line_numbers`

Type: `bool`

---

##### ExportOptions
###### Attributes

####### `render`

Type: `RenderOptions`

####### `parse`

Type: `ParseOptions`

####### `clean`

Type: `bool`

---
### File: `discovery.py`

#### Functions

##### iter_python_files

**Signature**

```python
def iter_python_files(root: Path, options: ParseOptions) -> Iterable[Path]
```

**Arguments**

- **`root`** : `Path`
- **`options`** : `ParseOptions`

**Returns**: `Iterable[Path]`

---

##### module_name_from_path

**Signature**

```python
def module_name_from_path(path: Path, root: Optional[Path]=None, depth: Optional[int]=None) -> str
```

**Arguments**

- **`path`** : `Path`
- **`root`** : `Optional[Path]`
- **`depth`** : `Optional[int]`

**Returns**: `str`

---

##### path_allowed

**Signature**

```python
def path_allowed(path: Path, root: Path, options: ParseOptions) -> bool
```

**Arguments**

- **`path`** : `Path`
- **`root`** : `Path`
- **`options`** : `ParseOptions`

**Returns**: `bool`

---
### File: `exporter.py`

#### Functions

##### export_project

**Signature**

```python
def export_project(project: ProjectDoc, outdir: str, options: ExportOptions) -> None
```

**Arguments**

- **`project`** : `ProjectDoc`
- **`outdir`** : `str`
- **`options`** : `ExportOptions`

**Returns**: `None`

---
### File: `__init__.py`
### File: `docs.py`

#### Functions

##### export_docs

**Signature**

```python
def export_docs(codepath: str, outdir: str, options: ExportOptions) -> None
```

**Arguments**

- **`codepath`** : `str`
- **`outdir`** : `str`
- **`options`** : `ExportOptions`

**Returns**: `None`

---
### File: `model.py`

#### Classes

##### ArgumentDoc
###### Attributes

####### `name`

Type: `str`

####### `annotation`

Type: `Optional[str]`

####### `comment`

Type: `str`

####### `lineno`

Type: `int`

---

##### FunctionDoc
###### Attributes

####### `name`

Type: `str`

####### `docstring`

Type: `str`

####### `arguments`

Type: `List[ArgumentDoc]`

####### `returns`

Type: `Optional[str]`

####### `returns_self`

Type: `bool`

####### `decorators`

Type: `List[str]`

####### `signature`

Type: `str`

####### `lineno`

Type: `int`

####### `is_private`

Type: `bool`

---

##### AttributeDoc
###### Attributes

####### `name`

Type: `str`

####### `annotation`

Type: `str`

####### `comment`

Type: `str`

####### `lineno`

Type: `int`

---

##### EnumVariantDoc
###### Attributes

####### `name`

Type: `str`

####### `comment`

Type: `str`

####### `lineno`

Type: `int`

---

##### EnumDoc
###### Attributes

####### `name`

Type: `str`

####### `docstring`

Type: `str`

####### `variants`

Type: `List[EnumVariantDoc]`

####### `lineno`

Type: `int`

####### `is_private`

Type: `bool`

---

##### ClassDoc
###### Attributes

####### `name`

Type: `str`

####### `bases`

Type: `List[str]`

####### `docstring`

Type: `str`

####### `methods`

Type: `List[FunctionDoc]`

####### `attributes`

Type: `List[AttributeDoc]`

####### `lineno`

Type: `int`

####### `is_private`

Type: `bool`

---

##### FileDoc
###### Attributes

####### `path`

Type: `str`

####### `module_name`

Type: `str`

####### `docstring`

Type: `str`

####### `classes`

Type: `List[ClassDoc]`

####### `enums`

Type: `List[EnumDoc]`

####### `functions`

Type: `List[FunctionDoc]`

---

##### ModuleDoc
###### Attributes

####### `name`

Type: `str`

####### `path`

Type: `str`

####### `files`

Type: `List[FileDoc]`

---

##### ProjectDoc
###### Attributes

####### `name`

Type: `str`

####### `root_path`

Type: `str`

####### `modules`

Type: `List[ModuleDoc]`

---
### File: `parser.py`

Pure parser that converts Python source into a structured, renderer-agnostic
representation. Exporters (Markdown, HTML, JSON, etc.) should consume these
data classes instead of the Python AST directly.

#### Classes

##### Parser
###### Methods

####### parse

**Signature**

```python
def parse(self) -> FileDoc
```

**Arguments**


**Returns**: `Self`

---

---

#### Functions

##### is_enum_class

Check if a class inherits from Enum (by name).

**Signature**

```python
def is_enum_class(class_node) -> bool
```

**Arguments**

- **`class_node`**

**Returns**: `bool`

---

##### check_function_returns_self

**Signature**

```python
def check_function_returns_self(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool
```

**Arguments**

- **`func`** : `ast.FunctionDef | ast.AsyncFunctionDef`

**Returns**: `bool`

---

##### get_function_signature

**Signature**

```python
def get_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str
```

**Arguments**

- **`node`** : `ast.FunctionDef | ast.AsyncFunctionDef`

**Returns**: `str`

---

##### parse_source

Parse a Python source string into a structured documentation tree.

**Signature**

```python
def parse_source(source: str, *, path: str='<memory>', module_name: str='<module>') -> FileDoc
```

**Arguments**

- **`source`** : `str`
- **`path`** : `str`
- **`module_name`** : `str`

**Returns**: `FileDoc`

---

##### parse_file

Parse a file path into a structured documentation tree.

**Signature**

```python
def parse_file(path: str, encoding: str='utf-8', *, fail_on_parse_error: bool=False) -> Optional[FileDoc]
```

**Arguments**

- **`path`** : `str`
- **`encoding`** : `str`
- **`fail_on_parse_error`** : `bool`

**Returns**: `Optional[FileDoc]`

---
### File: `cli.py`

Extracts documentation from a Python source file and generates Markdown files.

The output is structured for use with the [Nextra site generator](https://nextra.site/).

#### Functions

##### main

**Signature**

```python
def main()
```

**Arguments**


---
### File: `project.py`

#### Functions

##### build_project

**Signature**

```python
def build_project(path: str, options: ParseOptions) -> ProjectDoc
```

**Arguments**

- **`path`** : `str`
- **`options`** : `ParseOptions`

**Returns**: `Self`

---
### File: `markdown.py`

#### Classes

##### MarkdownRenderer
###### Methods

####### project_index

**Signature**

```python
def project_index(self, project: ProjectDoc) -> str
```

**Arguments**

- **`project`** : `ProjectDoc`

**Returns**: `str`

---

####### module_index

**Signature**

```python
def module_index(self, module: ModuleDoc) -> str
```

**Arguments**

- **`module`** : `ModuleDoc`

**Returns**: `str`

---

####### file_doc

**Signature**

```python
def file_doc(self, file_doc: FileDoc, *, heading_level: int=1) -> str
```

**Arguments**

- **`file_doc`** : `FileDoc`
- **`heading_level`** : `int`

**Returns**: `str`

---

---
