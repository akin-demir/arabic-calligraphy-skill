---
name: arabic-calligraphy-skill
description: Create correctly shaped Arabic typography, posters, certificates, SVG/PNG artwork and new PDF documents. Use when a user requests Arabic lettering, RTL typesetting, calligraphy style guidance or Arabic document generation. Distinguishes font typography from expert calligraphy.
license: MIT
compatibility: Python 3.11+ on Linux with Pango, Cairo, Fontconfig and HarfBuzz. Install the Python package separately; skill installation alone does not install native dependencies.
metadata:
  version: "0.1.0rc1"
---

# Arabic typography workflow

1. Preserve the user's exact Unicode text. Confirm uncertain spelling with the user before rendering. Never reverse text, replace letters, normalize marks or apply a separate reshaper.
2. Read [capabilities](capabilities.json). Select a genuinely implemented style for the purpose. Read only the corresponding `references/styles/<style>.md`. Reference-only traditions require manual artwork; offer a supported alternative explicitly.
3. Use the environment's installed `arabic-calligraphy` CLI, or install this directory with `python -m pip install .` after following [installation](docs/installation.md). Native dependencies are mandatory. Installation can require network; rendering does not.
4. Render: `arabic-calligraphy render --text "العلم نور" --style naskh --output artwork.svg`. For PNG change the extension. Use `poster` for artwork and `certificate` for structured certificates. Use `document --input examples/documents/report.md --output report.pdf` for new PDFs. Read [PDF layout](references/pdf-layout.md) for constraints.
5. Inspect the actual output for mark collisions, clipping, spelling, reading order and visual hierarchy. Report missing coverage or overflow; do not suppress errors. Review selectable PDF text separately from appearance.
6. Deliver the actual file with its capability classification. These are font-based approximations, never independently authenticated classical compositions. Request human calligraphy review for ceremonial, religious or historical fidelity.

Existing PDFs: preserve the original. This package creates new documents; it does not implement arbitrary replacement of text in supplied PDFs. See [typography](references/typography.md) and [poster guidance](references/posters.md) only as needed.
