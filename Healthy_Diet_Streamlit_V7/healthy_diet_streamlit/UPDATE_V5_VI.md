# V5: The Food Atlas | Hướng dẫn cập nhật GitHub

Đây là phiên bản thiết kế lại giao diện của project V4. Chỉ cập nhật code và thêm dữ liệu phái sinh; không thay đổi dữ liệu nguồn hoặc các ước lượng GDP, nutrition, inflation trước đó.

## 1. Có gì mới?

- Giao diện theo phong cách data journalism / editorial magazine: nền giấy ấm, chữ serif, trang bìa bất đối xứng, số liệu trình bày theo dải thay cho các KPI cards bo tròn.
- Điều hướng 9 chương ở sidebar thay cho thanh 8 tabs; hiển thị một chương tại một thời điểm.
- Dark reading mode và các đồ thị giữ màu sắc nhất quán.
- World atlas: đất liền thiếu dữ liệu có màu xám trung tính, đại dương xanh xám riêng; có chú thích trực tiếp. Không thay NA bằng 0.
- Thêm chương Inside the basket, dựa trên sáu giá trị PPP của nhóm thực phẩm chỉ có cho năm 2021.
- Thêm bảng `data/food_basket_costs_2021_derived.csv`, được tạo từ CSV gốc và có thể xây dựng lại.
- Giữ optional World Bank inflation Excel upload; không đưa số liệu inflation ước đoán vào dashboard.

## 2. Thay code trong repository đang deploy

ZIP có cấu trúc:

```
healthy_diet_streamlit/
    app.py
    src/charts.py
    src/styles.py
    src/basket.py       # MỚI
    data/food_basket_costs_2021_derived.csv # MỚI
    scripts/build_food_basket.py # MỚI
    tests/test_basket.py # MỚI
    tests/test_theme.py # ĐÃ SỬA
    .streamlit/config.toml
    ...
```

Hãy sao chép nguyên nội dung thư mục `healthy_diet_streamlit` vào **đúng thư mục trùng tên** trên repository GitHub. Giữ nguyên `src/economics.py` và `src/statistics.py` của bản V4/V3.1 trong package.

Nếu bạn đứng tại **repository root**:

```bash
git status
git pull --rebase origin main
git add healthy_diet_streamlit/
git commit -m "Redesign Healthy Diet as Food Atlas and clarify map missing data"
git push origin main
```

Nếu đang ở bên trong `healthy_diet_streamlit/`, dùng `git add .` thay cho `git add healthy_diet_streamlit/`.

Nếu `git pull --rebase` tạo conflict, giải quyết conflict trước khi commit/push; tuyệt đối không dùng `git push --force` để né lỗi.

## 3. Chạy thử local

```bash
cd healthy_diet_streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở `http://localhost:8501`, kiểm tra lần lượt:

1. Chế độ Light và Dark.
2. World atlas ở năm 2025, chọn cả 3 metrics, xem màu đất không có dữ liệu khác màu nước.
3. Inside the basket: thử Nigeria, Japan, India; lưu ý dữ liệu luôn ở 2021.
4. Wealth & prices, Nutrition và Country lab còn hoạt động.
5. Các biểu đồ và thanh navigation trên màn hình nhỏ.

Chạy test:

```bash
python -m pip install pytest
python -m pytest -q
```

## 4. Nếu muốn tải thêm lạm phát thực phẩm

World Bank Global Database of Inflation có workbook tại:
https://www.worldbank.org/en/brief/2025/05/04/inflation-database

Khi có file chính thức `Inflation-data.xlsx`, upload từ phần Wealth & prices hoặc đặt vào `healthy_diet_streamlit/data/Inflation-data.xlsx`, rồi kiểm tra tỷ lệ ghép ISO3/năm. Điều này **không bắt buộc** cho các phát hiện và biểu đồ V5.

## 5. Chú ý

Màu trắng/xám là **no data**, không phải bằng 0. Sáu nhóm thực phẩm chỉ có số liệu cho **2021**, không nên giới thiệu là chi phí thành phần của năm 2025. Các giá trị nhóm thu nhập là trung vị quốc gia không trọng số dân số. Dashboard là phân tích học thuật độc lập, không phải sản phẩm chính thức của Liên Hợp Quốc.
