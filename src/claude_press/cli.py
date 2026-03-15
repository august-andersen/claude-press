"""CLI entry point for claude-press."""

import argparse
import sys
from pathlib import Path

from .converter import convert_md_to_pdf


def main():
    parser = argparse.ArgumentParser(
        prog="claude-press",
        description="Convert Markdown files into beautifully typeset PDFs.",
    )
    parser.add_argument("input", help="Path to the Markdown file")
    parser.add_argument(
        "-o", "--output", help="Output PDF path (default: same name as input with .pdf extension)"
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.", file=sys.stderr)
        sys.exit(1)
    if not input_path.is_file():
        print(f"Error: {input_path} is not a file.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_suffix(".pdf")

    convert_md_to_pdf(input_path, output_path)
    print(f"✓ {output_path}")


if __name__ == "__main__":
    main()
