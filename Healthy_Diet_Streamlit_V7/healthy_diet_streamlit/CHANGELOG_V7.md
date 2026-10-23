# Changelog – Streamlit V7 (V6 + the data story’s standards)

Bản này ghép **thiết kế V6 của nhóm** với **toàn bộ chuẩn chữ và trải nghiệm** đã áp dụng cho bản web. Chép các file dưới đây vào đúng đường dẫn trong repo, ghi đè file cũ.

**Giữ nguyên, không có trong gói:** `src/basket.py`, `src/statistics.py`, `tests/`, toàn bộ dữ liệu CSV.

**`src/styles.py` có trong gói:** file V6 gốc không có trong bản đã gửi (các thư mục upload bị rỗng), nên file này được dựng lại từ `styles.py` V5 cộng toàn bộ phần thiết kế V6 theo `UPDATE_V6_VI.md`: sidebar dạng mục lục, chương đang chọn có viền và nền riêng, thanh tiến độ chương, KPI tách số và đơn vị, thẻ Highest/Lowest có tương phản riêng ở chế độ sáng/tối và một cột trên điện thoại, viền focus khi dùng bàn phím. Bạn Visual designer nên so với file V6 thật của mình: nếu muốn giữ bản gốc, chỉ cần không chép file này – mọi tính năng mới vẫn chạy vì CSS của chúng nằm trong `src/story_styles.py`.

## File trong gói
| File | Nội dung |
|---|---|
| `app.py` | V6 (sidebar mục lục, KPI tách số và đơn vị, thẻ Highest/Lowest) + mọi thay đổi bên dưới |
| `src/styles.py` | Thiết kế V6 dựng lại (xem trên) |
| `src/story_styles.py` (mới) | CSS cho các tính năng mới, nạp sau `styles.py` nên không đụng thiết kế V6 |
| `src/charts.py` | Ghi chú trên biểu đồ, tô đậm Sub-Saharan Africa, cờ trên biểu đồ, sửa trục bị cắt |
| `src/economics.py` | Nhãn trục GDP đúng; đường "Same price" và cờ Nigeria/Cyprus |
| `src/data.py`, `src/narrative.py` | Nhãn chỉ số thống nhất; câu insight tự nhiên |
| `src/flags.py` + `data/iso3_to_iso2.csv` (mới) | Cờ cho 180 nước |
| `SUBMISSION_DESCRIPTION.md` | Đoạn mô tả 198 từ |

## Thay đổi chính
1. **Đúng và thận trọng:** sửa lỗi GDP (current international $); bỏ mọi ghi chú nội bộ ("supplied", "Verify…", "snapshot"), câu nhắc inflation và tên biến kỹ thuật; nhãn KPI khớp giá trị; mọi quan hệ ghi là mối liên hệ, kèm ρ và số nước.
2. **Thêm giới hạn phương pháp** trong Methods, giống bản web: ρ không có trọng số; quy luật cấp quốc gia không mô tả hộ gia đình; độ phủ 147/180 nước; vì sao các chương dùng năm khác nhau.
3. **Cùng tên chương và tiêu đề với bản web:** 01 The paradox, 02 Where, 03 Left behind, 04 Income, not price, 05 The plate, 06 Fed vs. well fed, 07 Explore, 08 Sources and method.
4. **Gọn hơn:** mỗi biểu đồ chỉ còn một câu kết luận, phần "How to read this chart" thu gọn; phần mở đầu lớn chỉ ở chương 01, các chương khác có thanh bối cảnh; 8 chương (Field guide gộp vào sidebar).
5. **Dẫn dắt:** nút **Next →** cuối mỗi chương, tự cuộn lên đầu; ghi chú ngay trên biểu đồ (2020, Sub-Saharan Africa, Niger, Nigeria–Cyprus).
6. **Cờ quốc gia** ở mọi chỗ có tên nước: thẻ Highest/Lowest, câu kết luận, xếp hạng, so sánh, scatter, bảng.
7. **Liên kết hai chiều:** nút "Read the data story →" ở sidebar và dòng "New here? Read the data story first" ở chương 01.

## Đã kiểm tra
20/20 test (bộ test V5) chạy thành công; 8 chương × chế độ sáng/tối không lỗi; các năm 2017, 2020, 2025 không lỗi; nút Next chuyển chương đúng; không còn chữ nội bộ nào trên giao diện.

**Đã xem bằng trình duyệt thật:** chạy app trên máy chủ Streamlit và chụp màn hình bằng Chromium – sidebar, phần mở đầu, KPI, chương Where ở chế độ sáng và tối, điện thoại; không có lỗi. (Bản đồ và cờ cần mạng nên không hiện trong môi trường kiểm thử, sẽ hiện bình thường khi deploy.)

**Chưa kiểm tra được:** `tests/test_ui_v6.py` (không có trong bản đã gửi). Sau khi chép vào repo, chạy:
```
python -m pytest -q
python -m streamlit run app.py
```
Nếu `test_ui_v6.py` báo lỗi vì tìm chữ "HIGHEST OBSERVED" hoặc chương "09 Field guide", đó là do bản này đã đổi chữ và gộp chương – chỉ cần cập nhật test.
