> **Giao diện mới V4:** Bật hoặc tắt **🌙 Dark mode** ở đầu sidebar để chuyển toàn bộ trang và biểu đồ Plotly giữa nền tối và nền sáng. Việc đổi giao diện không làm thay đổi dữ liệu hoặc kết quả thống kê.

# Hướng dẫn sử dụng: The Hidden Cost of a Healthy Diet (Streamlit V3)

Hướng dẫn này dành cho thành viên nhóm và người chấm lần đầu mở trang. **Trên website đã có tab `🧭 How to Use` bằng tiếng Anh và thẻ `How to read / Key insight` ngay bên dưới từng biểu đồ.**

## 1. Mở trang và hiểu 3 ô KPI

1. Mở URL Streamlit hoặc chạy `python -m streamlit run app.py` trong thư mục dự án.
2. Nhìn ô **Daily healthy diet cost**: chi phí chế độ ăn lành mạnh trung bình toàn cầu, theo **PPP $/người/ngày**, có trọng số dân số.
3. Ô **Unable to afford a healthy diet**: **phần trăm** dân số không đủ khả năng chi trả.
4. Ô **People affected**: **số người** bị ảnh hưởng, hiển thị bằng tỷ người ở KPI và triệu người ở các biểu đồ.
5. Dòng so sánh dưới KPI là chênh lệch **so với năm 2017**. Đừng nhầm **percentage points (pp)** với phần trăm thay đổi tương đối.

## 2. Chọn năm và đi qua 8 tab

Trong **sidebar (bên trái)**, kéo `Explore reporting year` để chọn năm từ **2017 to 2025**. Bộ chọn này tác động đến KPI, Global Story, World Map, Regional & Income Divide, GDP & Inflation và Country Explorer. **Nutrition Link có year selector riêng** và chỉ sử dụng số liệu có sẵn đến năm **2024**.

### Tab 1: 📈 Global Story

- **Plot 1: The price of a healthy diet:** trục ngang là năm, trục dọc là chi phí **PPP $/người/ngày** (dữ liệu tổng hợp có trọng số). Hover vào từng chấm để đọc số. Thẻ insight diễn giải mức tăng/giảm theo **% tương đối**.
- **Plot 2: The unaffordability rate:** trục dọc là **% dân số** không đủ khả năng chi trả. Khi so hai năm, dùng **điểm phần trăm (pp)**.
- **Plot 3: The number of people affected:** trục dọc là **triệu người**, giúp thấy quy mô ảnh hưởng thực tế. Tỷ lệ giảm không nhất thiết số người giảm tương ứng.
- Gợi ý kể chuyện: dùng **2025** để so chi phí 2017→2025 với tỷ lệ unaffordability; xem thêm sự đảo chiều năm 2020.

### Tab 2: 🌍 World Map

- Chọn `Map indicator` để đổi màu bản đồ theo **tỷ lệ (%)**, **số người (triệu)** hoặc **chi phí PPP $**.
- **Di chuột qua quốc gia** để xem số liệu thực. Màu xám là thiếu dữ liệu, **không phải 0**.
- Ở mục `Explore a country on the map`, chọn quốc gia để so **hai đường thời gian**: tỷ lệ không đủ khả năng chi trả và chi phí ăn lành mạnh ở nước đó.
- Lưu ý: chi phí quốc gia lấy từ `CoHD_PPP`, không lấy biến tổng hợp toàn cầu `CoHD_PPP_PoP`.

### Tab 3: ⚖️ Regional & Income Divide

- `Compare by`: chọn **Region** (khu vực) hoặc **Income group** (nhóm thu nhập).
- Hai biểu đồ thanh đo thay đổi từ **2017 đến năm đang chọn**. Màu **teal = giảm**, **cam = tăng**. Biểu đồ bên trái dùng **pp**, bên phải dùng **triệu người**.
- Trong `Compare group trends`, chọn chỉ số và nhiều nhất **5 khu vực/nhóm** để vẽ các đường theo thời gian.
- Gợi ý: đặt **2025**, chuyển sang **Income group** để kiểm tra chênh lệch mức không đủ khả năng chi trả giữa low-income và high-income.

### Tab 4: 💰 GDP & Inflation

