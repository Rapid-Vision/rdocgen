# File: `example.py`

This module is used as an example of doc generation.

It doesn't have any useful functions or classes but is meant to represent everything that this project can generate.

## Classes

### `class ExampleClass` {#class-exampleclass}
This is an example of class doc generation

::: details Attributes

| Name | Type | Description |
| - | - | - |
| `literal_attr` | `Literal['one', 'two']` | example of a literal attribute |
| `name` | `str` | instance name |
| `count` | `int` | instance counter |

:::

::: details Methods

---
#### `increment`

Increase the internal counter by the given step.

**Signature**

```python
def increment(self, step: int) -> int
```

**Arguments**

- **`step`** : `int` — value to add

**Returns**: `int`

---
---
#### `rename`

Return self after changing the name.

**Signature**

```python
def rename(self, new_name: str) -> 'ExampleClass'
```

**Arguments**

- **`new_name`** : `str` — new name to set

**Returns**: `Self`

---
:::

---

## Enums

### ExampleEnum {#enum-exampleenum}
This is an example enum used for variant rendering.

::: details Variants

| Name | Description |
| - | - |
| `FIRST` | first option |
| `SECOND` | second option |

:::

---

## Functions

### `example_function` {#function-example-function}

Format a value with an optional label.

::: details Details

**Signature**

```python
def example_function(value: int, label: Optional[str]=None, test: Callable[[random.Random], dict | int]=None) -> str
```

**Arguments**

- **`value`** : `int` — input integer
- **`label`** : `Optional[str]` — optional label
- **`test`** : `Callable[[random.Random], dict | int]` — Samples a params dict from RNG

**Returns**: `str`

:::

### `example_returns_self` {#function-example-returns-self}

Example of a function returning a new instance.

::: details Details

**Signature**

```python
def example_returns_self(value: int) -> ExampleClass
```

**Arguments**

- **`value`** : `int` — value used to build the instance

**Returns**: `ExampleClass`

:::
