"""Generate the README hero from the actual manually authored Square Kufic grid."""

import json
from pathlib import Path

from arabic_calligraphy.engine import Canvas, backend, color
from arabic_calligraphy.grid import inspect_grid, load_grid
from arabic_calligraphy.layouts import draw_block
from arabic_calligraphy.native import P, bind, library

ROOT = Path(__file__).resolve().parents[1]


def generate_hero():
    data = load_grid(ROOT / "examples/square-kufic/readme-rosette.json")
    if not inspect_grid(data)["geometry_passed"]:
        raise ValueError("README motif must pass grid inspection")
    dest = ROOT / "examples/gallery"
    dest.mkdir(exist_ok=True)
    description = json.dumps({"title": "Arabic Calligraphy / Square Kufic manual study",
                              "grid": data}, ensure_ascii=False)
    for ext in ("png", "svg"):
        with Canvas(dest / f"readme-square-kufic.{ext}", 1600, 880, "#F5F0E6", description) as canvas:
            n = backend()
            fill = bind(library("cairo"), "cairo_fill", None, P)
            # Warm accents distinguish rotated source words, not invented filler strokes.
            for labels, ink in (("ABCDIJKL", "#173E3C"), ("EFGHMNOP", "#AB7F3C")):
                n.color(canvas.context, *color(ink))
                for y, row in enumerate(data["rows"]):
                    for x, label in enumerate(row):
                        if label in labels:
                            n.rectangle(canvas.context, 116 + x * 28, 176 + y * 28, 28, 28)
                fill(canvas.context)
            n.color(canvas.context, *color("#CFC6B5"))
            n.rectangle(canvas.context, 730, 176, 1, 532)
            n.rectangle(canvas.context, 116, 100, 1368, 1)
            fill(canvas.context)
            for text, size, x, y, width, height, ink in (
                ("A R A B I C   C A L L I G R A P H Y", 21, 116, 48, 1368, 40, "#173E3C"),
                ("SQUARE KUFIC / MANUAL GRID STUDY", 20, 808, 178, 675, 40, "#8F672F"),
                ("Arabic\nCalligraphy", 78, 800, 253, 684, 235, "#173E3C"),
                ("Four turns / One modular grid", 28, 808, 525, 675, 65, "#173E3C"),
                ("Twenty documented traditions\nFour font workflows + editable grid studies", 22, 808, 625, 675, 90, "#5C6962"),
                ("الله × 4", 30, 116, 745, 532, 65, "#173E3C"),
                ("OPEN SOURCE / OFFLINE / PNG + SVG", 18, 808, 777, 675, 40, "#5C6962"),
            ):
                draw_block(canvas, text, "Noto Naskh Arabic" if text == "الله × 4" else "Noto Sans",
                           size, x, y, width, height, align="left", ink=ink)


if __name__ == "__main__":
    generate_hero()
