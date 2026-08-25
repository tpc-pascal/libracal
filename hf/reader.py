import os
import fitz
from PIL import Image, ImageDraw

_pdf_cache = {}


def _get_doc(pdf_path):
    if pdf_path not in _pdf_cache:
        _pdf_cache[pdf_path] = fitz.open(pdf_path)
    return _pdf_cache[pdf_path]


def render_page(pdf_path, page_num, scale=2.0):
    if not pdf_path or not os.path.isfile(pdf_path):
        return None
    try:
        doc = _get_doc(pdf_path)
        if page_num < 0 or page_num >= len(doc):
            return None
        page = doc[page_num]
        mat = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    except Exception:
        return None


def get_page_count(pdf_path):
    if not pdf_path or not os.path.isfile(pdf_path):
        return 0
    try:
        doc = _get_doc(pdf_path)
        return len(doc)
    except Exception:
        return 0


def clear_cache():
    _pdf_cache.clear()
