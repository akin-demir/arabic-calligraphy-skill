"""Verified bundled fonts and deterministic process-local discovery."""

import hashlib
import json
import warnings
import unicodedata
from functools import lru_cache
from pathlib import Path

from fontTools.ttLib import TTFont

DATA = Path(__file__).parent / "data"


@lru_cache(maxsize=1)
def manifest():
    return json.loads((DATA / "fonts.json").read_text())


@lru_cache(maxsize=1)
def coverage():
    result = {}
    for record in manifest():
        path = DATA / "fonts" / record["file"]
        if not path.is_file():
            raise ValueError(f"Missing bundled font: {path.name}; reinstall the package")
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"Font hash mismatch: {path.name}")
        with TTFont(path) as font:
            if font["OS/2"].fsType != record["fs_type"] or record["license"] != "OFL-1.1":
                raise ValueError(f"Unverified embedding license: {path.name}")
            if record["fs_type"] != 0 and not (
                (record["fs_type"] == 2 and record.get("embedding_permission") is False
                 and record.get("export_formats") == ["png", "svg"])
                or (record["fs_type"] == 8 and record.get("embedding_permission") is True
                    and record.get("export_formats") == ["png", "svg", "pdf"])
            ):
                raise ValueError(f"Unsupported font embedding policy: {path.name}")
            required = ("GSUB",) if record.get("positioning") == "legacy-no-gpos" else ("GSUB", "GPOS")
            if not all(t in font for t in required):
                raise ValueError(f"Missing shaping tables: {path.name}")
            result[record["family"]] = set(font.getBestCmap())
    return result


def validate_coverage(text, family):
    record = next(item for item in manifest() if item["family"] == family)
    if record.get("positioning") == "legacy-no-gpos" and any(
        unicodedata.category(c) in ("Mn", "Me") for c in text
    ):
        label = record.get("display_style", family)
        raise ValueError(f"{label} combining marks/harakat are not supported by this font's positioning; use unvocalized text or Naskh")
    primary = coverage()[family]
    latin = coverage()["Noto Sans"]
    missing = set()
    fallback = set()
    for char in text:
        if char in "\n\t\r\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069":
            continue
        if ord(char) not in primary:
            # Only explicit Latin/Common fallback; never substitute Arabic letters.
            if ord(char) in latin and (ord(char) < 0x300 or char in "—–…•“”‘’"):
                fallback.add(char)
            else:
                missing.add(char)
    if missing:
        codes = ", ".join(f"U+{ord(c):04X}" for c in sorted(missing))
        raise ValueError(f"Font {family} lacks coverage: {codes}")
    if fallback:
        warnings.warn("Explicit Noto Sans fallback for Latin/Common characters", stacklevel=2)


def register(native):
    coverage()
    cfg = native.fc_create()
    try:
        for item in manifest():
            if not native.fc_add(cfg, str(DATA / "fonts" / item["file"]).encode()):
                raise RuntimeError(f"Fontconfig registration failed: {item['file']}")
        if not native.fc_current(cfg):
            raise RuntimeError("Fontconfig could not select bundled font configuration")
    finally:
        native.fc_destroy(cfg)
