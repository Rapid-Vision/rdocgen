# File: `model.py`

Data models representing parsed documentation structure.

## Classes

### `class ArgumentDoc` {#class-argumentdoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | argument name (with * or ** prefix if applicable) |
| `annotation` | `Optional[str]` | annotation string if present |
| `comment` | `str` | inline comment text attached to the argument |
| `lineno` | `int` | source line number |

:::

---

### `class FunctionDoc` {#class-functiondoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | function name |
| `docstring` | `str` | cleaned docstring text |
| `arguments` | `List[ArgumentDoc]` | parsed argument docs |
| `returns` | `Optional[str]` | return annotation string if present |
| `returns_self` | `bool` | True if all returns are a bare name (Self-like) |
| `decorators` | `List[str]` | decorator expressions as strings |
| `signature` | `str` | signature string for rendering |
| `lineno` | `int` | source line number |
| `is_private` | `bool` | True for underscore-prefixed names |

:::

---

### `class AttributeDoc` {#class-attributedoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | attribute name |
| `annotation` | `str` | annotation string |
| `comment` | `str` | inline comment text attached to the attribute |
| `lineno` | `int` | source line number |

:::

---

### `class EnumVariantDoc` {#class-enumvariantdoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | enum variant name |
| `comment` | `str` | inline comment text attached to the variant |
| `lineno` | `int` | source line number |

:::

---

### `class EnumDoc` {#class-enumdoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | enum class name |
| `docstring` | `str` | cleaned docstring text |
| `variants` | `List[EnumVariantDoc]` | parsed enum variants |
| `lineno` | `int` | source line number |
| `is_private` | `bool` | True for underscore-prefixed names |

:::

---

### `class ClassDoc` {#class-classdoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | class name |
| `bases` | `List[str]` | base class expressions as strings |
| `docstring` | `str` | cleaned docstring text |
| `methods` | `List[FunctionDoc]` | parsed methods |
| `attributes` | `List[AttributeDoc]` | parsed annotated attributes |
| `lineno` | `int` | source line number |
| `is_private` | `bool` | True for underscore-prefixed names |

:::

---

### `class FileDoc` {#class-filedoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `path` | `str` | filesystem path to the source file |
| `module_name` | `str` | dotted module path for this file |
| `docstring` | `str` | module docstring text |
| `classes` | `List[ClassDoc]` | classes in file |
| `enums` | `List[EnumDoc]` | enums in file |
| `functions` | `List[FunctionDoc]` | functions in file |

:::

---

### `class ModuleDoc` {#class-moduledoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | module grouping name |
| `path` | `str` | path used for grouping (informational) |
| `files` | `List[FileDoc]` | files in this module |

:::

---

### `class ProjectDoc` {#class-projectdoc}
::: details Attributes

| Name | Type | Description |
| - | - | - |
| `name` | `str` | project name |
| `root_path` | `str` | root path used for discovery |
| `modules` | `List[ModuleDoc]` | modules in project |

:::

---
