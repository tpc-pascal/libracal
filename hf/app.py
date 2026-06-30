import os
import gradio as gr
import gradio_client.utils as gc_utils

from bookshelf import list_books, build_library_html
from reader import render_page, get_page_count

_orig = gc_utils.get_type
gc_utils.get_type = lambda s: "boolean" if isinstance(s, bool) else _orig(s)

books_cache = []


def refresh_shelf():
    global books_cache
    books_cache = list_books()
    return build_library_html(books_cache)


def open_reader(filename):
    if not filename:
        return gr.update(visible=True), gr.update(visible=False), None, "", "", "", 0, 0
    for b in books_cache:
        if b["filename"] == filename:
            total = get_page_count(b["path"])
            if total == 0:
                return gr.update(visible=True), gr.update(visible=False), None, "", "", "", 0, 0
            img = render_page(b["path"], 0)
            return gr.update(visible=False), gr.update(visible=True), img, b["title"], f"1 / {total}", b["path"], 1, total
    return gr.update(visible=True), gr.update(visible=False), None, "", "", "", 0, 0


def _nav(pdf_path, page, delta):
    if not pdf_path or not os.path.isfile(pdf_path):
        return None, "", 1, 0
    total = get_page_count(pdf_path)
    if total == 0:
        return None, "", 1, 0
    new_page = max(1, min(page + delta, total))
    img = render_page(pdf_path, new_page - 1)
    return img, f"{new_page} / {total}", new_page, total


def prev(p, pg):
    return _nav(p, pg, -1)


def nxt(p, pg):
    return _nav(p, pg, 1)


def back_to_shelf():
    return gr.update(visible=True), gr.update(visible=False)


