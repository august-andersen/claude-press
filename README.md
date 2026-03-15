# claude-press

Convert markdown files into typeset PDFs with Claude research output formatting.

## Installation

```bash
git clone https://github.com/august-andersen/claude-press.git
cd claude-press
pip install .
```

## Usage

```bash
# Basic — outputs notes.pdf in the same directory
claude-press notes.md

# Custom output path
claude-press lecture.md -o formatted-lecture.pdf
```

## Supported Features

- **Headings** (H1–H6) with clean typographic hierarchy
- **Bold** and *italic* text
- Fenced code blocks with syntax highlighting (via Pygments)
- Inline `code` references
- Tables with minimal styling
- LaTeX math — inline ($...$) and display ($$...$$)
- Horizontal rules
- Blockquotes
- Images (embedded, centered)
- Bulleted and numbered lists

## Dependencies

- [WeasyPrint](https://weasyprint.org/) — HTML/CSS to PDF
- [Python-Markdown](https://python-markdown.github.io/) — Markdown parsing
- [Pygments](https://pygments.org/) — Syntax highlighting
- [matplotlib](https://matplotlib.org/) — LaTeX math rendering (optional, for math support)

## License

MIT
