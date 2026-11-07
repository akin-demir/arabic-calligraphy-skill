"""Manual grid integrity, refusal and export checks; not authenticity tests."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

from PIL import Image

from arabic_calligraphy.cli import main
from arabic_calligraphy.grid import inspect_grid, load_grid, render_grid

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples/square-kufic/allah-study.json"


class Grid(unittest.TestCase):
    def setUp(self):
        self.data = load_grid(SAMPLE)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_sample_geometry_and_source(self):
        report = inspect_grid(self.data)
        self.assertEqual(report["text"], "الله")
        self.assertTrue(report["geometry_passed"])
        self.assertEqual(report["occupied_cells"], 37)
        self.assertGreater(report["empty_2x2_count"], 0)
        self.assertEqual(self.data["rows"][0][-1], "A")  # alif physically at right
        self.assertEqual(self.data["text"], "".join(
            self.data["text"][item["start"]:item["end"]] for item in self.data["letters"]))

    def test_exports_are_exact_cells_and_svg_has_audit_map(self):
        png, svg = self.directory / "study.png", self.directory / "study.svg"
        render_grid(self.data, png, unit=8, padding=0, foreground="#000000", background="#ffffff")
        with Image.open(png) as picture:
            self.assertEqual(picture.size, (72, 72))
            rgb = picture.convert("RGB")
            for y, row in enumerate(self.data["rows"]):
                for x, label in enumerate(row):
                    expected = (255, 255, 255) if label == "." else (0, 0, 0)
                    for yy in range(y * 8, (y + 1) * 8):
                        for xx in range(x * 8, (x + 1) * 8):
                            self.assertEqual(rgb.getpixel((xx, yy)), expected)
        render_grid(self.data, svg)
        root = ET.parse(svg).getroot()
        metadata = json.loads(root.find("{http://www.w3.org/2000/svg}desc").text)
        self.assertEqual(metadata["grid"], self.data)
        self.assertIn("review pending", metadata["classification"])

    def test_invalid_source_mapping_is_refused(self):
        changes = [
            lambda d: d["letters"].pop(),
            lambda d: d["letters"][0].update(start=-1),
            lambda d: d["letters"][0].update(start=True),
            lambda d: d["letters"][1].update(start=0),
            lambda d: d["letters"][0].update(id="."),
            lambda d: d["letters"][1].update(id="A"),
            lambda d: d["rows"].__setitem__(0, "........."),
            lambda d: d["rows"].__setitem__(0, "....Z.B.A"),
            lambda d: d["rows"].__setitem__(0, "short"),
            lambda d: d.update(rows=[1]),
            lambda d: d.update(rows=[]),
            lambda d: d.update(text=""),
            lambda d: d.update(format="unsupported"),
        ]
        # Removing one occurrence is fine; removing every cell of a letter is not.
        changes[6] = lambda d: d.update(rows=[row.replace("A", ".") for row in d["rows"]])
        for change in changes:
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                change(data)
                with self.assertRaises(ValueError):
                    inspect_grid(data)

    def test_bad_geometry_reports_and_preserves_existing_output(self):
        for rows, counter in ((["AA", "AA"], "solid_2x2_count"),
                              (["A.", ".A"], "corner_only_2x2_count")):
            data = dict(format="square-kufic-grid-v1", text="ا",
                        letters=[dict(id="A", start=0, end=1)], rows=rows)
            report = inspect_grid(data)
            self.assertEqual(report[counter], 1)
            output = self.directory / "existing.svg"
            output.write_text("preserve")
            with self.assertRaisesRegex(ValueError, "inspect before export"):
                render_grid(data, output)
            self.assertEqual(output.read_text(), "preserve")

    def test_resource_limits_and_unsupported_pdf(self):
        for kwargs in (dict(unit=0), dict(unit=True), dict(padding=-1), dict(unit=256, padding=16),
                       dict(foreground="bad")):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                render_grid(self.data, self.directory / "x.png", **kwargs)
        with self.assertRaisesRegex(ValueError, "PNG and SVG only"):
            render_grid(self.data, self.directory / "x.pdf")
        oversized = self.directory / "big.json"
        oversized.write_bytes(b" " * 1_000_001)
        with self.assertRaises(ValueError):
            load_grid(oversized)

    def test_cli_inspection_export_and_same_file_refusal(self):
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            result = main(["grid", "--input", str(SAMPLE), "--output", str(self.directory / "x.svg")])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(capture.getvalue())["text"], "الله")
        source = self.directory / "input.json"
        source.write_text(SAMPLE.read_text())
        original = source.read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["grid", "--input", str(source), "--output", str(source)]), 2)
        self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
