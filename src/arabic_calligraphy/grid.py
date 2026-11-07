"""Manual Square Kufic studies. Geometry checks do not authenticate Arabic.

Rows are physical canvas coordinates, never a reversed or reshaped source string.
Each occupied cell belongs to a source span for human letter-by-letter review.
"""

import json
from pathlib import Path

from .engine import Canvas, backend, color, validate_text
from .native import P, bind, library


def inspect_grid(data):
    if not isinstance(data, dict) or data.get("format") != "square-kufic-grid-v1":
        raise ValueError("Expected square-kufic-grid-v1 object")
    text = validate_text(data.get("text"))
    if len(text) > 512:
        raise ValueError("Grid text exceeds 512 characters")
    rows, letters = data.get("rows"), data.get("letters")
    if (not isinstance(rows, list) or not 1 <= len(rows) <= 129
            or any(not isinstance(row, str) for row in rows)
            or not 1 <= len(rows[0]) <= 129
            or any(len(row) != len(rows[0]) for row in rows)):
        raise ValueError("Rows must be a rectangular grid of at most 129 by 129 cells")
    if not isinstance(letters, list) or not 1 <= len(letters) <= 62:
        raise ValueError("Provide 1–62 letter/source-span records")
    ids, covered = set(), set()
    for item in letters:
        if not isinstance(item, dict):
            raise ValueError("Each letter record must be an object")
        label, start, end = item.get("id"), item.get("start"), item.get("end")
        if (not isinstance(label, str) or len(label) != 1
                or label not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                or label in ids):
            raise ValueError("Letter IDs must be distinct ASCII letters or digits")
        if (type(start) is not int or type(end) is not int
                or not 0 <= start < end <= len(text)
                or not text[start:end].strip()):
            raise ValueError("Each source span must select nonempty text by Python character offsets")
        span = set(range(start, end))
        if covered & span:
            raise ValueError("Source spans must not overlap")
        covered |= span
        ids.add(label)
    required = {i for i, char in enumerate(text) if not char.isspace()}
    if required - covered:
        raise ValueError("Every non-whitespace source character needs a letter record")
    used = set("".join(rows)) - {"."}
    if used != ids:
        raise ValueError("Every letter ID needs cells; every occupied cell needs a letter record")
    width, height = len(rows[0]), len(rows)
    thick, corner, empty = [], [], 0
    for y in range(height - 1):
        for x in range(width - 1):
            block = tuple(rows[yy][xx] != "." for yy, xx in
                          ((y, x), (y, x + 1), (y + 1, x), (y + 1, x + 1)))
            if all(block):
                thick.append([x, y])
            if block in ((True, False, False, True), (False, True, True, False)):
                corner.append([x, y])
            if not any(block):
                empty += 1
    return {
        "classification": "manual-grid-study; Arabic and composition review pending",
        "text": text, "columns": width, "rows": height,
        "occupied_cells": sum(c != "." for row in rows for c in row),
        "geometry_passed": not thick and not corner,
        "solid_2x2_count": len(thick), "solid_2x2_first": thick[:16],
        "corner_only_2x2_count": len(corner), "corner_only_2x2_first": corner[:16],
        "empty_2x2_count": empty,
        "odd_dimensions": bool(width % 2 and height % 2),
        "note": "Checks cannot verify letterforms, joins, reading order or authenticity. "
                "Empty patches indicate space to compose; a rectangular study is not a packed emblem.",
    }


def load_grid(source):
    source = Path(source)
    if not source.is_file() or source.stat().st_size > 1_000_000:
        raise ValueError("Grid input must be a UTF-8 JSON file of at most 1 MB")
    data = json.loads(source.read_text(encoding="utf-8"))
    inspect_grid(data)
    return data


def render_grid(data, output, unit=48, padding=2,
                foreground="#132B2A", background="#F5EBD6"):
    report = inspect_grid(data)
    output = Path(output)
    if output.suffix.lower() not in (".png", ".svg"):
        raise ValueError("Manual grid studies support PNG and SVG only")
    if type(unit) is not int or not 1 <= unit <= 256:
        raise ValueError("Unit must be an integer from 1 to 256")
    if type(padding) is not int or not 0 <= padding <= 16:
        raise ValueError("Padding must be an integer from 0 to 16 grid units")
    width = (report["columns"] + 2 * padding) * unit
    height = (report["rows"] + 2 * padding) * unit
    if min(width, height) < 32 or max(width, height) > 8192 or width * height > 32_000_000:
        raise ValueError("Grid canvas must be 32–8192 pixels per side and at most 32 million pixels")
    if not report["geometry_passed"]:
        raise ValueError("Grid has solid 2x2 blocks or corner-only contacts; inspect before export")
    rgba = color(foreground)
    color(background)
    # Metadata records exact source and per-letter cells, never claims these prove spelling.
    description = json.dumps({"classification": report["classification"], "grid": data},
                             ensure_ascii=False, separators=(",", ":"))
    with Canvas(output, width, height, background, description) as canvas:
        n = backend()
        fill = bind(library("cairo"), "cairo_fill", None, P)
        n.color(canvas.context, *rgba)
        for y, row in enumerate(data["rows"]):
            for x, label in enumerate(row):
                if label != ".":
                    n.rectangle(canvas.context, (x + padding) * unit,
                                (y + padding) * unit, unit, unit)
        fill(canvas.context)
    return output
