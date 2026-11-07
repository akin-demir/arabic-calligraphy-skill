"""Command-line interface. No shell evaluation, HTML execution or network access."""

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .engine import render, styles
from .layouts import certificate, document, poster


def size(value):
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Size must be WIDTHxHEIGHT") from error


def main(argv=None):
    parser = argparse.ArgumentParser(prog="arabic-calligraphy")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("styles", help="Print honest style capability registry")
    for name in ("render", "poster"):
        p = commands.add_parser(name)
        p.add_argument("--text", required=True)
        p.add_argument("--style", default="naskh" if name == "render" else "kufic")
        p.add_argument("--output", type=Path, required=True)
        p.add_argument("--size", type=size, default=(1080, 1080 if name == "render" else 1350))
        p.add_argument("--font-size", type=float, default=96)
        p.add_argument("--margin", type=float, default=80)
        p.add_argument("--foreground", default="#132B2A" if name == "render" else "#F5EBD6")
        p.add_argument("--background", default="transparent" if name == "render" else "#132B2A")
        if name == "render":
            p.add_argument("--align", choices=["right", "center", "left"], default="right")
        else:
            p.add_argument("--subtitle")
    p = commands.add_parser("document")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--body-style", default="naskh")
    p.add_argument("--output", type=Path, required=True)
    p = commands.add_parser("certificate")
    p.add_argument("--recipient", required=True)
    p.add_argument("--body", required=True)
    p.add_argument("--title", default="شهادة تقدير")
    p.add_argument("--signature", default="")
    p.add_argument("--output", type=Path, required=True)
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        if command == "styles":
            print(json.dumps(styles(), ensure_ascii=False, indent=2))
            return 0
        if command in ("render", "poster"):
            args["width"], args["height"] = args.pop("size")
            result = (render if command == "render" else poster)(**args)
        elif command == "document":
            source = args.pop("input")
            if not source.is_file() or source.stat().st_size > 1_000_000:
                raise ValueError("Input must be a UTF-8 text file of at most 1 MB")
            if source.resolve() == args["output"].resolve():
                raise ValueError("Input and output must differ")
            result = document(source.read_text(encoding="utf-8"), **args)
        else:
            result = certificate(**args)
        print(result)
        return 0
    except (ValueError, RuntimeError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
