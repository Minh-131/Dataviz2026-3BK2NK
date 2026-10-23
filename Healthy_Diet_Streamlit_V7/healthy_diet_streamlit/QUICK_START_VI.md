# Hướng dẫn triển khai Streamlit Dashboard - từng bước

## Mục tiêu của project

Biến hai file CSV về **Cost and Affordability of a Healthy Diet** thành ứng dụng Streamlit kể một câu chuyện có bằng chứng về SDG 2: **chi phí bữa ăn lành mạnh tăng nhưng tỷ lệ không đủ khả năng chi trả trên toàn cầu giảm, trong khi một số khu vực vẫn tụt lại**.

## 1. Chuẩn bị Python và project

- Dùng Python 3.11 hoặc 3.12 và VS Code / PyCharm / terminal. RStudio cũng mở được các file nhưng Streamlit chạy bằng Python.
- Giải nén `Healthy_Diet_Streamlit_V4_Dark_Mode.zip`; mở thư mục `healthy_diet_streamlit` trong VS Code.
- Giữ nguyên đường dẫn `data/fpn_countries.csv` và `data/fpn_aggregates.csv`.

## 2. Cài và chạy thử

Mở terminal **bên trong thư mục dự án**:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo:

- macOS / Linux: `source .venv/bin/activate`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

Sau đó:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở `http://localhost:8501` nếu trình duyệt không tự mở.

## 3. Kiểm tra 8 trang dashboard

1. **Global Story:** so sánh chi phí, tỷ lệ, số người không đủ khả năng chi trả 2017 to 2025. Kiểm tra $2.94 → $4.28 và 41.0% → 32.7%.
2. **World Map:** thay năm và thay chỉ số; một số quốc gia có màu trống vì không có dữ liệu (không phải 0%).
3. **Regional & Income Divide:** chuyển giữa Region / Income group; xem chênh lệch % và chênh lệch số triệu người. Kiểm tra Sub-Saharan Africa +194.3 triệu và income gap 68.0 điểm phần trăm năm 2025.
4. **GDP & Inflation (MỚI):** kiểm tra 2025, `ρ = −0.824` với unaffordability và `ρ = −0.081` với healthy-diet cost (142 nước); so sánh Nigeria/Cyprus và nhóm income. Nếu muốn phân tích lạm phát thực phẩm, tải file Excel gốc từ World Bank, sau đó upload ngay tại tab hoặc lưu `data/Inflation-data.xlsx`. Không có file thì tab báo thiếu dữ liệu, không tạo số giả.
5. **Nutrition Link:** sử dụng năm 2024 và xem 125 điểm dữ liệu stunting với Spearman khoảng 0.784. Không thể nói đây là quan hệ nhân quả.
6. **Country Explorer:** chuyển xếp hạng theo tỷ lệ % / triệu người / chi phí PPP; chọn quốc gia để so sánh và thử tải CSV.
7. **Data & Methods:** đọc lại định nghĩa và ghi nguồn dữ liệu chính xác trước khi nộp.
8. **How to Use:** hướng dẫn xem từng biểu đồ, lọc, tìm quốc gia và đọc insight.

## 4. Chuyển Light mode và Dark mode

- Mở **sidebar** của website, bật nút **🌙 Dark mode** ở ngay dưới tên Diet Observatory.
- Bật: dùng nền navy tối, chữ sáng, thẻ KPI và các biểu đồ Plotly đổi màu theo nền.
- Tắt: trở về nền sáng. Dữ liệu, năm, bộ lọc và insights không bị thay đổi.
- Lựa chọn giữ trong phiên Streamlit đang mở. Nếu tải lại từ phiên mới, giao diện mặc định sáng.
- Màu sắc và CSS: `src/styles.py`. Màu biểu đồ, tooltip, bản đồ: `src/charts.py` và `src/economics.py`.
- Toàn bộ phần chữ chính trên dashboard không dùng dấu en dash hoặc em dash. Dấu trừ toán học, dấu gạch nối trong tên biến và cú pháp code vẫn giữ nguyên.

## 5. Sửa dashboard dễ nhất ở đâu?

- Sửa **title / hero / phần giải thích** trong `app.py`.
- Sửa **màu sắc, khoảng cách, card KPI** trong `src/styles.py`.
- Sửa **chart labels, hover, dạng biểu đồ** trong `src/charts.py`.
- Sửa **kiểm tra dữ liệu, dữ liệu chuẩn** trong `src/data.py`.
- Sửa **GDP and affordability / import Excel Food CPI** trong `src/economics.py`.
- Thêm các kiểm tra mới trong `tests/test_data.py`.
- Thêm module mới khi cần tính năng tương tác nâng cao; không nên nhồi toàn bộ code vào `app.py`.

## 6. Kiểm tra trước khi push GitHub

