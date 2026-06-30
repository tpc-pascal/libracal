# libracal

<p align="center">
  <img src="assets/logo.svg" alt="libracal logo" width="400">
</p>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tpc-pascal/libracal/blob/main/colab.ipynb)
[![Open in Hugging Face](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/tpc-pascal/libracal)

> Kệ sách ảo cá nhân — lưu trữ, duyệt và đọc PDF tài liệu.

**Lý do ra đời:** Bạn có quá nhiều PDF rải rác khắp nơi và muốn một nơi gọn gàng để đọc? libracal giúp bạn có một kệ sách ảo đẹp mắt với trình đọc PDF tích hợp, hỗ trợ toàn màn hình và điều hướng bằng bàn phím.

---

## Tính năng

- Kệ sách ảo với hiệu ứng gỗ 3D, hover tooltip, cuộn ngang
- Trình đọc PDF tích hợp (PyMuPDF), lật trang bằng phím ← →
- Ảnh bìa tự động từ file PNG/JPG trùng tên
- Chế độ toàn màn hình
- Chạy trên local, Hugging Face Spaces và Google Colab

---

## Cấu trúc thư mục

```
libracal/
├── hf/                          # Hugging Face Spaces deployment
│   ├── app.py                   # Entry point — Gradio UI + PDF reader
│   ├── bookshelf.py             # Library shelf HTML generator
│   ├── reader.py                # PDF rendering engine (PyMuPDF)
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # HF Space metadata
├── assets/
│   └── logo.svg
├── colab.ipynb                  # Google Colab notebook
├── GUIDE.md                     # Hướng dẫn setup chi tiết
├── CONTRIBUTING.md              # Hướng dẫn đóng góp
├── CREDITS.md                   # Credits & tham khảo
└── README.md
```

---

## Tech Stack

| Layer | Công nghệ |
|---|---|
| Language | Python 3.13 |
| Web UI | Gradio |
| PDF Engine | PyMuPDF (fitz) |
| Hosting | Hugging Face Spaces |

---

## Tác giả

**tpc-pascal** — [GitHub](https://github.com/tpc-pascal)

---

## License

MIT
