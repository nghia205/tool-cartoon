# 🎨 AI Webtoon Studio — Công Cụ Chuyển Thể Truyện Tranh Thương Mại

Công cụ tự động hóa quy trình sản xuất **Webtoon / Manhwa cuộn dọc** từ cốt truyện thuộc **Public Domain** (Cổ tích, Dã sử, Truyền thuyết Việt Nam) hoặc kịch bản riêng của bạn. Chỉ cần nhập **API Key** và **1 câu yêu cầu**, hệ thống sẽ tự động:

1. **AI Director (LLM):** Thiết kế kịch bản phân cảnh (`storyboard.json`), tạo hồ sơ ngoại hình nhân vật nhất quán (`character_bible`), viết lời dẫn truyện, lời thoại và chữ tượng thanh (SFX).
2. **AI Artist (Image Gen):** Vẽ từng khung hình dọc (Vertical Panels) chất lượng cao theo phong cách Manhwa hiện đại (*Solo Leveling* / *Redice Studio* style) không chứa chữ rác.
3. **Auto-Typesetter (`Pillow`):** Tự động làm tối viền chuyển cảnh, vẽ hộp dẫn truyện, đóng bóng thoại tiếng Việt có đuôi trỏ, vẽ chữ SFX phát sáng, ghép thành **Ảnh Dọc Nguyên Cột (`webtoon_full_strip.jpg`)** và đóng gói **File `.ZIP`** đầy đủ để tải về.

---

## 🚀 Cách Chạy Nhanh (Chỉ 1 Lệnh)

```bash
python3 studio_server.py
```

Sau đó mở trình duyệt truy cập: **`http://localhost:8080`**

- Trên cột trái, chọn **Google Gemini API** hoặc **OpenAI API** và dán API Key của bạn (hoặc để trống để dùng chế độ Free AI).
- Nhập yêu cầu (ví dụ: *"Tạo bộ truyện Sơn Tinh Thủy Tinh đầy đủ theo kiểu webtoon"*) và bấm **🚀 Tạo Bộ Truyện Webtoon Tự Động**.
- Bấm nút **📦 Tải Trọn Bộ Ảnh (.ZIP)** ở góc trên bên phải để tải toàn bộ ảnh về máy.

---

## 📂 Các Bộ Truyện Đã Được Tạo Sẵn Trong Kho (`projects/`)

1. **Sơn Tinh - Thủy Tinh: Đại Chiến Thần Linh** (`projects/son_tinh_thuy_tinh/`) — Đầy đủ 5 khung hình đại chiến thần thoại, file dọc nguyên cột và gói `.zip`.
2. **Dã Sử Dị Giới: Thạch Sanh** (`projects/thach_sanh/`) — Đầy đủ 4 khung hình chém Chằn Tinh tại miếu cổ, file dọc nguyên cột và gói `.zip`.
