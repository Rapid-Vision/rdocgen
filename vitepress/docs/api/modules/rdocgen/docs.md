# File: `docs.py`

High-level export API for rdocgen.

## Functions

### `export_docs`

High-level entrypoint: parse sources and export documentation.

::: details Details

**Signature**

```python
def export_docs(codepath: str, outdir: str, options: ExportOptions) -> None
```

**Arguments**

- **`codepath`** : `str` — file or directory path to parse
- **`outdir`** : `str` — output directory
- **`options`** : `ExportOptions` — parse/render/export configuration

**Returns**: `None`

:::
