# File: `config.py`

## Classes

### ParseOptions
Configuration for filesystem traversal and parsing behavior.

#### Attributes

##### `include_paths`

Type: `list[str]`

glob patterns to include

##### `exclude_paths`

Type: `list[str]`

glob patterns to exclude

##### `follow_symlinks`

Type: `bool`

follow directory symlinks in traversal

##### `module_depth`

Type: `Optional[int]`

grouping depth for module buckets

##### `fail_on_parse_error`

Type: `bool`

raise on SyntaxError

---

### RenderOptions
Configuration for how parsed docs are rendered into markdown.

#### Methods

##### extension

**Signature**

```python
@property
def extension(self) -> str
```

**Arguments**


**Returns**: `str`

---

#### Attributes

##### `output_format`

Type: `Literal['md-nextra', 'md-plain']`

output format

##### `output_extension`

Type: `str | None`

override for .md/.mdx

##### `include_types`

Type: `list[str]`

sections to include

##### `exclude_types`

Type: `list[str]`

sections to exclude

##### `include_private`

Type: `bool`

include underscore-prefixed items

##### `include_dunder`

Type: `bool`

include __dunder__ names

##### `sort`

Type: `Literal['source-order', 'alpha']`

order of definitions

##### `flatten`

Type: `bool`

emit a single output file

##### `split`

Type: `Literal['off', 'only', 'hybrid']`

split output mode

##### `index_title`

Type: `str`

title for root index page

##### `docstring_style`

Type: `str`

raw, python-fences, preserve

##### `code_fence_language`

Type: `str`

language for unlabeled fences

##### `show_line_numbers`

Type: `bool`

add showLineNumbers in fences

---

### ExportOptions
Top-level export configuration (parse + render + output behavior).

#### Attributes

##### `render`

Type: `RenderOptions`

render settings

##### `parse`

Type: `ParseOptions`

parse settings

##### `clean`

Type: `bool`

delete output directory before export

---
