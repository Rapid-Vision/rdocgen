# File: `parser.py`

AST parser that converts Python source into structured documentation models.

## Classes

### `class Parser`
Parse a single Python source file into documentation data classes.

::: details Methods

##### `parse`

**Signature**

```python
def parse(self) -> FileDoc
```

**Arguments**


**Returns**: `Self`

:::

---

## Functions

### `is_enum_class`

Check if a class inherits from Enum (by name).

::: details Details

**Signature**

```python
def is_enum_class(class_node: ast.AST) -> bool
```

**Arguments**

- **`class_node`** : `ast.AST` — candidate class node to test for Enum inheritance

**Returns**: `bool`

:::

### `check_function_returns_self`

::: details Details

**Signature**

```python
def check_function_returns_self(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool
```

**Arguments**

- **`func`** : `ast.FunctionDef | ast.AsyncFunctionDef` — function node to analyze

**Returns**: `bool`

:::

### `get_function_signature`

::: details Details

**Signature**

```python
def get_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str
```

**Arguments**

- **`node`** : `ast.FunctionDef | ast.AsyncFunctionDef` — function node to stringify

**Returns**: `str`

:::

### `parse_source`

Parse a Python source string into a structured documentation tree.

::: details Details

**Signature**

```python
def parse_source(source: str, *, path: str='<memory>', module_name: str='<module>') -> FileDoc
```

**Arguments**

- **`source`** : `str` — source code text to parse
- **`path`** : `str` — source path for diagnostics
- **`module_name`** : `str` — dotted module path for this file

**Returns**: `FileDoc`

:::

### `parse_file`

Parse a file path into a structured documentation tree.

::: details Details

**Signature**

```python
def parse_file(path: str, encoding: str='utf-8', *, module_name: Optional[str]=None, fail_on_parse_error: bool=False) -> Optional[FileDoc]
```

**Arguments**

- **`path`** : `str` — file path to parse
- **`encoding`** : `str` — file encoding
- **`module_name`** : `Optional[str]` — dotted module path for this file
- **`fail_on_parse_error`** : `bool` — raise if a SyntaxError occurs

**Returns**: `Optional[FileDoc]`

:::
