# File: `config.py`

Configuration dataclasses for parsing and rendering.

## Classes

### `class ParseOptions` {#class-parseoptions}
Configuration for filesystem traversal and parsing behavior.

::: details Attributes

| Name | Type | Description |
| - | - | - |
| `include_paths` | `list[str]` | glob patterns to include |
| `exclude_paths` | `list[str]` | glob patterns to exclude |
| `project_name` | `Optional[str]` | override for the displayed project name |
| `follow_symlinks` | `bool` | follow directory symlinks in traversal |
| `module_depth` | `Optional[int]` | grouping depth for module buckets |
| `fail_on_parse_error` | `bool` | retained for compatibility; parsing is strict |

:::

---

### `class RenderOptions` {#class-renderoptions}
Configuration for how parsed docs are rendered into markdown.

::: details Attributes

| Name | Type | Description |
| - | - | - |
| `output_extension` | `str \| None` | override for .md/.mdx |
| `include_types` | `list[str]` | sections to include |
| `exclude_types` | `list[str]` | sections to exclude |
| `include_private` | `bool` | include underscore-prefixed items |
| `include_dunder` | `bool` | include __dunder__ names |
| `sort` | `Literal['source-order', 'alpha']` | order of definitions |
| `flatten` | `bool` | emit a single output file |
| `index_title` | `str` | title for root index page |
| `docstring_style` | `str` | raw, python-fences, preserve |
| `code_fence_language` | `str` | language for unlabeled fences |
| `code_fence_suffix` | `str` | extra tokens appended to opening fences |

:::

::: details Methods

---
#### `extension`

**Signature**

```python
@property
def extension(self) -> str
```

**Arguments**


**Returns**: `str`

---
:::

---

### `class ExportOptions` {#class-exportoptions}
Top-level export configuration (parse + render + output behavior).

::: details Attributes

| Name | Type | Description |
| - | - | - |
| `render` | `RenderOptions` | render settings |
| `parse` | `ParseOptions` | parse settings |
| `clean` | `bool` | delete output directory before export |
| `force` | `bool` | allow deleting protected directories |
| `dry_run` | `bool` | report actions without writing files |

:::

---
