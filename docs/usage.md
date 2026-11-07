# CLI and Python API

`render` requires `--text` and `--output`. Options: `--style naskh|kufic|nastaliq`, `--size WIDTHxHEIGHT` (default 1080x1080), `--font-size` (96), `--margin` (80), `--align right|center|left`, `--foreground` and `--background`. Colors accept #RRGGBB, #RRGGBBAA or transparent. PNG dimensions are pixels; SVG uses user units; PDF uses points (72 per inch). Larger PNG dimensions with proportional font/margin sizing provide higher pixel resolution; no misleading DPI-only option is offered.

`poster` shares those options except alignment, and adds `--subtitle`; its default canvas is 1080x1350. For an Instagram square use 1080x1080; for a story use 1080x1920. Review composition for each aspect ratio. `certificate` accepts `--recipient`, `--body`, optional `--title`, `--signature`, and `--output`; canvas is landscape 1190x842. Long entries that do not fit fail rather than being clipped.

`document --input report.md --body-style naskh --output report.pdf` creates a new paginated PDF. Input is a UTF-8 text file up to 1 MB. Only #, ## and ### headings receive special treatment. Other Markdown and HTML are literal text. Code is never evaluated. Font size and page dimensions are configurable through the Python API, not this CLI command.

```python
from arabic_calligraphy.engine import render
from arabic_calligraphy.layouts import poster, certificate, document

render("العلم نور", "wordmark.svg", width=900, height=400,
       font_size=80, margin=50, align="center")
poster("اللغة العربية", "poster.png", subtitle="العلم نور")
certificate("أحمد محمد", "تقديراً للجهود المتميزة", "certificate.pdf")
document("# عنوان\nنص التقرير", "report.pdf", font_size=18, margin=54)
```

Functions return a pathlib.Path. Invalid text, absent coverage, unsupported styles, invalid dimensions and overflow raise ValueError. Native export failures raise RuntimeError. The CLI reports these on stderr and returns 2. Output parents must exist. Writes use a sibling temporary file followed by atomic replacement; failures preserve an existing output. An explicit existing output path is replaced on success. Symlink outputs are refused. Callers choose paths deliberately; do not derive output paths directly from untrusted document titles.

SVG is outlined artwork with original text in a description, not editable live text. PDFs embed font subsets and include logical ActualText mappings; generic extractors may still reorder characters. Retain the structured source for text fidelity.
