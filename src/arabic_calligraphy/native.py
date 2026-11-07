"""Small typed ctypes boundary to stable Pango/Cairo/Fontconfig C APIs.

Pango delegates OpenType shaping to HarfBuzz and bidi layout to its native stack.
No custom glyph shaping or string reversal is performed here.
"""

import ctypes as C
from ctypes.util import find_library

P = C.c_void_p
I = C.c_int
D = C.c_double
S = C.c_char_p


def library(name):
    path = find_library(name)
    if not path:
        raise RuntimeError(f"Missing native dependency {name}; see docs/installation.md")
    return C.CDLL(path)


def bind(lib, name, result, *args):
    fn = getattr(lib, name)
    fn.restype = result
    fn.argtypes = args
    return fn


class Rectangle(C.Structure):
    _fields_ = [(name, I) for name in ("x", "y", "width", "height")]


class Native:
    def __init__(self):
        cairo = library("cairo")
        pango = library("pango-1.0")
        pc = library("pangocairo-1.0")
        fc = library("fontconfig")
        go = library("gobject-2.0")
        self.image = bind(cairo, "cairo_image_surface_create", P, I, I, I)
        self.svg = bind(cairo, "cairo_svg_surface_create", P, S, D, D)
        self.pdf = bind(cairo, "cairo_pdf_surface_create", P, S, D, D)
        self.context = bind(cairo, "cairo_create", P, P)
        self.destroy = bind(cairo, "cairo_destroy", None, P)
        self.finish = bind(cairo, "cairo_surface_finish", None, P)
        self.surface_destroy = bind(cairo, "cairo_surface_destroy", None, P)
        self.surface_status = bind(cairo, "cairo_surface_status", I, P)
        self.status = bind(cairo, "cairo_status", I, P)
        self.status_string = bind(cairo, "cairo_status_to_string", S, I)
        self.png = bind(cairo, "cairo_surface_write_to_png", I, P, S)
        self.color = bind(cairo, "cairo_set_source_rgba", None, P, D, D, D, D)
        self.paint = bind(cairo, "cairo_paint", None, P)
        self.move = bind(cairo, "cairo_move_to", None, P, D, D)
        self.rectangle = bind(cairo, "cairo_rectangle", None, P, D, D, D, D)
        self.stroke = bind(cairo, "cairo_stroke", None, P)
        self.line_width = bind(cairo, "cairo_set_line_width", None, P, D)
        self.show_page = bind(cairo, "cairo_show_page", None, P)
        self.layout = bind(pc, "pango_cairo_create_layout", P, P)
        self.show = bind(pc, "pango_cairo_show_layout", None, P, P)
        self.set_text = bind(pango, "pango_layout_set_text", None, P, S, I)
        self.set_width = bind(pango, "pango_layout_set_width", None, P, I)
        self.set_wrap = bind(pango, "pango_layout_set_wrap", None, P, I)
        self.set_alignment = bind(pango, "pango_layout_set_alignment", None, P, I)
        self.set_auto_dir = bind(pango, "pango_layout_set_auto_dir", None, P, I)
        self.get_context = bind(pango, "pango_layout_get_context", P, P)
        self.base_dir = bind(pango, "pango_context_set_base_dir", None, P, I)
        self.font_desc = bind(pango, "pango_font_description_from_string", P, S)
        self.font_size = bind(pango, "pango_font_description_set_absolute_size", None, P, D)
        self.set_font = bind(pango, "pango_layout_set_font_description", None, P, P)
        self.free_font = bind(pango, "pango_font_description_free", None, P)
        self.extents = bind(pango, "pango_layout_get_pixel_extents", None, P, P, P)
        self.unknown = bind(pango, "pango_layout_get_unknown_glyphs_count", I, P)
        self.line_count = bind(pango, "pango_layout_get_line_count", I, P)
        self.line = bind(pango, "pango_layout_get_line_readonly", P, P, I)
        self.line_start = bind(pango, "pango_layout_line_get_start_index", I, P)
        self.line_length = bind(pango, "pango_layout_line_get_length", I, P)
        self.unref = bind(go, "g_object_unref", None, P)
        self.fc_create = bind(fc, "FcConfigCreate", P)
        self.fc_add = bind(fc, "FcConfigAppFontAddFile", I, P, S)
        self.fc_current = bind(fc, "FcConfigSetCurrent", I, P)
        self.fc_destroy = bind(fc, "FcConfigDestroy", None, P)
        self.pango_version = bind(pango, "pango_version_string", S)
        self.cairo_version = bind(cairo, "cairo_version_string", S)

    def check(self, status):
        if status:
            raise RuntimeError(self.status_string(status).decode())
