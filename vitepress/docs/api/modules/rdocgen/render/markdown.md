# File: `markdown.py`

Markdown renderer for rdocgen outputs.

## Classes

### `class MarkdownRenderer` {#class-markdownrenderer}
Render Project/Module/File docs into Markdown.

::: details Methods

##### `project_index`

Render the root project index page.

**Signature**

```python
def project_index(self, project: ProjectDoc, *, include_module_links: bool=True) -> str
```

**Arguments**

- **`project`** : `ProjectDoc` — project to render
- **`include_module_links`** : `bool` — whether to render module links

**Returns**: `str`

##### `module_index`

Render a module index page with file links and item anchors.

**Signature**

```python
def module_index(self, module: ModuleDoc) -> str
```

**Arguments**

- **`module`** : `ModuleDoc` — module to render

**Returns**: `str`

##### `file_doc`

Render a single file page with classes, enums, and functions.

**Signature**

```python
def file_doc(self, file_doc: FileDoc, *, heading_level: int=1) -> str
```

**Arguments**

- **`file_doc`** : `FileDoc` — file to render
- **`heading_level`** : `int` — heading level for top title

**Returns**: `str`

##### `class_doc`

Render a standalone class page.

**Signature**

```python
def class_doc(self, cls: ClassDoc) -> str
```

**Arguments**

- **`cls`** : `ClassDoc` — class to render

**Returns**: `str`

##### `function_doc`

Render a standalone function page.

**Signature**

```python
def function_doc(self, func: FunctionDoc) -> str
```

**Arguments**

- **`func`** : `FunctionDoc` — function to render

**Returns**: `str`

##### `enum_doc`

Render a standalone enum page.

**Signature**

```python
def enum_doc(self, enm: EnumDoc) -> str
```

**Arguments**

- **`enm`** : `EnumDoc` — enum to render

**Returns**: `str`

##### `filter_items`

Public wrapper around item filtering used by exporters.

**Signature**

```python
def filter_items(self, items: Sequence, item_type: str) -> list
```

**Arguments**

- **`items`** : `Sequence` — list of items to filter
- **`item_type`** : `str` — item type label (class/function/enum/attribute)

**Returns**: `list`

##### `file_output_relpath`

Compute the relative output path for a file within a module.

**Signature**

```python
def file_output_relpath(self, file_doc: FileDoc, module_prefix: str) -> str
```

**Arguments**

- **`file_doc`** : `FileDoc` — source file doc
- **`module_prefix`** : `str` — module grouping prefix

**Returns**: `str`

:::

---
