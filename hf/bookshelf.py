import json
import os
from pathlib import Path

BOOKS_DIR = Path("books")
IMAGES_DIR = Path("images")
META_EXT = ".meta.json"

SLOTS = 10


def _read_meta(stem):
    meta_file = BOOKS_DIR / f"{stem}{META_EXT}"
    if not meta_file.is_file():
        return {}
    try:
        with open(meta_file, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def list_books():
    books = []
    if not BOOKS_DIR.is_dir():
        return books
    for f in sorted(BOOKS_DIR.iterdir()):
        if f.suffix.lower() != ".pdf":
            continue
        cover = None
        for ext in (".png", ".jpg", ".jpeg"):
            candidate = IMAGES_DIR / f"{f.stem}{ext}"
            if candidate.is_file():
                cover = str(candidate)
                break
        meta = _read_meta(f.stem)
        books.append({
            "filename": f.name,
            "title": meta.get("title") or f.stem,
            "author": meta.get("author"),
            "year": meta.get("year"),
            "pages": meta.get("pages"),
            "description": meta.get("description"),
            "path": str(f),
            "cover": cover,
        })
    return books


BOOK_COLORS = [
    "#6B1A1A",  # đỏ rượu
    "#1B3B3B",  # xanh rêu
    "#3B1B4B",  # tím than
    "#4B3010",  # nâu gỗ
    "#1B1B4B",  # xanh navy
    "#7B6B10",  # vàng gold
    "#1B4B1B",  # xanh lá
    "#4B3060",  # tử đinh hương
    "#4B4B5B",  # xám đá
    "#6B3020",  # đỏ gạch
    "#1B3B5B",  # xanh dương
    "#6B4B20",  # hổ phách
]


def book_color(title):
    return BOOK_COLORS[hash(title) % len(BOOK_COLORS)]


def build_library_html(books):
    shelves_html = ""
    for i in range(0, len(books), SLOTS):
        row = list(books[i:i + SLOTS])
        row += [None] * (SLOTS - len(row))

        books_html = ""
        for b in row:
            if b is None:
                books_html += '<div class="book empty"><span>📖</span></div>'
            else:
                tooltip_cover_html = '<div class="tip-cover placeholder">📖</div>'
                if b["cover"] and os.path.isfile(b["cover"]):
                    cover_url = f"/file={b['cover']}"
                    tooltip_cover_html = f'<div class="tip-cover" style="background-image: url(\'{cover_url}\')"></div>'
                color = book_color(b["title"])
                tip_meta = ""
                if b.get("author"):
                    tip_meta += f'<div class="tip-author">✍️ {b["author"]}</div>'
                if b.get("pages"):
                    tip_meta += f'<div class="tip-pages">📄 {b["pages"]} trang</div>'
                if b.get("description"):
                    tip_meta += f'<div class="tip-desc">{b["description"]}</div>'
                books_html += f'''
                <div class="book" onclick="selectBook('{b["filename"]}')" style="background-color: {color};">
                    <div class="book-body">
                        <div class="band band-top"></div>
                        <span class="book-title">{b["title"]}</span>
                        <div class="band band-bottom"></div>
                    </div>
                    <div class="pages-edge"></div>
                    <div class="book-tip">
                        {tooltip_cover_html}
                        <div class="tip-title">{b["title"]}</div>
                        <div class="tip-meta">{tip_meta}</div>
                    </div>
                </div>'''

        shelves_html += f'''
        <div class="shelf">
            <div class="books-row">{books_html}</div>
            <div class="shelf-board"></div>
        </div>'''

    if not shelves_html:
        empty_row = '<div class="book empty"><span>📖</span></div>' * SLOTS
        shelves_html = f'''
        <div class="shelf">
            <div class="books-row">{empty_row}</div>
            <div class="shelf-board"></div>
        </div>'''

    html = f'''<div class="library-wrapper">
    <div class="library">
        <div class="library-title">🏛️ libracal</div>
        <div class="library-inner">
            {shelves_html}
        </div>
    </div>
</div>
<style>
.library-wrapper {{
    display: flex;
    justify-content: center;
    padding: 20px 0;
    align-items: flex-start;
    overflow: visible;
}}
.library {{
    width: 100%;
    max-width: 960px;
    box-sizing: border-box;
    background:
        repeating-linear-gradient(90deg, transparent, transparent 20px, rgba(0,0,0,0.015) 20px, rgba(0,0,0,0.015) 21px),
        repeating-linear-gradient(0deg, transparent, transparent 50px, rgba(0,0,0,0.02) 50px, rgba(0,0,0,0.02) 51px),
        radial-gradient(ellipse 60px 45px at 18% 28%, rgba(0,0,0,0.05) 0%, transparent 70%),
        radial-gradient(ellipse 45px 35px at 75% 55%, rgba(0,0,0,0.04) 0%, transparent 70%),
        radial-gradient(ellipse 35px 25px at 45% 85%, rgba(255,255,255,0.03) 0%, transparent 70%),
        radial-gradient(ellipse 50px 40px at 88% 15%, rgba(0,0,0,0.035) 0%, transparent 70%),
        linear-gradient(180deg, #9B7924 0%, #8B6914 15%, #7A5C1E 40%, #6B4F12 65%, #5C4210 85%, #4A3510 100%);
    border-radius: 6px;
    padding: 30px 25px 20px;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(255,255,255,0.08),
        inset 0 -1px 0 rgba(0,0,0,0.2);
    position: relative;
    border: 2px solid #4A3510;
}}
.library-title {{
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    color: #F5E6C8;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    margin-bottom: 25px;
    letter-spacing: 4px;
}}
.library-inner {{
    position: relative;
    z-index: 1;
}}
.shelf {{
    margin-bottom: 8px;
    overflow: visible;
}}
.books-row {{
    display: flex;
    align-items: flex-end;
    justify-content: space-evenly;
    padding: 0;
    min-height: 175px;
    overflow: visible;
}}
.shelf-board {{
    height: 16px;
    background: linear-gradient(180deg, #A0842C 0%, #8B6914 20%, #6B4F12 45%, #5C4210 70%, #3D2D0C 100%);
    border-radius: 2px;
    box-shadow:
        0 8px 16px rgba(0,0,0,0.35),
        inset 0 2px 0 rgba(255,255,255,0.1),
        inset 0 -1px 0 rgba(0,0,0,0.3);
    margin-top: 4px;
    position: relative;
}}
.shelf-board::after {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 2px;
    background: repeating-linear-gradient(90deg, transparent, transparent 4px, rgba(0,0,0,0.04) 4px, rgba(0,0,0,0.04) 5px);
    pointer-events: none;
}}
.book {{
    width: 55px;
    height: 162px;
    flex-shrink: 0;
    border-radius: 2px 3px 3px 2px;
    cursor: pointer;
    position: relative;
    display: flex;
    flex-direction: row;
    transform: perspective(1000px) rotateY(-2deg);
    box-shadow:
        -3px 0 6px rgba(0,0,0,0.3),
        1px 1px 4px rgba(0,0,0,0.15);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}
.book:hover {{
    transform: perspective(1000px) rotateY(-2deg) translateZ(18px) translateY(-4px);
    box-shadow:
        -5px 0 14px rgba(0,0,0,0.4),
        3px 8px 20px rgba(0,0,0,0.35);
    z-index: 999999;
}}
.book-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px 4px;
    position: relative;
    background: linear-gradient(90deg,
        rgba(0,0,0,0.25) 0%,
        rgba(255,255,255,0.06) 15%,
        transparent 30%,
        transparent 70%,
        rgba(0,0,0,0.1) 85%,
        rgba(0,0,0,0.2) 100%);
}}
.band {{
    width: 75%;
    height: 3px;
    border-radius: 1px;
    background: linear-gradient(90deg,
        rgba(255,215,0,0.2) 0%,
        rgba(255,215,0,0.8) 20%,
        rgba(255,215,0,0.4) 50%,
        rgba(255,215,0,0.8) 80%,
        rgba(255,215,0,0.2) 100%);
    flex-shrink: 0;
}}
.band-top {{
    margin-bottom: auto;
}}
.band-bottom {{
    margin-top: auto;
}}
.book-title {{
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 11px;
    color: #ffffff !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    font-weight: 500;
    letter-spacing: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 120px;
    margin: 8px 0;
}}
.pages-edge {{
    width: 4px;
    background: linear-gradient(90deg, #f5f0e0 0%, #e8e0c8 40%, #ddd5b8 100%);
    flex-shrink: 0;
    position: relative;
}}
.pages-edge::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -1px;
    width: 2px;
    height: 100%;
    background: rgba(0,0,0,0.06);
}}
.book::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.08) 50%, rgba(0,0,0,0.15) 100%);
    border-radius: 0 0 3px 2px;
    pointer-events: none;
}}
.book.empty {{
    background: transparent !important;
    border: 2px dashed rgba(139,105,20,0.2);
    box-shadow: none;
    cursor: default;
    transform: none;
}}
.book.empty:hover {{
    transform: none;
    box-shadow: none;
}}
.book.empty > span {{
    font-size: 26px;
    opacity: 0.2;
}}
.book.empty::after {{
    display: none;
}}

.book-tip {{
    position: absolute;
    top: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%) scale(0.9);
    background: linear-gradient(180deg, #4a3520 0%, #2c1810 100%);
    border: 1px solid #A0842C;
    border-radius: 8px;
    padding: 8px 10px 10px;
    width: 130px;
    opacity: 0;
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 999999;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    pointer-events: none;
}}
.book-tip::after {{
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    margin-left: -6px;
    border: 6px solid transparent;
    border-bottom-color: #4a3520;
}}
.book:hover .book-tip {{
    opacity: 1;
    transform: translateX(-50%) scale(1);
}}
.tip-cover {{
    width: 110px;
    height: 146px;
    border-radius: 4px;
    margin: 0 auto 8px;
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(139,105,20,0.3);
}}
.tip-cover.placeholder {{
    background: linear-gradient(135deg, #c62828, #8e0000);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
}}
.tip-title {{
    font-size: 12px;
    color: #ffffff !important;
    text-align: center;
    font-weight: 600;
    line-height: 1.3;
    word-break: break-word;
    max-width: 110px;
    margin: 0 auto;
}}
.tip-meta {{
    margin-top: 6px;
    border-top: 1px solid rgba(160,132,44,0.25);
    padding-top: 6px;
}}
.tip-author,
.tip-pages {{
    font-size: 11px;
    color: #ffffff !important;
    line-height: 1.5;
}}
.tip-desc {{
    font-size: 10px;
    color: #ffffff !important;
    line-height: 1.4;
    margin-top: 4px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}
</style>'''
    return html
