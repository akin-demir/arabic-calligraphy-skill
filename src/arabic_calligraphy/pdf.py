"""Associate original logical text with drawn content using PDF ActualText.

This is a semantic replacement for the real drawn glyphs, not an invisible duplicate
text layer. Consumers that ignore ActualText can still extract in visual order.
"""

import io

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject


def attach_actual_text(path, page_texts):
    reader = PdfReader(io.BytesIO(path.read_bytes()))
    if len(reader.pages) != len(page_texts):
        raise ValueError("PDF page/text count mismatch")
    writer = PdfWriter()
    for page, text in zip(reader.pages, page_texts, strict=True):
        original = page.get_contents().get_data()
        semantic = (b"\xfe\xff" + text.encode("utf-16-be")).hex().encode("ascii")
        stream = DecodedStreamObject()
        stream.set_data(b"/Span << /ActualText <" + semantic + b"> >> BDC\n" + original + b"\nEMC\n")
        page[NameObject("/Contents")] = stream
        writer.add_page(page)
    writer.add_metadata({"/Creator": "Arabic Calligraphy Agent Skill", "/Language": "ar"})
    with path.open("wb") as dest:
        writer.write(dest)
