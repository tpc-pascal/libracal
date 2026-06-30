## Hướng dẫn sử dụng

### Yêu cầu

- Python 3.10+
- File PDF (bắt buộc)
- Ảnh bìa PNG/JPG trùng tên file PDF (tùy chọn)

### Chuẩn bị

```
libracal/
├── hf/
│   ├── app.py
│   ├── bookshelf.py
│   ├── reader.py
│   ├── requirements.txt
│   └── README.md
├── colab.ipynb
├── GUIDE.md
├── CONTRIBUTING.md
├── CREDITS.md
└── README.md
```

> `books/` (PDF) và `images/` (ảnh bìa) không có trong repo — chúng được đính kèm dưới dạng **release assets** (file `.zip`) trên GitHub. Workflow `sync.yml` tự động tải về và đồng bộ lên Hugging Face Spaces.

### Chạy local

```bash
git clone https://github.com/tpc-pascal/libracal.git
cd libracal
pip install -r hf/requirements.txt
python hf/app.py
```

Mở trình duyệt tại `http://localhost:7860`.

### Chạy trên Hugging Face Spaces

Truy cập: [huggingface.co/spaces/tpc-pascal/libracal](https://huggingface.co/spaces/tpc-pascal/libracal)

Tạo một [GitHub Release](https://github.com/tpc-pascal/libracal/releases) mới, đính kèm file `.zip` chứa `books/` và `images/`, workflow sẽ tự đồng bộ lên HF Spaces.

### Chạy trên Google Colab

Mở `colab.ipynb` và chạy lần lượt các cell.