with gr.Blocks(theme=gr.themes.Soft(), title="libracal") as demo:
    current_pdf = gr.State("")
    current_page = gr.State(1)
    total_pgs = gr.State(0)
    hidden = gr.Textbox(value="", elem_id="hf-hidden", container=True, label="")

    gr.HTML("""
<div style="display:none;height:0;width:0;overflow:hidden;position:absolute;pointer-events:none;" aria-hidden="true">
<style>
#hf-hidden { display: none !important; }
html, body { overflow-x: hidden; margin: 0; padding: 0; }
.gradio-container { overflow: visible !important; max-width: 100% !important; }
.gradio-container .tabs,
.gradio-container .tabitem,
.gradio-container .tabitem > div,
.gradio-container .column,
.gradio-container .block {
    overflow: visible !important;
}

#reader-col {
    display: none;
    background: #161618;
    border-radius: 8px;
    overflow: hidden;
    flex-direction: column;
    max-width: 720px;
    margin: 0 auto;
}

#reader-topbar {
    display: flex !important;
    align-items: center;
    padding: 0 20px;
    height: 56px;
    background: rgba(0,0,0,0.35);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    gap: 16px;
}
#reader-back {
    flex-shrink: 0;
}
#reader-back button {
    background: rgba(255,255,255,0.07) !important;
    border: none !important;
    color: rgba(255,255,255,0.8) !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    border-radius: 22px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
#reader-back button:hover {
    background: rgba(255,255,255,0.14) !important;
    color: rgba(255,255,255,1) !important;
}
#reader-title {
    flex: 1;
    margin: 0 !important;
    overflow: hidden;
}
#reader-title p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 0 !important;
    letter-spacing: 0.3px;
}
#reader-page-info {
    flex-shrink: 0;
    margin: 0 !important;
}
#reader-page-info p {
    color: rgba(255,255,255,0.5) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
#reader-col:-webkit-full-screen,
#reader-col:fullscreen {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
}
#reader-view {
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px 16px;
    overflow-y: auto;
    position: relative;
}
#reader-view img {
    max-width: 100%;
    max-height: 85vh;
    width: auto;
    height: auto;
    display: block;
    box-shadow: 0 6px 40px rgba(0,0,0,0.5);
    border-radius: 3px;
}
#reader-view:-webkit-full-screen {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
    padding: 24px;
    background: #161618;
}
#reader-view:fullscreen {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
    padding: 24px;
    background: #161618;
}
#reader-floating-controls {
    position: absolute !important;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%);
    display: flex !important;
    align-items: center;
    background: rgba(20,20,28,0.92) !important;
    z-index: 100;
    border-radius: 28px;
    padding: 6px 12px;
    gap: 6px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}
#reader-floating-controls button {
    background: transparent !important;
    border: none !important;
    color: rgba(255,255,255,0.9) !important;
    font-size: 34px !important;
    font-weight: 300 !important;
    min-width: 46px !important;
    height: 46px !important;
    padding: 0 4px !important;
    border-radius: 23px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
#reader-floating-controls button:hover {
    background: rgba(255,255,255,0.1) !important;
    color: rgba(255,255,255,1) !important;
    font-size: 38px !important;
}
#reader-floating-controls button:active {
    background: rgba(255,255,255,0.16) !important;
    transform: scale(0.94);
}
#fs-page-overlay {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 48px;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.4);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    z-index: 200;
    pointer-events: none;
}
#fs-page-text {
    color: #fff;
    font-size: 15px;
    font-weight: 500;
}
#reader-view:fullscreen #fs-page-overlay,
#reader-view:-webkit-full-screen #fs-page-overlay {
    display: flex;
}
</style>
<script>
function selectBook(f) {
    var el = document.querySelector('#hf-hidden input') || document.querySelector('#hf-hidden textarea');
    if (!el) return;
    el.value = f;
    el.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
    var shelf = document.querySelector('#shelf-col');
    var reader = document.querySelector('#reader-col');
    if (shelf) shelf.style.display = 'none';
    if (reader) reader.style.display = 'flex';
}
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') {
        var b = document.querySelector('#pg-prev button');
        if (b) b.click();
    } else if (e.key === 'ArrowRight') {
        var b = document.querySelector('#pg-next button');
        if (b) b.click();
    } else if (e.key === 'Escape') {
        if (document.fullscreenElement) return;
        var s = document.querySelector('#shelf-col');
        var r = document.querySelector('#reader-col');
        if (s) s.style.display = '';
        if (r) r.style.display = 'none';
        var b = document.querySelector('#reader-back button');
        if (b) b.click();
    } else if (e.key === 'f' || e.key === 'F') {
        var b = document.querySelector('#fullscreen-btn button');
        if (b) b.click();
    }
});
document.addEventListener('click', function(e) {
    if (e.target.closest('#reader-back, #reader-back button')) {
        var s = document.querySelector('#shelf-col');
        var r = document.querySelector('#reader-col');
        if (s) s.style.display = '';
        if (r) r.style.display = 'none';
    }
    if (e.target.closest('#fullscreen-btn, #fullscreen-btn button')) {
        var el = document.querySelector('#reader-view');
        if (!document.fullscreenElement) {
            (el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen)?.call(el);
        } else {
            (document.exitFullscreen || document.webkitExitFullscreen || document.msExitFullscreen)?.call(document);
        }
    }
});
function setupPageOverlay() {
    var rv = document.querySelector('#reader-view');
    if (!rv) return;
    if (!rv.querySelector('#fs-page-overlay')) {
        var ov = document.createElement('div');
        ov.id = 'fs-page-overlay';
        ov.innerHTML = '<span id="fs-page-text">0 / 0</span>';
        rv.appendChild(ov);
    }
}
function syncPageOverlay() {
    var src = document.querySelector('#reader-page-info p');
    var dst = document.querySelector('#fs-page-text');
    if (src && dst) dst.textContent = src.textContent;
}
setupPageOverlay();
syncPageOverlay();
setInterval(syncPageOverlay, 500);
document.addEventListener('click', function(e) {
    if (e.target.closest('[onclick*="selectBook"]')) {
        setTimeout(setupPageOverlay, 50);
        setTimeout(syncPageOverlay, 100);
    }
});
</script>
</div>
""", visible=True)

    with gr.Column(visible=True, elem_id="shelf-col") as shelf_col:
        shelf_html = gr.HTML(value=refresh_shelf(), elem_id="shelf-html")

    with gr.Column(visible=True, elem_id="reader-col") as reader_col:
        with gr.Row(elem_id="reader-topbar"):
            back_btn = gr.Button("◀  Về kệ sách", elem_id="reader-back")
            title_md = gr.Markdown("", elem_id="reader-title")
            page_info = gr.Markdown("", elem_id="reader-page-info")
        with gr.Column(elem_id="reader-view"):
            page_img = gr.Image(type="pil", show_label=False, elem_id="reader-image")
            with gr.Row(elem_id="reader-floating-controls"):
                prev_btn = gr.Button("◀", elem_id="pg-prev")
                fullscreen_btn = gr.Button("⛶", elem_id="fullscreen-btn")
                next_btn = gr.Button("▶", elem_id="pg-next")

    hidden.change(
        open_reader,
        inputs=[hidden],
        outputs=[shelf_col, reader_col, page_img, title_md, page_info, current_pdf, current_page, total_pgs],
    )

    back_btn.click(back_to_shelf, outputs=[shelf_col, reader_col])

    prev_btn.click(prev, inputs=[current_pdf, current_page],
                   outputs=[page_img, page_info, current_page, total_pgs])

    next_btn.click(nxt, inputs=[current_pdf, current_page],
                   outputs=[page_img, page_info, current_page, total_pgs])

demo.launch(server_name="0.0.0.0", server_port=7860)
