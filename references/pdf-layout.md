# New and existing PDFs

Create new reports, letters and simple booklets with document(). Paragraphs use RTL base direction, Pango wrapping and embedded bundled fonts. Markdown headings, page numbers and configurable API margins are implemented. Tables, running headers, footnotes, images, imposition and full Markdown publishing are not.

PDF ActualText stores logical source text associated with the drawn glyphs; extracting and selecting Arabic remains reader-dependent. Source mapping tests pass, but pypdf raw extraction of mixed/marked Arabic is not exact. Do not promise universal searchable strings or lossless copy/paste. Keep the original UTF-8 document and test the target viewer.

Existing PDF modification is not implemented. For a separate editing workflow, inspect original fonts, encoding, encryption, form fields and annotations before choosing a PDF library. Adding an overlay or filling a form can be safer than replacing page content. Preserve the supplied original; no general-purpose text replacement with perfect layout preservation is promised.
