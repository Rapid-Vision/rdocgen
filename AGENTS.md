# Repository Guidelines

## Project Structure & Module Organization
- `src/rdocgen/cli.py`: CLI entry point parsing `--code` and `--outdir` flags.
- `src/rdocgen/docs.py`: AST-based extractor that rewrites docstrings into Nextra-friendly MDX.
- `src/rdocgen/__init__.py`: Exposes `main` for the `rdocgen` console script.
- `dist/`: Built wheel/tarball artifacts; regenerated on builds.
- `README.md`: Placeholder for product-level docs; keep in sync with CLI behavior.

## Development Setup
- Requires Python 3.13+.
- `uv` is used.

## Build, Test, and Development Commands
- `rdocgen -c path/to/source.py -o ./out_docs --format md-nextra`: Generate docs for a module; `out_docs` is deleted before writing. Use `md-plain` to omit Nextra annotations.
- `python -m rdocgen.cli -c ... -o ... --format md-plain`: Alternate invocation without the console script.
- `uv build`: Produce the wheel and sdist into `dist/`.
- Prefer running commands from the repo root to pick up the local package.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation; keep functions/classes named in `snake_case`/`CamelCase`.
- Add type hints for public interfaces; avoid underscores on parameters you want documented.
- Write docstrings with Markdown and fenced code blocks; the exporter annotates them with `python copy showLineNumbers`.
- Keep dependencies standard-library-first; update `pyproject.toml` before adding new ones.

## Testing Guidelines
- No automated suite yet; validate changes by running `rdocgen` against a sample module and reviewing the generated MDX.
- When adding tests, place them under `tests/` with `test_*.py` names and target pytest.
- Check that argument parsing, comment extraction, and docstring rewriting still produce expected sections.

## Commit & Pull Request Guidelines
- Use imperative, concise commit subjects (e.g., `Improve docstring rewrite for enums`); include context in the body when changing behavior.
- PRs should describe scope, include the exact command used to validate output, and link issues when applicable.
- Add before/after snippets or sample generated MDX when altering formatting or signatures.

## Security & Configuration Tips
- `--outdir` is removed before export; point it at a dedicated directory to avoid accidental data loss.
- Reject untrusted input paths; the tool reads and executes nothing, but avoid writing into shared system locations.
