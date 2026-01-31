# Proposal: rdocgen vNext

## Goals
- Turn the current script into a configurable documentation generator with predictable output.
- Provide CLI flags to control scope, visibility, ordering, and formatting.
- Keep a clean separation between parsing (AST) and exporting (Markdown).

## Planned Features

### Input Scope
- `--code` accepts file or directory (current behavior).
- `--include` / `--exclude` glob filters for file paths.
- `--follow-symlinks` to include symlinked paths in traversal.

### Module Hierarchy
- `--module-depth` to control package grouping (e.g., `1`, `2`, `all`).
- `--flatten` to emit a single file per project.

### Visibility Filters
- `--public-only` to exclude private members by default.
- `--include-private` to include `_private` names.
- `--include-dunder` to include `__magic__` names.

### Type/Element Filters
- `--include` to select sections to emit: `class,function,enum,attribute`.
- `--exclude` with the same list to disable sections.

### Export Formats
- `--format` supports `md-plain` and `md-nextra` (current).
- `--output-extension` overrides default extension.

### Docstring Handling
- `--docstring-style` with `raw`, `python-fences`, or `preserve`.
- `--code-fence-language` default language for unlabeled fences.
- `--no-line-numbers` to omit `showLineNumbers` in Nextra.

### Output Structure
- `--outdir` (current) with `--clean/--no-clean` control.
- `--index-title` override for root index heading.
- `--include-file-summary` adds per-file summary block.

### Ordering
- `--sort` with `alpha`, `source-order`, or `grouped`.

### Metadata
- `--emit-json` to save the parsed tree as JSON.
- `--emit-tree` to print a tree to stdout for debugging.

### Error Handling
- `--fail-on-parse-error` to abort on syntax errors.
- `--ignore-parse-errors` to skip invalid files with warnings.

## Modular Refactor Plan

### Target Structure
- `src/rdocgen/config.py`
  - `ParseOptions`, `ExportOptions`, `RenderOptions`
  - Validation helpers (e.g., `validate_options()`)
- `src/rdocgen/model.py`
  - Data classes only (`ProjectDoc`, `ModuleDoc`, `FileDoc`, `ClassDoc`, `FunctionDoc`, etc.)
- `src/rdocgen/discovery.py`
  - `iter_python_files(root, include, exclude, follow_symlinks)`
  - `module_name_from_path(path, root, depth)`
- `src/rdocgen/parser.py`
  - `Parser` parses one file → `FileDoc`
- `src/rdocgen/project.py`
  - `build_project(root_or_file, options)` constructs Project → Module → File
- `src/rdocgen/render/`
  - `render/base.py`: `Renderer` interface
  - `render/markdown.py`: Markdown renderer (plain/nextra)
  - `render/json.py`: JSON exporter
- `src/rdocgen/exporter.py`
  - Manages output directories and writes files
- `src/rdocgen/cli.py`
  - CLI parsing only; calls `build_project` + `exporter`

### Benefits
- Each layer does one job (easier tests, faster iteration).
- New output formats become plug-ins.
- Parser is filesystem-agnostic.
- Discovery is AST-agnostic.

### Concrete Refactor Steps
1. Extract data classes from `parser.py` → `model.py`.
2. Move path traversal + filtering from `parser.py` → `discovery.py`.
3. Make `parser.py` strictly “parse one file”.
4. Add `project.py` to build the hierarchy from files.
5. Split rendering from filesystem writing (`render/` vs `exporter.py`).
6. Update CLI to use the new pipeline.

## Implementation Plan (initial)
1. Add CLI flags and a config object for parser/exporter options.
2. Implement include/exclude filtering and module depth control in parser.
3. Add visibility/type filters + sorting in exporter.
4. Improve docstring fence rewriting (correct open/close handling).
5. Add clean/no-clean and optional JSON emit.
