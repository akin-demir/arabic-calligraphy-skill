"""Pango layout, offline Cairo exports and explicit overflow errors."""

import ctypes as C
import json
import math
import os
from pathlib import Path
import re
import tempfile
from functools import lru_cache
from xml.etree import ElementTree as ET

from .fonts import DATA, manifest, register, validate_coverage
from .native import Native, Rectangle


@lru_cache(maxsize=1)
def backend():
    native = Native()
    register(native)
    return native


def styles():
    return json.loads((DATA / "capabilities.json").read_text())["styles"]


def family_for(style):
    for entry in styles():
        if entry["id"] == style:
            if not entry["implemented"]:
                raise ValueError(f"Style '{style}' is Reference Only; choose naskh, kufic, nastaliq or diwani")
            return entry["font_family"]
    raise ValueError(f"Unknown style: {style}")


def validate_style_output(style, output):
    family = family_for(style)
    record = next(item for item in manifest() if item["family"] == family)
    allowed = record.get("export_formats", ["png", "svg", "pdf"])
    if Path(output).suffix.lower().lstrip(".") not in allowed:
        raise ValueError(f"Style '{style}' supports only {', '.join(allowed)}; this font's embedding flag prevents PDF export")
    return family


def validate_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a nonempty Unicode string")
    if len(text) > 100_000:
        raise ValueError("Text exceeds 100000 characters")
    for c in text:
        if (ord(c) < 32 and c not in "\n\r\t") or 0xD800 <= ord(c) <= 0xDFFF:
            raise ValueError("Text contains unsupported control or surrogate characters")
    return text


def color(value):
    if value == "transparent":
        return (0, 0, 0, 0)
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", value):
        raise ValueError("Color must be #RRGGBB, #RRGGBBAA or transparent")
    return tuple(int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)) + (
        int(value[7:9], 16) / 255 if len(value) == 9 else 1,
    )


def finite(value, name, low, high):
    if not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be between {low} and {high}")


class Layout:
    def __init__(self, context, text, family, size, width, align="right"):
        n = backend()
        self.ptr = n.layout(context)
        try:
            n.base_dir(n.get_context(self.ptr), 1)  # PANGO_DIRECTION_RTL
            n.set_auto_dir(self.ptr, 0)  # RTL paragraph; bidi runs remain automatic.
            encoded = text.encode("utf-8")
            n.set_text(self.ptr, encoded, len(encoded))
            n.set_width(self.ptr, int(max(1, width - 4) * 1024))
            n.set_wrap(self.ptr, 2)  # PANGO_WRAP_WORD_CHAR
            n.set_alignment(self.ptr, {"left": 0, "center": 1, "right": 2}[align])
            desc = n.font_desc((family + ",Noto Sans").encode())
            try:
                n.font_size(desc, size * 1024)
                n.set_font(self.ptr, desc)
            finally:
                n.free_font(desc)
            if n.unknown(self.ptr):
                raise ValueError("Pango produced unknown glyphs; export refused")
            ink, logical = Rectangle(), Rectangle()
            n.extents(self.ptr, C.byref(ink), C.byref(logical))
            self.left = min(0, ink.x) if ink.x < 0 else max(0, ink.x + ink.width - width)
            self.top = min(0, ink.y, logical.y)
            self.right = max(ink.x + ink.width, logical.x + logical.width)
            self.bottom = max(ink.y + ink.height, logical.y + logical.height)
            self.height = self.bottom - self.top
            self.width = max(ink.width, logical.width)
        except BaseException:
            self.close()
            raise

    def draw(self, context, x, y):
        n = backend()
        n.move(context, x, y - self.top)
        n.show(context, self.ptr)

    def close(self):
        if self.ptr:
            backend().unref(self.ptr)
            self.ptr = None


