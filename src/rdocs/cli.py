"""
Extracts documentation from a Python source file and generates Markdown files.

The output is structured for use with the [Nextra site generator](https://nextra.site/).
"""

import argparse
from .docs import extract_docs


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
        help="Directory where the generated documentation will be saved. Warning: this directory will be deleted before export.",
        required=True,
    )
    args = parser.parse_args()

    extract_docs(
        codepath=args.code,
        outdir=args.outdir,
    )


if __name__ == "__main__":
    main()
