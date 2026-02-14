# File: `exporter.py`

Filesystem exporter that writes rendered docs to disk.

## Functions

### `export_project` {#function-export-project}

Write a ProjectDoc to disk using the configured renderer.

::: details Details

**Signature**

```python
def export_project(project: ProjectDoc, outdir: str, options: ExportOptions) -> None
```

**Arguments**

- **`project`** : `ProjectDoc` — parsed project tree to export
- **`outdir`** : `str` — output directory
- **`options`** : `ExportOptions` — render/export configuration

**Returns**: `None`

:::

### `export_single_file` {#function-export-single-file}

Write a single FileDoc into one output file without indexes.

::: details Details

**Signature**

```python
def export_single_file(file_doc: FileDoc, outdir: str, options: ExportOptions) -> None
```

**Arguments**

- **`file_doc`** : `FileDoc` — parsed file doc to export
- **`outdir`** : `str` — output directory
- **`options`** : `ExportOptions` — render/export configuration

**Returns**: `None`

:::
