# Getting started

`rdocgen` is an alternative to python documentation generators that use standard docstrings.
It uses inline comments as source of descriptions and exports documentation in markdown files compatible with SSG tools such as [vitepress](https://vitepress.dev/).

Write documentation like this:
```python
def example_function(
    value: int,  # input integer
    label: Optional[str] = None,  # optional label
) -> str:
```

Generated with vitepress documentation will look like:
![function docs example](example.png)

## Why?
- It is simpler then docstrings
- It provides a single source of truth. Documentation drift from code becomes less likely.

Use this project only if you do not rely on standard docstring tooling. 

## Usage

### Single file
```bash
rdocgen -c path/to/module.py -o ./out_docs
```

### Directory
```bash
rdocgen -c path/to/package -o ./out_docs
```

### Include / exclude files
```bash
rdocgen -c src -o ./out_docs \
  --include-path "rdocgen/**" \
  --exclude-path "**/tests/**"
```

### Control hierarchy and output
```bash
rdocgen -c src -o ./out_docs \
  --module-depth 2 \
  --project-name "My SDK" \
  --flatten \
  --index-title "API"
```

### Visibility and types
```bash
rdocgen -c src -o ./out_docs \
  --include-private \
  --include-dunder \
  --include-types class,function
```

### Docstring rendering
```bash
rdocgen -c src -o ./out_docs \
  --docstring-style python-fences \
  --code-fence-language python \
  --code-fence-suffix "copy showLineNumbers"
```

## CLI flags (high level)
- `--code` / `-c`: File or directory to parse.
- `--outdir` / `-o`: Output directory (deleted by default before export).
- `--include-path` / `--exclude-path`: Glob filters (repeatable).
- `--module-depth`: Grouping depth (`1`, `2`, or `all`).
- `--project-name`: Override the project name shown in indexes.
- `--clean` / `--no-clean`: Control output dir deletion.
- `--include-private` / `--include-dunder`: Include hidden members.
- `--include-types` / `--exclude-types`: Filter by `class,function,enum,attribute`.
- `--sort`: `source-order` or `alpha`.
- `--flatten`: Emit a single output file.
- `--index-title`: Override root index title.
- `--docstring-style`: `raw`, `python-fences`, or `preserve`.
- `--code-fence-language`: Default language for unlabeled fences.
- `--code-fence-suffix`: Extra tokens for opening fences (e.g., `copy showLineNumbers`).
- `--output-extension`: Override `.md`/`.mdx`.
- `--fail-on-parse-error`: Abort on invalid Python files.

## Notes
- Output directories are deleted by default before writing.
- This project only reads source files; it does not execute code.
