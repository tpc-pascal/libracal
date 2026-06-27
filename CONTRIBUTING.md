# Hướng dẫn Đóng góp (Contributing Guidelines)

Vui lòng đọc kỹ các hướng dẫn dưới đây trước khi bắt đầu đóng góp.

---

## 1. Thiết lập môi trường phát triển (Setup)

```bash
git clone https://github.com/tpc-pascal/libracal.git
cd libracal
pip install -r hf/requirements.txt
python hf/app.py
```

Truy cập `http://localhost:7860` để xem kết quả.

---

## 2. Quy trình gửi đóng góp (Git Workflow)

1. **Fork** dự án về tài khoản cá nhân.
2. **Tạo Branch mới:**
   - Tính năng mới: `git checkout -b feat/ten-tinh-nang`
   - Sửa lỗi: `git checkout -b fix/ten-loi`
   - Tài liệu: `git checkout -b docs/ten-tai-lieu`
3. **Commit:** Sử dụng tiếng Việt hoặc tiếng Anh rõ nghĩa.
4. **Push & PR:** Đẩy branch lên GitHub và tạo **Pull Request**.

---

## 3. Quy chuẩn viết mã (Coding Standards)

- **Nhất quán:** Tuân thủ các quy tắc đặt tên đã có sẵn trong dự án.
- **Comment:** Giải thích các logic phức tạp.

---

## 4. Kiểm thử (Testing)

Trước khi gửi Pull Request, vui lòng đảm bảo:

- Code chạy được trên máy cá nhân không lỗi.
- Không làm ảnh hưởng đến các tính năng cũ.

---

## Liên hệ

- [Mở một Issue](https://github.com/tpc-pascal/libracal/issues)
- [Thảo luận (Discussions)](https://github.com/tpc-pascal/libracal/discussions)
