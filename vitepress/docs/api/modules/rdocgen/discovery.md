# File: `discovery.py`

## Functions

### iter_python_files

Yield Python files under root, applying include/exclude rules.

**Signature**

```python
def iter_python_files(root: Path, options: ParseOptions) -> Iterable[Path]
```

**Arguments**

- **`root`** : `Path` — directory root to scan for Python files
- **`options`** : `ParseOptions` — traversal filters and symlink behavior

**Returns**: `Iterable[Path]`

---

### module_name_from_path

Convert a file path into a dotted module path, with optional depth.

**Signature**

```python
def module_name_from_path(path: Path, root: Optional[Path]=None, depth: Optional[int]=None) -> str
```

**Arguments**

- **`path`** : `Path` — file path to convert
- **`root`** : `Optional[Path]` — root used to compute relative module path
- **`depth`** : `Optional[int]` — maximum number of module path segments

**Returns**: `str`

---

### path_allowed

Return True if a path matches include/exclude filters.

**Signature**

```python
def path_allowed(path: Path, root: Path, options: ParseOptions) -> bool
```

**Arguments**

- **`path`** : `Path` — candidate file path
- **`root`** : `Path` — root used to compute relative globs
- **`options`** : `ParseOptions` — include/exclude filters

**Returns**: `bool`

---
