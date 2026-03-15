# claude-press

Convert markdown files into typeset PDFs with Claude research output formatting.

## Installation

**Recommended** (installs globally without a virtual environment):

```bash
brew install pipx && pipx ensurepath   # one-time setup, if you don't have pipx
pipx install git+https://github.com/august-andersen/claude-press.git
```

**Alternative** (using pip in a virtual environment):

```bash
git clone https://github.com/august-andersen/claude-press.git
cd claude-press
python3 -m venv .venv && source .venv/bin/activate
pip install .
```

## Usage

```bash
# Basic — outputs notes.pdf in the same directory
claude-press notes.md

# Custom output path
claude-press lecture.md -o formatted-lecture.pdf
```

## Dependencies

- [WeasyPrint](https://weasyprint.org/) — HTML/CSS to PDF
- [Python-Markdown](https://python-markdown.github.io/) — Markdown parsing
- [Pygments](https://pygments.org/) — Syntax highlighting
- [matplotlib](https://matplotlib.org/) — LaTeX math rendering (optional, for math support)

## License

MIT
