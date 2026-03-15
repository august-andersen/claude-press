"""Markdown to PDF conversion pipeline."""

import re
from pathlib import Path

import markdown
from weasyprint import HTML

_STYLE_CSS = Path(__file__).parent / "style.css"

# Regex patterns for LaTeX math
_BLOCK_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")


def _render_math_to_svg(latex: str, display: bool = False) -> str:
    """Render a LaTeX expression to an inline SVG using matplotlib."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64

        fig, ax = plt.subplots(figsize=(0.01, 0.01))
        ax.set_axis_off()

        fontsize = 16 if display else 12
        text = ax.text(
            0.5,
            0.5,
            f"${latex}$",
            fontsize=fontsize,
            ha="center",
            va="center",
            transform=ax.transAxes,
        )

        fig.patch.set_alpha(0)
        buf = BytesIO()
        fig.savefig(
            buf,
            format="svg",
            bbox_inches="tight",
            pad_inches=0.05,
            transparent=True,
        )
        plt.close(fig)
        buf.seek(0)
        svg_data = buf.getvalue().decode("utf-8")

        # Strip XML declaration and doctype for inline embedding
        svg_data = re.sub(r"<\?xml.*?\?>", "", svg_data)
        svg_data = re.sub(r"<!DOCTYPE.*?>", "", svg_data, flags=re.DOTALL)

        if display:
            return f'<div class="math-block">{svg_data}</div>'
        else:
            return f'<span class="math-inline">{svg_data}</span>'

    except ImportError:
        # Fallback: render as styled monospace
        if display:
            return f'<div class="math-block"><code class="math-fallback">{latex}</code></div>'
        else:
            return f'<code class="math-fallback">{latex}</code>'


def _process_math(md_text: str) -> str:
    """Pre-process LaTeX math expressions before Markdown parsing."""

    def replace_block(m):
        return _render_math_to_svg(m.group(1).strip(), display=True)

    def replace_inline(m):
        return _render_math_to_svg(m.group(1).strip(), display=False)

    # Block math first ($$...$$), then inline ($...$)
    md_text = _BLOCK_MATH_RE.sub(replace_block, md_text)
    md_text = _INLINE_MATH_RE.sub(replace_inline, md_text)
    return md_text


def convert_md_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert a Markdown file to a styled PDF."""
    md_text = input_path.read_text(encoding="utf-8")

    # Process math before markdown conversion
    md_text = _process_math(md_text)

    # Convert Markdown to HTML
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "codehilite",
            "smarty",
            "attr_list",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": True,
                "noclasses": False,
            },
        },
    )
    body_html = md.convert(md_text)

    # Read CSS
    css = _STYLE_CSS.read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    # Generate PDF
    HTML(string=html, base_url=str(input_path.parent)).write_pdf(str(output_path))