- Biểu đồ 1: **x = GDP per capita (PPP), thang logarithmic**, **y = tỷ lệ không đủ khả năng chi trả**, mỗi chấm là một quốc gia; màu thể hiện nhóm thu nhập.
- Biểu đồ 2: **x = chi phí chế độ ăn lành mạnh PPP**, **y = tỷ lệ không đủ khả năng chi trả**; ví dụ Nigeria và Cyprus trong 2025 minh họa khác biệt giữa **giá** và **khả năng chi trả**.
- Thẻ Spearman **ρ** cho biết tương quan thứ hạng, **không chứng minh nguyên nhân**. GDP per capita không phải thu nhập khả dụng của từng hộ.
- **Food Inflation** là phần *tùy chọn*: tải Excel gốc từ World Bank, đưa vào uploader hoặc đặt tại `data/Inflation-data.xlsx`. Nếu chưa có, dashboard hiển thị thông báo pending, **không tự tạo số liệu**.
- Khi có inflation, biểu đồ x = lạm phát thực phẩm theo CPI (%), y = thay đổi tỷ lệ unaffordability so với năm trước (pp). Đây là hai khái niệm khác nhau về basket và phương pháp.

### Tab 5: 🌱 Nutrition Link

- Chọn `Nutrition reporting year` (**muộn nhất 2024**) và `Nutrition outcome` (stunting hoặc prevalence of undernourishment / PoU).
- Biểu đồ bubble: x = unaffordability (%), y = nutrition outcome (%), kích thước chấm ≈ dân số quốc gia, màu = khu vực.
- Thẻ ρ và `Countries with paired data` tính **trên các quốc gia có cả 2 chỉ số**, loại những giá trị thiếu. Các PoU đánh dấu dưới 2,5% không được coi là số chính xác.
- Đây là **liên hệ mô tả**, không phải bằng chứng nhân quả.

### Tab 6: 🔎 Country Explorer

- `Rank by`: chọn **%**, **triệu người** hoặc **PPP $**.
- `Region`: lọc quốc gia trong **ranking và bảng**; `Top countries`: chọn số thanh từ 5 to 20.
- Trong `Compare countries over time`, chọn tối đa **5 nước** để xem đường xu hướng (không bị ràng buộc bởi Region filter của bảng).
- Bấm `Download filtered CSV` để tải dữ liệu đã lọc; số trống có nghĩa là **missing**, không phải 0.
- Gợi ý: so ranking **%** với **triệu người** để phân biệt *mức độ nghiêm trọng* và *quy mô*.

### Tab 7: 📚 Data & Methods

Tra cứu tên các biến CSV, đơn vị, cách tạo aggregate, giới hạn diễn giải, nguồn tham khảo và liên hệ SDG 2. Trước khi nộp, nhóm cần xác minh **data provenance (nguồn gốc bản trích xuất, phiên bản, ngày tải và bước làm sạch)**.

### Tab 8: 🧭 How to Use

Hướng dẫn tiếng Anh trực tiếp trong trang Streamlit, phù hợp cho giám khảo quốc tế. Có bảng chức năng từng tab, 3 gợi ý khám phá, giải thích đơn vị và giới hạn thống kê.

## 3. Các thao tác chung của Plotly

- **Hover** vào chấm, đường, cột hoặc quốc gia trên bản đồ để xem giá trị chi tiết.
- **Zoom** (phóng lớn) vùng quan tâm bằng toolbar Plotly khi khả dụng; có thể double-click để reset.
- **Legend**: click tên nhóm/đường để ẩn hoặc hiện (ở các chart có legend).
- **Insight dưới plot**: hai phần `📖 How to read` và `💡 Key insight` tự thay đổi theo năm/chỉ số/nhóm quốc gia người dùng chọn.

## 4. Ba kịch bản demo khi trình bày bài thi

1. **Global paradox (60 giây):** năm 2025 → Global Story → so cost vs unaffordability vs người bị ảnh hưởng.
2. **Unequal access (60 giây):** Regional & Income Divide → Income group → GDP & Inflation → Nigeria/Cyprus năm 2025.
3. **Decision-making (60 giây):** World Map → đổi % sang triệu người → Country Explorer → Top 12 → so 2 to 3 quốc gia.

## 5. Chạy project và đưa lên Streamlit Cloud

```bash
cd healthy_diet_streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở `http://localhost:8501`. Chạy tests:

```bash
python -m pip install pytest
python -m pytest -q
```

Để deploy: đẩy **toàn bộ nội dung trong thư mục `healthy_diet_streamlit/` lên root GitHub repo**, gồm thư mục `data/` và `.streamlit/`, rồi chọn repository và entrypoint `app.py` tại `https://share.streamlit.io/`. Kiểm tra đường link công khai bằng trình duyệt ẩn danh và điện thoại.

**Quan trọng:** thay đổi code ở máy **không tự sửa website Streamlit đã deploy** nếu bạn chưa push lên đúng repository/branch đang được deploy. Dự án không cần API key để sử dụng hai CSV gốc.