class Canvas:
    def __init__(self, output, width, height, background, text=None):
        self.output = Path(output)
        self.suffix = self.output.suffix.lower()
        if self.suffix not in (".png", ".svg", ".pdf"):
            raise ValueError("Output extension must be .png, .svg or .pdf")
        if self.output.is_symlink():
            raise ValueError("Refusing symlink output")
        if not self.output.parent.is_dir():
            raise ValueError("Output parent directory does not exist")
        self.bg = color(background)
        self.width, self.height, self.text = width, height, text
        self.page_texts = [text] if text is not None else []
        self.surface = self.context = None
        fd, self.temp = tempfile.mkstemp(prefix=".arabic-", suffix=self.suffix, dir=self.output.parent)
        os.close(fd)

    def __enter__(self):
        n = backend()
        try:
            if self.suffix == ".png":
                self.surface = n.image(0, self.width, self.height)
            else:
                self.surface = (n.svg if self.suffix == ".svg" else n.pdf)(
                    os.fsencode(self.temp), self.width, self.height
                )
            n.check(n.surface_status(self.surface))
            self.context = n.context(self.surface)
            n.check(n.status(self.context))
            self.background()
            return self
        except BaseException:
            self.cleanup()
            raise

    def background(self):
        n = backend()
        n.color(self.context, *self.bg)
        n.paint(self.context)

    def cleanup(self):
        n = backend()
        if self.context:
            n.destroy(self.context)
            self.context = None
        if self.surface:
            n.surface_destroy(self.surface)
            self.surface = None
        Path(self.temp).unlink(missing_ok=True)

    def __exit__(self, exc_type, exc, tb):
        n = backend()
        try:
            if exc_type is None:
                n.check(n.status(self.context))
                if self.suffix == ".png":
                    n.check(n.png(self.surface, os.fsencode(self.temp)))
                n.finish(self.surface)
                n.check(n.surface_status(self.surface))
                if self.suffix == ".svg" and self.text is not None:
                    # Outlined artwork plus exact original text as accessible metadata.
                    tree = ET.parse(self.temp)
                    desc = ET.Element("{http://www.w3.org/2000/svg}desc")
                    desc.text = self.text
                    tree.getroot().insert(0, desc)
                    serialized = ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True)
                    Path(self.temp).write_bytes(serialized.replace(b"\r", b"&#13;"))
                if self.suffix == ".pdf" and self.page_texts:
                    from .pdf import attach_actual_text

                    attach_actual_text(Path(self.temp), self.page_texts)
                os.replace(self.temp, self.output)
        finally:
            self.cleanup()


def dimensions(width, height, margin, font_size):
    for value, name, low, high in (
        (width, "width", 32, 8192), (height, "height", 32, 8192),
        (margin, "margin", 0, 4096), (font_size, "font size", 1, 1024),
    ):
        finite(value, name, low, high)
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Canvas dimensions must be integers")
    if width * height > 32_000_000:
        raise ValueError("Canvas exceeds 32 million pixels")
    if 2 * margin >= min(width, height):
        raise ValueError("Margins leave no content area")


def render(text, output, *, style="naskh", width=1080, height=1080, font_size=96,
           margin=80, foreground="#132B2A", background="transparent", align="right"):
    """Render exact Unicode input. SVG outlines; PDF native selectable text.

    Dimensions are pixels for PNG and user units for SVG / points for PDF.
    Overflow raises ValueError without replacing an existing output.
    """
    validate_text(text)
    dimensions(width, height, margin, font_size)
    if align not in ("left", "center", "right"):
        raise ValueError("Alignment must be left, center or right")
    family = validate_style_output(style, output)
    validate_coverage(text, family)
    fg = color(foreground)
    with Canvas(output, width, height, background, text) as canvas:
        layout = Layout(canvas.context, text, family, font_size, width - 2 * margin, align)
        try:
            if layout.height > height - 2 * margin or layout.width > width - 2 * margin:
                raise ValueError("Text overflow: increase canvas size or reduce font size")
            backend().color(canvas.context, *fg)
            layout.draw(canvas.context, margin - layout.left, (height - layout.height) / 2)
        finally:
            layout.close()
    return Path(output)
