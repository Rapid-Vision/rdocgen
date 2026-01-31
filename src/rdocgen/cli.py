"""
Extracts documentation from a Python source file and generates Markdown files.

The output is structured for use with the [Nextra site generator](https://nextra.site/).
"""

import argparse

from .config import ExportOptions, ParseOptions, RenderOptions
from .docs import export_docs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--code",
        help="Path to the Python source file from which to extract documentation.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--outdir",
        help=(
            "Directory where the generated documentation will be saved. "
            "Warning: this directory will be deleted before export."
        ),
        required=True,
    )
    parser.add_argument(
        "--format",
        choices=["md-plain", "md-nextra"],
        default="md-nextra",
        help="Output format for generated docs.",
    )
    parser.add_argument(
        "--include-path",
        action="append",
        default=[],
        help="Glob pattern to include files (can be repeated).",
    )
    parser.add_argument(
        "--exclude-path",
        action="append",
        default=[],
        help="Glob pattern to exclude files (can be repeated).",
    )
    parser.add_argument(
        "--follow-symlinks",
        action="store_true",
        help="Follow symlinks when scanning directories.",
    )
    parser.add_argument(
        "--module-depth",
        default="1",
        help="Module grouping depth (e.g., 1, 2, all).",
    )
    parser.add_argument(
        "--clean",
        dest="clean",
        action="store_true",
        help="Delete output directory before export.",
    )
    parser.add_argument(
        "--no-clean",
        dest="clean",
        action="store_false",
        help="Do not delete output directory before export.",
    )
    parser.set_defaults(clean=True)
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private members starting with underscore.",
    )
    parser.add_argument(
        "--include-dunder",
        action="store_true",
        help="Include dunder members like __init__.",
    )
    parser.add_argument(
        "--include-types",
        default="",
        help="Comma-separated list of sections to include (class,function,enum,attribute).",
    )
    parser.add_argument(
        "--exclude-types",
        default="",
        help="Comma-separated list of sections to exclude (class,function,enum,attribute).",
    )
    parser.add_argument(
        "--sort",
        choices=["source-order", "alpha"],
        default="source-order",
        help="Ordering within sections.",
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Emit a single output file with all content.",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split output into separate files for classes, functions, and enums.",
    )
    parser.add_argument(
        "--index-title",
        default="Overview",
        help="Title for the root index page.",
    )
    parser.add_argument(
        "--docstring-style",
        choices=["raw", "python-fences", "preserve"],
        default="python-fences",
        help="Docstring rendering style for code fences.",
    )
    parser.add_argument(
        "--code-fence-language",
        default="python",
        help="Default language for unlabeled code fences.",
    )
    parser.add_argument(
        "--no-line-numbers",
        action="store_true",
        help="Disable showLineNumbers for Nextra code fences.",
    )
    parser.add_argument(
        "--output-extension",
        default="",
        help="Override output extension (e.g., .md, .mdx).",
    )
    parser.add_argument(
        "--fail-on-parse-error",
        action="store_true",
        help="Abort when a Python file fails to parse.",
    )
    args = parser.parse_args()

    include_types = [t.strip() for t in args.include_types.split(",") if t.strip()]
    exclude_types = [t.strip() for t in args.exclude_types.split(",") if t.strip()]

    module_depth = None
    if args.module_depth != "all":
        try:
            module_depth = int(args.module_depth)
        except ValueError:
            raise SystemExit(f"Invalid --module-depth: {args.module_depth}")
        if module_depth <= 0:
            module_depth = None

    parse_options = ParseOptions(
        include_paths=args.include_path,
        exclude_paths=args.exclude_path,
        follow_symlinks=args.follow_symlinks,
        module_depth=module_depth,
        fail_on_parse_error=args.fail_on_parse_error,
    )
    render_options = RenderOptions(
        output_format=args.format,
        output_extension=args.output_extension or None,
        include_types=include_types,
        exclude_types=exclude_types,
        include_private=args.include_private,
        include_dunder=args.include_dunder,
        sort=args.sort,
        flatten=args.flatten,
        split=args.split,
        index_title=args.index_title,
        docstring_style=args.docstring_style,
        code_fence_language=args.code_fence_language,
        show_line_numbers=not args.no_line_numbers,
    )
    export_options = ExportOptions(
        render=render_options,
        parse=parse_options,
        clean=args.clean,
    )

    export_docs(
        codepath=args.code,
        outdir=args.outdir,
        options=export_options,
    )


if __name__ == "__main__":
    main()
