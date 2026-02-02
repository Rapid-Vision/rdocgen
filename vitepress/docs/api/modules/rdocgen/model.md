# File: `model.py`

## Classes

### ArgumentDoc
#### Attributes

##### `name`

Type: `str`

argument name (with * or ** prefix if applicable)

##### `annotation`

Type: `Optional[str]`

annotation string if present

##### `comment`

Type: `str`

inline comment text attached to the argument

##### `lineno`

Type: `int`

source line number

---

### FunctionDoc
#### Attributes

##### `name`

Type: `str`

function name

##### `docstring`

Type: `str`

cleaned docstring text

##### `arguments`

Type: `List[ArgumentDoc]`

parsed argument docs

##### `returns`

Type: `Optional[str]`

return annotation string if present

##### `returns_self`

Type: `bool`

True if all returns are a bare name (Self-like)

##### `decorators`

Type: `List[str]`

decorator expressions as strings

##### `signature`

Type: `str`

signature string for rendering

##### `lineno`

Type: `int`

source line number

##### `is_private`

Type: `bool`

True for underscore-prefixed names

---

### AttributeDoc
#### Attributes

##### `name`

Type: `str`

attribute name

##### `annotation`

Type: `str`

annotation string

##### `comment`

Type: `str`

inline comment text attached to the attribute

##### `lineno`

Type: `int`

source line number

---

### EnumVariantDoc
#### Attributes

##### `name`

Type: `str`

enum variant name

##### `comment`

Type: `str`

inline comment text attached to the variant

##### `lineno`

Type: `int`

source line number

---

### EnumDoc
#### Attributes

##### `name`

Type: `str`

enum class name

##### `docstring`

Type: `str`

cleaned docstring text

##### `variants`

Type: `List[EnumVariantDoc]`

parsed enum variants

##### `lineno`

Type: `int`

source line number

##### `is_private`

Type: `bool`

True for underscore-prefixed names

---

### ClassDoc
#### Attributes

##### `name`

Type: `str`

class name

##### `bases`

Type: `List[str]`

base class expressions as strings

##### `docstring`

Type: `str`

cleaned docstring text

##### `methods`

Type: `List[FunctionDoc]`

parsed methods

##### `attributes`

Type: `List[AttributeDoc]`

parsed annotated attributes

##### `lineno`

Type: `int`

source line number

##### `is_private`

Type: `bool`

True for underscore-prefixed names

---

### FileDoc
#### Attributes

##### `path`

Type: `str`

filesystem path to the source file

##### `module_name`

Type: `str`

dotted module path for this file

##### `docstring`

Type: `str`

module docstring text

##### `classes`

Type: `List[ClassDoc]`

classes in file

##### `enums`

Type: `List[EnumDoc]`

enums in file

##### `functions`

Type: `List[FunctionDoc]`

functions in file

---

### ModuleDoc
#### Attributes

##### `name`

Type: `str`

module grouping name

##### `path`

Type: `str`

path used for grouping (informational)

##### `files`

Type: `List[FileDoc]`

files in this module

---

### ProjectDoc
#### Attributes

##### `name`

Type: `str`

project name

##### `root_path`

Type: `str`

root path used for discovery

##### `modules`

Type: `List[ModuleDoc]`

modules in project

---
