"""Measured poster, certificate and paginated plain-Markdown PDF layouts."""

from pathlib import Path
import re

from .engine import (
    Canvas, Layout, backend, color, dimensions, family_for, validate_text, validate_style_output,
)
from .fonts import validate_coverage


def draw_block(canvas, text, family, size, x, y, width, available, align="center", ink="#F5EBD6"):
    validate_text(text)
    validate_coverage(text, family)
    layout = Layout(canvas.context, text, family, size, width, align)
    try:
        if layout.height > available or layout.width > width:
            raise ValueError("Layout overflow: shorten text or reduce font size")
        backend().color(canvas.context, *color(ink))
        layout.draw(canvas.context, x - layout.left, y)
        return layout.height
    finally:
        layout.close()


def border(canvas, inset, ink="#B89960"):
    n = backend()
    n.color(canvas.context, *color(ink))
    n.line_width(canvas.context, 2)
    n.rectangle(canvas.context, inset, inset, canvas.width - 2 * inset, canvas.height - 2 * inset)
    n.stroke(canvas.context)


def poster(text, output, *, style="kufic", subtitle=None, width=1080, height=1350,
           font_size=100, margin=90, foreground="#F5EBD6", background="#132B2A"):
    """Measured headline and optional Naskh supporting line with a fine border."""
    validate_text(text)
    dimensions(width, height, margin, font_size)
    family = validate_style_output(style, output)
    text_all = text + ("\n" + subtitle if subtitle else "")
    with Canvas(output, width, height, background, text_all) as canvas:
        border(canvas, margin / 2)
        draw_block(canvas, text, family, font_size, margin, margin + (height - 2 * margin) * .25,
                   width - 2 * margin, (height - 2 * margin) * .4, ink=foreground)
        if subtitle:
            draw_block(canvas, subtitle, family_for("naskh"), font_size * .42, margin,
                       margin + (height - 2 * margin) * .75, width - 2 * margin,
                       (height - 2 * margin) * .25, ink=foreground)
    return Path(output)


def certificate(recipient, body, output, *, title="شهادة تقدير", signature="",
                width=1190, height=842):
    """Landscape certificate; Naskh typography, not the Ijazah calligraphic hand."""
    validate_text(recipient)
    validate_text(body)
    dimensions(width, height, 70, 52)
    scale = min(width / 1190, height / 842)
    text_all = "\n".join(x for x in (title, recipient, body, signature) if x)
    with Canvas(output, width, height, "#FAF6EC", text_all) as canvas:
        border(canvas, 30 * scale)
        border(canvas, 40 * scale)
        family = family_for("naskh")
        for text, size, y, available in (
            (title, 64, 90, 150), (recipient, 52, 260, 130),
            (body, 30, 430, 180), (signature, 26, 680, 80),
        ):
            if text:
                draw_block(canvas, text, family, size * scale, 80 * scale, y * height / 842,
                           width - 160 * scale, available * height / 842,
                           ink="#132B2A")
    return Path(output)


def document(text, output, *, body_style="naskh", width=595, height=842,
             font_size=18, margin=54):
    """Create paginated PDF. Supports #/##/### headings and plain text lines.

    Other Markdown (links, HTML, tables, code) is displayed literally, never run.
    No external resources are loaded. Numbers in footers use explicit Noto Sans.
    """
    validate_text(text)
    if Path(output).suffix.lower() != ".pdf":
        raise ValueError("Documents require .pdf output")
    dimensions(width, height, margin, font_size)
    family = validate_style_output(body_style, output)
    n = backend()
    page = 1
    y = margin
    current = []
    with Canvas(output, width, height, "#FFFFFF") as canvas:
        def footer():
            draw_block(canvas, str(page), "Noto Sans", 11, margin, height - margin + 12,
                       width - 2 * margin, 30, ink="#66716E")

        def next_page():
            nonlocal page, y, current
            if page >= 200:
                raise ValueError("Document exceeds 200 pages")
            footer()
            canvas.page_texts.append("\n".join(current) + "\n" + str(page))
            n.show_page(canvas.context)
            canvas.background()
            page += 1
            y = margin
            current = []

        for raw in text.splitlines():
            match = re.match(r"^(#{1,3}) (.+)$", raw)
            content = match[2] if match else raw
            size = font_size * (1.6 - len(match[1]) * .12) if match else font_size
            if not content.strip():
                y += size * .7
                continue
            validate_coverage(content, family)
            # Ask Pango for UTF-8 line boundaries; never split codepoints or guess widths.
            probe = Layout(canvas.context, content, family, size, width - 2 * margin)
            try:
                encoded = content.encode()
                lines = []
                for i in range(n.line_count(probe.ptr)):
                    line = n.line(probe.ptr, i)
                    start, length = n.line_start(line), n.line_length(line)
                    lines.append(encoded[start:start + length].decode())
            finally:
                probe.close()
            for line in lines:
                # Whitespace is retained in semantic PDF text; avoid blank draw calls.
                if not line.strip():
                    current.append(line)
                    continue
                measured = Layout(canvas.context, line, family, size, width - 2 * margin)
                try:
                    h = measured.height
                    if h > height - 2 * margin:
                        raise ValueError("A single line exceeds the page content area")
                    if y + h > height - margin:
                        next_page()
                    if measured.width > width - 2 * margin:
                        raise ValueError("Document line overflows its margins")
                    n.color(canvas.context, *color("#132B2A"))
                    measured.draw(canvas.context, margin - measured.left, y)
                    y += h + size * .12
                    current.append(line)
                finally:
                    measured.close()
            y += size * .35
        footer()
        canvas.page_texts.append("\n".join(current) + "\n" + str(page))
    return Path(output)