```bash
python -m pip install pytest
python -m pytest -q
```

Nếu chạy trên máy riêng, hãy kiểm tra bằng trình duyệt ở cửa sổ bình thường và trên điện thoại.

## 7. Push GitHub

Đứng trong thư mục `healthy_diet_streamlit/`:

```bash
git init
git add .
git commit -m "Build interactive SDG 2 healthy diet dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/healthy-diet-sdg-dashboard.git
git push -u origin main
```

Bạn phải tạo GitHub repository `healthy-diet-sdg-dashboard` trước và thay `YOUR_USERNAME` bằng tài khoản của mình. Nếu đang dùng repository có sẵn, **không cần chạy lại** `git init` hoặc `git remote add origin`; chỉ `git add`, `git commit`, `git push`.

## 8. Deploy lên Streamlit

1. Vào https://share.streamlit.io/ và đăng nhập qua GitHub.
2. Chọn repo + branch `main` + main file path `app.py`.
3. Bấm Deploy và đọc logs nếu có lỗi.
4. Copy public URL do Streamlit cung cấp.
5. Test trên tab ẩn danh: nếu bị yêu cầu đăng nhập mà ban giám khảo không có quyền, hãy đổi quyền sharing theo chính sách của Streamlit.

**Không cần API key** vì hai CSV được lưu cùng mã nguồn.

## 9. Hoàn thiện để cạnh tranh giải thưởng

- Đưa một key insight lên trước mỗi cụm biểu đồ, tránh để người xem tự đoán ý nghĩa.
- Dùng **một câu chuyện** chính thay vì chỉ trình bày thật nhiều charts.
- Kiểm tra labels, units và tooltip kỹ: PPP $/person/day, million people, percentage-point change.
- Giải thích biến `pou`, `stunting_pct`, `CoHD_headcount` và các giới hạn correlation.
- Ghi nguồn dữ liệu, ngày truy cập, phiên bản, phương pháp xử lý, và link nguồn gốc; hiện hai CSV không có đầy đủ thông tin provenance.
- Giới hạn mô tả nộp theo đề và dùng `SUBMISSION_DESCRIPTION.md` để chỉnh sửa.
- Nhờ một người chưa xem dashboard thử giải thích câu chuyện sau 30 to 60 giây.
- Thử trên mobile, desktop, tab ẩn danh; đảm bảo URL hoạt động khi ban giám khảo truy cập.

**Lưu ý:** Code đã được test phần tính toán và tạo biểu đồ Plotly trong môi trường này. Chưa thể chạy thử giao diện Streamlit tại đây vì package Streamlit không có sẵn và môi trường không cho tải package mới. Phải tự chạy `python -m streamlit run app.py` để test UI trước khi nộp.

## 10. Bổ sung bộ dữ liệu World Bank Inflation thật

1. Mở https://www.worldbank.org/en/brief/2025/05/04/inflation-database và chọn **Inflation data (Excel)**.
2. Lưu tên `Inflation-data.xlsx` trong `healthy_diet_streamlit/data/`, hoặc upload qua tab **GDP & Inflation** của ứng dụng.
3. Bảng Excel phải có sheet `fcpi_a` (food CPI inflation annual); `hcpi_a` (headline CPI inflation annual) nếu có. Module `src/economics.py` nối dữ liệu bằng ISO3 và năm.
4. Chạy `python -m pytest -q` và kiểm tra số cặp quan sát có dữ liệu trên app. Kiểm tra từng điểm dữ liệu gốc, đặc biệt các năm 2024 to 2025.
5. Phân biệt **Food CPI inflation (%)** với **cost of healthy diet (PPP $/person/day)**. Chúng không cùng rổ hàng hóa và không thể dùng thay cho nhau.

Đọc `ECONOMIC_INSIGHTS_V2.md` để xem chi tiết phát hiện mới. File Excel nguồn chưa được tích hợp sẵn vì link URL không phải là bảng số liệu đã được tải xuống.


## Mới trong V3: cách sử dụng website

- Bên dưới **mọi biểu đồ** có `How to read` (giải thích cách đọc trục, màu, đơn vị) và `Key insight` (nhận xét được cập nhật theo filter); một số có `Note` để tránh diễn giải sai.
- Sidebar có mục `🧭 Quick guide: how to use`.
- Website có tab **`🧭 How to Use`** bằng tiếng Anh phù hợp với giám khảo.
- Mở file **`USER_GUIDE_VI.md`** để đọc hướng dẫn tiếng Việt chi tiết cho 8 tab, cách hover, đổi năm, download, các kịch bản thuyết trình.
- Sau khi sửa mã: `git add .`, `git commit -m "Add explanations and how-to guide"`, `git push` lên đúng nhánh của Streamlit Cloud để cập nhật website.
