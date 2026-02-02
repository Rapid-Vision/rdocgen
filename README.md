# rdocgen

Generate Markdown documentation from Python source files using an AST-based parser.
The tool can scan a single file or an entire directory and export either plain
Markdown or Nextra-flavored Markdown with copy/line-number code fences.

## Usage

### Single file
```bash
rdocgen -c path/to/module.py -o ./out_docs --format md-nextra
```

### Directory
```bash
rdocgen -c path/to/package -o ./out_docs --format md-plain
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

### Split by kind
```bash
rdocgen -c src -o ./out_docs --split
```

### Split by kind + per-file pages
```bash
rdocgen -c src -o ./out_docs --split=hybrid
```

Note: `--split` cannot be combined with `--flatten`.

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
  --no-line-numbers
```

## CLI flags (high level)
- `--code` / `-c`: File or directory to parse.
- `--outdir` / `-o`: Output directory (deleted by default before export).
- `--format`: `md-plain` or `md-nextra`.
- `--include-path` / `--exclude-path`: Glob filters (repeatable).
- `--module-depth`: Grouping depth (`1`, `2`, or `all`).
- `--project-name`: Override the project name shown in indexes.
- `--clean` / `--no-clean`: Control output dir deletion.
- `--include-private` / `--include-dunder`: Include hidden members.
- `--include-types` / `--exclude-types`: Filter by `class,function,enum,attribute`.
- `--sort`: `source-order` or `alpha`.
- `--flatten`: Emit a single output file.
- `--split`: Emit separate files for classes, functions, and enums (`off`, `only`, `hybrid`).
- `--index-title`: Override root index title.
- `--docstring-style`: `raw`, `python-fences`, or `preserve`.
- `--code-fence-language`: Default language for unlabeled fences.
- `--no-line-numbers`: Disable `showLineNumbers` for Nextra fences.
- `--output-extension`: Override `.md`/`.mdx`.
- `--fail-on-parse-error`: Abort on invalid Python files.

## Notes
- Output directories are deleted by default before writing.
- This project only reads source files; it does not execute code.
